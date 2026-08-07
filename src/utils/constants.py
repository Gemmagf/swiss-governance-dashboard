"""Configuration constants for Swiss Governance Dashboard."""

# Cantons (26 total) — SHORT CODES for CANTONS variable
CANTONS = ["AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR",
           "JU", "LU", "NE", "NW", "OW", "SG", "SH", "SO", "SZ", "TG",
           "TI", "UR", "VD", "VS", "ZG", "ZH"]

SWISS_CANTONS = {
    "AG": {"name": "Aargau", "region": "North"},
    "AI": {"name": "Appenzell Innerrhoden", "region": "East"},
    "AR": {"name": "Appenzell Ausserrhoden", "region": "East"},
    "BE": {"name": "Bern", "region": "Central"},
    "BL": {"name": "Basel-Landschaft", "region": "Northwest"},
    "BS": {"name": "Basel-Stadt", "region": "Northwest"},
    "FR": {"name": "Fribourg", "region": "Central"},
    "GE": {"name": "Geneva", "region": "West"},
    "GL": {"name": "Glarus", "region": "East"},
    "GR": {"name": "Grisons", "region": "East"},
    "JU": {"name": "Jura", "region": "West"},
    "LU": {"name": "Lucerne", "region": "Central"},
    "NE": {"name": "Neuchâtel", "region": "West"},
    "NW": {"name": "Nidwalden", "region": "Central"},
    "OW": {"name": "Obwalden", "region": "Central"},
    "SG": {"name": "St. Gallen", "region": "East"},
    "SH": {"name": "Schaffhausen", "region": "North"},
    "SO": {"name": "Solothurn", "region": "North"},
    "SZ": {"name": "Schwyz", "region": "Central"},
    "TG": {"name": "Thurgau", "region": "North"},
    "TI": {"name": "Ticino", "region": "South"},
    "UR": {"name": "Uri", "region": "Central"},
    "VD": {"name": "Vaud", "region": "West"},
    "VS": {"name": "Valais", "region": "South"},
    "ZG": {"name": "Zug", "region": "Central"},
    "ZH": {"name": "Zurich", "region": "North"},
}

# Indicators: 32 total across 7 domains
INDICATORS = {
    "forest_biodiversity": [
        {"id": "forest_cover", "label": "Forest cover", "unit": "%", "domain": "Forest & Biodiversity"},
        {"id": "species_richness", "label": "Species diversity index", "unit": "index", "domain": "Forest & Biodiversity"},
    ],
    "water": [
        {"id": "water_consumption", "label": "Drinking water consumption", "unit": "l/hab·day", "domain": "Water"},
        {"id": "water_network_loss", "label": "Network water loss", "unit": "%", "domain": "Water"},
        {"id": "water_quality", "label": "Water quality index", "unit": "/100", "domain": "Water"},
        {"id": "annual_precipitation", "label": "Annual precipitation", "unit": "mm", "domain": "Water"},
    ],
    "education": [
        {"id": "school_enrollment", "label": "Compulsory school enrollment", "unit": "students", "domain": "Education"},
        {"id": "student_teacher_ratio", "label": "Student-teacher ratio", "unit": "students", "domain": "Education"},
        {"id": "childcare_places", "label": "Childcare places per 100 infants", "unit": "places", "domain": "Education"},
        {"id": "spending_per_student", "label": "Spending per student", "unit": "CHF", "domain": "Education"},
    ],
    "mobility": [
        {"id": "public_transit_trips", "label": "Public transit trips", "unit": "trips/hab·year", "domain": "Mobility"},
        {"id": "bike_modal_share", "label": "Bike modal share", "unit": "%", "domain": "Mobility"},
        {"id": "motorized_traffic", "label": "Motorized traffic volume", "unit": "vehicles/day", "domain": "Mobility"},
        {"id": "network_punctuality", "label": "Network punctuality (VBZ)", "unit": "%", "domain": "Mobility"},
    ],
    "energy_climate": [
        {"id": "co2_emissions", "label": "CO₂ emissions", "unit": "t/hab·year", "domain": "Energy & Climate"},
        {"id": "renewable_energy_share", "label": "Renewable energy share", "unit": "%", "domain": "Energy & Climate"},
        {"id": "final_energy_consumption", "label": "Final energy consumption", "unit": "MWh/hab", "domain": "Energy & Climate"},
        {"id": "solar_capacity", "label": "Solar capacity installed", "unit": "kWp/1000 hab", "domain": "Energy & Climate"},
    ],
    "housing": [
        {"id": "median_rent", "label": "Median rent offered", "unit": "CHF/m²·year", "domain": "Housing"},
        {"id": "vacancy_rate", "label": "Housing vacancy rate", "unit": "%", "domain": "Housing"},
        {"id": "housing_completions", "label": "Housing completions", "unit": "per 1000 hab", "domain": "Housing"},
        {"id": "cooperative_housing", "label": "Cooperative & public housing", "unit": "%", "domain": "Housing"},
    ],
    "waste": [
        {"id": "urban_waste_generated", "label": "Urban waste generated", "unit": "kg/hab·year", "domain": "Waste"},
        {"id": "separate_collection_rate", "label": "Separate collection rate", "unit": "%", "domain": "Waste"},
        {"id": "organic_waste_collection", "label": "Organic waste collection", "unit": "kg/hab·year", "domain": "Waste"},
        {"id": "waste_management_cost", "label": "Waste service cost", "unit": "CHF/hab·year", "domain": "Waste"},
    ],
    "air_environment": [
        {"id": "no2_concentration", "label": "NO₂ annual average", "unit": "µg/m³", "domain": "Air & Environment"},
        {"id": "pm10_concentration", "label": "PM10 annual average", "unit": "µg/m³", "domain": "Air & Environment"},
        {"id": "green_space_per_capita", "label": "Green space per capita", "unit": "m²", "domain": "Air & Environment"},
        {"id": "heat_days", "label": "Heat days (>30°C)", "unit": "days", "domain": "Air & Environment"},
    ],
}

# Data sources
DATA_SOURCES = {
    "BFS": {
        "name": "Federal Statistical Office (Bundesamt für Statistik)",
        "url": "https://www.bfs.admin.ch/",
        "api": "https://www.pxweb.bfs.admin.ch/api/v1/",
        "auth": None,
    },
    "opendata.swiss": {
        "name": "Swiss Open Data Portal",
        "url": "https://opendata.swiss/",
        "api": "https://ckan.opendata.swiss/api/3/",
        "auth": None,
    },
    "BAFU": {
        "name": "Federal Office for the Environment",
        "url": "https://www.bafu.admin.ch/",
        "api": "https://data.geo.admin.ch/",
        "auth": None,
    },
    "Swisstopo": {
        "name": "Swiss Federal Office of Topography",
        "url": "https://www.swisstopo.admin.ch/",
        "api": "https://geo.ld.admin.ch/",
        "auth": None,
    },
}

# Timeframe
YEAR_START = 2015
YEAR_END = 2024
FORECAST_END = 2032

# Scenarios
SCENARIOS = {
    "opt": {"label": "Optimistic", "factor": 1.35},
    "base": {"label": "Baseline", "factor": 1.0},
    "str": {"label": "Stress", "factor": -0.45},
}
