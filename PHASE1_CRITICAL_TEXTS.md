# FASE 1: TEXTOS CRÍTICOS - Pla d'implementació

## 📋 Textos crítics identificats (10 prioritats)

### Grup 1: Títol (Línia 234)
```html
ACTUAL: <h1>Datencockpit Schweiz<small>Cockpit de dades de la Confederació · prototip interdepartamental</small></h1>
```

| Key | Català (Actual) | Anglès | Alemany |
|-----|---|---|---|
| title_main | Datencockpit Schweiz | Swiss Data Cockpit | Schweizerisches Datencockpit |
| title_sub | Cockpit de dades de la Confederació · prototip interdepartamental | Confederation Data Cockpit · interdepartmental prototype | Datencockpit der Konföderation · interdepartamentaler Prototyp |

**Implementació:**
```javascript
// Al JavaScript que genera la pàgina, canviar:
document.querySelector('h1').textContent = t('title_main');
document.querySelector('h1 small').textContent = t('title_sub');

// Però PROBLEM: El h1 és estàtic HTML, no dinàmic
// SOLUCIÓ: Fer servir data-i18n attributes
```

---

### Grup 2: Botons de Scenario (Línies 264-266)
```html
ACTUAL:
<button data-s="opt">Acord</button>
<button data-s="base" aria-pressed="true">Tendencial</button>
<button data-s="str">Estrès</button>
```

| Key | Català | Anglès | Alemany |
|-----|---|---|---|
| btn_scenario_opt | Acord | Agreement | Vereinbarung |
| btn_scenario_base | Tendencial | Baseline | Szenario |
| btn_scenario_str | Estrès | Stress | Stress |

**Implementació:**
```javascript
// Buscar TOTS els buttons amb data-s
document.querySelectorAll('button[data-s]').forEach(btn => {
  const scenario = btn.dataset.s;
  const key = 'btn_scenario_' + scenario;
  btn.textContent = t(key);
});
```

---

### Grup 3: Botons principals (Línies 268-271)
```html
ACTUAL:
<button class="btn" id="play" aria-pressed="false">▶ Anima</button>
<button class="btn" id="reset">Vista nacional</button>
<button class="btn" id="csv">CSV</button>
```

| Key | Català | Anglès | Alemany |
|-----|---|---|---|
| btn_animate | ▶ Anima | ▶ Animate | ▶ Animieren |
| btn_reset | Vista nacional | National View | Nationale Ansicht |
| btn_csv | CSV | CSV | CSV |

**Implementació:**
```javascript
// Specific IDs - fàcil
document.getElementById('play').textContent = t('btn_animate');
document.getElementById('reset').textContent = t('btn_reset');
document.getElementById('csv').textContent = t('btn_csv');
```

---

### Grup 4: Zoom buttons (Línies 282-284)
```html
ACTUAL:
<button id="zin" title="Amplia">＋</button>
<button id="zout" title="Redueix">－</button>
<button id="zfit" title="Tot Suïssa">⤢</button>
```

| Key | Català | Anglès | Alemany |
|-----|---|---|---|
| title_zoom_in | Amplia | Zoom in | Vergrößern |
| title_zoom_out | Redueix | Zoom out | Verkleinern |
| title_zoom_fit | Tot Suïssa | Fit all Switzerland | Ganzes Schweiz |

**Implementació:**
```javascript
document.getElementById('zin').title = t('title_zoom_in');
document.getElementById('zout').title = t('title_zoom_out');
document.getElementById('zfit').title = t('title_zoom_fit');
```

---

### Grup 5: Panel títols (Línies 316-343)
```html
ACTUAL:
<h2>Evolució i previsió</h2><span class="ai">Conjunt probabilístic</span>
<h2>Simulador de mesures</h2><span class="ai">Contrafactual</span>
<h2>Nota de situació</h2><span class="ai">Generada</span>
<h2>Senyals d'alerta</h2><span class="ai">Detecció d'anomalies</span>
<h2>Fitxa del model i dades</h2>
```

| Key | Català | Anglès | Alemany |
|-----|---|---|---|
| panel_forecast | Evolució i previsió | Forecast & Evolution | Entwicklung und Prognose |
| panel_forecast_badge | Conjunt probabilístic | Probabilistic ensemble | Probabilistisches Ensemble |
| panel_simulator | Simulador de mesures | Policy Simulator | Policy-Simulator |
| panel_simulator_badge | Contrafactual | Counterfactual | Kontrafaktisch |
| panel_situation | Nota de situació | Situation Report | Situationsbericht |
| panel_situation_badge | Generada | AI Generated | KI-generiert |
| panel_alerts | Senyals d'alerta | Alert Signals | Warnsignale |
| panel_alerts_badge | Detecció d'anomalies | Anomaly detection | Anomalieerkennung |
| panel_model | Fitxa del model i dades | Model & Data Card | Modell- und Datenkarte |

**Implementació:**
```javascript
// Buscar els h2 dins els panel headers
document.querySelectorAll('header h2').forEach((h2, idx) => {
  const keys = ['panel_forecast', 'panel_simulator', 'panel_situation', 'panel_alerts', 'panel_model'];
  if (keys[idx]) {
    h2.textContent = t(keys[idx]);
  }
});

// Buscar els badges (span.ai)
document.querySelectorAll('header span.ai').forEach((span, idx) => {
  const keys = ['panel_forecast_badge', 'panel_simulator_badge', 'panel_situation_badge', 'panel_alerts_badge'];
  if (keys[idx]) {
    span.textContent = t(keys[idx]);
  }
});
```

---

### Grup 6: Capa del mapa - "Suïssa" (Línia 902)
```javascript
ACTUAL:
$("crumb").innerHTML='<button id="crCH">Suïssa</button>...'
```

| Key | Català | Anglès | Alemany |
|-----|---|---|---|
| crumb_switzerland | Suïssa | Switzerland | Schweiz |

**Implementació:**
```javascript
// Buscar la funció que genera aquesta línea i canviar:
$("crumb").innerHTML='<button id="crCH">'+t('crumb_switzerland')+'</button>...'
```

---

## ✅ CHECKLIST D'IMPLEMENTACIÓ FASE 1

### Step 1: Backup
- [ ] `git status` (verificar branca translation-safe)
- [ ] Crear commit inicial: `git commit --allow-empty -m "PHASE 1: Start critical texts translation"`

### Step 2: Implementar updateUITexts()
- [ ] Crear funció que actualitzi tots els textos crítics
- [ ] Usar selectors CSS simples (ID, class)
- [ ] Testejar cada selector al browser console primer

### Step 3: Afegir traducció al dashboard_real.html
- [ ] Incloure translation_solution.js ANTES de </body>
- [ ] Verificar que t() funció es carrega
- [ ] Testejar t('btn_animate') a consola

### Step 4: Afegir inicialització
- [ ] Cridar updateUITexts(getCurrentLanguage()) al final
- [ ] Verificar que els textos es carreguin en idioma guardatß

### Step 5: Test local
- [ ] Abrir dashboard al browser
- [ ] Verificar que títols apareixin correctes
- [ ] Verificar que botons funcionen
- [ ] Cambiar idioma i veure si actualitza

### Step 6: Commit
- [ ] `git add dashboard_real.html translation_solution.js`
- [ ] `git commit -m "feat: translate critical UI texts (title, buttons, panels)"`
- [ ] `git push origin translation-safe`

---

## 🔴 RISCOS A EVITAR

| Risc | Com evitar |
|-----|-----------|
| Trencar HTML structure | Usar querySelector, no regex |
| Perdre funcionalitat buttons | Conservar attributes (id, data-*, aria-*) |
| Textos que no es tradueixen | Testejar cada text de forma individual |
| Problemes de encoding | UTF-8 en tot el codi |
| Cache del navegador | Forçar reload: `Ctrl+Shift+R` |

---

## 📊 Estimació temps FASE 1
- Preparació: 15 min
- Implementació: 30 min
- Testing: 15 min
- Commit: 5 min
- **TOTAL: 1 hora aprox**

