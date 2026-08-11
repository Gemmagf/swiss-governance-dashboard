/**
 * Auto-translate Dashboard
 * Scans DOM and applies translations from translation_system.js
 * This script works alongside translation_system.js to automatically
 * translate the entire dashboard interface
 */

function autoTranslateDashboard() {
  // Wait for translation system to load
  if (typeof t !== 'function') {
    console.log('Waiting for translation_system.js...');
    setTimeout(autoTranslateDashboard, 100);
    return;
  }

  // Map of selectors to translation keys
  const translationMap = {
    // Headers
    '.hdr h1': 'hdr.title',
    '.hdr h1 small': 'hdr.subtitle',

    // Controls bar labels
    '.lbl': {
      'Gebiet': 'meta.domain',
      'Bevölkerung': 'meta.population',
      'Fläche': 'meta.area',
      'Modelle': 'meta.models',
      'Jahr': 'ctrl.year'
    },

    // View buttons (Karte, Tabelle, Details, etc.)
    '.seg button': {
      'Karte': 'btn.map_view',
      'Tabelle': 'btn.table_view',
      'Details': 'btn.details_view'
    },

    // Main buttons
    '.btn': {
      '▶ Animieren': 'btn.animate',
      'Nationalansicht': 'btn.national_view',
      'Kantonansicht': 'btn.canton_view'
    },

    // Scenario toggles
    '.seg button': {
      'Tendenzielle': 'ctrl.scenario_baseline',
      'Abkommen': 'ctrl.scenario_agreement',
      'Stress': 'ctrl.scenario_stress'
    },

    // Sidebar sections
    '.side h3': {
      'Territorium': 'sidebar.territory',
      'Indikatoren': 'sidebar.indicators',
      'Zeitreihe': 'sidebar.timeseries'
    }
  };

  // Function to translate element content
  function translateElement(el, key) {
    if (typeof key === 'object') {
      // Map of text → key
      const text = el.textContent.trim();
      const translatedKey = key[text];
      if (translatedKey) {
        el.textContent = t(translatedKey);
        el.setAttribute('data-i18n', translatedKey);
      }
    } else {
      // Direct key
      el.textContent = t(key);
      el.setAttribute('data-i18n', key);
    }
  }

  // Apply translations to all selectors
  for (const [selector, keyMap] of Object.entries(translationMap)) {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      if (el.getAttribute('data-i18n')) return; // Skip already translated
      translateElement(el, keyMap);
    });
  }

  // Translate scenario year labels
  const yearvalSpans = document.querySelectorAll('.yearval span');
  yearvalSpans.forEach(span => {
    const text = span.textContent.trim();
    if (text === 'beobachtet') span.textContent = t('ctrl.year_status_observed');
    if (text === 'Prognose') span.textContent = t('ctrl.year_status_forecast');
  });

  console.log('✅ Dashboard auto-translated to', getCurrentLanguage());
}

// Re-translate when language changes
document.addEventListener('languageChanged', () => {
  autoTranslateDashboard();
});

// Start translation on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', autoTranslateDashboard);
} else {
  autoTranslateDashboard();
}
