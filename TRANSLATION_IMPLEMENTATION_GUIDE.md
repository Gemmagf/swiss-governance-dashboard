# German Translation Implementation Guide

## Overview

This guide explains how to integrate the comprehensive German translations for domains 3-7 (Education, Mobility, Energy & Climate, Health & Public Services, Territory & Housing) into the Swiss Governance Dashboard.

**Files Generated:**
- `GERMAN_TRANSLATIONS.md` - Human-readable reference document
- `GERMAN_TRANSLATIONS.json` - Machine-readable JSON format
- `GERMAN_TRANSLATIONS_COMPLETE.csv` - CSV format for find-and-replace operations

**Coverage:**
- ✅ 5 domains (Educació, Mobilitat, Energia, Serveis, Territori)
- ✅ 25 metrics total (5 per domain)
- ✅ 25 metric units
- ✅ 25 data sources
- ✅ 45+ policy levers
- ✅ 50+ drivers/factors
- ✅ Common UI labels and section headings

---

## Implementation Methods

### Method 1: Update translations.json (Recommended)

**File:** `/translations.json`

Add the German translations to the existing translations.json structure:

```json
{
  "translations": {
    // Add these new keys for domain-specific content:
    
    "domain.education": {
      "de": "Bildung",
      "ca": "Educació",
      // ... existing translations
    },
    
    "metric.educacio.ratio.label": {
      "de": "Schüler-Lehrer-Verhältnis",
      "ca": "Ràtio alumnat per docent"
    },
    
    "metric.educacio.ratio.unit": {
      "de": "Schüler",
      "ca": "alumnes"
    },
    
    "source.educacio.ratio": {
      "de": "BFS · Schulstatistik",
      "ca": "BFS Estadística escolar"
    },
    
    "lever.educacio.ratio.salary_increase": {
      "de": "Erhöhung der Lehrergehälter",
      "ca": "Augment de salari docent"
    },
    
    "driver.educacio.ratio.budget_education": {
      "de": "Bildungsbudget",
      "ca": "Pressupost d'educació"
    }
    
    // Repeat for all remaining domains...
  }
}
```

**Advantages:**
- Centralized translation management
- Single source of truth
- Easy to maintain alongside existing translations
- Consistent with current infrastructure

### Method 2: Create Separate Domain Translation Files

**New Files:** 
- `/configs/translations_educacio.yaml`
- `/configs/translations_mobilitat.yaml`
- `/configs/translations_energia.yaml`
- `/configs/translations_serveis.yaml`
- `/configs/translations_territori.yaml`

**YAML Format Example:**

```yaml
# configs/translations_educacio.yaml
translations:
  de:
    domain:
      label: "Bildung"
    metrics:
      ratio:
        label: "Schüler-Lehrer-Verhältnis"
        unit: "Schüler"
        source: "BFS · Schulstatistik"
      despesa:
        label: "Öffentliche Ausgaben pro Schüler"
        unit: "CHF/Jahr"
        source: "BFS · Bildungskonten"
      # ... remaining metrics
    levers:
      ratio:
        - "Erhöhung der Lehrergehälter"
        - "Lehrer-Weiterbildungsprogramm"
        - "Investitionen in Klassenzimmer"
        - "Lehrerwerbungskampagnen"
      digital:
        - "Investitionen in Schul-IKT"
        - "Lehrerschulung in digitaler Technologie"
        - "Zuschüsse für digitale Geräte"
        - "Cloud-Infrastruktur für Schulen"
    drivers:
      ratio:
        - "Bildungsbudget"
        - "Verfügbarkeit von Lehrern"
        - "Schülerzahl/Anmeldungen"
        - "Lehrerbindung"
      digital:
        - "IKT-Budget"
        - "Lehrerfortbildung in Technologie"
        - "Internetverfügbarkeit"
        - "Verfügbarkeit von Geräten"

  ca:
    # Mirror existing Catalan translations
```

**Advantages:**
- Modular organization (one file per domain)
- Easier to maintain large translation sets
- Clear separation of concerns
- Can be loaded conditionally

### Method 3: Update Data Files Directly

**Files to Update:**
- `/data/processed/real_data_hybrid.json`
- `/src/causal/dags.py`

**For real_data_hybrid.json:**

```json
{
  "domains": [
    {
      "id": "educacio",
      "label": "Bildung",  // Add German label
      "label_ca": "Educació",  // Keep Catalan
      "metrics": {
        "ratio": {
          "label": "Schüler-Lehrer-Verhältnis",  // Add German
          "label_ca": "Ràtio alumnat per docent",  // Keep Catalan
          "unit": "Schüler",  // Add German
          "unit_ca": "alumnes",  // Keep Catalan
          "source": "BFS · Schulstatistik",  // Add German
          "source_ca": "BFS Estadística escolar"  // Keep Catalan
        }
      }
    }
  ]
}
```

**For dags.py:**

```python
CAUSAL_DAGS = {
    "educacio": {
        "label_de": "Bildung",
        "label_ca": "Educació",
        "metrics": {
            "ratio": {
                "label_de": "Schüler-Lehrer-Verhältnis",
                "label_ca": "Ràtio alumnat per docent",
                "dag": { ... },
                "policy_levers_de": [
                    "Erhöhung der Lehrergehälter",
                    "Lehrer-Weiterbildungsprogramm",
                    "Investitionen in Klassenzimmer",
                    "Lehrerwerbungskampagnen"
                ],
                "policy_levers_ca": [
                    "Augment de salari docent",
                    "Programa de formació contínua de docents",
                    "Inversió en aules escolars",
                    "Campanyes de reclutament de docents"
                ]
            }
        }
    }
}
```

**Advantages:**
- Changes at the source
- No translation lookups needed
- Simplifies frontend logic
- Better performance

---

## Frontend Integration

### Using in Streamlit App

**Example:** `/src/frontend/app.py`

```python
import json

# Load translations
with open('GERMAN_TRANSLATIONS.json', 'r', encoding='utf-8') as f:
    german_trans = json.load(f)

# Use in UI
if selected_language == 'de':
    st.title(german_trans['translations']['section_headings']['canton_ranking'])
    
    metric_label = german_trans['translations']['educacio']['metrics']['ratio']['label']
    metric_unit = german_trans['translations']['educacio']['metrics']['ratio']['unit']
    
    st.metric(label=metric_label, value=123.45, delta="1.2%")
```

### Using with Translation Function

**Create a translation utility:**

```python
# src/utils/i18n.py

import json

class Translator:
    def __init__(self, language='de'):
        with open('GERMAN_TRANSLATIONS.json', 'r', encoding='utf-8') as f:
            self.translations = json.load(f)
        self.lang = language
    
    def translate(self, domain, category, item):
        """
        Example:
        translate('educacio', 'metrics', 'ratio.label')
        """
        parts = item.split('.')
        result = self.translations['translations'].get(domain, {})
        for part in parts:
            result = result.get(part, {})
        return result if isinstance(result, str) else ''
    
    def metric_label(self, domain, metric_id):
        return self.translations['translations'][domain]['metrics'][metric_id]['label']
    
    def metric_unit(self, domain, metric_id):
        return self.translations['translations'][domain]['metrics'][metric_id]['unit']
    
    def data_source(self, domain, metric_id):
        return self.translations['translations'][domain]['sources'].get(metric_id, '')
    
    def policy_levers(self, domain, metric_id):
        levers_key = f"{metric_id}_levers"
        return self.translations['translations'][domain]['levers'].get(levers_key, [])
    
    def drivers(self, domain, metric_id):
        drivers_key = f"{metric_id}_drivers"
        return self.translations['translations'][domain]['drivers'].get(drivers_key, [])

# Usage in app
t = Translator('de')
st.write(t.metric_label('educacio', 'ratio'))
st.write(t.data_source('educacio', 'ratio'))
st.multiselect("Hebel", t.policy_levers('educacio', 'ratio'))
```

---

## Find-and-Replace Guide (CSV Method)

**Using the CSV file for bulk replacements:**

### In Excel/Google Sheets:
1. Open `GERMAN_TRANSLATIONS_COMPLETE.csv`
2. Filter by Domain = "Educació" (or desired domain)
3. Filter by Category = "Metric Label" (or desired category)
4. Export filtered results as a reference list
5. Use Find-and-Replace in code editor:
   - Find: `Ràtio alumnat per docent`
   - Replace with: `Schüler-Lehrer-Verhältnis` (+ DE flag or conditional)

### In VS Code:
1. Use Find-and-Replace (Ctrl+H)
2. Enable Regex
3. Search: `(Ràtio alumnat per docent)` 
4. Replace: `Schüler-Lehrer-Verhältnis` (with language context)

### In Python:
```python
import pandas as pd

# Read translations
translations_df = pd.read_csv('GERMAN_TRANSLATIONS_COMPLETE.csv')

# Create lookup dictionary
ca_to_de = dict(zip(translations_df['Catalan'], translations_df['German']))

# Apply to data
def translate_domain(data, domain):
    for old, new in ca_to_de.items():
        data = data.replace(old, new)
    return data

# Use:
data = translate_domain(data, 'educacio')
```

---

## Testing Checklist

Before deploying German translations:

- [ ] All 5 domain labels display correctly
- [ ] All 25 metric labels appear in German
- [ ] All metric units translated (e.g., "CHF/Jahr" not "CHF/any")
- [ ] All 25 data sources show German abbreviations (BFS · Schulstatistik)
- [ ] All 45+ policy levers display in German
- [ ] All 50+ drivers/factors translate properly
- [ ] Section headings in German (KANTONALES RANKING)
- [ ] UI elements translated (Indikator, Einheit, Quelle, Hebel, Faktor)
- [ ] No mixed-language text (e.g., "Bildung | Educació" unless intentional)
- [ ] Language selector shows "🇩🇪 Deutsch"
- [ ] Charts and tables respect German number format (. for thousands, , for decimals where appropriate)
- [ ] Date formats follow German convention (DD.MM.YYYY)
- [ ] No untranslated Catalan text leaks through

---

## Rollout Strategy

### Phase 1: Static Content (Week 1)
- Add all translations to `translations.json`
- Ensure domain labels, metric labels, units display correctly
- Test in Streamlit app with German language selected

### Phase 2: Dynamic Content (Week 2)
- Integrate data sources and policy lever translations
- Verify DAG-based explanations use German labels
- Test simulator with German interface

### Phase 3: Edge Cases (Week 3)
- Handle special characters (ü, ö, ä, ß)
- Test with different screen sizes and resolutions
- Verify chart axis labels and tooltips
- Test hover text and help messages

### Phase 4: Deployment (Week 4)
- Merge to main branch
- Deploy to staging environment
- Final QA with German-speaking stakeholders
- Deploy to production

---

## Common Pitfalls & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Mixed languages in UI | Partial translation | Ensure all keys in `translations.json` updated |
| Corrupted umlauts (ü→ü) | Encoding issue | Ensure UTF-8 encoding in all files |
| Levers not appearing | Key mismatch in DAGs | Use consistent metric_id format (e.g., "ratio_levers") |
| Drivers/factors untranslated | Technical names used | Map technical IDs to user-facing labels |
| Truncated text in UI | German text longer | Adjust UI width/font size for longer text |
| Date formats wrong | Regional settings | Use German locale (de_DE) for date formatting |

---

## File Locations Summary

| File | Purpose | Format |
|------|---------|--------|
| `GERMAN_TRANSLATIONS.md` | Reference document | Markdown |
| `GERMAN_TRANSLATIONS.json` | Programmatic use | JSON |
| `GERMAN_TRANSLATIONS_COMPLETE.csv` | Find-and-replace, spreadsheet | CSV |
| `translations.json` | Integration point | JSON |
| `configs/translations.yaml` | Alternative integration | YAML |
| `src/causal/dags.py` | DAG source data | Python |
| `data/processed/real_data_hybrid.json` | Real data + metadata | JSON |

---

## Contact & Support

For questions about specific translations or implementation:

1. Review the markdown reference (`GERMAN_TRANSLATIONS.md`)
2. Check the JSON structure (`GERMAN_TRANSLATIONS.json`)
3. Cross-reference with CSV for context (`GERMAN_TRANSLATIONS_COMPLETE.csv`)
4. Consult existing translations.json for pattern consistency

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-08-11 | Initial comprehensive translation dictionary for domains 3-7 |

