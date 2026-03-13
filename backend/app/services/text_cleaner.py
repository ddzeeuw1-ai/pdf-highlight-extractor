"""
Text cleaning utilities for PDF highlight extraction.
Fixes common issues introduced by PDF encoding: ligatures, merged words,
missing spaces after punctuation.
"""

import re
import unicodedata

# Common PDF ligature characters and their plain-text replacements
LIGATURES: dict[str, str] = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\ufb05": "st",
    "\ufb06": "st",
    "\u0192": "f",   # latin small f with hook, used as ligature in some fonts
}


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text:
    1. Replace ligature unicode characters with ASCII equivalents
    2. NFC-normalize unicode (fixes decomposed accented characters)
    3. Insert missing spaces between merged words
    4. Collapse duplicate spaces
    """
    # 1. Replace ligatures
    for char, replacement in LIGATURES.items():
        text = text.replace(char, replacement)

    # 2. Normalize unicode
    text = unicodedata.normalize("NFC", text)

    # 3. Insert space between lowercase→uppercase merges (e.g. "wordWord")
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

    # 4. Insert space after sentence-ending punctuation with no space
    text = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", text)

    # 5. Insert space after comma/semicolon/colon with no space
    text = re.sub(r"([,;:])([A-Za-z])", r"\1 \2", text)

    # 6. Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)

    return text.strip()
