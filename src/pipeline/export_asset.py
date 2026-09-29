"""Export the KVA Hagenholz asset drill-down to data/processed/asset_hagenholz.json.

Runs every layer of the `asset` package (formerly Züri-Kreislauf) on the cached
City of Zurich open data and writes ONE JSON document that `embed_asset.py`
injects into dashboard_real.html. Every number shown in the asset view of the
cockpit comes from this file — nothing is typed into the HTML by hand.

Usage:  python src/pipeline/export_asset.py [--out PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from collections import Counter
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from asset.config import ALL_SOURCES, PROCESSED_DIR, ensure_dirs  # noqa: E402
from asset.data.fetch import ensure_downloaded  # noqa: E402
from asset.data.loader import KHKW_INT_COLUMNS, load_khkw  # noqa: E402
from asset.data.preprocess import (  # noqa: E402
    MONITORING_COLUMNS,
    RATIO_COLUMNS,
    build_intensity_ratios,
)
from asset.decision import constants as C  # noqa: E402
from asset.decision.cost import REAGENT_PRICES_CHF_PER_KG, monthly_impact  # noqa: E402
from asset.detection.iforest import run_iforest  # noqa: E402
from asset.detection.spc import run_spc, top_contributors  # noqa: E402
from asset.forecast.backtest import expanding_window_backtest, summarize_backtest  # noqa: E402
from asset.forecast.baseline import seasonal_naive_forecast  # noqa: E402
from asset.forecast.sarima import (  # noqa: E402
    DEFAULT_ORDER,
    DEFAULT_SEASONAL_ORDER,
    fit_and_forecast,
)

DEFAULT_OUT = PROCESSED_DIR / "asset_hagenholz.json"
HORIZON = 6
MIN_TRAIN_SIZE = 48
SPC_ALPHA = 0.01
IFOREST_CONTAMINATION = 0.1
CI_LEVEL = 0.95

EPISODES = [
    {
        "id": "turbine_outage",
        "from": "2021-09",
        "to": "2022-04",
        "label": "Generator turbine offline",
    }
]

SOURCE_USE = {
    "erz_abfallmenge_energie_khkw": "primary monthly plant data",
    "entsorgungskalender_bioabfall": "bio-waste collection calendar by PLZ (context, not rendered)",
    "erz_elog_kennzahlen": "city-wide waste/recycling KPIs (context)",
}

CONSTANTS = [
    (
        "HEAT_PRICE_CHF_PER_KWH",
        C.HEAT_PRICE_CHF_PER_KWH,
        "CHF/kWh",
        "City of Zurich district-heat tariff, Oct 2025",
        "sourced",
    ),
    (
        "ELECTRICITY_PRICE_CHF_PER_KWH",
        C.ELECTRICITY_PRICE_CHF_PER_KWH,
        "CHF/kWh",
        "ElCom 2026 tariffs, C4 profile",
        "sourced",
    ),
    (
        "ELECTRICITY_EMISSION_FACTOR_KG_CO2_PER_KWH",
        C.ELECTRICITY_EMISSION_FACTOR_KG_CO2_PER_KWH,
        "kgCO₂eq/kWh",
        "Swiss consumption mix 2024 (SFOE statistics commentary)",
        "sourced",
    ),
    (
        "GAS_EMISSION_FACTOR_KG_CO2_PER_KWH",
        C.GAS_EMISSION_FACTOR_KG_CO2_PER_KWH,
        "kgCO₂/kWh",
        "FOEN GHG-inventory emission factors, 2024 data",
        "sourced",
    ),
    (
        "NAOH_PRICE_CHF_PER_KG",
        C.NAOH_PRICE_CHF_PER_KG,
        "CHF/kg",
        "European bulk market ~EUR 510/t (2025), EUR→CHF 0.93",
        "rough",
    ),
    (
        "HCL_PRICE_CHF_PER_KG",
        C.HCL_PRICE_CHF_PER_KG,
        "CHF/kg",
        "European bulk market ~EUR 140/t (2025), EUR→CHF 0.93",
        "rough",
    ),
    (
        "LIME_PRICE_CHF_PER_KG",
        C.LIME_PRICE_CHF_PER_KG,
        "CHF/kg",
        "European bulk market ~EUR 157/t (Q1 2026), EUR→CHF 0.93",
        "rough",
    ),
    (
        "AMMONIA_PRICE_CHF_PER_KG",
        C.AMMONIA_PRICE_CHF_PER_KG,
        "CHF/kg",
        "planning estimate for ~25 % solution, not a market quote",
        "assumption",
    ),
]

NOTES = [
    "Reagent columns are reported in tonnes (confirmed via the dataset's CKAN sszFields "
    "metadata); converted to kg per tonne of waste for the intensity ratios.",
    "Heat is monitored as a seasonally adjusted ratio (value / across-year mean of the same "
    "calendar month) so the winter/summer demand cycle does not mask anomalies.",
    "The seasonal-naive baseline (same month last year) beats SARIMA at 3- and 6-month "
    "horizons; the forecast is shown with both for that reason.",
    "Decision-layer baselines are medians of non-flagged months; the all-months total ranks "
    "and explains episodes but is not an audited cost figure.",
    "No COVID-19 level shift was found: 2020 monthly throughput is in line with other years.",
]


def ym(ts: pd.Timestamp) -> str:
    return ts.strftime("%Y-%m")


def rnd(x: float, d: int = 2) -> float:
    return float(round(float(x), d))


def ints(values) -> list[int]:
    return [round(float(v)) for v in values]


def floats(values, d: int = 2) -> list[float]:
    return [rnd(v, d) for v in values]


def _rows_in(source) -> int:
    encoding = "utf-8-sig" if source.name == "entsorgungskalender_bioabfall" else "utf-8"
    return len(pd.read_csv(source.path, encoding=encoding))


def build() -> dict:
    warnings.filterwarnings("ignore")
    ensure_dirs()
    ensure_downloaded()

    khkw = load_khkw()
    ratios = build_intensity_ratios(khkw)
    index = ratios.index
    months = [ym(t) for t in index]

    # --- Layer 2: multivariate monitor + model-free cross-check ---
    spc = run_spc(ratios, MONITORING_COLUMNS, alpha=SPC_ALPHA)
    iforest = run_iforest(ratios, MONITORING_COLUMNS, contamination=IFOREST_CONTAMINATION)
    flags = spc.flags.reindex(index, fill_value=False)
    if_flags = iforest["flag"].reindex(index, fill_value=False)
    normal_mask = ~flags

    top: dict[str, list] = {}
    for t in index:
        contrib = top_contributors(spc.t2_contributions, t, k=3)
        t2_total = float(spc.t2.loc[t]) or 1.0
        top[ym(t)] = [[str(k), rnd(v / t2_total, 3)] for k, v in contrib.items()]

    # --- Layer 1: throughput forecast + expanding-window backtest ---
    series = khkw["Kehrichtdurchsatz"].astype(float).asfreq("MS")
    fc = fit_and_forecast(series, HORIZON, alpha=1 - CI_LEVEL)
    naive = seasonal_naive_forecast(series, HORIZON)
    backtest: dict[str, dict] = {}
    for h in (1, 3, 6):
        res = expanding_window_backtest(series, min_train_size=MIN_TRAIN_SIZE, horizon=h)
        s = summarize_backtest(res)
        backtest[str(h)] = {
            "sarima": {
                "mape": rnd(s.loc["sarima", "MAPE_%"]),
                "mae": rnd(s.loc["sarima", "MAE"], 1),
            },
            "naive": {
                "mape": rnd(s.loc["seasonal_naive", "MAPE_%"]),
                "mae": rnd(s.loc["seasonal_naive", "MAE"], 1),
            },
            "folds": len(res),
        }

    # --- Layer 4: CHF / tCO2eq decision layer ---
    impact = monthly_impact(khkw, ratios, normal_mask)
    reagent_cols = [f"{c}_chf" for c in REAGENT_PRICES_CHF_PER_KG]
    reagents_chf = impact[reagent_cols].sum(axis=1)

    episodes = []
    for e in EPISODES:
        w = impact.loc[e["from"] : e["to"]]
        drivers = Counter(top[ym(t)][0][0] for t in w.index if top[ym(t)])
        episodes.append(
            {
                **e,
                "months": len(w),
                "flagged_months": int(flags.loc[e["from"] : e["to"]].sum()),
                "electricity_chf_lost": round(float(w["electricity_chf"].sum())),
                "electricity_tco2eq": rnd(w["electricity_co2_kg"].sum() / 1000, 1),
                "heat_chf_offset": round(float(w["heat_chf"].sum())),
                "heat_tco2eq": rnd(w["heat_co2_kg"].sum() / 1000, 1),
                "reagents_chf": round(float(reagents_chf.loc[e["from"] : e["to"]].sum())),
                "net_chf": round(float(w["total_chf"].sum())),
                "net_tco2eq": rnd(w["total_co2_kg"].sum() / 1000, 1),
                "dominant_driver": drivers.most_common(1)[0][0] if drivers else None,
            }
        )

    year_2020 = series[series.index.year == 2020]
    return {
        "id": "hagenholz",
        "name": "KVA Hagenholz",
        "operator": "ERZ Entsorgung + Recycling Zürich",
        "canton": "ZH",
        "domain": "energia",
        "generated": date.today().isoformat(),
        "n_months": len(khkw),
        "range": [months[0], months[-1]],
        "months": months,
        "raw": {c: ints(khkw[c]) for c in KHKW_INT_COLUMNS},
        "ratios": {
            **{c: floats(ratios[c], 4 if c == "residual_fraction" else 2) for c in RATIO_COLUMNS},
            "heat_kwh_per_t_sa": floats(ratios["heat_kwh_per_t_sa"], 3),
        },
        "monitoring_columns": list(MONITORING_COLUMNS),
        "spc": {
            "alpha": SPC_ALPHA,
            "t2": floats(spc.t2.reindex(index)),
            "t2_ucl": rnd(spc.t2_ucl),
            "q": floats(spc.q.reindex(index)),
            "q_ucl": rnd(spc.q_ucl),
            "flags": [bool(v) for v in flags],
            "n_flagged": int(flags.sum()),
            "top_contributors": top,
        },
        "iforest": {
            "contamination": IFOREST_CONTAMINATION,
            "score": floats(iforest["score"].reindex(index), 3),
            "flags": [bool(v) for v in if_flags],
            "n_flagged": int(if_flags.sum()),
            "n_flagged_both": int((flags & if_flags).sum()),
        },
        "forecast": {
            "horizon": HORIZON,
            "months": [ym(t) for t in fc.mean.index],
            "sarima": {
                "mean": ints(fc.mean),
                "lo": ints(fc.ci_lower),
                "hi": ints(fc.ci_upper),
                "order": f"{DEFAULT_ORDER}{DEFAULT_SEASONAL_ORDER}".replace(" ", ""),
                "ci": CI_LEVEL,
            },
            "naive": ints(naive),
        },
        "backtest": {"min_train_size": MIN_TRAIN_SIZE, "horizons": backtest},
        "impact": {
            "electricity_chf": ints(impact["electricity_chf"]),
            "electricity_co2_kg": ints(impact["electricity_co2_kg"]),
            "heat_chf": ints(impact["heat_chf"]),
            "heat_co2_kg": ints(impact["heat_co2_kg"]),
            "reagents_chf": ints(reagents_chf),
            "total_chf": ints(impact["total_chf"]),
            "total_co2_kg": ints(impact["total_co2_kg"]),
        },
        "episodes": episodes,
        "totals": {
            "chf_all_months": round(float(impact["total_chf"].sum())),
            "tco2eq_all_months": rnd(impact["total_co2_kg"].sum() / 1000, 1),
            "throughput_2020_mean_t": round(float(year_2020.mean())),
            "throughput_all_mean_t": round(float(series.mean())),
        },
        "sources": [
            {
                "name": s.name,
                "url": f"https://data.stadt-zuerich.ch/dataset/{s.name}",
                "rows": _rows_in(s),
                "retrieved": s.retrieved,
                "use": SOURCE_USE.get(s.name, ""),
            }
            for s in ALL_SOURCES
        ],
        "constants": [
            {"key": k, "value": rnd(v, 4), "unit": u, "source": src, "quality": q}
            for k, v, u, src, q in CONSTANTS
        ],
        "notes": NOTES,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    doc = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n")
    size_kb = args.out.stat().st_size / 1024
    bt = doc["backtest"]["horizons"]
    ep = doc["episodes"][0]
    print(f"Wrote {args.out} ({size_kb:.0f} KB)")
    print(f"n={doc['n_months']} months {doc['range'][0]} → {doc['range'][1]}")
    print(
        "backtest MAPE (sarima/naive): "
        + " · ".join(f"{h}m {v['sarima']['mape']}/{v['naive']['mape']}" for h, v in bt.items())
    )
    print(
        f"SPC: T² UCL {doc['spc']['t2_ucl']}, Q UCL {doc['spc']['q_ucl']}, "
        f"{doc['spc']['n_flagged']}/{doc['n_months']} flagged; "
        f"IsolationForest {doc['iforest']['n_flagged']}; both {doc['iforest']['n_flagged_both']}"
    )
    print(
        f"outage: electricity lost CHF {ep['electricity_chf_lost']:,}, "
        f"{ep['electricity_tco2eq']} tCO₂eq, heat offset CHF {ep['heat_chf_offset']:,}; "
        f"all months net CHF {doc['totals']['chf_all_months']:,} / "
        f"{doc['totals']['tco2eq_all_months']} tCO₂eq"
    )


if __name__ == "__main__":
    main()
