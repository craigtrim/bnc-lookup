# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Text normalization utilities for BNC lookup.

Handles normalization of Unicode apostrophe variants, accented characters,
and other text transformations to ensure consistent matching against the
BNC corpus (which uses ASCII-only word forms).

Related GitHub Issue:
    #8 - Normalize unicode accents before lookup
    https://github.com/craigtrim/bnc-lookup/issues/8
"""

import unicodedata

# Unicode characters that should normalize to ASCII apostrophe (U+0027)
# Ordered by likelihood of occurrence in English text
APOSTROPHE_VARIANTS = (
    '\u2019'  # RIGHT SINGLE QUOTATION MARK (most common smart quote)
    '\u2018'  # LEFT SINGLE QUOTATION MARK
    '\u0060'  # GRAVE ACCENT
    '\u00B4'  # ACUTE ACCENT
    '\u201B'  # SINGLE HIGH-REVERSED-9 QUOTATION MARK
    '\u2032'  # PRIME
    '\u2035'  # REVERSED PRIME
    '\u02B9'  # MODIFIER LETTER PRIME
    '\u02BC'  # MODIFIER LETTER APOSTROPHE
    '\u02C8'  # MODIFIER LETTER VERTICAL LINE
    '\u0313'  # COMBINING COMMA ABOVE
    '\u0315'  # COMBINING COMMA ABOVE RIGHT
    '\u055A'  # ARMENIAN APOSTROPHE
    '\u05F3'  # HEBREW PUNCTUATION GERESH
    '\u07F4'  # NKO HIGH TONE APOSTROPHE
    '\u07F5'  # NKO LOW TONE APOSTROPHE
    '\uFF07'  # FULLWIDTH APOSTROPHE
    '\u1FBF'  # GREEK PSILI
    '\u1FBD'  # GREEK KORONIS
    '\uA78C'  # LATIN SMALL LETTER SALTILLO
)

# Pre-compiled translation table for fast apostrophe normalization
_APOSTROPHE_TABLE = str.maketrans({char: "'" for char in APOSTROPHE_VARIANTS})


def normalize_apostrophes(text: str) -> str:
    """Normalize Unicode apostrophe variants to ASCII apostrophe.

    Converts curly quotes, prime marks, and other apostrophe-like
    characters to the standard ASCII apostrophe (U+0027) used in
    the BNC corpus data.

    Args:
        text: Input text potentially containing Unicode apostrophes.

    Returns:
        Text with all apostrophe variants converted to ASCII apostrophe.
    """
    return text.translate(_APOSTROPHE_TABLE)


def normalize_unicode_accents(text: str) -> str:
    """Strip Unicode accents and diacritics, keeping ASCII base characters.

    Applies NFKD normalization to decompose characters into base + combining
    marks, then encodes to ASCII (dropping combining marks). This ensures
    that accented variants like "protégé" match their ASCII form "protege"
    in the BNC corpus.

    Args:
        text: Input text potentially containing accented characters.

    Returns:
        Text with accents stripped (non-Latin characters are dropped).

    Examples:
        >>> normalize_unicode_accents('café')
        'cafe'
        >>> normalize_unicode_accents('protégé')
        'protege'
        >>> normalize_unicode_accents('naïve')
        'naive'
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


def normalize(text: str) -> str:
    """Normalize text for BNC lookup.

    Applies all normalization steps in order:
    1. Convert apostrophe variants to ASCII
    2. Strip Unicode accents/diacritics to ASCII
    3. Convert to lowercase
    4. Strip leading/trailing whitespace

    Apostrophe normalization runs first so that apostrophe-like characters
    (e.g., U+2019 RIGHT SINGLE QUOTATION MARK) are preserved as ASCII
    apostrophes before the accent-stripping step encodes to ASCII.

    Args:
        text: Input text to normalize.

    Returns:
        Normalized text ready for BNC lookup.
    """
    text = normalize_apostrophes(text)
    text = normalize_unicode_accents(text)
    return text.lower().strip()
