/**
 * Auto-translate Dashboard
 * Dynamically translates UI text from translations.json
 * Works alongside translation_system.js
 */

function autoTranslateDashboard() {
  // Ensure translation system is ready
  if (typeof t !== 'function' || typeof TRANSLATIONS === 'undefined') {
    console.log('⏳ Waiting for translation_system.js...');
    setTimeout(autoTranslateDashboard, 200);
    return;
  }

  // Translation map: text content → translation key
  // Format: { originalText: 'translationKey' }
  const textMap = {
    // German text → translation keys
    'Gebiet': 'meta.domain',
    'Bevölkerung': 'meta.population',
    'Fläche': 'meta.area',
    'Modelle': 'meta.models',
    'Jahr': 'ctrl.year',
    'beobachtet': 'ctrl.year_status_observed',
    'Prognose': 'ctrl.year_status_forecast',
    'Karte': 'btn.map_view',
    'Tabelle': 'btn.table_view',
    'Details': 'btn.details_view',
    'Kantonansicht': 'btn.canton_view',
    'Nationalansicht': 'btn.national_view',
    '▶ Animieren': 'btn.animate',
    'Tendenzielle': 'ctrl.scenario_baseline',
    'Abkommen': 'ctrl.scenario_agreement',
    'Stress': 'ctrl.scenario_stress',
    'Territorium': 'sidebar.territory',
    'Indikatoren': 'sidebar.indicators',
    'Zeitreihe': 'sidebar.timeseries',
  };

  // Find and translate text nodes
  function walkDOM(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent.trim();
      if (text && textMap[text]) {
        const translatedText = t(textMap[text]);
        if (translatedText && translatedText !== text) {
          node.textContent = translatedText;
          // Mark parent as translated
          if (node.parentElement) {
            node.parentElement.setAttribute('data-i18n', textMap[text]);
          }
        }
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      // Skip script/style/meta tags
      if (!['SCRIPT', 'STYLE', 'META', 'LINK'].includes(node.tagName)) {
        Array.from(node.childNodes).forEach(walkDOM);
      }
    }
  }

  // Start translation from body
  if (document.body) {
    walkDOM(document.body);
  }

  const currentLang = document.getElementById('htmlRoot')?.lang || 'de';
  console.log('✅ Dashboard auto-translated to', currentLang);
}

// Re-translate when language changes
window.addEventListener('languageChanged', () => {
  console.log('🔄 Language changed, re-translating dashboard...');
  autoTranslateDashboard();
});

// Auto-translate on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit for other scripts to load
    setTimeout(autoTranslateDashboard, 300);
  });
} else {
  // Page already loaded
  setTimeout(autoTranslateDashboard, 300);
}
