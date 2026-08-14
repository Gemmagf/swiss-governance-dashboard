# VERIFICATION CHECKLIST - Safety Protocol

## Executar SEMPRE després de cada canvi

### 🔴 CRÍTICO: Verificació visual (30 segons)

Obrir dashboard_real.html al navegador local:
```bash
cd /tmp/swiss-governance-dashboard
python3 -m http.server 8000
# Obrir http://localhost:8000/dashboard_real.html
```

**Checklist visual:**
- [ ] Dashboard carrega sense errors
- [ ] Títol visible: "Datencockpit Schweiz" (o traducció correcta)
- [ ] Botons de scenario visibles: "Acord", "Tendencial", "Estrès"
- [ ] Botons principals visibles: "▶ Anima", "Vista nacional", "CSV"
- [ ] Mapa de cantones es mostra
- [ ] Panells del costat dret visibles
- [ ] Sense text truncat o deformat

### 🟠 MAJOR: Verificació de funcionalitat (1 minut)

**Botons**
- [ ] Click a "▶ Anima" → animació comença
- [ ] Click a "Vista nacional" → torna a Suïssa
- [ ] Click a "CSV" → descàrrega fitxer (o intent)
- [ ] Botons scenario canvien estat

**Selector de idioma**
- [ ] Selector carrega amb idioma correcte
- [ ] Cambiar a "en" → textos canvien a anglès
- [ ] Cambiar a "ca" → textos canvien a català
- [ ] Reload pàgina → manté l'idioma seleccionat (localStorage)

**Slider de any**
- [ ] Arrossega correctament
- [ ] Número d'any s'actualitza

**Mapa**
- [ ] Hover over canton → color canvia
- [ ] Click canton → detalls del cantó

### 🟡 MEDIUM: Verificació de consola (30 segons)

Obrir Developer Tools (F12) → Console tab:
```
✓ No errors (cap text roig)
✓ No warnings específics de traducció
✓ Funcions disponibles: t(), changeLanguage(), getCurrentLanguage()
```

Provar:
```javascript
// Consola
t('btn_animate')
// Esperada resposta: "▶ Anima" (o traducció correcta)

getCurrentLanguage()
// Esperada resposta: "ca" (o idioma actual)

changeLanguage('en')
// Els textos han de cambiar a anglès

changeLanguage('ca')
// Els textos han de tornar a català
```

### 🟢 LOW: Verificació de código (30 segons)

```bash
# Verificar que translation_solution.js es carrega
grep -n "translation_solution.js" /tmp/swiss-governance-dashboard/dashboard_real.html

# Verificar que t() funció es defineix ANTES de usarla
grep -n "function t(" /tmp/swiss-governance-dashboard/dashboard_real.html
```

---

## ⚠️ PROBLEMES COMUNS I SOLUCIONS

### Problema: "t is not defined" a la consola
**Solució:**
1. Verificar que `<script src="translation_solution.js"></script>` està al dashboard
2. Verificar que est ANTES del script que fa servir t()
3. Hard refresh: `Ctrl+Shift+R`

### Problema: Idioma canvia pero els textos no
**Solució:**
1. Verificar que updateUITexts() s'executa
2. Afegir console.log('Updating to lang:', lang) dins updateUITexts()
3. Verificar que els selectors CSS són correctes

### Problema: Dashboard no carrega
**Solució:**
1. Obrir Console (F12) i veure l'error exacte
2. Si syntax error: revisar translation_solution.js
3. Si 404: verificar path de traducció.js
4. Git revert: `git checkout dashboard_real.html`

### Problema: Alguns textos no es tradueixen
**Solució:**
1. Verificar que el text es trobi dins l'HTML
2. Grep: `grep -n "text exacte" dashboard_real.html`
3. Afegiría entrada al diccionari TRANSLATIONS
4. Afegir selector CSS a updateUITexts()

---

## 📋 REGISTRE DE VERIFICACIONS

Omplir après de cada commit:

### Commit: [COMMIT HASH]
Fecha: [DATA]
Fase: [1/2/3/4]

**Verificació visual:** ✓ / ✗
**Funcionalitat botons:** ✓ / ✗
**Idioma selector:** ✓ / ✗
**Console errors:** ✓ / ✗

**Issues encontrats:**
- [Llistar problemes]

**Solució aplicada:**
- [Llistar solucions]

---

## 🚀 ROLLBACK RÀPID

Si algo es trenca irremediablement:

```bash
# Ver estado actual
git status

# Revertir dashboard a última versió bona
git checkout dashboard_real.html

# O revertir úlitm commit
git reset --soft HEAD~1

# O checkout de branca anterior
git checkout main
git branch -D translation-safe
git checkout -b translation-safe
```

---

## ✅ DEPLOYMENT FINAL

Solo después de que FASE 4 esté completa y verificada:

```bash
# Ver cambios finales
git diff main...translation-safe

# Merge a main
git checkout main
git merge translation-safe

# Push a producción
git push origin main
```

