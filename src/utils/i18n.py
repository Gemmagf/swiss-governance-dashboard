"""Internationalization (i18n) utilities."""

import yaml
from pathlib import Path
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
TRANSLATIONS_FILE = PROJECT_ROOT / "configs" / "translations.yaml"


class I18n:
    """Translation manager."""

    def __init__(self):
        self.translations = self._load_translations()
        self.languages = self._get_languages()
        self.default_language = "en"

    def _load_translations(self) -> Dict[str, Any]:
        """Load translations from YAML."""
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("translations", {})

    def _get_languages(self) -> list:
        """Get available languages."""
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("languages", [])

    def t(self, key: str, lang: str = "en") -> str:
        """Translate a key to the specified language.

        Args:
            key: Translation key (e.g., "app_title")
            lang: Language code (de, fr, it, en)

        Returns:
            Translated string or key if not found
        """
        if key not in self.translations:
            return key

        trans = self.translations[key]
        if isinstance(trans, dict):
            return trans.get(lang, trans.get(self.default_language, key))

        return str(trans)

    def get_language_options(self) -> Dict[str, str]:
        """Get language selection options.

        Returns:
            Dict mapping language code to display name
        """
        return {lang["code"]: f"{lang['flag']} {lang['name']}" for lang in self.languages}

    def get_language_names(self) -> Dict[str, str]:
        """Get language names (without flags)."""
        return {lang["code"]: lang["name"] for lang in self.languages}


# Global instance
i18n = I18n()
