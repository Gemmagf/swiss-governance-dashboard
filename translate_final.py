#!/usr/bin/env python3
"""
Final comprehensive translation - all remaining Catalan text
"""

with open('dashboard_real.html', 'r', encoding='utf-8') as f:
    content = f.read()

TRANSLATIONS = {
    # Lever notes
    "Reducció de pèrdues i millora de la resiliència en episodis de sequera.": "Reduction of losses and improvement of resilience during drought episodes.",
    "Més oferta a les hores punta als eixos amb més saturació.": "More supply at peak hours on the most saturated routes.",
    "Infraestructura contínua, no trams aïllats: l'efecte és no lineal amb la connectivitat.": "Continuous infrastructure, not isolated sections: the effect is nonlinear with connectivity.",
    "És la palanca més cara i la de més recorregut a llarg termini.": "It is the most expensive lever and the one with the most long-term reach.",
    "Plans de fertilització i franges de protecció a les zones de captació.": "Fertilization plans and protection strips in catchment areas.",

    # Drivers
    "Càrrega agrícola of the watershed": "Agricultural load of the watershed",
    "Cabal i dilució": "Flow and dilution",
    "Grau de tractament a les EDAR": "Treatment level in EDAR plants",
    "Densitat urbana": "Urban density",

    # Data sources
    "NAQUA · aigües subterrànies": "NAQUA · groundwater",
    "NADUF · xarxa de rius": "NADUF · river network",
    "Estacions hidromètriques FOEN": "Hydrometric stations FOEN",
    "Cadastre d'abocaments": "Discharge registry",
    "schedule": "schedule",
    "quarterly": "quarterly",
    "monthly": "monthly",
    "annual": "annual",

    # Populate display
    " mil": " thousand",
}

count = 0
for original, english in TRANSLATIONS.items():
    if original in content:
        content = content.replace(original, english)
        count += 1
        print(f"✓ {original[:50]}... → {english[:50]}...")
    else:
        print(f"✗ NOT FOUND: {original[:50]}...")

# Write
with open('dashboard_real.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✓ Final translation: {count} texts replaced")
