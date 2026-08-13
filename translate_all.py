#!/usr/bin/env python3
"""
Complete translation of dashboard from Catalan to English
"""

# Read the file
with open('dashboard_real.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Complete translation dictionary - ALL Catalan to English
TRANSLATIONS = {
    # Comments
    "vermell CD Bund": "red CD Bund",
    "accent d'domain, dynamic": "accent of domain, dynamic",
    "colors del cantó, dinàmics": "canton colors, dynamic",

    # Metrics - Water (Aigua)
    "Qualitat ecològica dels rius": "Ecological quality of rivers",
    "Nitrats a l'aigua subterrània": "Nitrates in groundwater",
    "Ús d'aigua captada": "Water extraction",
    "Consum d'aigua potable": "Drinking water consumption",
    "Micropol·luents eliminats a les depuradores": "Micropollutants removed in treatment plants",
    "% de la superfície": "% of area",
    "% de depuradores": "% of treatment plants",
    "% de superfície amb pla": "% of area with plan",

    # Metrics - Education (Educació)
    "Ràtio alumnat per teacher": "Student teacher ratio",
    "Despesa pública per alumne": "Public spending per student",
    "Titulació de secundària II als 25 years": "Secondary II qualification by age 25",
    "Alumnat en formació professional dual": "Students in dual vocational training",
    "Inversió en infraestructura digital": "Investment in digital infrastructure",
    "alumnes": "students",
    "% de centres/any": "% of centers/year",

    # Metrics - Mobility (Mobilitat)
    "Viatges en transport públic": "Public transport trips",
    "Hores de retenció a la xarxa": "Traffic congestion hours",
    "Vehicles elèctrics in the park": "Electric vehicles in the fleet",
    "Puntualitat ferroviària": "Train punctuality",
    "viatges/inhabitants·any": "trips/inhabitants·year",
    "h/1000 inhabitants": "h/1000 inhabitants",
    "% de trens": "% of trains",
    "Increment de freqüència ferroviària": "Increase in train frequency",
    "Tarifació de l'ús de la carretera": "Road pricing",
    "intensitat": "intensity",

    # Metrics - Energy (Energia)
    "Potència fotovoltaica installed": "Photovoltaic power installed",
    "Cobertura del dèficit winter": "Winter deficit coverage",
    "W/inhabitants": "W/inhabitants",
    "Ritme de reinhabitantsilitació energètica d'edificis": "Building energy retrofit rate",
    "% del parc/any": "% of fleet/year",
    "É la palanca més cara i la de més recorregut a llarg termini": "It is the most expensive lever and the one with the most long-term reach",
    "Replacement de calefaccions fòssils": "Replacement of fossil heating",
    "1000 unitats/any": "1000 units/year",

    # Metrics - Health (Salut)
    "Metges de família per 10 000 inhabitantsitants": "General practitioners per 10,000 inhabitants",
    "Temps d'espera a urgències": "Emergency department wait time",
    "Despesa sanitària per inhabitantsitant": "Healthcare spending per inhabitant",
    "Cobertura d'atenció domiciliària": "Home care coverage",
    "Historial clínic electrònic actiu": "Active electronic health record",
    "metges": "doctors",
    "minutes": "minutes",
    "% de la demanda": "% of demand",
    "% de la població": "% of population",
    "Reforç of care primària": "Reinforcement of primary care",
    "% of places noves": "% of new places",
    "Triatge i seguiment a distància": "Triage and remote monitoring",
    "% de casos": "% of cases",
    "Coordinació entre nivells assistencials": "Coordination between care levels",
    "% de regions": "% of regions",

    # Metrics - Territory (Territori)
    "Lloguer mitjà ofert": "Average rent offered",
    "Consum de sòl per inhabitantsitant": "Land consumption per inhabitant",
    "Habitatge nou en sòl ja urbanitzat": "New housing on already developed land",
    "Area agrícola útil": "Useful agricultural area",
    "CHF/m²·any": "CHF/m²·year",
    "m²": "m²",
    "% of territory": "% of territory",
    "Increment d'edificabilitat en àrees ben servides": "Increase in buildability in well-served areas",
    "% of zones": "% of zones",
    "Foment d'inhabitantsitatge d'utilitat pública": "Support for social housing",
    "% de l'obra nova": "% of new construction",
    "Reducció de terminis d'autorització": "Reduction of authorization periods",
    "% més ràpid": "% faster",

    # Data sources
    "Arealstatistik · swisstopo": "Areastatistics · swisstopo",
    "Estadística d'inhabitantsitatges buits": "Vacancy statistics",
    "Registre d'edificis GWR": "Building register GWR",
    "Índex de lloguers": "Rental index",
    "3 years": "3 years",
    "annual": "annual",
    "monthly": "monthly",
    "trimestral": "quarterly",
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

print(f"\n✓ Translation complete: {count} texts replaced")
print(f"File saved: dashboard_real.html")
