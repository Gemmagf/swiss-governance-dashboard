#!/usr/bin/env python3
"""Translate dashboard to English using simple find & replace"""

with open('dashboard_real.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Catalan -> English translations (comprehensive)
translations = {
    # Critical UI
    "Any": "Year",
    "ESCENARI": "SCENARIO",
    "Acord": "Agreement",
    "Tendencial": "Baseline",
    "Estrès": "Stress",
    "▶ Anima": "▶ Animate",
    "Vista nacional": "National View",
    "Panells": "Panels",
    "Amplia": "Zoom in",
    "Redueix": "Zoom out",
    "Tot Suïssa": "Fit all Switzerland",
    
    # Panels
    "Evolució i previsió": "Forecast & Evolution",
    "Conjunt probabilístic": "Probabilistic ensemble",
    "Simulador de mesures": "Policy Simulator",
    "Contrafactual": "Counterfactual",
    "Nota de situació": "Situation Report",
    "Generada": "AI Generated",
    "Senyals d'alerta": "Alert Signals",
    "Detecció d'anomalies": "Anomaly detection",
    "Fitxa del model i dades": "Model & Data Card",
    
    # Meta
    "Confederació Suïssa": "Swiss Confederation",
    "26 cantons · 4 llengües oficials": "26 cantons · 4 official languages",
    
    # Sidebar sections
    "ÀMBITS": "DOMAINS",
    "INDICADORS": "INDICATORS",
    
    # Rankings
    "RÀNQUING CANTONAL": "CANTONAL RANKING",
    "més és millor": "more is better",
    
    # Contributions
    "CONTRIBUCIÓ ALS CANVIS PREVISTOS · ATRIBUCIÓ DEL MODEL": "CONTRIBUTION TO FORECASTED CHANGES · MODEL ATTRIBUTION",
    
    # Backtest
    "COMPROVACIÓ RETROSPECTIVA": "BACKTESTING",
    
    # Simulator
    "Mou les palanques per veure com canvia la trajectòria fins al 2035": "Move the levers to see how the trajectory changes until 2035",
    "Els efectes són elasticitats estimades amb interval de confiança, no garanties": "Effects are estimated elasticities with confidence intervals, not guarantees",
    
    # Notes
    "VALOR": "VALUE",
    "EFECTE VS BASE": "EFFECT VS BASE",
    "COST ANUAL ESTIMAT": "ESTIMATED ANNUAL COST",
    "COST PER PUNT": "COST PER POINT",
}

count = 0
for ca, en in translations.items():
    if ca in content:
        content = content.replace(ca, en)
        count += 1
        print(f"✓ {ca} → {en}")

with open('dashboard_real.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Translated {count} terms to English")
