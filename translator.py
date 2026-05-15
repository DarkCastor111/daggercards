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
    "classe": {"en": "CLASS", "fr": "CLASSE", "es": "todo"},
    "classe bard": {"en": "Bard", "fr": "Barde", "es": "todo"},
    "classe druid": {"en": "Druid", "fr": "Druide", "es": "todo"},
    "classe guardian": {"en": "Guardian", "fr": "Champion", "es": "todo"},
    "classe warrior": {"en": "Warrior", "fr": "Guerrier", "es": "todo"},
    "classe wizard": {"en": "Wizard", "fr": "Arcaniste", "es": "todo"},
    "classe rogue": {"en": "Rogue", "fr": "Roublard", "es": "todo"},
    "classe ranger": {"en": "Ranger", "fr": "Rôdeur", "es": "todo"},
    "classe seraph": {"en": "Seraph", "fr": "Paladin", "es": "todo"},
    "classe sorcerer": {"en": "Sorcerer", "fr": "Ensorceleur", "es": "todo"},
    "trait incantation": {"en": "Spellcast Trait:", "fr": "Trait d'incantation :", "es": "todo"},
    "ppage titre origine": {"en": "COMMUNITY CARDS", "fr": "CARTES D'ORIGINES", "es": "todo"},
    "ppage titre ascendance": {"en": "ANCESTRY CARDS", "fr": "CARTES D'ASCENDANCES", "es": "todo"},
    "ppage titre domaine": {"en": "DOMAIN CARDS", "fr": "CARTES DE DOMAINES", "es": "todo"},
    "ppage titre sous classe": {"en": "SUBCLASS CARDS", "fr": "CARTES DE SOUS-CLASSES", "es": "todo"},
    "ppage titre classe": {"en": "CLASS CARDS", "fr": "CARTES DE CLASSES", "es": "todo"},
    "ppage titre beastform": {"en": "DRUID BEASTFORM CARDS", "fr": "CARTES DE FORME BESTIALE DU DRUIDE", "es": "todo"},
    "ppage sstitre domaines": {"en": "Domain(s):", "fr": "Domaine(s) :", "es": "todo"},
    "ppage sstitre rang": {"en": "Tier:", "fr": "Rang :", "es": "todo"},
    "ppage sstitre langue": {"en": "Language:", "fr": "Langue :", "es": "todo"},
    "ppage sstitre trad": {"en": "(SRD 1.0)", "fr": "(Traduction 'AI powered' non officielle)", "es": "todo"},
    "ppage sstitre sous classe": {"en": "Type(s):", "fr": "Type(s) :", "es": "todo"},
    "ppage sstitre classe": {"en": "Class:", "fr": "Classe :", "es": "todo"},
    "ppage sstitre process": {"en": "See the full creation process (in French) at:", "fr": "Le processus de création en détail :", "es": "todo"},
    "ppage sstitre materiel blog": {"en": "More content in my blog (in French)!", "fr": "Plus de matériel dans mon blog (en français) !", "es": "todo"},
    "ppage sstitre materiel patreon": {"en": "Follow my Patreon!", "fr": "Suivez ma page Patreon !", "es": "todo"},
    "ppage sstitre version": {"en": "Version:", "fr": "Version :", "es": "todo"},
    "ppage pack": {"en": "PACK", "fr": "PACK", "es": "todo"},
    "ppage pack complet": {"en": "FULL", "fr": "COMPLET", "es": "todo"},
    "ppage pack bard": {"en": "Bard", "fr": "Barde (Bard)", "es": "todo"},
    "ppage pack druid": {"en": "Druid", "fr": "Druide (Druid)", "es": "todo"},
    "ppage pack guardian": {"en": "Guardian", "fr": "Champion (Guardian)", "es": "todo"},
    "ppage pack warrior": {"en": "Warrior", "fr": "Guerrier (Warrior)", "es": "todo"},
    "ppage pack wizard": {"en": "Wizard", "fr": "Arcaniste (Wizard)", "es": "todo"},
    "ppage pack rogue": {"en": "Rogue", "fr": "Roublard (Rogue)", "es": "todo"},
    "ppage pack ranger": {"en": "Ranger", "fr": "Rodeur (Ranger)", "es": "todo"},
    "ppage pack seraph": {"en": "Seraph", "fr": "Paladin (Seraph)", "es": "todo"},
    "ppage pack sorcerer": {"en": "Sorcerer", "fr": "Ensorceleur (Sorcerer)", "es": "todo"},
    "classe espoir": {"en": "Hope Feature", "fr": "Capacité d'Espoir", "es": "todo"},
    "classe capacites": {"en": "Class Features", "fr": "Capacités de Classe", "es": "todo"},
    "classe spe": {"en": "Subclasses", "fr": "Sous-Classes", "es": "todo"},
    "beastform description": {"en": "Description", "fr": "Description", "es": "todo"},
    "beastform options": {"en": "Options", "fr": "Options", "es": "todo"},
    "beastform adv": {"en": "Gain advantage on", "fr": "Avantagé sur ", "es": "todo"},
    "beastform sub": {"en": "DRUID BEASTFORM", "fr": "FORME BESTIALE DU DRUIDE", "es": "todo"},

    "ppage copyright": {"en": "This product includes materials from the Daggerheart System Reference Document 1.0, ©Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others.", 
                  "fr": "This product includes materials from the Daggerheart System Reference Document 1.0, ©Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others.", 
                  "es": "This product includes materials from the Daggerheart System Reference Document 1.0, ©Critical Role, LLC. under the terms of the Darrington Press Community Gaming (DPCGL) License. More information can be found at https://www.daggerheart.com. There are no previous modifications by others."},
    "ppage logo": {"en": "Darrington Press™ and the Darrington Press authorized work logo are trademarks of Critical Role, LLC and used with permission.", 
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

