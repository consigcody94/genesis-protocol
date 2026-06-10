"""
Shared Hebrew alphabet constants.

Single source of truth for the Base-22 digit mapping used across the
toolkit. The 22-letter alphabet maps Aleph=0 through Tav=21; the five
final (sofit) letterforms fold into their base letters so that every
consonant in the Masoretic canon gets a digit.
"""

ALPHABET = "אבגדהוזחטיכלמנסעפצקרשת"  # Aleph=0 .. Tav=21

SOFIT_MAP = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}


def build_char_map():
    """Base-22 digit map covering the 22 base letters and 5 final forms."""
    char_map = {char: i for i, char in enumerate(ALPHABET)}
    for sofit, base in SOFIT_MAP.items():
        char_map[sofit] = char_map[base]
    return char_map
