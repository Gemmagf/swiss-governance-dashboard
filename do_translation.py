#!/usr/bin/env python3
"""
Simple text replacement for dashboard translation
Uses the CSV from the agent analysis
"""
import csv

# Read dashboard
with open('dashboard_real.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content

# Translation map (CRÍTICOS FIRST - 15 most important)
TRANSLATIONS = {
    # Título principal
    "Datencockpit Schweiz": "Swiss Data Cockpit",
    "Cockpit de dades de la Confederació · prototip interdepartamental": "Confederation Data Cockpit · interdepartmental prototype",

    # Botones scenario
    "Acord": "Agreement",
    "Tendencial": "Baseline",
    "Estrès": "Stress",

    # Botones acción
    "▶ Anima": "▶ Animate",
    "Vista nacional": "National View",

    # Zoom tooltips
    "Amplia": "Zoom in",
    "Redueix": "Zoom out",
    "Tot Suïssa": "Fit all Switzerland",

    # Panel titles
    "Evolució i previsió": "Forecast & Evolution",
    "Simulador de mesures": "Policy Simulator",
    "Nota de situació": "Situation Report",
    "Senyals d'alerta": "Alert Signals",
    "Fitxa del model i dades": "Model & Data Card",
}

# Apply translations
count = 0
for original, english in TRANSLATIONS.items():
    if original in content:
        content = content.replace(original, english)
        count += 1
        print(f"✓ Translated: {original} → {english}")
    else:
        print(f"✗ NOT FOUND: {original}")

# Write result
if count > 0:
    with open('dashboard_real.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✓ Translation complete: {count} texts replaced")
    print(f"File saved: dashboard_real.html")
else:
    print("\n✗ No translations applied")
    exit(1)
