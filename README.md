# Swiss Data Cockpit

Interdepartmental prototype of a governance cockpit for the Swiss Confederation: **35 indicators in 7 policy domains**, observed national series to 2024, scenario forecasts to 2040, a policy-lever simulator and auto-generated situation reports — in a single static HTML file, styled after the federal CD Bund design language.

**Live:** https://gemmagf.github.io/swiss-governance-dashboard/

## What it shows

| View | Content |
|---|---|
| **National scorecard** (landing) | All 35 indicators with sparklines 2015→2040, change since 2015 and status against their objective — *on track / at risk / off track* — plus the largest gaps and strongest improvements. |
| **Domain view** | KPI tiles with sparklines and objective status, cantonal choropleth (26 cantons, swisstopo geometry), cantonal ranking, driver attribution, ex-ante backtest, fan chart with P10–P90 bands and the three scenarios, policy simulator with cost estimates, situation report, alert signals, model & data card. |
| **Asset drill-down** | The level built on real monthly *operating* data of City of Zurich assets: **KVA Hagenholz** (waste-to-energy plant: throughput forecast, multivariate process monitor, per-month contributions, CHF/tCO₂eq decision layer), **Klärwerk Werdhölzli** (wastewater treatment plant: daily inflow) and the **ewz grid load** of the city (15-minute electricity delivered). See [below](#asset-drill-down-kva-hagenholz) and [Series assets](#series-assets-klärwerk-werdhölzli-and-ewz-grid-load). |
| **Explain** | One button, every view: a generated explanation of what is on screen — why the cockpit exists, how to read a status, the conclusions (counts under each scenario, statutory targets met or missed, largest gaps, strongest improvements, a forecast reading per domain), what drives the forecast and what the simulator says, and what the numbers are *not*. Every figure is computed from the data on screen; none is typed in. |

Domains: Forest & Biodiversity · Water · Education · Mobility · Energy & Climate · Health & Public Services · Territory & Housing.

## Data honesty

- **National series** are official statistics (BFS, FOEN, SFOE, FOPH, WSL, swisstopo, SBB, FEDRO, FMH, Pronovo, Swissgrid, eHealth Suisse, opendata.swiss), taken from `data/processed/real_data_hybrid.json` and linearly interpolated between publication years. Publication years are marked as dots on the charts.
- **Forecasts** (2025–2040) are damped log-linear trend extrapolations with scenario elasticities (*Agreement / Baseline / Stress*) and lever effects. Every indicator carries a leave-last-out hold-out error and an ex-ante MAPE for 2019–2024.
- **Cantonal values** are deterministic model estimates calibrated so that the population-weighted mean equals the national series. They are **not** official cantonal statistics and are labelled as estimates throughout.
- **Objectives** distinguish *statutory targets* (e.g. CO₂ Act −50 % vs 1990 by 2030, Energy Act −43 % final energy per capita vs 2000 by 2035, EDK/SBFI 95 % upper-secondary qualification, GSchV nitrate requirement value) from *planning references* that are not statutory.
- **The asset level is real operating data** (Stadt Zürich open data for KVA Hagenholz, monthly, n=78); **the cantonal level remains a model estimate.** Decision-layer prices and emission factors are sourced constants, except the ammonia price, which is a planning assumption.
- Nothing here is an official position.

## Using it

- **Deep links** — the URL hash encodes the view, e.g. `#d=energia&m=co2&y=2030&s=opt&c=ZH` (domain, indicator, year, scenario, canton). *Share view* copies it.
- **Print brief** — prints the situation report, alerts and model card of the current view.
- **CSV** — exports the current indicator (national + cantonal, observed/interpolated/forecast flagged) or the whole scorecard.
- Keyboard: ← → change the year, Esc closes an expanded panel.

## Asset drill-down (KVA Hagenholz)

The cockpit's fourth navigation level: **Switzerland › Energy & Climate › Zurich › KVA Hagenholz**, the
waste-to-energy plant operated by ERZ (Entsorgung + Recycling Zürich). It is reached from the Energy & Climate
domain (button *Drill down › KVA Hagenholz*), from the *Assets* entry in the sidebar, or directly via the deep link
`#v=asset&a=hagenholz&mo=2021-11` (`mo` = selected month). It merges the former standalone project
[Züri-Kreislauf](https://github.com/Gemmagf/zuri-kreislauf) into the cockpit; its Python package now lives in
`src/asset/` (MIT, see `src/asset/LICENSE`) and its results are **precomputed and embedded** in `dashboard_real.html`
— no Streamlit, no JavaScript libraries.

**What it shows.** Monthly waste throughput with a 6-month SARIMA forecast (95 % CI) next to the seasonal-naive
baseline and an expanding-window backtest; a multivariate process monitor (Hotelling T² on a robust MinCovDet
covariance + PCA-Q, α = 0.01, cross-checked with IsolationForest) on seven intensity ratios; the top T² contributors
for any month you click; and a CHF/tCO₂eq decision layer that prices each month's deviation from its normal-month
baseline — including the one real, explainable episode in the data: the generator turbine outage of Sep 2021 – Apr 2022.

**Four layers.**

```
data.stadt-zuerich.ch (3 CSVs) ── src/pipeline/fetch_asset_data.py ── data/raw/ (cached, not committed)
        │
   src/asset/data      loader.py (dtype, Swiss thousands separator) · preprocess.py (7 intensity ratios, seasonally adjusted heat)
        │
   ┌────┴─────────────────┬────────────────────────┐
   forecast/              detection/               decision/
   SARIMA vs seasonal     Hotelling T²/Q +         deviations × sourced CHF/tCO₂eq
   naive, expanding-      IsolationForest,         constants (cost.py, constants.py)
   window backtest        T² contributions
   └────┬─────────────────┴────────────────────────┘
   src/pipeline/export_asset.py ── data/processed/asset_hagenholz.json ── src/pipeline/embed_asset.py ── dashboard_real.html
```

**Results** — generated from `data/processed/asset_hagenholz.json` by `make asset`; regenerate rather than trusting this table.

| Horizon | SARIMA MAPE | Naive MAPE | SARIMA MAE (t) | Naive MAE (t) |
|---|---|---|---|---|
| 1 month | 12.56 % | 12.49 % | 2 298 | 2 198 |
| 3 months | 13.74 % | 12.66 % | 2 440 | 2 194 |
| 6 months | 15.80 % | **11.39 %** | 2 972 | **2 081** |

The seasonal-naive baseline is competitive at one month and clearly beats SARIMA at 3 and 6 months — reported as the
finding, not hidden. Monitor: T² UCL 22.31, Q UCL 8.06, 20/78 months flagged by T²/Q, 8/78 by IsolationForest, 7 by
both. Decision layer: turbine outage Sep 2021 – Apr 2022 → **CHF 18.84 M** of lost electricity value, **9 022 tCO₂eq**
of displaced grid emissions, **CHF 8.78 M** of offsetting extra heat revenue; sum over all 78 months CHF 12.66 M /
−8 703 tCO₂eq (a ranking aid, *not* an audited total).

**Data provenance.** Three open CSVs from data.stadt-zuerich.ch, no authentication, retrieved **2026-07-17**
(`erz_abfallmenge_energie_khkw`, 78 monthly rows 2020-01 → 2026-06, primary; `entsorgungskalender_bioabfall`, 1 253
rows, context; `erz_elog_kennzahlen`, 1 427 rows, context). Reagent and drinking-water columns are reported in
**tonnes** (confirmed via the dataset's CKAN `sszFields` metadata) and converted to kg per tonne of waste — getting this
wrong would put every ratio and CHF figure off by 1000×.

**Assumptions & limitations.** n = 78 rules out data-hungry models; classical SPC has analytic control limits for
small samples. Decision-layer constants are a mix of well-sourced (Zurich district-heat tariff, ElCom electricity
price, Swiss consumption-mix carbon intensity, FOEN gas emission factor) and rough (European bulk reagent prices;
the ammonia-solution price is a planning assumption). Baselines are medians of non-flagged months; the all-months
total is not audited. No COVID-19 level shift was found (2020 mean throughput 20 854 t, in line with other years).

**Reproducing.**

```bash
make install      # .venv (python3.11) with the asset extra + dev tools
make asset-data   # fetch and cache the 3 CSVs (idempotent)
make asset        # export data/processed/asset_hagenholz.json and embed it in dashboard_real.html
make test         # pytest (data-contract tests skip if data is not cached)
make lint         # ruff on the asset code
```

CI (`.github/workflows/ci.yml`) runs ruff + pytest on Python 3.11 and 3.12 and checks that the embedded block
matches the committed JSON.

### Series assets: Klärwerk Werdhölzli and ewz grid load

Two further assets use the same navigation (`#v=asset&a=werdhoelzli`, `#v=asset&a=ewz_load`; also from the Water /
Energy & Climate domains and the *Assets* entry in the sidebar) but carry **one operating series** each rather than a
set of process ratios, so the T²/Q monitor does not apply. `src/pipeline/export_series_assets.py` builds them from:

| Asset | Dataset (data.stadt-zuerich.ch) | Raw resolution | Monthly series | Coverage |
|---|---|---|---|---|
| Klärwerk Werdhölzli (ERZ) | `erz_abwassermenge_klaerwerk_werdhoelzli` | daily m³/day | mean inflow (+ peak day, lowest day) | 2020-01 → last complete month |
| ewz grid load · City of Zurich | `ewz_bruttolastgang_stadt_zuerich` (one CSV per year) | 15-minute kWh | GWh delivered (+ average and peak load in MW) | 2019-01 → last complete month |

Method (`src/asset/series.py`): calendar-month aggregation that **drops partial months** instead of extrapolating
them; a 6-month SARIMA forecast with the seasonal-naive baseline and the same expanding-window backtest as Hagenholz;
and a **seasonal monitor** — each month divided by the mean of the same calendar month across years, scored with a
robust z (median / MAD), flagged at |z| > 3, with consecutive flagged months reported as runs. No cost or emission
constants are attached to these assets: the datasets carry volumes only. The ewz series is the city's demand, not a
single plant, so its flags point to weather, holidays or structural change rather than faults; the share of
not-yet-plausibilised intervals (status F/W) is reported in the view.

## Repository

```
dashboard_real.html   the cockpit (self-contained, no build step; embeds the asset JSON between /*ASSET-DATA-*/ markers)
index.html            redirect to the cockpit (GitHub Pages)
data/processed/       national series, model outputs, metadata and asset_hagenholz.json
data/raw/             cached City of Zurich CSVs for the asset level (gitignored)
src/asset/            asset pipeline (former Züri-Kreislauf): data, forecast, detection, decision, logistics
src/pipeline/         export_asset.py · export_series_assets.py · embed_asset.py · fetch_asset_data.py · national-series pipeline
src/                  older Python pipeline (fetch, ETL, models, causal simulator) and Streamlit prototype
tests/                pytest suite for src/asset
```

Local preview: `make serve` (or any static server) and open `http://127.0.0.1:9000/dashboard_real.html`.
