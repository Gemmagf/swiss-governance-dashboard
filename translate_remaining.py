#!/usr/bin/env python3
"""
Complete translation of remaining Catalan text to English
Including dynamic text generation and comments
"""

# Read the file
with open('dashboard_real.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Complete translation dictionary - REMAINING Catalan to English
TRANSLATIONS = {
    # UI Labels
    "PREVISIÓ · BASELINE": "FORECAST · BASELINE",
    "INDICADORS": "INDICATORS",
    "% de cobertura": "% of coverage",
    "VALOR 2035": "VALUE 2035",
    "EFECTE VS BASE": "EFFECT VS BASE",
    "COST ANNUAL ESTIMAT": "ESTIMATED ANNUAL COST",
    "COST PER PUNT": "COST PER POINT",
    "HORITZÓ FIABLE": "RELIABLE HORIZON",
    "DERIVA DEL MODEL": "MODEL DRIFT",
    "DARRER REENTRENAMENT": "LAST RETRAINING",

    # Data sources and labels
    "Inventari Forestal Nacional (LFI)": "National Forest Inventory (LFI)",
    "Sentinel-2 · NDVI": "Sentinel-2 · NDVI",
    "MeteoSwiss · IDAWEB": "MeteoSwiss · IDAWEB",
    "WSL · monitoratge de sanitat": "WSL · sanitation monitoring",
    "Inventari nacional de GEH": "National renewable energy inventory",
    "Estadística energètica SFOE": "Energy statistics SFOE",
    "Pronovo · registre d'instal·lacions": "Pronovo · installation registry",
    "Swissgrid · balanç de xarxa": "Swissgrid · grid balance",

    # Metric labels
    "Cabal estival respecte de la mitjana": "Summer flow compared to average",

    # Dynamic text parts (code generation)
    "predit vs realitzat als darrers 6 years": "predicted vs actual in the last 6 years",
    "cantó amb la desviació més gran respecte de la tendència pròpia": "canton with the largest deviation from its own trend",
    "es desvia un": "deviates by",
    "respecte de l'prior year a": "compared to prior year in",
    "Probability of persistence 12 months": "Probability of persistence 12 months",
    "Suggested action: data verification and technical visit.": "Suggested action: data verification and technical visit.",
    "per arribar a l'objectiu": "to reach the target",
    "amb les mesures actuals el 2035 falta un": "with current measures in 2035 is missing a",
    "% per arribar a l'objectiu": "% to reach the target",
    "Check if whether the difference is due to structural factors or unequal application.": "Check if whether the difference is due to structural factors or unequal application.",
    "la sèrie de": "the series of",
    "arriba amb": "arrives with",
    "months late; values for the recent period are estimated.": "months late; values for the recent period are estimated.",
    "The uncertainty for this canton is inflated in the model.": "The uncertainty for this canton is inflated in the model.",

    # Brief text (situation report)
    "per sobre": "above",
    "per sota": "below",
    "del 2015. La direcció és": "of 2015. The trend is",
    "favorable": "favorable",
    "desfavorable": "unfavorable",
    "respecte de l'objectiu de política pública": "compared to public policy target",
    "Amb les mesures simulades, el resultat previst millora respecte del cas base; el cost recau majoritàriament en el pressupost cantonal.": "With simulated measures, the forecasted result improves compared to the base case; costs fall mainly on the canton budget.",
    "el tanca. Aquesta dispersió condiciona qualsevol mesura d'aplicació uniforme.": "closes it. This dispersion conditions any measure of uniform application.",
    "Fiabilitat del model en els darrers sis years: error mitjà del": "Model reliability in the last six years: average error of",
    "%. Les xifres recents són provisionals.": "%. Recent figures are provisional.",

    # Signature line
    'Automatically generated el '+'"ca-ES"': 'Automatically generated on'+'"en-US"',
    "Automatically generated el": "Automatically generated on",
    'toLocaleDateString("ca-ES")': 'toLocaleDateString("en-US")',

    # Federated learning note
    "Federated learning: cantons retain raw data in their systems i only share model parameters. Each forecast carries origin tracing i requires human validation before entering a file.": "Federated learning: cantons retain raw data in their systems and only share model parameters. Each forecast carries origin tracing and requires human validation before entering a file.",
    " i only share": " and only share",
    " i requires": " and requires",
}

# Apply all translations
count = 0
for original, english in TRANSLATIONS.items():
    if original in content:
        content = content.replace(original, english)
        count += 1
        print(f"✓ {original} → {english}")
    else:
        print(f"✗ NOT FOUND: {original}")

# Write the file
with open('dashboard_real.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✓ Translation complete: {count} additional texts replaced")
print(f"File saved: dashboard_real.html")
