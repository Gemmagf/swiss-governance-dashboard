# 🤖 FASE 2: MODELS ML ENTRENATS

**Data**: 7 d'agost de 2026  
**Status**: FUNCIONAL (models lineal simple; millora necessària)  
**Responsable**: Gemma Gardela

---

## ✅ QUÈ S'HA ACONSEGUIT

### **Entrenament de Models Bayesians**
- ✅ 35 indicadors entrenats (7 dominis × 5 indicadors)
- ✅ Linear regression amb incertesa (P10–P90)
- ✅ Predictions 2025–2032 (8 anys futurs)
- ✅ Backtesting 2015–2024

### **Fitxers Generats**

| Fitxer | Mida | Contingut |
|--------|------|----------|
| `predictions_2025_2032.json` | 75.9 KB | Predictions + P10–P90 intervals |
| `backtesting_metrics.json` | — | MAPE, MAE per validació |

---

## 📊 ESTRUCTURA DE PREDICTIONS

```json
{
  "metadata": {
    "model_version": "linear-bayesian-v1",
    "forecast_period": "2025–2032",
    "domains": 7,
    "indicators": 35
  },
  "predictions": {
    "bosc": {
      "superficie": {
        "label": "Superfície forestal",
        "unit": "% del territori",
        "last_observed": {"year": 2024, "value": 31.6},
        "forecast": [
          {
            "year": 2025,
            "p10": X,    ← 10th percentile (pessimistic)
            "p50": Y,    ← median (expected)
            "p90": Z,    ← 90th percentile (optimistic)
            "std": σ,    ← uncertainty
            "status": "forecast",
            "model": "linear-bayesian-v1"
          },
          ...
        ]
      }
    }
  }
}
```

---

## 🎯 MODEL: Linear Bayesian Regression

### Fórmula
```
y_t = intercept + slope × (t - t0) + ε_t
ε_t ~ N(0, σ_residual)

Forecast: y_{t+h} ~ N(μ, σ_forecast)
σ_forecast = σ_residual × (1 + horizon_factor × h)
```

### Avantatges
- Simple, interpretable, ràpid
- P10–P90 intervals sense supòsits distribucionals
- Funciona amb poques dades (5–10 punts)

### Limitacions
- **NO captura no-linearitats** (alguns indicadors creixen exponencialment)
- **NO modelitza tendències canviants** (policy breaks)
- **Intervals constants** (haurien de dependre de la qualitat de la font)

---

## ⚠️ QUALITAT ACTUAL: BAIXA (necessita millora)

### Backtesting Results
```
MAPE promig: 3854% ❌
MAPE mediana: 1110% ❌
Indicadors < 5% error: 0/35
Indicadors > 10% error: 35/35
```

### Explicació de l'error
1. **Dades insuficients**: Molts indicadors només tenen 5–6 punts (2004, 2009, 2014, 2019, 2024)
2. **Backtesting pobre**: Hold-out només 1 any (2024) — estadísticament débil
3. **Model lineal inadequat**: Indicadors amb tendències curvades necessiten polinomis o transformacions

---

## 🔧 MILLORES PER A FASE 2.2 (next iteration)

### 1. Millor Model de Regressió
```python
# Actual: Linear
y = a + b*t

# Proposat: Polinomial 2n ordre
y = a + b*t + c*t²

# Millor: Gaussian Process o LOESS
# Captura tendències complexes amb incertesa adaptativa
```

### 2. Backtesting Robust
```
# Actual: Hold-out últim any (1 punt)

# Proposat: K-fold cross-validation
# Entrenar: 2015–2022
# Validar: 2023, 2024
# Mètrica: RMSE, MAE, directional accuracy
```

### 3. Priors Bayesians Informatius
```
# Per a cada indicador:
# - Prior sobre el trend: "creïxement esperant" per categoria
# - Prior sobre volatilitat: depèn de la font
# - Hierarchical model: compartir informació entre cantons

# Exemple (Energia CO₂):
# Prior: "baixa ~3% per any" (política de descarbonització)
# Likelihood: dades 2015–2024
# Posterior: predicció amb aquesta informació prèvia
```

---

## 📈 PREDICTIONS REALS (MOSTRA)

### Bosc i Biodiversitat
- **Superfície forestal**: 31.6% (2024) → 31.8% (2032, p50)
- **Vitalitat capçada**: 74 (2024) → ? (depèn de trend)

### Energia i Clima
- **CO₂ emissions**: 5.3 t/hab (2024) → 4.5 t/hab (2032, p50)
- **Renovables**: 23% (2024) → 35% (2032, p50, optimista)

### Educació
- **Ràtio alumnat/docent**: 14.9 (2024) → 14.7 (2032)
- **Digital infrastructure**: 36% (2024) → 85% (2032, optimista)

---

## 🚀 INTEGRACIÓ AL DASHBOARD (FASE 2.5)

Una vegada els models millors:

### Modification a `dashboard_real.html`
```javascript
// Afegir predictions al timeline
timeline.max = 2032  // estendre fins 2032

// Afegir banda de confiança al gràfic
chart.addTrace({
  x: [2025, 2026, ..., 2032],
  y: p50_values,
  fill: 'tonexty',
  fillcolor: 'rgba(blue, 0.2)',
  name: 'P10–P90 interval'
});

// Afegir etiqueta de model
card.append(`Model: ${model_version} | RMSE: ${rmse.toFixed(2)}`);
```

### Scenarios
```
Base:       P50 predictions (tendència actual)
Optimista:  P90 predictions (escenari amb polítiques)
Stress:     P10 predictions (sense polítiques)
```

---

## 📁 FITXERS DE FASE 2

```
✅ src/pipeline/train_models.py       — Script de training
✅ data/processed/predictions_2025_2032.json    — Predictions
✅ data/processed/backtesting_metrics.json      — Validació
✅ FASE_2_MODELS.md                  — Aquesta documentació
```

---

## 🎯 NEXT STEPS

### FASE 2.2: Millora de Models (1 setmana)
```
□ Implementar polynomial regression
□ K-fold cross-validation
□ Hierarchical Bayesian models
□ Bayesian priors per categoria de domain
□ Model selection (AIC/BIC)
```

### FASE 3: Especialitats (1 setmana)
```
□ Causal DAGs per indicador
□ Counterfactual simulator
□ SHAP feature attribution
□ Anomaly detection
```

### FASE 4: Production (3–5 días)
```
□ FastAPI backend per predictions
□ Model versioning + serving
□ Multi-language UI (DE, FR, IT, RM, CA, EN)
□ PDF export + model cards
```

---

## 🌐 NOTA: MULTILINGÜE (per FASE 4)

Requisit: Dashboard disponible en:
- ✅ Català
- □ Alemany (CH)
- □ Francés (CH)
- □ Italià (CH)
- □ Romanx (CH)
- □ Anglès

Implementació a FASE 4 amb i18n framework.

---

## ✨ CONCLUSION

**FASE 2 estructura és funcional**:
- ✅ Models entrenats (linear simple, millorable)
- ✅ Predictions generades (2025–2032)
- ✅ P10–P90 intervals de confiança
- ✅ Backtesting infrastructure

**Qualitat del model**: Baixa (MAPE 3854%) perquè linear model inadequat + poques dades. **FASE 2.2 millorarà significantment** amb polynomial models + priors Bayesians.

**Pròxim**: FASE 2.2 millora de models, llavors FASE 3 especialitats.

---

**Gemma Gardela · 7 d'agost de 2026**

