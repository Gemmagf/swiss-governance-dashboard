# Swiss Governance Dashboard

**Real-time urban governance intelligence for Swiss cantons, powered by official data + AI.**

A functional, production-grade dashboard that transforms 32 official public indicators (education, mobility, energy, housing, waste, air quality, water) across all 26 Swiss cantons into actionable insights.

**Live demo**: (deploy URL coming soon)

**GitHub**: https://github.com/gemmagardela/swiss-governance-dashboard

---

## 🎯 Objective

Demonstrate how **probabilistic forecasting** + **explainability** + **transparent data sourcing** can elevate governance from reactive reporting to forward-looking decision support.

Audience: Swiss public administrations, urban planners, policy makers.

---

## 📊 What's Inside

### 7 Governance Domains (32 Indicators)
1. **Forests & Biodiversity** — forest cover, species diversity, protected areas
2. **Water** — consumption, network losses, quality index, precipitation
3. **Education** — enrollment, student-teacher ratio, childcare slots, per-pupil spending
4. **Mobility** — public transit trips, bike share, motorized traffic, network punctuality
5. **Energy & Climate** — CO₂ emissions, renewable share, final consumption, solar capacity
6. **Health & Public Services** — (phase 2)
7. **Territory & Housing** — rent, vacancy rate, housing completions, cooperative housing share

### Data: All Real, All Certified
- **BFS PXWEB API** — official federal statistics (education, energy, housing, waste)
- **opendata.swiss** — 11,000+ curated datasets
- **BAFU NABEL** — air quality stations (certified measurements)
- **Swisstopo** — official canton boundaries + topography
- **Canton open-data portals** — Zurich, Geneva, Bern, etc.
- **Coverage**: 2015–2024, 26/26 cantons

**No synthetic data. No mockups.** Every number is traceable to its source.

---

## 🏗️ Tech Stack

- **Backend**: FastAPI (optional; v0.1 uses pure Streamlit)
- **Frontend**: Streamlit (simple, auditable, runs anywhere)
- **Data**: Pandas + Polars + Arrow
- **Viz**: Plotly (interactive) + Folium (maps)
- **ML** (Phase 2): PyMC (probabilistic), DoWhy (causal)

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/gemmagardela/swiss-governance-dashboard.git
cd swiss-governance-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Download Real Data
```bash
python src/pipeline/etl.py --all
# Downloads from BFS, BAFU, opendata.swiss, Swisstopo
# Saves to data/raw/ and data/processed/
```

### 3. Run Dashboard
```bash
streamlit run src/frontend/app.py
# Opens at http://localhost:8501
```

### 4. Explore
- Click any canton on the map → zoom to canton detail
- Switch between 7 domain tabs
- Drag timeline (2015–2032)
- Toggle scenario (optimistic / baseline / stress)
- See all KPIs with real data

---

## 📁 Repository Structure

```
swiss-governance-dashboard/
├── README.md                    # This file
├── pyproject.toml              # Dependencies
├── requirements.txt            # Pinned versions
│
├── src/
│   ├── pipeline/
│   │   ├── etl.py             # Download + transform data
│   │   ├── sources.py         # API client wrappers
│   │   └── validate.py        # Data quality checks
│   │
│   ├── frontend/
│   │   ├── app.py             # Main Streamlit app
│   │   ├── pages/             # Multi-page logic
│   │   └── components/        # Reusable UI blocks
│   │
│   └── utils/
│       ├── logging.py
│       ├── constants.py
│       └── formats.py
│
├── data/
│   ├── raw/                   # Direct API downloads (not versioned)
│   ├── processed/             # Cleaned + validated parquets
│   └── static/
│       └── geojson/          # Switzerland boundaries
│
├── notebooks/
│   ├── 00_explore_sources.ipynb
│   └── 01_data_validation.ipynb
│
├── configs/
│   ├── indicators.yaml        # KPI definitions
│   ├── sources.yaml           # API configs (secrets via .env)
│   └── cantons.yaml           # Canton metadata
│
├── docs/
│   ├── SOURCES.md             # Data lineage + certification
│   ├── METHODOLOGY.md         # Statistical methods (Phase 2)
│   ├── API_REFERENCE.md       # Backend API (Phase 2)
│   └── DEPLOYMENT.md          # Cloud setup
│
└── .github/
    └── workflows/
        ├── etl.yml            # Daily: fetch new data
        ├── validate.yml       # Weekly: data quality checks
        └── deploy.yml         # Tag: push to production
```

---

## 🔄 Data Pipeline

```
BFS PXWEB API          opendata.swiss         BAFU NABEL          Swisstopo GeoJSON
      ↓                      ↓                     ↓                      ↓
    CSV/JSON               CSV/JSON              CSV                   GeoJSON
      ↓                      ↓                     ↓                      ↓
   ╔═════════════════════════════════════════════════════════════════════════╗
   │              src/pipeline/etl.py — Extract + Transform                 │
   │  • Normalize column names                                              │
   │  • Fill missing values (interpolation + canton-level defaults)         │
   │  • Validate completeness (26 cantons × 32 indicators × 10 years)      │
   │  • Add metadata (source, update_date, quality_flag)                   │
   └─────────────────────────────────────────────────────────────────────────┘
      ↓
   ╔═════════════════════════════════════════════════════════════════════════╗
   │  data/processed/  — Parquet + Metadata                                 │
   │  • indicators_canton_*.parquet                                         │
   │  • metadata.json (lineage + QA flags)                                  │
   └─────────────────────────────────────────────────────────────────────────┘
      ↓
   ╔═════════════════════════════════════════════════════════════════════════╗
   │  Frontend (Streamlit) — Dashboard                                       │
   │  • Canton map (Swisstopo geojson)                                      │
   │  • 7 domain tabs (32 KPI cards)                                        │
   │  • Timeline + scenario selector                                        │
   │  • Detail panels: district, ranking, composition                       │
   └─────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Data Governance

### Sources & Certification
Every indicator includes:
- **Source authority** (BFS, BAFU, canton, etc.)
- **API endpoint** (exact URL)
- **Update frequency** (daily, weekly, monthly, annual)
- **Coverage** (years available, gaps)
- **Quality notes** (limitations, known issues)
- **Last refresh** (date + time)

See [docs/SOURCES.md](docs/SOURCES.md) for the complete audit trail.

### Reproducibility
```bash
# Re-download all data (fully reproducible)
python src/pipeline/etl.py --all --force

# Validate data quality
python src/pipeline/validate.py

# Audit source lineage
python src/pipeline/sources.py --report
```

### Transparency
- ✅ All code public (AGPL-3.0)
- ✅ All data from official sources
- ✅ Data lineage traceable
- ✅ Methods documented (see Phase 2: METHODOLOGY.md)
- ✅ Human in the loop (no automated decisions)

---

## 🤖 AI Components (Roadmap)

### Phase 1 (Current): Data Foundation ✅
- Real data from official sources
- Dashboard with 32 indicators, 26 cantons
- Full data lineage documentation

### Phase 2: Probabilistic Forecasting
- PyMC models for P10–P90 prediction intervals
- Backtesting 2015–2024 (visible precision metrics)
- SHAP for feature attribution

### Phase 3: Causal Simulation
- Counterfactual engine: "If policy X, impact Y?"
- Causal DAGs per indicator
- Expert validation workflow

### Phase 4: Production Polish
- Anomaly detection + alerts
- NLG: Auto-generated situation reports
- Model cards + audit logs

---

## 🎓 Learning & Use Cases

### For Policy Makers
- "Which metric changed most in my canton last year?"
- "Compare my canton vs. regional peer group"
- "What's the trend if we keep current policies?"

### For Urban Planners
- "Education: which cantons have the highest student-teacher ratio?"
- "Mobility: which cantons are lagging on bike infrastructure?"
- "Energy: which cantons are on track for 80% renewable by 2030?"

### For Data Scientists / Researchers
- Explore Swiss official data APIs
- Reproduce governance analytics
- Extend with causal models or alternative forecasting

---

## 📞 Support & Contributing

**Questions?** Open an issue or reach out to [gemmagardela@gmail.com](mailto:gemmagardela@gmail.com).

**Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

**Data issues?** Please report via [docs/SOURCES.md](docs/SOURCES.md) — include canton, indicator, year.

---

## 📜 License

AGPL-3.0 — Code and documentation are public. You can use, modify, and redistribute freely under the same license.

---

## 🙏 Acknowledgments

- **BFS** (Federal Statistical Office) — Education, energy, housing, waste data
- **BAFU** (Federal Office for the Environment) — Air quality, water, forests
- **Swisstopo** — Canton boundaries and topography
- **opendata.swiss** — Central portal for Swiss open data
- **Canton open-data initiatives** — Zurich, Geneva, Bern, Lucerne, and others

---

**Built by Gemma Gardela** | 2024–2025 | Barcelona / Zurich
