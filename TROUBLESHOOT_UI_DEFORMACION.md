# 🚨 Solución: UI Deformada

## Causa probable
- Caché del navegador mostrando versión vieja
- Ventana de navegador muy pequeña
- Zoom del navegador modificado
- CSS no cargando correctamente

## ✅ Soluciones (en orden)

### 1. **Limpiar caché y recargar (PRIMERA OPCIÓN)**
```bash
# En el navegador:
Ctrl+Shift+R  (recargar forzado, limpiar caché)
# o
Cmd+Shift+R   (en Mac)
```

### 2. **Verificar tamaño de ventana**
```
- Maximizar ventana del navegador
- Asegurarse que NO está en modo móvil (F12 → Device Toolbar)
- Zoom en 100% (Ctrl+0)
```

### 3. **Verificar el archivo HTML localmente**
```bash
# Ver que el archivo no está corrompido:
cd /tmp/swiss-governance-dashboard
wc -l dashboard_real.html  # Debe ser 1037 líneas
tail -20 dashboard_real.html  # Debe terminar con </html>
```

### 4. **Reiniciar servidor HTTP**
```bash
# Matar servidor actual
pkill -9 -f http.server

# Reiniciar:
cd /tmp/swiss-governance-dashboard
python3 -m http.server 9000 > /tmp/http.log 2>&1 &

# Esperar 2 segundos
sleep 2

# Probar
curl -s http://127.0.0.1:9000/dashboard_real.html | head -1
# Debe mostrar: <!DOCTYPE html>
```

### 5. **Si sigue deformado, revertir cambios**
```bash
# Ver el estado
cd /tmp/swiss-governance-dashboard
git status

# Si hay cambios no committeados:
git stash

# Revertir a última versión buena:
git checkout HEAD~1 dashboard_real.html
git commit -m "revert: dashboard UI deformation - reverting to prior version"

# Reload en navegador (Ctrl+Shift+R)
```

---

## 📋 Verificación rápida

**El dashboard DEBE verse así:**
- ✅ Título grande: "Swiss Data Cockpit" (en inglés) o "Datencockpit Schweiz" (en catalán)
- ✅ Subtítulo visible: "Confederation Data Cockpit..."
- ✅ Mapa de cantones a la derecha
- ✅ Botones de scenario: Agreement, Baseline, Stress
- ✅ Botón Animate, National View, CSV
- ✅ Indicadores abajo: números, gráficos

**NO debe verse:**
- ❌ Texto truncado o superpuesto
- ❌ Barras de scroll horizontales
- ❌ Elementos fuera de pantalla
- ❌ Errores en consola (F12)

---

## 🔍 Debug

Si el problema persiste, revisar:

```bash
# 1. Ver los últimos errores del servidor
tail -50 /tmp/http.log

# 2. Ver cambios en git
git diff dashboard_real.html | head -100

# 3. Verificar líneas críticas
grep -n "Swiss Data Cockpit\|Datencockpit" dashboard_real.html

# 4. Comprobar que CSS no fue modificado
grep -c "\.hdr\|\.body\|\.side" dashboard_real.html  # Debe ser > 0
```

---

## ✨ Resultado esperado tras fix:

**Con Caché limpio + Navegador maximizado + Servidor reiniciado:**

El dashboard debe verse IDÉNTICO a la última captura de pantalla, excepto:
- Algunos textos en INGLÉS (los 15 que tradujimos)
- Todo lo demás = igual

