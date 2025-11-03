"""
Simple translation module to map code words to English, French and Spanish.

This is a lightweight start for a translator used by the project. It stores
an in-memory TRANSLATIONS dictionary and provides helper functions to
translate single words, translate lists, add new translations, and persist
to a JSON file.

Usage:
    from translator import translate, bulk_translate
    translate('guerrier', 'en')  # -> 'warrior'

Future improvements:
 - Load translations from external sources (CSV/JSON)
 - Fuzzy matching / pluralization
 - Context-aware translations
 - Integration with project files
"""
from __future__ import annotations

import json
from typing import Dict, List, Optional, Tuple

# Supported languages: keys are language codes
SUPPORTED_LANGS = {"en", "fr", "es"}

# Basic translations: code_word -> {lang: translation}
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # example entries
    "mon blog :": {"en": "My blog:", "fr": "Visitez mon blog :", "es": "Mi blog:"},
    "domaine": {"en": "DOMAIN", "fr": "DOMAINE", "es": "todo"},
    "origine": {"en": "COMMUNITY", "fr": "ORIGINE", "es": "todo"},
    "ascendance": {"en": "ANCESTRY", "fr": "ASCENDANCE", "es": "todo"},
    "rappel": {"en": "Recall", "fr": "Rappel ", "es": "todo"},
    "foundations": {"en": "Foundation", "fr": "Novice", "es": "todo"},
    "specializations": {"en": "Specialization", "fr": "Spécialiste", "es": "todo"},
    "masteries": {"en": "Mastery", "fr": "Maître", "es": "todo"},
    "sous classe de": {"en": "SUBCLASS OF", "fr": "SOUS-CLASSE DE", "es": "todo"},
    "trait incantation": {"en": "Spellcast Trait:", "fr": "Trait d'incantation :", "es": "todo"},
    "ppage titre origine": {"en": "COMMUNITY CARDS", "fr": "CARTES D'ORIGINES", "es": "todo"},
    "ppage titre ascendance": {"en": "ANCESTRY CARDS", "fr": "CARTES D'ASCENDANCES", "es": "todo"},
    "ppage titre domaine": {"en": "DOMAIN CARDS", "fr": "CARTES DE DOMAINES", "es": "todo"},
    "ppage titre sous classe": {"en": "SUBCLASS CARDS", "fr": "CARTES DE SOUS-CLASSES", "es": "todo"},
    "ppage titre classe": {"en": "CLASS CARDS", "fr": "CARTES DE CLASSES", "es": "todo"},
    "ppage sstitre domaines": {"en": "Domain(s):", "fr": "Domaine(s) :", "es": "todo"},
    "ppage sstitre rang": {"en": "Tier:", "fr": "Rang :", "es": "todo"},
    "ppage sstitre langue": {"en": "Language:", "fr": "Langue :", "es": "todo"},
    "ppage sstitre trad": {"en": "(SRD 1.0)", "fr": "(Traduction non officielle)", "es": "todo"},
    "ppage sstitre sous classe": {"en": "Type(s):", "fr": "Type(s) :", "es": "todo"},
    "ppage sstitre classe": {"en": "Class:", "fr": "Classe :", "es": "todo"},
    "ppage pack complet": {"en": "COMPLETE PACK", "fr": "PACK COMPLET", "es": "todo"},
    "classe espoir": {"en": "Hope Feature", "fr": "Capacité d'Espoir", "es": "todo"},
    "classe capacites": {"en": "Class Features", "fr": "Capacités de Classe", "es": "todo"},

    "fp copyright": {"en": "This product includes materials from the Daggerheart System Reference Document 1.0, ©Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others.", 
                  "fr": "This product includes materials from the Daggerheart System Reference Document 1.0, ©Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others.", 
                  "es": "This product includes materials from the Daggerheart System Reference Document 1.0, ©Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others."},
    "fp logo": {"en": "Darrington Press™ and the Darrington Press authorized work logo are trademarks of Critical Role, LLC and used with permission.", 
                  "fr": "Darrington Press™ and the Darrington Press authorized work logo are trademarks of Critical Role, LLC and used with permission.", 
                  "es": "Darrington Press™ and the Darrington Press authorized work logo are trademarks of Critical Role, LLC and used with permission."},
}

def translate(code_word: str, target_lang: str):
    """Translate a single code word to a target language.

    Args:
        code_word: the source code word (case-insensitive)
        target_lang: one of 'en', 'fr', 'es'
        default: value to return if translation not found (None by default)

    Returns:
        Translated string or default
    """
    default = "None"

    if not code_word:
        return default

    lang = target_lang.lower()
    if lang not in SUPPORTED_LANGS:
        raise ValueError(f"Unsupported language: {target_lang}")

    key = code_word.strip().lower()
    entry = TRANSLATIONS.get(key)
    if not entry:
        return default

    return entry.get(lang, default)


def bulk_translate(words: List[str], target_lang: str, missing: Optional[str] = None) -> List[Optional[str]]:
    """Translate a list of words to the target language."""
    return [translate(w, target_lang) for w in words]

