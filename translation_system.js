/**
 * SWISS GOVERNANCE DASHBOARD - TRANSLATION SYSTEM
 * Supports: German (default), Catalan, English, French, Italian, Romansh
 *
 * Implementation Strategy:
 * 1. Load this translation dictionary at the top of your <script> section
 * 2. Initialize language on page load from localStorage (default: "de")
 * 3. Replace all hardcoded text strings with calls to t(key)
 * 4. Add event listeners to update DOM when language changes
 * 5. Persist selection in localStorage on change
 */

const TRANSLATIONS = {
  // ===== HEADER & META =====
  "hdr.title": {
    de: "Datencockpit Schweiz",
    ca: "Cockpit de dades de Suïssa",
    en: "Swiss Data Cockpit",
    fr: "Cockpit de données suisse",
    it: "Cruscotto dati svizzero",
    rm: "Cockpit da datas svizras"
  },
  "hdr.subtitle": {
    de: "Cockpit de dades de la Confederació · prototip interdepartamental",
    ca: "Cockpit de dades de la Confederació · prototip interdepartamental",
    en: "Confederation Data Cockpit · interdepartmental prototype",
    fr: "Cockpit de données de la Confédération · prototype interministériel",
    it: "Cruscotto dati della Confederazione · prototipo interdepartimentale",
    rm: "Cockpit da datas da la Confederaziun · prototip interdepartamental"
  },
  "hdr.page_title": {
    de: "Schweizerisches Datencockpit · Cockpit de dades de la Confederació",
    ca: "Cockpit de dades de la Confederació · Cockpit de dades suïssa",
    en: "Swiss Data Cockpit · Confederation Data Cockpit",
    fr: "Cockpit de données suisse · Cockpit de données de la Confédération",
    it: "Cruscotto dati svizzero · Cruscotto dati della Confederazione",
    rm: "Cockpit da datas svizras · Cockpit da datas da la Confederaziun"
  },

  // ===== META LABELS =====
  "meta.domain": {
    de: "Àmbit",
    ca: "Àmbit",
    en: "Domain",
    fr: "Domaine",
    it: "Ambito",
    rm: "Ambit"
  },
  "meta.population": {
    de: "Bevölkerung",
    ca: "Població",
    en: "Population",
    fr: "Population",
    it: "Popolazione",
    rm: "Populaziun"
  },
  "meta.area": {
    de: "Fläche",
    ca: "Superfície",
    en: "Area",
    fr: "Superficie",
    it: "Superficie",
    rm: "Superficcha"
  },
  "meta.models": {
    de: "Modelle",
    ca: "Models",
    en: "Models",
    fr: "Modèles",
    it: "Modelli",
    rm: "Models"
  },
  "meta.models_active": {
    de: "{n} aktiv",
    ca: "{n} actius",
    en: "{n} active",
    fr: "{n} actifs",
    it: "{n} attivi",
    rm: "{n} actius"
  },

  // ===== LANGUAGE SELECTOR =====
  "lang.german": {
    de: "🇩🇪 Deutsch",
    ca: "🇩🇪 Alemany",
    en: "🇩🇪 German",
    fr: "🇩🇪 Allemand",
    it: "🇩🇪 Tedesco",
    rm: "🇩🇪 Tudestg"
  },
  "lang.catalan": {
    de: "🇨🇭 Katalanisch",
    ca: "🇨🇭 Català",
    en: "🇨🇭 Catalan",
    fr: "🇨🇭 Catalan",
    it: "🇨🇭 Catalano",
    rm: "🇨🇭 Catalan"
  },
  "lang.english": {
    de: "🇬🇧 Englisch",
    ca: "🇬🇧 Anglès",
    en: "🇬🇧 English",
    fr: "🇬🇧 Anglais",
    it: "🇬🇧 Inglese",
    rm: "🇬🇧 Englais"
  },
  "lang.french": {
    de: "🇫🇷 Französisch",
    ca: "🇫🇷 Francès",
    en: "🇫🇷 French",
    fr: "🇫🇷 Français",
    it: "🇫🇷 Francese",
    rm: "🇫🇷 Franzos"
  },
  "lang.italian": {
    de: "🇮🇹 Italienisch",
    ca: "🇮🇹 Italià",
    en: "🇮🇹 Italian",
    fr: "🇮🇹 Italien",
    it: "🇮🇹 Italiano",
    rm: "🇮🇹 Talian"
  },
  "lang.romansh": {
    de: "🗣️ Rätoromanisch",
    ca: "🗣️ Romanx",
    en: "🗣️ Romansh",
    fr: "🗣️ Romanche",
    it: "🗣️ Romancio",
    rm: "🗣️ Rumantsch"
  },

  // ===== CONTROL BAR =====
  "ctrl.year": {
    de: "Jahr",
    ca: "Any",
    en: "Year",
    fr: "Année",
    it: "Anno",
    rm: "Onn"
  },
  "ctrl.year_status_observed": {
    de: "beobachtet",
    ca: "observat",
    en: "observed",
    fr: "observé",
    it: "osservato",
    rm: "observà"
  },
  "ctrl.year_status_forecast": {
    de: "Prognose",
    ca: "previsió",
    en: "forecast",
    fr: "prévision",
    it: "previsione",
    rm: "previsiun"
  },
  "ctrl.scenario": {
    de: "Szenario",
    ca: "Escenari",
    en: "Scenario",
    fr: "Scénario",
    it: "Scenario",
    rm: "Scenario"
  },
  "ctrl.scenario_agreement": {
    de: "Abkommen",
    ca: "Acord",
    en: "Agreement",
    fr: "Accord",
    it: "Accordo",
    rm: "Accord"
  },
  "ctrl.scenario_baseline": {
    de: "Tendenzielle",
    ca: "Tendencial",
    en: "Baseline",
    fr: "Tendanciel",
    it: "Tendenziale",
    rm: "Tendenzial"
  },
  "ctrl.scenario_stress": {
    de: "Stress",
    ca: "Estrès",
    en: "Stress",
    fr: "Stress",
    it: "Stress",
    rm: "Stress"
  },

  // ===== BUTTONS =====
  "btn.animate": {
    de: "▶ Animieren",
    ca: "▶ Anima",
    en: "▶ Animate",
    fr: "▶ Animer",
    it: "▶ Anima",
    rm: "▶ Animar"
  },
  "btn.national_view": {
    de: "Nationalansicht",
    ca: "Vista nacional",
    en: "National View",
    fr: "Vue nationale",
    it: "Vista nazionale",
    rm: "Glista naziunala"
  },
  "btn.csv": {
    de: "CSV",
    ca: "CSV",
    en: "CSV",
    fr: "CSV",
    it: "CSV",
    rm: "CSV"
  },
  "btn.panels": {
    de: "Fenster",
    ca: "Panells",
    en: "Panels",
    fr: "Panneaux",
    it: "Pannelli",
    rm: "Panellas"
  },
  "btn.zoom_in": {
    de: "Vergrößern",
    ca: "Amplia",
    en: "Zoom in",
    fr: "Agrandir",
    it: "Ingrandisci",
    rm: "Grandina"
  },
  "btn.zoom_out": {
    de: "Verkleinern",
    ca: "Redueix",
    en: "Zoom out",
    fr: "Réduire",
    it: "Riduci",
    rm: "Reducescha"
  },
  "btn.zoom_fit": {
    de: "Ganz Schweiz",
    ca: "Tot Suïssa",
    en: "All Switzerland",
    fr: "Toute la Suisse",
    it: "Tutta la Svizzera",
    rm: "Tutta Svizra"
  },
  "btn.expand": {
    de: "Vergrößern",
    ca: "Amplia",
    en: "Expand",
    fr: "Agrandir",
    it: "Espandi",
    rm: "Grandina"
  },

  // ===== BOTTOM STRIP SECTIONS =====
  "section.ranking": {
    de: "Kantonsranking",
    ca: "Rànquing cantonal",
    en: "Canton Ranking",
    fr: "Classement des cantons",
    it: "Ranking cantoni",
    rm: "Classifiziun chantunala"
  },
  "section.contribution": {
    de: "Beitrag zu Prognoseänderungen · Modellzuordnung",
    ca: "Contribució als canvis previstos · atribució del model",
    en: "Contribution to Forecast Changes · Model Attribution",
    fr: "Contribution aux changements prévus · attribution du modèle",
    it: "Contributo ai cambiamenti previsti · attribuzione del modello",
    rm: "Contribuziun a las midadas previstas · atribuziun dal model"
  },
  "section.backtest": {
    de: "Rückwärts Überprüfung",
    ca: "Comprovació retrospectiva",
    en: "Backtest",
    fr: "Vérification rétrospective",
    it: "Verifica retrospettiva",
    rm: "Controllas retrospectiva"
  },

  // ===== SIDEBAR PANELS =====
  "panel.identity": {
    de: "Identität",
    ca: "Identitat",
    en: "Identity",
    fr: "Identité",
    it: "Identità",
    rm: "Identitad"
  },
  "panel.evolution": {
    de: "Entwicklung und Prognose",
    ca: "Evolució i previsió",
    en: "Evolution and Forecast",
    fr: "Évolution et prévision",
    it: "Evoluzione e previsione",
    rm: "Evoluziun e previsiun"
  },
  "panel.evolution_ai": {
    de: "Probabilistische Ensemble",
    ca: "Conjunt probabilístic",
    en: "Probabilistic Ensemble",
    fr: "Ensemble probabiliste",
    it: "Insieme probabilistico",
    rm: "Cumparsa probabilistica"
  },
  "panel.simulator": {
    de: "Maßnahmensimulator",
    ca: "Simulador de mesures",
    en: "Measure Simulator",
    fr: "Simulateur de mesures",
    it: "Simulatore misure",
    rm: "Simulatur da midadas"
  },
  "panel.simulator_ai": {
    de: "Kontrafaktisch",
    ca: "Contrafactual",
    en: "Counterfactual",
    fr: "Contrefactuel",
    it: "Controffattuale",
    rm: "Counterfactual"
  },
  "panel.status_note": {
    de: "Lagebericht",
    ca: "Nota de situació",
    en: "Status Note",
    fr: "Note de situation",
    it: "Nota di situazione",
    rm: "Nota da situaziun"
  },
  "panel.status_note_ai": {
    de: "Generiert",
    ca: "Generada",
    en: "Generated",
    fr: "Générée",
    it: "Generata",
    rm: "Generada"
  },
  "panel.alerts": {
    de: "Warnmeldungen",
    ca: "Senyals d'alerta",
    en: "Alert Signals",
    fr: "Signaux d'alerte",
    it: "Segnali di alerta",
    rm: "Signals d'alerta"
  },
  "panel.alerts_ai": {
    de: "Anomalieerkennung",
    ca: "Detecció d'anomalies",
    en: "Anomaly Detection",
    fr: "Détection d'anomalies",
    it: "Rilevamento anomalie",
    rm: "Detectiun d'anomalias"
  },
  "panel.model_card": {
    de: "Modell- und Datenblatt",
    ca: "Fitxa del model i dades",
    en: "Model & Data Card",
    fr: "Fiche modèle et données",
    it: "Scheda modello e dati",
    rm: "Charta dal model e datas"
  },

  // ===== CANTON INFO =====
  "canton.switzerland": {
    de: "Schweizerische Eidgenossenschaft",
    ca: "Confederació Suïssa",
    en: "Swiss Confederation",
    fr: "Confédération suisse",
    it: "Confederazione Svizzera",
    rm: "Confederaziun Svizra"
  },
  "canton.stats": {
    de: "26 Kantone · 4 Amtssprachen",
    ca: "26 cantons · 4 llengües oficials",
    en: "26 cantons · 4 official languages",
    fr: "26 cantons · 4 langues officielles",
    it: "26 cantoni · 4 lingue ufficiali",
    rm: "26 chantuns · 4 linguas officials"
  },

  // ===== SIMULATOR HELP TEXT =====
  "help.simulator": {
    de: "Verschieben Sie die Hebel, um zu sehen, wie sich die Flugbahn bis 2035 ändert. Die Auswirkungen sind geschätzte Elastizitäten mit Konfidenzintervallen, keine Garantien.",
    ca: "Mou les palanques per veure com canvia la trajectòria fins al 2035. Els efectes són elasticitats estimades amb interval de confiança, no garanties.",
    en: "Move the levers to see how the trajectory changes to 2035. Effects are estimated elasticities with confidence intervals, not guarantees.",
    fr: "Déplacez les leviers pour voir comment la trajectoire change jusqu'en 2035. Les effets sont des élasticités estimées avec intervalles de confiance, pas des garanties.",
    it: "Muovi le leve per vedere come cambia la traiettoria fino al 2035. Gli effetti sono elasticità stimate con intervalli di confidenza, non garanzie.",
    rm: "Mova las palancas per vair co la trajetoria sa midada sin al 2035. Ils effects èn elasticitads estimadas cun interval da confidenza, no garantias."
  },

  // ===== CHART/DATA LABELS =====
  "chart.model_drift": {
    de: "Modell Drift",
    ca: "Deriva del model",
    en: "Model Drift",
    fr: "Dérive du modèle",
    it: "Deriva del modello",
    rm: "Deriva dal model"
  },
  "chart.annual_cost": {
    de: "Geschätzter Jahresaufwand",
    ca: "Cost anual estimat",
    en: "Estimated Annual Cost",
    fr: "Coût annuel estimé",
    it: "Costo annuale stimato",
    rm: "Cost annual estimà"
  },
  "chart.cost_per_point": {
    de: "Kosten pro Punkt",
    ca: "Cost per punt",
    en: "Cost per Point",
    fr: "Coût par point",
    it: "Costo per punto",
    rm: "Cost per punct"
  },
  "chart.last_retrain": {
    de: "Letztes Retraining",
    ca: "Darrer reentrenament",
    en: "Last Retrain",
    fr: "Dernier réentraînement",
    it: "Ultimo riaddestramento",
    rm: "Ultima retrenada"
  },
  "chart.reliable_horizon": {
    de: "Zuverlässiger Horizont",
    ca: "Horitzó fiable",
    en: "Reliable Horizon",
    fr: "Horizon fiable",
    it: "Orizzonte affidabile",
    rm: "Horizont fidavel"
  },
  "chart.retroactive_error": {
    de: "Rückwärts Fehler",
    ca: "Error retrospectiu",
    en: "Retroactive Error",
    fr: "Erreur rétrospective",
    it: "Errore retroattivo",
    rm: "Eir retrospectiva"
  },
  "chart.forecast_effect": {
    de: "Effekt vs Basis",
    ca: "Efecte vs base",
    en: "Effect vs Base",
    fr: "Effet vs base",
    it: "Effetto vs base",
    rm: "Effect vs basa"
  },

  // ===== INTERVALS & STATISTICS =====
  "stat.p10_p90": {
    de: "Bereich P10–P90",
    ca: "Interval P10–P90",
    en: "Range P10–P90",
    fr: "Intervalle P10–P90",
    it: "Intervallo P10–P90",
    rm: "Interval P10–P90"
  },
  "stat.p25_p75": {
    de: "Bereich P25–P75",
    ca: "Interval P25–P75",
    en: "Range P25–P75",
    fr: "Intervalle P25–P75",
    it: "Intervallo P25–P75",
    rm: "Interval P25–P75"
  },
  "stat.predicted_ex_ante": {
    de: "Ex-ante vorhergesagt",
    ca: "Predit ex-ante",
    en: "Predicted ex-ante",
    fr: "Prédit ex-ante",
    it: "Predetto ex-ante",
    rm: "Predì ex-ante"
  },
  "stat.realized": {
    de: "Realisiert",
    ca: "Realitzat",
    en: "Realized",
    fr: "Réalisé",
    it: "Realizzato",
    rm: "Realisà"
  },
  "stat.value_2035": {
    de: "Wert 2035",
    ca: "Valor 2035",
    en: "Value 2035",
    fr: "Valeur 2035",
    it: "Valore 2035",
    rm: "Valur 2035"
  },
  "stat.target": {
    de: "Ziel",
    ca: "objectiu",
    en: "Target",
    fr: "Cible",
    it: "Obiettivo",
    rm: "Ubiectif"
  },
  "stat.observed": {
    de: "Beobachtet",
    ca: "observat",
    en: "Observed",
    fr: "Observé",
    it: "Osservato",
    rm: "Observà"
  },
  "stat.forecast": {
    de: "Prognose",
    ca: "previsió",
    en: "Forecast",
    fr: "Prévision",
    it: "Previsione",
    rm: "Previsiun"
  },

  // ===== MODEL ACCURACY =====
  "model.accuracy_msg": {
    de: "Modellzuverlässigkeit in den letzten sechs Jahren: durchschnittlicher Fehler {pct}%. Aktuelle Zahlen sind vorläufig.",
    ca: "Fiabilitat del model en els darrers sis anys: error mitjà del {pct}%. Les xifres recents són provisionals.",
    en: "Model reliability in the past six years: average error {pct}%. Recent figures are provisional.",
    fr: "Fiabilité du modèle au cours des six dernières années: erreur moyenne {pct}%. Les chiffres récents sont provisoires.",
    it: "Affidabilità del modello negli ultimi sei anni: errore medio {pct}%. I dati recenti sono provvisori.",
    rm: "Fidavaivladad dal model en ils ultims sis onns: eir media {pct}%. Las cifras recents èn provisoricas."
  },
  "model.accuracy_short": {
    de: "MAPE {pct}%",
    ca: "MAPE {pct}%",
    en: "MAPE {pct}%",
    fr: "MAPE {pct}%",
    it: "MAPE {pct}%",
    rm: "MAPE {pct}%"
  },

  // ===== SCENARIO DESCRIPTIONS =====
  "scenario.baseline_desc": {
    de: "Mit Annahmen basierend auf historischen Trends...",
    ca: "Amb assumpcions basades en les tendències històriques...",
    en: "Based on assumptions from historical trends...",
    fr: "Basé sur les tendances historiques...",
    it: "Basato su supposizioni dalle tendenze storiche...",
    rm: "Basà sin assuminas da las tendenzas historicas..."
  },
  "scenario.agreement_desc": {
    de: "Mit simulierten Maßnahmen verbessert sich die Prognose; die Kosten fallen hauptsächlich in das Kantonsbudget.",
    ca: "Amb les mesures simulades, el resultat previst millora respecte del cas base; el cost recau majoritàriament en el pressupost cantonal.",
    en: "With simulated measures, the forecast improves over the baseline; costs fall mainly in cantonal budgets.",
    fr: "Avec les mesures simulées, la prévision s'améliore par rapport au cas de base; les coûts incombent principalement aux budgets cantonaux.",
    it: "Con le misure simulate, la previsione migliora rispetto al caso base; i costi ricadono principalmente sui bilanci cantonali.",
    rm: "Cun las midadas simuladas, la previsiun s'amellora respectiv dal cas basa; ils costs chattan majoritariamain en ils budgets chantunals."
  },

  // ===== ARIA LABELS (Accessibility) =====
  "a11y.year_slider": {
    de: "Jahr Schieberegler",
    ca: "Selector d'any",
    en: "Year range slider",
    fr: "Curseur d'années",
    it: "Slider dell'anno",
    rm: "Selector d'onn"
  },
  "a11y.canton_map": {
    de: "Kantonkarte",
    ca: "Mapa dels cantons",
    en: "Canton map",
    fr: "Carte des cantons",
    it: "Mappa dei cantoni",
    rm: "Mapa dals chantuns"
  }
};

// ===== LANGUAGE STATE & FUNCTIONS =====
let currentLanguage = localStorage.getItem("dashboardLanguage") || "de";

/**
 * Get translated string
 * @param {string} key - Translation key (e.g. "ctrl.year")
 * @param {object} vars - Optional variables to replace (e.g. {pct: "1.5"})
 * @returns {string} Translated text or fallback to German
 */
function t(key, vars = {}) {
  const entry = TRANSLATIONS[key];
  if (!entry) {
    console.warn(`Translation key not found: ${key}`);
    return key;
  }

  let text = entry[currentLanguage] || entry.de || key;

  // Replace variables
  Object.entries(vars).forEach(([varName, value]) => {
    text = text.replace(`{${varName}}`, value);
  });

  return text;
}

/**
 * Change language and update all UI text
 * @param {string} lang - Language code (de, ca, en, fr, it, rm)
 */
function changeLanguage(lang) {
  if (!["de", "ca", "en", "fr", "it", "rm"].includes(lang)) return;

  currentLanguage = lang;
  localStorage.setItem("dashboardLanguage", lang);
  document.documentElement.lang = lang;

  // Update all elements with data-i18n attribute
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    const vars = el.dataset.i18nVars ? JSON.parse(el.dataset.i18nVars) : {};
    el.textContent = t(key, vars);
  });

  // Update attributes (aria-label, title, placeholder)
  document.querySelectorAll("[data-i18n-attr]").forEach((el) => {
    const attr = el.dataset.i18nAttr;
    const key = el.dataset.i18nAttrKey;
    const vars = el.dataset.i18nVars ? JSON.parse(el.dataset.i18nVars) : {};
    el.setAttribute(attr, t(key, vars));
  });

  // Emit custom event for dynamic content
  window.dispatchEvent(new CustomEvent("languageChanged", { detail: { lang } }));
}

/**
 * Initialize language from localStorage on page load
 * Call this in your main script initialization
 */
function initLanguage() {
  const saved = localStorage.getItem("dashboardLanguage") || "de";
  currentLanguage = saved;
  document.documentElement.lang = saved;

  // Set dropdown to saved language
  const selector = document.getElementById("langSelect");
  if (selector) selector.value = saved;

  // Initial translation of all elements
  changeLanguage(saved);
}

// Auto-initialize when script loads (if DOM is ready)
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initLanguage);
} else {
  initLanguage();
}
