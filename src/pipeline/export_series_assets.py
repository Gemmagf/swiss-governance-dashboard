"""Export the "series" assets (Klärwerk Werdhölzli, ewz grid load) to data/processed/asset_<id>.json.

Same contract as export_asset.py: every number shown in the cockpit for these
assets comes from this file. Both assets are built on official City of Zurich
open data; the monitor is a seasonal-ratio robust z-score (see asset.series).

Usage:  python src/pipeline/export_series_assets.py [--out-dir DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from asset.config import EWZ_LOAD, PROCESSED_DIR, WERDHOELZLI, ensure_dirs  # noqa: E402
from asset.data.fetch import ensure_downloaded  # noqa: E402
from asset.data.loader import load_ewz_load, load_werdhoelzli  # noqa: E402
from asset.forecast.backtest import expanding_window_backtest, summarize_backtest  # noqa: E402
from asset.forecast.baseline import seasonal_naive_forecast  # noqa: E402
from asset.forecast.sarima import (  # noqa: E402
    DEFAULT_ORDER,
    DEFAULT_SEASONAL_ORDER,
    fit_and_forecast,
)
from asset.series import (  # noqa: E402
    flagged_runs,
    monthly_from_daily,
    monthly_from_quarter_hourly,
    seasonal_zscore_monitor,
)

HORIZON = 6
MIN_TRAIN_SIZE = 48
Z_LIMIT = 3.0
CI_LEVEL = 0.95


def ym(ts: pd.Timestamp) -> str:
    return ts.strftime("%Y-%m")


def rnd(x: float, d: int = 2) -> float:
    return float(round(float(x), d))


def floats(values, d: int = 2) -> list[float]:
    return [rnd(v, d) for v in values]


def forecast_block(series: pd.Series) -> tuple[dict, dict]:
    s = series.asfreq("MS")
    fc = fit_and_forecast(s, HORIZON, alpha=1 - CI_LEVEL)
    naive = seasonal_naive_forecast(s, HORIZON)
    backtest: dict[str, dict] = {}
    for h in (1, 3, 6):
        res = expanding_window_backtest(s, min_train_size=MIN_TRAIN_SIZE, horizon=h)
        sm = summarize_backtest(res)
        backtest[str(h)] = {
            "sarima": {
                "mape": rnd(sm.loc["sarima", "MAPE_%"]),
                "mae": rnd(sm.loc["sarima", "MAE"], 1),
            },
            "naive": {
                "mape": rnd(sm.loc["seasonal_naive", "MAPE_%"]),
                "mae": rnd(sm.loc["seasonal_naive", "MAE"], 1),
            },
            "folds": len(res),
        }
    forecast = {
        "horizon": HORIZON,
        "months": [ym(t) for t in fc.mean.index],
        "sarima": {
            "mean": floats(fc.mean),
            "lo": floats(fc.ci_lower),
            "hi": floats(fc.ci_upper),
            "order": f"{DEFAULT_ORDER}{DEFAULT_SEASONAL_ORDER}".replace(" ", ""),
            "ci": CI_LEVEL,
        },
        "naive": floats(naive),
    }
    return forecast, {"min_train_size": MIN_TRAIN_SIZE, "horizons": backtest}


def monitor_block(series: pd.Series) -> dict:
    mon = seasonal_zscore_monitor(series, k=Z_LIMIT)
    cal = series.groupby(series.index.month).mean()
    return {
        "method": "seasonal ratio · robust z-score (median / MAD)",
        "k": Z_LIMIT,
        "ratio": floats(mon["ratio"], 3),
        "z": floats(mon["z"], 2),
        "flags": [bool(v) for v in mon["flag"]],
        "n_flagged": int(mon["flag"].sum()),
        "calendar_mean": {int(m): rnd(v, 1) for m, v in cal.items()},
        "episodes": flagged_runs(mon["flag"], mon["z"]),
    }


def base_doc(asset_id: str, months: list[str]) -> dict:
    return {
        "id": asset_id,
        "kind": "series",
        "canton": "ZH",
        "generated": date.today().isoformat(),
        "n_months": len(months),
        "range": [months[0], months[-1]],
        "months": months,
    }


def build_werdhoelzli() -> dict:
    daily = load_werdhoelzli()["abwasser_m3_pro_d"]
    m = monthly_from_daily(daily)
    months = [ym(t) for t in m.index]
    primary = m["mean"]
    forecast, backtest = forecast_block(primary)
    doc = base_doc("werdhoelzli", months)
    doc.update(
        {
            "name": "Klärwerk Werdhölzli",
            "operator": "ERZ Entsorgung + Recycling Zürich",
            "domain": "aigua",
            "series": {
                "primary": {
                    "key": "inflow_m3_per_d",
                    "label": "Treated wastewater inflow · monthly mean",
                    "unit": "m³/day",
                    "dec": 0,
                    "values": floats(primary, 0),
                },
                "extras": [
                    {
                        "key": "max_m3_per_d",
                        "label": "Peak day",
                        "unit": "m³/day",
                        "dec": 0,
                        "values": floats(m["max"], 0),
                    },
                    {
                        "key": "min_m3_per_d",
                        "label": "Lowest day",
                        "unit": "m³/day",
                        "dec": 0,
                        "values": floats(m["min"], 0),
                    },
                    {
                        "key": "days",
                        "label": "Days observed",
                        "unit": "days",
                        "dec": 0,
                        "values": floats(m["days"], 0),
                    },
                ],
            },
            "forecast": forecast,
            "backtest": backtest,
            "monitor": monitor_block(primary),
            "daily_stats": {
                "n_days": int(daily.notna().sum()),
                "missing_days": int(daily.isna().sum()),
                "median_m3_per_d": rnd(daily.median(), 0),
                "max_m3_per_d": rnd(daily.max(), 0),
                "max_day": daily.idxmax().strftime("%Y-%m-%d"),
            },
            "sources": [
                {
                    "name": WERDHOELZLI.name,
                    "url": f"https://data.stadt-zuerich.ch/dataset/{WERDHOELZLI.name}",
                    "rows": len(daily),
                    "retrieved": WERDHOELZLI.retrieved,
                    "use": "daily treated wastewater volume, incl. stormwater returned from retention basins",
                }
            ],
            "notes": [
                "Daily inflow (m³/day) aggregated to calendar-month means; a partial month is dropped, not extrapolated.",
                "Inflow includes rainwater stored in retention basins and pumped back, so wet months read high by design; the monitor compares each month with its own calendar-month norm.",
                "No cost or emission layer: the dataset carries volumes only and no constants are assumed.",
            ],
        }
    )
    return doc


def build_ewz_load() -> dict:
    q = load_ewz_load()
    m = monthly_from_quarter_hourly(q["bruttolastgang"])
    months = [ym(t) for t in m.index]
    primary = m["gwh"]
    forecast, backtest = forecast_block(primary)
    non_plausible = float((q["status"] != "E").mean())
    doc = base_doc("ewz_load", months)
    doc.update(
        {
            "name": "ewz grid load · City of Zurich",
            "operator": "ewz Elektrizitätswerk der Stadt Zürich",
            "domain": "energia",
            "series": {
                "primary": {
                    "key": "energy_gwh",
                    "label": "Gross electricity delivered · monthly",
                    "unit": "GWh",
                    "dec": 1,
                    "values": floats(primary, 2),
                },
                "extras": [
                    {
                        "key": "avg_mw",
                        "label": "Average load",
                        "unit": "MW",
                        "dec": 0,
                        "values": floats(m["avg_mw"], 1),
                    },
                    {
                        "key": "peak_mw",
                        "label": "Peak 15-min load",
                        "unit": "MW",
                        "dec": 0,
                        "values": floats(m["peak_mw"], 1),
                    },
                    {
                        "key": "intervals",
                        "label": "15-min intervals",
                        "unit": "",
                        "dec": 0,
                        "values": floats(m["intervals"], 0),
                    },
                ],
            },
            "forecast": forecast,
            "backtest": backtest,
            "monitor": monitor_block(primary),
            "quality": {
                "share_not_plausibilised": rnd(non_plausible, 4),
                "gap_adjusted_months": {
                    ym(t): rnd(gf, 4) for t, gf in m["gap_factor"].items() if gf > 1.0001
                },
                "dropped_incomplete_months": [
                    ym(t)
                    for t in q["bruttolastgang"].resample("MS").sum().index
                    if ym(t) not in months
                ],
            },
            "sources": [
                {
                    "name": s.name,
                    "url": "https://data.stadt-zuerich.ch/dataset/ewz_bruttolastgang_stadt_zuerich",
                    "rows": int((q.index.year == int(s.filename[:4])).sum()),
                    "retrieved": s.retrieved,
                    "use": "15-minute gross electricity delivered in the city (all end consumers, net of losses)",
                }
                for s in EWZ_LOAD
            ],
            "notes": [
                "15-minute gross energy delivered (kWh) summed to calendar months; months with fewer than 95 % of the expected intervals are dropped (a partial current month is never extrapolated), and months missing a few intervals are scaled by expected/observed — the factor is reported per month.",
                "Rows with status F/W (not yet plausibilised) are kept and their share is reported; they are concentrated at the start of 2020 and in the current year.",
                "This is the city's grid load, not a single plant: the monitor detects demand anomalies (weather, holidays, structural change), not equipment faults.",
            ],
        }
    )
    return doc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=PROCESSED_DIR)
    args = parser.parse_args()
    warnings.filterwarnings("ignore")
    ensure_dirs()
    ensure_downloaded()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for build in (build_werdhoelzli, build_ewz_load):
        doc = build()
        out = args.out_dir / f"asset_{doc['id']}.json"
        out.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n")
        bt = doc["backtest"]["horizons"]
        print(
            f"Wrote {out.name} ({out.stat().st_size / 1024:.0f} KB): n={doc['n_months']} "
            f"{doc['range'][0]} → {doc['range'][1]}; flagged {doc['monitor']['n_flagged']}; "
            "MAPE sarima/naive "
            + " · ".join(f"{h}m {v['sarima']['mape']}/{v['naive']['mape']}" for h, v in bt.items())
        )


if __name__ == "__main__":
    main()
