#!/usr/bin/env python3
"""
FASE 3: Causal DAGs (Directed Acyclic Graphs)

Define causal relationships per indicator + domain.
Used for:
- Identifying confounders + mediators
- Policy effect estimation
- Counterfactual simulations
"""

# ============================================================================
# CAUSAL DAGs PER DOMAIN
# ============================================================================

CAUSAL_DAGS = {
    "bosc": {
        "label": "Bosc i biodiversitat",
        "metrics": {
            "superficie": {
                "label": "Superfície forestal",
                "dag": {
                    "outcome": "superficie",
                    "direct_causes": ["precipitation", "temperature", "forest_management"],
                    "confounders": ["topography", "historical_use"],
                    "mediators": ["soil_quality", "species_composition"],
                    "policy_levers": ["area_protected", "reforestation_program", "harvesting_reduction"]
                },
                "elasticities": {
                    "area_protected": {"effect": 0.15, "lag_years": 2},
                    "reforestation_program": {"effect": 0.20, "lag_years": 3},
                    "harvesting_reduction": {"effect": -0.10, "lag_years": 1}
                }
            },
            "vitalitat": {
                "label": "Vitalitat de la capçada",
                "dag": {
                    "outcome": "vitalitat",
                    "direct_causes": ["precipitation", "temperature", "pest_pressure", "forest_age"],
                    "confounders": ["elevation", "soil_type"],
                    "mediators": ["water_stress", "nutrient_availability"],
                    "policy_levers": ["pest_monitoring", "water_retention_works", "species_diversification"]
                },
                "elasticities": {
                    "pest_monitoring": {"effect": 0.18, "lag_years": 1},
                    "water_retention_works": {"effect": 0.22, "lag_years": 2},
                    "species_diversification": {"effect": 0.12, "lag_years": 4}
                }
            }
        }
    },

    "aigua": {
        "label": "Aigua",
        "metrics": {
            "consum": {
                "label": "Consum d'aigua potable",
                "dag": {
                    "outcome": "consum",
                    "direct_causes": ["population", "income_level", "temperature", "industrial_activity"],
                    "confounders": ["urbanization", "water_availability"],
                    "mediators": ["irrigation_efficiency", "household_behavior"],
                    "policy_levers": ["price_increase", "efficiency_standards", "awareness_campaign", "industrial_recycling"]
                },
                "elasticities": {
                    "price_increase": {"effect": -0.25, "lag_years": 1},
                    "efficiency_standards": {"effect": -0.18, "lag_years": 2},
                    "awareness_campaign": {"effect": -0.08, "lag_years": 1},
                    "industrial_recycling": {"effect": -0.12, "lag_years": 3}
                }
            },
            "nitrats": {
                "label": "Nitrats a l'aigua subterrània",
                "dag": {
                    "outcome": "nitrats",
                    "direct_causes": ["agricultural_intensity", "fertilizer_use", "precipitation", "groundwater_flow"],
                    "confounders": ["soil_permeability", "land_use"],
                    "mediators": ["denitrification", "plant_uptake"],
                    "policy_levers": ["fertilizer_tax", "precision_agriculture", "riparian_buffer_zones", "organic_farming_subsidy"]
                },
                "elasticities": {
                    "fertilizer_tax": {"effect": -0.22, "lag_years": 2},
                    "precision_agriculture": {"effect": -0.15, "lag_years": 2},
                    "riparian_buffer_zones": {"effect": -0.18, "lag_years": 3},
                    "organic_farming_subsidy": {"effect": -0.12, "lag_years": 4}
                }
            }
        }
    },

    "educacio": {
        "label": "Educació",
        "metrics": {
            "ratio": {
                "label": "Ràtio alumnat per docent",
                "dag": {
                    "outcome": "ratio",
                    "direct_causes": ["budget_education", "teacher_supply", "student_enrollment", "teacher_retention"],
                    "confounders": ["gdp_per_capita", "urbanization"],
                    "mediators": ["teacher_recruitment", "classroom_availability"],
                    "policy_levers": ["salary_increase", "teacher_training_program", "classroom_investment", "recruitment_campaign"]
                },
                "elasticities": {
                    "salary_increase": {"effect": 0.20, "lag_years": 2},
                    "teacher_training_program": {"effect": 0.10, "lag_years": 1},
                    "classroom_investment": {"effect": 0.15, "lag_years": 2},
                    "recruitment_campaign": {"effect": 0.12, "lag_years": 1}
                }
            },
            "digital": {
                "label": "Centres amb infraestructura digital",
                "dag": {
                    "outcome": "digital",
                    "direct_causes": ["budget_ict", "teacher_training", "internet_availability", "device_supply"],
                    "confounders": ["school_size", "urbanization"],
                    "mediators": ["teacher_competence", "adoption_rate"],
                    "policy_levers": ["ict_investment", "teacher_upskilling", "device_subsidy", "cloud_infrastructure"]
                },
                "elasticities": {
                    "ict_investment": {"effect": 0.30, "lag_years": 1},
                    "teacher_upskilling": {"effect": 0.18, "lag_years": 2},
                    "device_subsidy": {"effect": 0.22, "lag_years": 1},
                    "cloud_infrastructure": {"effect": 0.15, "lag_years": 2}
                }
            }
        }
    },

    "mobilitat": {
        "label": "Mobilitat",
        "metrics": {
            "tp": {
                "label": "Viatges en transport públic",
                "dag": {
                    "outcome": "tp",
                    "direct_causes": ["pt_frequency", "pt_cost", "pt_coverage", "car_cost", "congestion"],
                    "confounders": ["density", "employment_centers"],
                    "mediators": ["accessibility", "comfort_perception"],
                    "policy_levers": ["frequency_increase", "fare_reduction", "network_expansion", "car_pricing"]
                },
                "elasticities": {
                    "frequency_increase": {"effect": 0.32, "lag_years": 1},
                    "fare_reduction": {"effect": 0.28, "lag_years": 1},
                    "network_expansion": {"effect": 0.25, "lag_years": 2},
                    "car_pricing": {"effect": 0.38, "lag_years": 1}
                }
            },
            "bici": {
                "label": "Quota modal de bicicleta",
                "dag": {
                    "outcome": "bici",
                    "direct_causes": ["bike_infrastructure", "topography", "weather", "distance_to_work", "car_cost"],
                    "confounders": ["income_level", "culture"],
                    "mediators": ["safety_perception", "convenience"],
                    "policy_levers": ["bike_lane_expansion", "bike_sharing_subsidy", "parking_provision", "e_bike_subsidy"]
                },
                "elasticities": {
                    "bike_lane_expansion": {"effect": 0.29, "lag_years": 2},
                    "bike_sharing_subsidy": {"effect": 0.15, "lag_years": 1},
                    "parking_provision": {"effect": 0.18, "lag_years": 2},
                    "e_bike_subsidy": {"effect": 0.22, "lag_years": 1}
                }
            }
        }
    },

    "energia": {
        "label": "Energia i clima",
        "metrics": {
            "co2": {
                "label": "Emissions de GEH",
                "dag": {
                    "outcome": "co2",
                    "direct_causes": ["energy_consumption", "heating_fuel_mix", "transport_fuel_mix", "industrial_output"],
                    "confounders": ["gdp", "population", "climate"],
                    "mediators": ["electrification", "renewable_share"],
                    "policy_levers": ["carbon_tax", "pv_subsidy", "heat_pump_retrofit", "ev_incentive", "industrial_emission_trading"]
                },
                "elasticities": {
                    "carbon_tax": {"effect": -0.35, "lag_years": 2},
                    "pv_subsidy": {"effect": -0.18, "lag_years": 2},
                    "heat_pump_retrofit": {"effect": -0.33, "lag_years": 3},
                    "ev_incentive": {"effect": -0.15, "lag_years": 2},
                    "industrial_emission_trading": {"effect": -0.22, "lag_years": 3}
                }
            },
            "renov": {
                "label": "Quota renovable",
                "dag": {
                    "outcome": "renov",
                    "direct_causes": ["hydroelectric_capacity", "solar_capacity", "wind_capacity", "fossil_retirement"],
                    "confounders": ["geography", "water_availability"],
                    "mediators": ["grid_investment", "storage_capacity"],
                    "policy_levers": ["pv_target", "wind_expansion", "hydropower_upgrade", "grid_modernization"]
                },
                "elasticities": {
                    "pv_target": {"effect": 0.20, "lag_years": 2},
                    "wind_expansion": {"effect": 0.18, "lag_years": 3},
                    "hydropower_upgrade": {"effect": 0.12, "lag_years": 4},
                    "grid_modernization": {"effect": 0.15, "lag_years": 2}
                }
            }
        }
    },

    "serveis": {
        "label": "Salut i serveis públics",
        "metrics": {
            "metges": {
                "label": "Metges de família",
                "dag": {
                    "outcome": "metges",
                    "direct_causes": ["doctor_supply", "salary_level", "working_conditions", "medical_education"],
                    "confounders": ["urbanization", "income_level"],
                    "mediators": ["recruitment_success", "retention_rate"],
                    "policy_levers": ["salary_increase", "working_conditions_improvement", "rural_incentive", "training_subsidy"]
                },
                "elasticities": {
                    "salary_increase": {"effect": 0.15, "lag_years": 2},
                    "working_conditions_improvement": {"effect": 0.12, "lag_years": 1},
                    "rural_incentive": {"effect": 0.18, "lag_years": 1},
                    "training_subsidy": {"effect": 0.10, "lag_years": 3}
                }
            },
            "espera": {
                "label": "Temps d'espera",
                "dag": {
                    "outcome": "espera",
                    "direct_causes": ["emergency_volume", "staffing_level", "icu_capacity", "triage_efficiency"],
                    "confounders": ["hospital_size", "demographics"],
                    "mediators": ["process_efficiency", "resource_allocation"],
                    "policy_levers": ["staff_hiring", "triage_improvement", "icu_expansion", "primary_care_strengthening"]
                },
                "elasticities": {
                    "staff_hiring": {"effect": -0.28, "lag_years": 1},
                    "triage_improvement": {"effect": -0.15, "lag_years": 1},
                    "icu_expansion": {"effect": -0.22, "lag_years": 2},
                    "primary_care_strengthening": {"effect": -0.25, "lag_years": 2}
                }
            }
        }
    },

    "territori": {
        "label": "Territori i habitatge",
        "metrics": {
            "lloguer": {
                "label": "Lloguer mitjà",
                "dag": {
                    "outcome": "lloguer",
                    "direct_causes": ["housing_supply", "demand", "location_desirability", "income_level", "interest_rates"],
                    "confounders": ["gdp", "urbanization"],
                    "mediators": ["investment_attractiveness", "construction_cost"],
                    "policy_levers": ["housing_construction", "rent_control", "affordable_housing_subsidy", "interest_rate_policy"]
                },
                "elasticities": {
                    "housing_construction": {"effect": -0.18, "lag_years": 2},
                    "rent_control": {"effect": -0.25, "lag_years": 1},
                    "affordable_housing_subsidy": {"effect": -0.20, "lag_years": 2},
                    "interest_rate_policy": {"effect": 0.30, "lag_years": 1}
                }
            },
            "vacants": {
                "label": "Taxa d'habitatges buits",
                "dag": {
                    "outcome": "vacants",
                    "direct_causes": ["housing_stock", "turnover_rate", "investment_property_share", "speculation"],
                    "confounders": ["wealth_level", "immigration"],
                    "mediators": ["maintenance_incentive", "rental_return"],
                    "policy_levers": ["vacancy_tax", "owner_incentive", "rental_control", "speculation_tax"]
                },
                "elasticities": {
                    "vacancy_tax": {"effect": -0.35, "lag_years": 1},
                    "owner_incentive": {"effect": -0.12, "lag_years": 2},
                    "rental_control": {"effect": -0.22, "lag_years": 1},
                    "speculation_tax": {"effect": -0.30, "lag_years": 1}
                }
            }
        }
    }
}

# ============================================================================
# DAG DOCUMENTATION
# ============================================================================

DAG_STRUCTURE = """
Each indicator DAG includes:

1. outcome: The target variable (e.g., "co2_emissions")

2. direct_causes: Variables that directly cause the outcome
   (e.g., energy_consumption → CO₂)

3. confounders: Common causes of both outcome + treatment
   (e.g., GDP causes both emissions AND renewable investment)
   → Must be controlled in causal inference

4. mediators: Variables through which policy effects propagate
   (e.g., carbon_tax → electrification → CO₂ reduction)
   → Used to trace mechanisms

5. policy_levers: Interventions that decision-makers control
   (e.g., carbon_tax, pv_subsidy)
   → Each has elasticity (effect size) + lag (delay in effect)

Example: CO₂ Emissions DAG
─────────────────────────
    Confounders (uncontrolled)
         ↓
    GDP ← → Population ← → Climate

    Direct Causes
         ↓
    Energy mix → [CO₂ Emissions] ← Energy consumption
         ↓
    Transport mix

    Mediators (mechanism)
         ↓
    Electrification → Renewable share

    Policy Levers (controllable)
         ↓
    Carbon tax ──┐
    PV subsidy ─┼→ CO₂ reduction (lag: 2-3 years)
    Heat pump ──┘
"""

print(__doc__)
print(DAG_STRUCTURE)
print(f"\n✅ {len(CAUSAL_DAGS)} domains documented with causal structures")
