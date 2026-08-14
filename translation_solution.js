/**
 * TRANSLATION SYSTEM - INLINE
 * Simple, robust, no external dependencies
 * ============================================
 *
 * ESTRATÈGIA:
 * 1. Tot el diccionari dins aquest fitxer
 * 2. Funcions simples: t(key, lang) i changeLanguage(lang)
 * 3. S'inclou al final de dashboard_real.html
 * 4. NO càrrega externa, NO dependències
 * 5. localStorage per persistència de preferència
 *
 * USO:
 * - Textos estàtics: <button>t('btn_animate')</button>
 * - Textos dinàmics: document.getElementById('id').textContent = t('key_name')
 * - Canviar idioma: changeLanguage('en')
 * - Idioma actual: getCurrentLanguage()
 */

// ====== DICCIONARI DE TRADUCCIONS ======
const TRANSLATIONS = {
  'en': {
    // CRÍTICOS - Títol i controls principals
    'title_main': 'Swiss Data Cockpit',
    'title_sub': 'Confederation Data Cockpit · interdepartmental prototype',
    'btn_scenario_opt': 'Agreement',
    'btn_scenario_base': 'Baseline',
    'btn_scenario_str': 'Stress',
    'btn_animate': '▶ Animate',
    'btn_reset': 'National View',
    'btn_csv': 'CSV',
    'btn_panels': 'Panels',

    // ZOOM BUTTONS
    'title_zoom_in': 'Zoom in',
    'title_zoom_out': 'Zoom out',
    'title_zoom_fit': 'Fit all Switzerland',

    // PANEL TÍTOLS (Right side)
    'panel_forecast': 'Forecast & Evolution',
    'panel_forecast_badge': 'Probabilistic ensemble',
    'panel_simulator': 'Policy Simulator',
    'panel_simulator_badge': 'Counterfactual',
    'panel_situation': 'Situation Report',
    'panel_situation_badge': 'AI Generated',
    'panel_alerts': 'Alert Signals',
    'panel_alerts_badge': 'Anomaly detection',
    'panel_model': 'Model & Data Card',

    // MAPA (Left side - Cantons)
    'crumb_switzerland': 'Switzerland',

    // INDICADORS (Dinàmics - els noms específics)
    // Anirà actualitzant segons necessitat
    'ind_example': 'Example Indicator',

    // CONTROLS BAR
    'lbl_year': 'YEAR',
    'lbl_scenario': 'SCENARIO',

    // STATUS/MESSAGES
    'status_loading': 'Loading...',
    'status_ready': 'Ready',
  },

  'ca': {
    // CRÍTICOS - Títol i controls principals
    'title_main': 'Datencockpit Schweiz',
    'title_sub': 'Cockpit de dades de la Confederació · prototip interdepartamental',
    'btn_scenario_opt': 'Acord',
    'btn_scenario_base': 'Tendencial',
    'btn_scenario_str': 'Estrès',
    'btn_animate': '▶ Anima',
    'btn_reset': 'Vista nacional',
    'btn_csv': 'CSV',
    'btn_panels': 'Panells',

    // ZOOM BUTTONS
    'title_zoom_in': 'Amplia',
    'title_zoom_out': 'Redueix',
    'title_zoom_fit': 'Tot Suïssa',

    // PANEL TÍTOLS (Right side)
    'panel_forecast': 'Evolució i previsió',
    'panel_forecast_badge': 'Conjunt probabilístic',
    'panel_simulator': 'Simulador de mesures',
    'panel_simulator_badge': 'Contrafactual',
    'panel_situation': 'Nota de situació',
    'panel_situation_badge': 'Generada',
    'panel_alerts': 'Senyals d\'alerta',
    'panel_alerts_badge': 'Detecció d\'anomalies',
    'panel_model': 'Fitxa del model i dades',

    // MAPA
    'crumb_switzerland': 'Suïssa',

    // INDICADORS
    'ind_example': 'Indicador exemple',

    // CONTROLS BAR
    'lbl_year': 'ANY',
    'lbl_scenario': 'ESCENARI',

    // STATUS/MESSAGES
    'status_loading': 'Carregant...',
    'status_ready': 'Llest',
  },

  'de': {
    // CRÍTICOS - Títol i controls principals
    'title_main': 'Schweizerisches Datencockpit',
    'title_sub': 'Datencockpit der Konföderation · interdepartamentaler Prototyp',
    'btn_scenario_opt': 'Vereinbarung',
    'btn_scenario_base': 'Szenario',
    'btn_scenario_str': 'Stress',
    'btn_animate': '▶ Animieren',
    'btn_reset': 'Nationale Ansicht',
    'btn_csv': 'CSV',
    'btn_panels': 'Panels',

    // ZOOM BUTTONS
    'title_zoom_in': 'Vergrößern',
    'title_zoom_out': 'Verkleinern',
    'title_zoom_fit': 'Ganzes Schweiz',

    // PANEL TÍTOLS
    'panel_forecast': 'Entwicklung und Prognose',
    'panel_forecast_badge': 'Probabilistisches Ensemble',
    'panel_simulator': 'Policy-Simulator',
    'panel_simulator_badge': 'Kontrafaktisch',
    'panel_situation': 'Situationsbericht',
    'panel_situation_badge': 'KI-generiert',
    'panel_alerts': 'Warnsignale',
    'panel_alerts_badge': 'Anomalieerkennung',
    'panel_model': 'Modell- und Datenkarte',

    // MAPA
    'crumb_switzerland': 'Schweiz',

    // INDICADORS
    'ind_example': 'Beispielindikator',

    // CONTROLS BAR
    'lbl_year': 'JAHR',
    'lbl_scenario': 'SZENARIO',

    // STATUS/MESSAGES
    'status_loading': 'Lädt...',
    'status_ready': 'Bereit',
  }
};

// ====== FUNCIONS DE TRADUCCIÓ ======

/**
 * Obtenir traducció d'una clau
 * @param {string} key - Clau de traducció (ex: 'btn_animate')
 * @param {string} lang - Idioma (defecte: idioma actual)
 * @returns {string} Texte traducit o clau si no existeix
 */
function t(key, lang = null) {
  if (!lang) lang = getCurrentLanguage();

  if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
    return TRANSLATIONS[lang][key];
  }

  // Fallback: Anglès si no existeix en l'idioma sol·licitat
  if (lang !== 'en' && TRANSLATIONS['en'][key]) {
    return TRANSLATIONS['en'][key];
  }

  // Última resort: retornar la clau
  return key;
}

/**
 * Obtenir idioma actual
 * @returns {string} Codi d'idioma (en, ca, de, etc.)
 */
function getCurrentLanguage() {
  return localStorage.getItem('preferredLanguage') || 'en';
}

/**
 * Canviar idioma (i guardar preferència)
 * @param {string} lang - Codi d'idioma
 */
function changeLanguage(lang) {
  if (!TRANSLATIONS[lang]) {
    console.warn('Language not supported:', lang);
    return;
  }

  localStorage.setItem('preferredLanguage', lang);

  // Actualitzar SELECT
  const select = document.getElementById('langSelect');
  if (select) select.value = lang;

  // AQUÍ ANIRAN LES ACTUALITZACIONS DE TEXTOS
  updateUITexts(lang);

  console.log('Language changed to:', lang);
}

/**
 * Actualitzar tots els textos del UI a un idioma determinat
 * @param {string} lang - Codi d'idioma
 */
function updateUITexts(lang) {
  // Aquesta funció s'anirà omplint segons anem afegint les traduccions
  // Per ara deixem que el JavaScript existent no es trenqui

  // FASE 1: Actualitzar textos estàtics que podem trobar
  const updates = {
    // Afegir IDs de elements aquí:
    // 'id_element': 'key_traducció'
  };

  for (const [elementId, key] of Object.entries(updates)) {
    const el = document.getElementById(elementId);
    if (el) {
      el.textContent = t(key, lang);
    }
  }
}

/**
 * Inicialitzar sistema de traduccions al carregament
 */
function initTranslations() {
  const preferredLang = getCurrentLanguage();

  // Actualitzar SELECT amb idioma guardatß
  const select = document.getElementById('langSelect');
  if (select) {
    select.value = preferredLang;
  }

  // Aplicar idioma (quan implementem updateUITexts completament)
  // changeLanguage(preferredLang);
}

// Auto-inicialitzar quan el DOM sigui llest
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTranslations);
} else {
  initTranslations();
}
