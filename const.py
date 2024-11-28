import json

KEY_SPACE = "clube_dos_tampinha"

with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

LANGUAGE_MAP = {"English": "en", "Português": "pt-br"}
