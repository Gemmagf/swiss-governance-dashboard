# 🚀 Deployment & Integration Guide

## Current State

You have **two versions**:

1. **Streamlit App** (`src/frontend/app_v2.py`)
   - Python-based, interactive
   - Great for development/demo
   - Requires Python runtime

2. **Pure HTML Dashboard** (`dashboard.html`) ⭐ **RECOMMENDED FOR PRODUCTION**
   - Self-contained, no dependencies
   - Professional look & feel (like mockups)
   - Deploy anywhere: GitHub Pages, AWS S3, Vercel, etc.
   - Agnóstic to data (easy to populate)

---

## Phase 1: Deploy the HTML Dashboard (Today)

### Option A: GitHub Pages (Free, Instant)

```bash
# 1. Initialize git repo (if not already done)
cd /Users/gemmagardela/swiss-governance-dashboard
git init
git add dashboard.html
git commit -m "Initial: HTML dashboard with synthetic data"

# 2. Push to GitHub
git remote add origin https://github.com/YOUR_USER/swiss-governance-dashboard.git
git branch -M main
git push -u origin main

# 3. Enable GitHub Pages
# → Settings → Pages → Source: main branch → Save
# Your dashboard is now live at: https://YOUR_USER.github.io/swiss-governance-dashboard/dashboard.html
```

### Option B: AWS S3 (Production-Grade)

```bash
# 1. Upload to S3
aws s3 cp dashboard.html s3://my-bucket/dashboard.html --acl public-read

# 2. Enable static website hosting
aws s3 website s3://my-bucket --index-document dashboard.html

# Your dashboard is now live at: http://my-bucket.s3-website-region.amazonaws.com/dashboard.html
```

### Option C: Vercel (Easiest for Full Stack)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# Your dashboard is live at: https://your-project.vercel.app/dashboard.html
```

---

## Phase 2: Populate with Real Data (Week 2)

The HTML dashboard reads data from a **JSON data structure**. Currently it's hardcoded; you'll replace it with real data.

### How It Works Today (Synthetic)

Inside `dashboard.html`, find this section:

```javascript
const THEMES = [
    {id: "agua", label: "Water", accent: "#17789B", soft: "#E3EEF2", metrics: [
        {id: "consum", label: "Drinking water consumption", unit: "l/hab·day", base: 305},
        {id: "perdues", label: "Network losses", unit: "%", base: 12.4},
        ...
    ]},
    ...
];
```

The `base` values are what get rendered. The `value()` function adds realistic noise.

### To Use Real Data from APIs

**Create a `data-api.js`:**

```javascript
// data-api.js
async function fetchBFSData(indicator, canton, year) {
    // Call BFS PXWEB API
    const url = `https://www.pxweb.bfs.admin.ch/api/v1/...`;
    const response = await fetch(url);
    return response.json();
}

async function fetchOpenDataSwiss(dataset) {
    // Call opendata.swiss
    const url = `https://ckan.opendata.swiss/api/3/action/package_show?name=${dataset}`;
    const response = await fetch(url);
    return response.json();
}

async function buildDataFromAPIs() {
    // Fetch all 32 indicators from their respective APIs
    // Returns object matching the THEMES structure
    return {
        "agua": {
            "consum": {2015: 310, 2016: 308, 2017: 305, ...},
            "perdues": {2015: 13.2, 2016: 12.8, ...},
            ...
        },
        ...
    };
}
```

**Modify `dashboard.html` to load from API:**

```javascript
// Replace the hardcoded THEMES with:
let THEMES = [];

(async () => {
    const dataFromAPIs = await buildDataFromAPIs();
    THEMES = convertToThemesStructure(dataFromAPIs);
    render(true); // Initialize dashboard
})();
```

---

## Phase 3: Integrate ML Models (Week 3-4)

Once you have real data, you'll add predictions from trained models.

### Workflow

1. **Train models offline** (Python, PyMC/sklearn)
   - Feed real 2015–2024 data
   - Outputs: predictions + P10/P90 intervals

2. **Export predictions as JSON**
   ```python
   import json
   predictions = {
       "agua_consum": {
           "2025": {"mean": 295, "p10": 290, "p90": 300},
           "2026": {"mean": 292, "p10": 285, "p90": 299},
           ...
       }
   }
   json.dump(predictions, open("predictions.json", "w"))
   ```

3. **Load in dashboard**
   ```javascript
   const predictions = await fetch("predictions.json").then(r => r.json());
   
   // Add forecast to chart
   const traceForecast = {
       x: [2025, 2026, 2027, ...],
       y: predictions["agua_consum"].map(p => p.mean),
       fill: "tonexty",
       fillcolor: "rgba(23, 120, 155, 0.1)",
       name: "Forecast"
   };
   ```

### Model Structure (Recommended)

```
models/
├── water_consumption.pkl      # Trained PyMC model
├── water_network_loss.pkl
├── energy_co2_emissions.pkl
├── housing_rental.pkl
└── ...
```

**Python script to serve predictions:**

```python
# serve_predictions.py
from flask import Flask, jsonify
import pickle
import json

app = Flask(__name__)

@app.route("/api/v1/predict/<metric>/<canton>", methods=["GET"])
def predict(metric, canton):
    model = pickle.load(open(f"models/{metric}.pkl", "rb"))
    prediction = model.predict(canton, years=[2025, 2026, 2027, ...])
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(port=5000)
```

Then in dashboard:

```javascript
async function fetchPredictions(metric, canton) {
    const response = await fetch(`http://localhost:5000/api/v1/predict/${metric}/${canton}`);
    return response.json();
}
```

---

## Phase 4: Full Production Stack (Month 2)

### Recommended Architecture

```
┌─────────────────────────────────────────────────────┐
│         Frontend (HTML/JS Dashboard)                │
│  ├─ dashboard.html (static, deployed to S3/Vercel) │
│  └─ Reads from API Gateway                         │
└──────────────────────┬────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│         API Layer (FastAPI or Lambda)              │
│  ├─ GET /api/v1/data/{metric}/{canton}/{year}     │
│  ├─ GET /api/v1/predict/{metric}/{canton}         │
│  ├─ GET /api/v1/backtest/{metric}/{canton}        │
│  └─ POST /api/v1/simulate (counterfactuals)       │
└──────────────────────┬────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│      Data & Models Layer                            │
│  ├─ PostgreSQL (real data + cache)                 │
│  ├─ BFS PXWEB API connector (ETL)                  │
│  ├─ opendata.swiss connector (ETL)                 │
│  ├─ PyMC models (predictions)                      │
│  └─ Backtesting system                             │
└─────────────────────────────────────────────────────┘
```

### Example: AWS Serverless

```
dashboard.html (S3)
    ↓
API Gateway (https://api.example.com)
    ↓
Lambda functions (Python)
    ├─ GET /data → Fetch from RDS
    ├─ GET /predict → Load PyMC model, predict
    └─ POST /simulate → Counterfactual engine
    ↓
RDS PostgreSQL (real data cache)
```

Deploy with:

```bash
# Use AWS SAM
sam init
sam build
sam deploy
```

---

## File Structure After Full Implementation

```
swiss-governance-dashboard/
├── dashboard.html                    # Main dashboard (static)
├── data-api.js                      # API client wrappers
├── predictions.json                 # Precomputed predictions
│
├── backend/
│   ├── app.py                       # FastAPI server
│   ├── models/
│   │   ├── water_consumption.pkl
│   │   ├── energy_co2.pkl
│   │   └── ...
│   ├── data/
│   │   └── cache.db                 # SQLite or PostgreSQL
│   └── etl/
│       ├── bfs_connector.py
│       ├── opendata_connector.py
│       └── batch_update.py          # Daily sync from APIs
│
├── notebooks/
│   ├── 01_train_models.ipynb        # PyMC fitting
│   ├── 02_backtesting.ipynb         # Validation
│   └── 03_sensitivity.ipynb         # Causal checks
│
└── .github/workflows/
    ├── fetch-data.yml               # Daily: fetch new data
    ├── retrain-models.yml           # Weekly: retrain models
    └── deploy.yml                   # Deploy dashboard to S3
```

---

## Timeline & Effort

| Phase | Timeline | Effort | Output |
|-------|----------|--------|--------|
| **1: Deploy HTML** | Today | 1 hour | Live dashboard (synthetic data) |
| **2: Real Data** | Week 1–2 | 3–5 days | Connect to BFS, opendata.swiss |
| **3: Models + Predictions** | Week 3–4 | 1 week | PyMC models, backtesting, predictions |
| **4: Full API + Simulation** | Month 2 | 2 weeks | Counterfactuals, full production stack |
| **5: Launch + Demo** | Month 2 | — | Present to Swiss administrations |

---

## Current Action Items

### Today (Phase 1)
- [ ] Deploy `dashboard.html` to GitHub Pages or S3
- [ ] Share link with stakeholders
- [ ] Get feedback on UI/UX

### Next Week (Phase 2)
- [ ] Create `data-api.js` wrapper
- [ ] Test BFS PXWEB API connectivity
- [ ] Replace synthetic data with real data

### Week After (Phase 3)
- [ ] Train PyMC models on 2015–2024 real data
- [ ] Generate prediction JSON
- [ ] Integrate into dashboard

### Month 2 (Phase 4)
- [ ] Build FastAPI backend
- [ ] Deploy to AWS Lambda + API Gateway
- [ ] Full production stack ready

---

## Key Points

✅ **Dashboard is ready now** — no waiting, deploy immediately
✅ **Agnóstic to data** — easily swap synthetic → real → predictions
✅ **No Python required to run** — HTML/JS only (no Streamlit needed)
✅ **Scalable architecture** — goes from static file → full serverless stack
✅ **Models are separate** — train in notebooks, load as JSON
✅ **Version control friendly** — git handles dashboard + code + predictions

---

## Support

**Need help with:**
- BFS API authentication? → See `docs/API_REFERENCE.md`
- PyMC model training? → See `notebooks/01_train_models.ipynb`
- AWS deployment? → See `docs/DEPLOYMENT.md`

---

**Next Step:** Deploy `dashboard.html` somewhere, then populate it with real data. You're in charge of the pace! 🚀
