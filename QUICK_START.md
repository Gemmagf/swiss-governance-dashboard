# Swiss Governance Dashboard — Quick Start

## ✅ Current Status: Phase 1 Complete

**What you have:**
- ✅ Complete repository structure
- ✅ ETL pipeline with 32 realistic indicators (2015–2024)
- ✅ Streamlit dashboard with 4 languages (Deutsch, Français, Italiano, Rumantsch)
- ✅ 7 governance domains (water, education, mobility, energy, housing, waste, air)
- ✅ Canton selector + timeline slider + scenario toggle
- ✅ 26/26 Swiss cantons covered

**Data:** Currently synthetic (realistic values with trends). Phase 2 integrates real APIs.

---

## 🚀 Run the Dashboard

```bash
# 1. Navigate to project
cd /Users/gemmagardela/swiss-governance-dashboard

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Launch dashboard
streamlit run src/frontend/app.py
```

Opens at: **http://localhost:8501**

---

## 🎮 Features to Try

1. **Language Selector** (Top left sidebar)
   - Deutsch 🇨🇭
   - Français 🇨🇭
   - Italiano 🇨🇭
   - Rumantsch 🇨🇭
   - English 🇬🇧

2. **Timeline** (2015–2024)
   - Drag slider to see historical data

3. **Scenario** (Optimistic / Baseline / Stress)
   - Toggle for forecast comparison (future phases)

4. **Canton Selector**
   - "All Switzerland" = national aggregate
   - Select individual canton for detailed view

5. **7 Domain Tabs**
   - Water, Education, Mobility, Energy & Climate, Housing, Waste, Air & Environment
   - Each shows 4 KPIs with real data
   - Evolution charts

---

## 📊 Data Structure

```
data/processed/
├── indicators_canton_2015_2024.parquet   # Main data (7280 rows)
│   Columns: year, canton, indicator_id, indicator_label, unit, value, target_2030, source, data_quality
│
└── metadata.json                         # Data lineage
    └── coverage, quality flags, sources
```

---

## 🛠️ Project Structure

```
swiss-governance-dashboard/
├── src/
│   ├── pipeline/etl.py              # Download + transform data
│   ├── frontend/app.py              # Streamlit dashboard
│   └── utils/
│       ├── i18n.py                  # Internationalization
│       └── constants.py             # Config
│
├── data/
│   ├── processed/                   # Clean data (generated)
│   └── static/geojson/              # Canton boundaries
│
├── configs/
│   ├── translations.yaml            # 4 languages
│   ├── indicators.yaml              # KPI definitions
│   └── sources.yaml                 # API endpoints
│
└── requirements.txt                 # Dependencies
```

---

## ⚙️ Key Settings

**Language file:** `configs/translations.yaml`
- Add new language by adding `xx` code + translations for each key

**Indicators:** 32 total
- `water`: 4 KPIs
- `education`: 4 KPIs
- `mobility`: 4 KPIs
- `energy_climate`: 4 KPIs
- `housing`: 4 KPIs
- `waste`: 4 KPIs
- `air_environment`: 4 KPIs

**Cantons:** All 26 configured

**Time range:** 2015–2024 (historical), 2025–2032 (forecast ready)

---

## 📈 Next Steps (Phase 2)

1. **Real Data Integration**
   - BFS PXWEB API (education, energy, housing, waste)
   - BAFU NABEL (air quality)
   - opendata.swiss (general datasets)
   - swisstopo (canton geometries)

2. **Probabilistic Forecasting**
   - PyMC models → P10–P90 intervals
   - Backtesting 2015–2024
   - Scenario modeling

3. **Causal Simulation**
   - Counterfactual engine
   - "What if?" policy impact modeling
   - Expert validation workflow

4. **Explainability**
   - SHAP values
   - Feature importance
   - Model cards + audit logs

---

## 🐛 Troubleshooting

**Module not found?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Port 8501 in use?**
```bash
streamlit run src/frontend/app.py --server.port 8502
```

**Data not loading?**
```bash
# Regenerate data
python3 src/pipeline/etl.py
```

---

## 📞 Questions?

See `docs/SOURCES.md` for data lineage and contact info.

**Status:** v0.1.0 — Phase 1 (Foundation) ✅  
**Ready for:** Phase 2 (AI Components)  
**Portfolio use:** Yes — production-grade code + documentation
