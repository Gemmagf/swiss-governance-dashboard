# 🚀 GitHub Pages Setup — FASE 1 Live Deployment

## Status
✅ **Code pushed to GitHub**: https://github.com/Gemmagf/swiss-governance-dashboard

## 🎯 LIVE URL (when enabled)
```
https://gemmagf.github.io/swiss-governance-dashboard/
```

---

## 📋 Steps to Enable GitHub Pages (5 min)

### Option A: GitHub Web UI (Easiest)
1. Go to: https://github.com/Gemmagf/swiss-governance-dashboard
2. Click: **Settings** (top right)
3. Left sidebar: **Pages**
4. Under "Build and deployment":
   - Source: **Deploy from branch**
   - Branch: **main**
   - Folder: **(root)**
5. Click **Save**
6. Wait 5–10 minutes
7. Visit: https://gemmagf.github.io/swiss-governance-dashboard/

### Option B: GitHub CLI (if installed)
```bash
gh repo edit Gemmagf/swiss-governance-dashboard \
  --enable-github-pages=true \
  --github-pages-branch=main \
  --github-pages-source=/(root)
```

---

## 📍 What Gets Deployed

### Main Files
| File | URL |
|------|-----|
| **Dashboard (Mockup)** | `/dashboard_real.html` |
| **Data (JSON)** | `/data/processed/real_data_hybrid.json` |
| **Documentation** | `/FASE_1_COMPLETE.md` |
| **Sources Catalog** | `/DATA_SOURCES_COMPLETE.md` |

### Direct Links (after Pages enabled)
- Dashboard: https://gemmagf.github.io/swiss-governance-dashboard/dashboard_real.html
- Data: https://gemmagf.github.io/swiss-governance-dashboard/data/processed/real_data_hybrid.json
- Docs: https://gemmagf.github.io/swiss-governance-dashboard/FASE_1_COMPLETE.md

---

## ✅ Verification Checklist

After enabling Pages (wait ~10 min):

- [ ] Visit https://gemmagf.github.io/swiss-governance-dashboard/
- [ ] See the dashboard load (header visible)
- [ ] Click "Bosc" domain → should load indicators
- [ ] Open browser console (F12) → no 404 errors for data files
- [ ] Timeline slider works (2015–2024)
- [ ] Escenaris buttons (Acord, Tendencial, Estrès)

---

## 🔧 Troubleshooting

### "404 Not Found"
**Cause**: Pages not yet enabled or wrong URL
**Fix**: 
1. Check https://github.com/Gemmagf/swiss-governance-dashboard/settings/pages
2. Verify source is set to "main / (root)"
3. Wait 10 minutes for GitHub to build

### "Cannot load data/processed/real_data_hybrid.json"
**Cause**: Path mismatch (pages root != dashboard root)
**Fix**: 
```javascript
// In dashboard, use root-relative paths:
fetch('/swiss-governance-dashboard/data/processed/real_data_hybrid.json')
```

### Dashboard loads but no data
**Cause**: CORS or fetch path issue
**Fix**: 
1. Open DevTools (F12)
2. Check Network tab for failed requests
3. Verify file exists: `/data/processed/real_data_hybrid.json`

---

## 📊 What's Live

### Dashboard (FASE 1)
- ✅ Structure: 100% mockup-faithful
- ✅ Interactivity: Domains, timeline, scenarios
- ✅ Data: 35 real indicators (7 domains)
- ✅ Sources: 50+ official Swiss APIs documented

### Dataset
- ✅ File: `real_data_hybrid.json`
- ✅ Coverage: 26 cantons, 2015–2024, 35 indicators
- ✅ Sources: BFS, BAFU, SFOE, OFSP, WSL, Swisstopo, SBB, opendata.swiss

---

## 🎯 Next Steps (FASE 2–4)

### FASE 2: ML Models
- Train PyMC on real data (2015–2024)
- Generate predictions (2025–2032)
- P10–P90 prediction intervals
- Timeline: 1–2 weeks

### FASE 3: Specialties
- Policy simulator (levers)
- Causal inference
- SHAP explainability
- Anomaly detection
- Timeline: 1 week

### FASE 4: Production Stack
- FastAPI backend
- Multi-language (DE, FR, IT, RM)
- PDF export
- Full API surface
- Timeline: 3–5 days

---

## 📝 File Structure (deployed)

```
📦 https://gemmagf.github.io/swiss-governance-dashboard/
├── dashboard_real.html              ← Main dashboard
├── data/
│   ├── processed/
│   │   ├── real_data_hybrid.json   ← 35 indicators
│   │   └── metadata.json
│   └── static/
│       └── geojson/
│           └── swiss_cantons.geojson
├── src/
│   ├── frontend/
│   │   ├── app.py
│   │   └── app_v2.py
│   └── pipeline/
│       └── fetch_all_real_data.py
├── FASE_1_COMPLETE.md               ← Docs
├── DATA_SOURCES_COMPLETE.md         ← Sources catalog
└── README.md                        ← (to create)
```

---

## 🔐 Security Notes

- ✅ No API keys in repo (all public APIs)
- ✅ No secrets in URLs or code
- ✅ No authentication required
- ✅ CORS safe (local + GitHub Pages origin)

---

## 📞 Support

For issues with GitHub Pages:
- GitHub Docs: https://docs.github.com/en/pages
- Status: https://www.githubstatus.com/

For issues with dashboard:
1. Check Network tab (F12)
2. Verify files exist in repo
3. Clear browser cache (Ctrl+Shift+Del)
4. Try incognito window

---

**Created**: August 7, 2026  
**Status**: Ready for deployment  
**Next**: FASE 2 ML models  

