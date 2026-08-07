#!/usr/bin/env python3
"""
FASE 4: FastAPI Backend for Swiss Governance Dashboard

Provides REST API endpoints for:
- Predictions (GET /predict)
- Policy simulations (GET /simulate)
- SHAP explanations (GET /explain)
- Anomaly detection (GET /anomalies)
- Model cards (GET /model-card)

Multi-language support (DE, FR, IT, RM, CA, EN)
Model versioning + audit logs
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
from pathlib import Path
from datetime import datetime
import logging

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Swiss Governance Dashboard API",
    description="Policy impact analysis and forecasting API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class PredictionResponse(BaseModel):
    indicator: str
    domain: str
    value_2024: float
    forecast_2025_2032: Dict[int, Dict[str, float]]
    model_version: str
    unit: str

class SimulationRequest(BaseModel):
    policies: Dict[str, float]  # {policy_id: intensity (0-1)}
    year: int = 2032

class SimulationResponse(BaseModel):
    baseline_2024: float
    baseline_forecast: float
    with_policies_forecast: float
    impact: float
    impact_pct: float
    confidence: str

class ExplanationResponse(BaseModel):
    indicator: str
    explanation: str
    factors: List[Dict[str, Any]]
    confidence: str

class AnomalyResponse(BaseModel):
    indicator: str
    anomaly_score: float
    anomaly_type: str
    alert_level: str
    recommendation: str

class ModelCard(BaseModel):
    indicator: str
    domain: str
    version: str
    training_data: str
    accuracy: Dict[str, float]
    limitations: List[str]
    responsible: str

# ============================================================================
# DATA LOADING
# ============================================================================

def load_json(filename: str) -> Dict:
    """Load JSON data file"""
    filepath = DATA_PROCESSED / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filename}")
    with open(filepath) as f:
        return json.load(f)

# Cache loaded data
predictions_cache = None
shap_cache = None
anomalies_cache = None
real_data_cache = None

def get_predictions():
    global predictions_cache
    if predictions_cache is None:
        predictions_cache = load_json("predictions_2025_2032_v2.json")
    return predictions_cache

def get_shap():
    global shap_cache
    if shap_cache is None:
        shap_cache = load_json("shap_values.json")
    return shap_cache

def get_anomalies():
    global anomalies_cache
    if anomalies_cache is None:
        anomalies_cache = load_json("anomalies.json")
    return anomalies_cache

def get_real_data():
    global real_data_cache
    if real_data_cache is None:
        real_data_cache = load_json("real_data_hybrid.json")
    return real_data_cache

# ============================================================================
# TRANSLATIONS
# ============================================================================

TRANSLATIONS = {
    "ca": {
        "title": "Dashboard de Governança Suïssa",
        "prediction": "Predicció",
        "baseline": "Escenari base",
        "with_policies": "Amb polítiques",
        "impact": "Impacte",
        "confidence": "Confiança"
    },
    "en": {
        "title": "Swiss Governance Dashboard",
        "prediction": "Prediction",
        "baseline": "Baseline scenario",
        "with_policies": "With policies",
        "impact": "Impact",
        "confidence": "Confidence"
    },
    "de": {
        "title": "Schweizer Governance-Dashboard",
        "prediction": "Vorhersage",
        "baseline": "Basis-Szenario",
        "with_policies": "Mit Maßnahmen",
        "impact": "Auswirkung",
        "confidence": "Vertrauen"
    },
    "fr": {
        "title": "Tableau de bord de la gouvernance suisse",
        "prediction": "Prévision",
        "baseline": "Scénario de base",
        "with_policies": "Avec politiques",
        "impact": "Impact",
        "confidence": "Confiance"
    },
    "it": {
        "title": "Dashboard di governance svizzera",
        "prediction": "Previsione",
        "baseline": "Scenario di base",
        "with_policies": "Con politiche",
        "impact": "Impatto",
        "confidence": "Fiducia"
    }
}

def get_translation(lang: str, key: str) -> str:
    """Get translated string"""
    if lang not in TRANSLATIONS:
        lang = "en"
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ============================================================================
# AUDIT LOGGING
# ============================================================================

class AuditLog:
    def __init__(self, log_file: str = "api_audit.jsonl"):
        self.log_file = PROJECT_ROOT / log_file

    def log_request(self, endpoint: str, params: Dict, user: str = "anonymous"):
        """Log API request"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "params": params,
            "user": user
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

audit = AuditLog()

# ============================================================================
# ENDPOINTS: PREDICTIONS
# ============================================================================

@app.get("/predict", response_model=PredictionResponse)
async def predict(
    indicator: str = Query(..., description="Indicator ID (e.g., 'co2', 'nitrats')"),
    lang: str = Query("en", description="Language: ca, en, de, fr, it")
):
    """
    Get forecast for an indicator (2025-2032)

    Example: /predict?indicator=co2
    """
    try:
        audit.log_request("/predict", {"indicator": indicator})

        predictions = get_predictions()
        real_data = get_real_data()

        # Find indicator across domains
        for domain in real_data["domains"]:
            if indicator in domain.get("metrics", {}):
                metric = domain["metrics"][indicator]
                metric_label = metric.get("label", indicator)

                if domain["id"] in predictions["predictions"]:
                    if indicator in predictions["predictions"][domain["id"]]:
                        forecast_data = predictions["predictions"][domain["id"]][indicator]

                        # Extract forecasts by year
                        forecasts_by_year = {}
                        for f in forecast_data.get("forecast", []):
                            forecasts_by_year[f["year"]] = {
                                "p10": f["p10"],
                                "p50": f["p50"],
                                "p90": f["p90"],
                                "std": f["std"]
                            }

                        return PredictionResponse(
                            indicator=indicator,
                            domain=domain["id"],
                            value_2024=forecast_data["last_observed"]["value"],
                            forecast_2025_2032=forecasts_by_year,
                            model_version="polynomial-bayesian-v2",
                            unit=metric.get("unit", "")
                        )

        raise HTTPException(status_code=404, detail=f"Indicator '{indicator}' not found")

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS: SIMULATIONS
# ============================================================================

@app.post("/simulate", response_model=SimulationResponse)
async def simulate(request: SimulationRequest):
    """
    Simulate policy impact on an indicator

    Example: POST /simulate
    {
        "policies": {
            "carbon_tax": 0.5,
            "pv_subsidy": 0.8
        },
        "year": 2032
    }
    """
    try:
        audit.log_request("/simulate", {"policies": request.policies, "year": request.year})

        # Baseline CO2 for demo
        baseline_2024 = 5.3
        baseline_forecast = 4.9  # Without policy

        # Apply policy multipliers
        impact = 0.0
        for policy_name, intensity in request.policies.items():
            # Elasticities (simplified)
            elasticities = {
                "carbon_tax": -0.35,
                "pv_subsidy": -0.18,
                "heat_pump": -0.25,
                "fert_tax": -0.22
            }
            elasticity = elasticities.get(policy_name, 0)
            impact += elasticity * intensity

        with_policies = baseline_forecast * (1 + impact)
        impact_absolute = with_policies - baseline_forecast
        impact_pct = (impact_absolute / baseline_forecast * 100) if baseline_forecast != 0 else 0

        return SimulationResponse(
            baseline_2024=baseline_2024,
            baseline_forecast=baseline_forecast,
            with_policies_forecast=max(0, with_policies),
            impact=impact_absolute,
            impact_pct=impact_pct,
            confidence="high"
        )

    except Exception as e:
        logger.error(f"Simulation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS: EXPLANATIONS (SHAP)
# ============================================================================

@app.get("/explain", response_model=ExplanationResponse)
async def explain(
    indicator: str = Query(..., description="Indicator ID"),
    factor: Optional[str] = Query(None, description="Factor to explain")
):
    """
    Get SHAP explanation for indicator change

    Example: /explain?indicator=co2&factor=energy_mix
    """
    try:
        audit.log_request("/explain", {"indicator": indicator, "factor": factor})

        shap = get_shap()

        # Find explanation
        for domain, indicators in shap.get("explanations", {}).items():
            if indicator in indicators:
                exp = indicators[indicator]

                return ExplanationResponse(
                    indicator=indicator,
                    explanation=exp.get("explanation", ""),
                    factors=[
                        {"name": f["factor"], "shap_value": f["shap_value"]}
                        for f in exp.get("top_factors", [])
                    ],
                    confidence=exp.get("confidence", "medium")
                )

        raise HTTPException(status_code=404, detail=f"Explanation not found for '{indicator}'")

    except Exception as e:
        logger.error(f"Explanation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS: ANOMALIES
# ============================================================================

@app.get("/anomalies", response_model=AnomalyResponse)
async def get_anomalies_endpoint(
    indicator: str = Query(..., description="Indicator ID")
):
    """
    Get anomaly detection results for indicator

    Example: /anomalies?indicator=co2
    """
    try:
        audit.log_request("/anomalies", {"indicator": indicator})

        anomalies = get_anomalies()

        # Find anomaly
        for domain, indicators in anomalies.get("anomalies", {}).items():
            if indicator in indicators:
                anom = indicators[indicator]

                return AnomalyResponse(
                    indicator=indicator,
                    anomaly_score=anom.get("anomaly_score", 0.0),
                    anomaly_type=anom.get("anomaly_type", "normal"),
                    alert_level=anom.get("alert", "None"),
                    recommendation=anom.get("recommendation", "")
                )

        raise HTTPException(status_code=404, detail=f"Anomaly data not found for '{indicator}'")

    except Exception as e:
        logger.error(f"Anomaly error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS: MODEL CARDS
# ============================================================================

@app.get("/model-card")
async def model_card(indicator: str = Query(..., description="Indicator ID")):
    """
    Get model card for an indicator

    Example: /model-card?indicator=co2
    """
    try:
        audit.log_request("/model-card", {"indicator": indicator})

        metadata = load_json("model_metadata_v2.json")

        # Find model metadata
        for domain, indicators in metadata.get("models", {}).items():
            if indicator in indicators:
                model = indicators[indicator]

                return {
                    "indicator": indicator,
                    "domain": domain,
                    "model_version": "polynomial-bayesian-v2",
                    "training_data": "2015-2024 Swiss real data",
                    "accuracy": {
                        "r2": model.get("r2", 0.0),
                        "mape": model.get("mape", 0.0),
                        "cv_mean": model.get("cv_mean", 0.0)
                    },
                    "data_points": model.get("n_training_points", 0),
                    "model_degree": model.get("degree", 1),
                    "limitations": [
                        "Trained on sparse data (typically 2-10 points per indicator)",
                        "Polynomial degree auto-selected via AIC/BIC",
                        "Linear extrapolation beyond 8-year horizon not recommended"
                    ],
                    "responsible": "Swiss Data Science Team",
                    "created": datetime.utcnow().isoformat()
                }

        raise HTTPException(status_code=404, detail=f"Model card not found for '{indicator}'")

    except Exception as e:
        logger.error(f"Model card error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENDPOINTS: HEALTH & INFO
# ============================================================================

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/info")
async def info(lang: str = Query("en")):
    """API information"""
    return {
        "title": get_translation(lang, "title"),
        "version": "1.0.0",
        "endpoints": [
            "/predict - Get indicator forecast",
            "/simulate - Simulate policy impact",
            "/explain - Get SHAP explanation",
            "/anomalies - Get anomaly detection",
            "/model-card - Get model metadata",
            "/docs - Interactive API documentation"
        ],
        "languages": ["ca", "en", "de", "fr", "it"],
        "data_sources": "Official Swiss data (BFS, BAFU, SFOE, etc.)",
        "last_updated": datetime.utcnow().isoformat()
    }

# ============================================================================
# ROOT & DOCUMENTATION
# ============================================================================

@app.get("/")
async def root():
    """API root"""
    return {
        "title": "Swiss Governance Dashboard API",
        "description": "Policy impact analysis and forecasting",
        "version": "1.0.0",
        "documentation": "/docs",
        "base_url": "https://api.swiss-governance-dashboard.ch/v1"
    }

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
