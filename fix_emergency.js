/**
 * EMERGENCY FIX: Force German + make language selector work
 * This script runs IMMEDIATELY on page load
 */

// 1. FORCE GERMAN on page load
document.documentElement.lang = 'de';
document.documentElement.id = 'htmlRoot';
localStorage.setItem('dashboardLang', 'de');

// 2. Ensure language selector is set to German
window.addEventListener('load', () => {
  const selector = document.getElementById('langSelect');
  if (selector) {
    selector.value = 'de';
    console.log('✅ Language selector set to German');
  }
});

// 3. Make language selector ACTUALLY work
setTimeout(() => {
  const selector = document.getElementById('langSelect');
  if (selector) {
    selector.addEventListener('change', (e) => {
      const newLang = e.target.value;
      console.log(`🌍 Language changed to: ${newLang}`);
      
      // Force reload to apply language change
      localStorage.setItem('dashboardLang', newLang);
      document.documentElement.lang = newLang;
      
      // Try to call translation functions if they exist
      if (typeof changeLanguage === 'function') {
        changeLanguage(newLang);
      }
      if (typeof updateDashboardTexts === 'function') {
        updateDashboardTexts();
      }
      if (typeof autoTranslateDashboard === 'function') {
        autoTranslateDashboard();
      }
      
      // Reload page to apply changes
      window.location.reload();
    });
    
    console.log('✅ Language selector event listener attached');
  }
}, 100);

console.log('🚀 Emergency fix loaded - German forced, selector ready');
