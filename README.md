# Swiss Data Cockpit

Interdepartmental prototype of a governance cockpit for the Swiss Confederation: **35 indicators in 7 policy domains**, observed national series to 2024, scenario forecasts to 2040, a policy-lever simulator and auto-generated situation reports — in a single static HTML file, styled after the federal CD Bund design language.

**Live:** https://gemmagf.github.io/swiss-governance-dashboard/

## What it shows

| View | Content |
|---|---|
| **National scorecard** (landing) | All 35 indicators with sparklines 2015→2040, change since 2015 and status against their objective — *on track / at risk / off track* — plus the largest gaps and strongest improvements. |
| **Domain view** | KPI tiles with sparklines and objective status, cantonal choropleth (26 cantons, swisstopo geometry), cantonal ranking, driver attribution, ex-ante backtest, fan chart with P10–P90 bands and the three scenarios, policy simulator with cost estimates, situation report, alert signals, model & data card. |

Domains: Forest & Biodiversity · Water · Education · Mobility · Energy & Climate · Health & Public Services · Territory & Housing.

## Data honesty

- **National series** are official statistics (BFS, FOEN, SFOE, FOPH, WSL, swisstopo, SBB, FEDRO, FMH, Pronovo, Swissgrid, eHealth Suisse, opendata.swiss), taken from `data/processed/real_data_hybrid.json` and linearly interpolated between publication years. Publication years are marked as dots on the charts.
- **Forecasts** (2025–2040) are damped log-linear trend extrapolations with scenario elasticities (*Agreement / Baseline / Stress*) and lever effects. Every indicator carries a leave-last-out hold-out error and an ex-ante MAPE for 2019–2024.
- **Cantonal values** are deterministic model estimates calibrated so that the population-weighted mean equals the national series. They are **not** official cantonal statistics and are labelled as estimates throughout.
- **Objectives** distinguish *statutory targets* (e.g. CO₂ Act −50 % vs 1990 by 2030, Energy Act −43 % final energy per capita vs 2000 by 2035, EDK/SBFI 95 % upper-secondary qualification, GSchV nitrate requirement value) from *planning references* that are not statutory.
- Nothing here is an official position.

## Using it

- **Deep links** — the URL hash encodes the view, e.g. `#d=energia&m=co2&y=2030&s=opt&c=ZH` (domain, indicator, year, scenario, canton). *Share view* copies it.
- **Print brief** — prints the situation report, alerts and model card of the current view.
- **CSV** — exports the current indicator (national + cantonal, observed/interpolated/forecast flagged) or the whole scorecard.
- Keyboard: ← → change the year, Esc closes an expanded panel.

## Repository

```
dashboard_real.html   the cockpit (self-contained, no build step)
index.html            redirect to the cockpit (GitHub Pages)
data/processed/       national series, model outputs and metadata from the Python pipeline
src/                  Python pipeline (fetch, ETL, models, causal simulator) and Streamlit prototype
```

Local preview: any static server, e.g. `python3 -m http.server 9000` and open `http://127.0.0.1:9000/dashboard_real.html`.
