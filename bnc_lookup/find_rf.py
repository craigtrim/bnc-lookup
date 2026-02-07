# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Relative frequency lookup for BNC words.

Provides per-word relative frequency (raw_count / corpus_size) for
quantitative frequency analysis. Unlike the bucket() function which
returns a coarse ordinal tier (1-100), relative_frequency() returns
the precise proportion of the corpus occupied by each word.

The BNC corpus contains 100,106,029 tokens across 4,124 documents.

Uses the same MD5-based hash distribution as find_bnc.py, but stores
relative frequency floats. Each of the 256 bucket files (rf_00.py
through rf_ff.py) maps hash suffixes to relative frequency values.
"""

import hashlib
import importlib

from bnc_lookup.normalize import normalize
from bnc_lookup.find_bnc import _split_contraction

_cache = {}


def _get_rf_dict(prefix: str) -> dict:
    """Load and cache the relative frequency dictionary for a given 2-char hex prefix.

    Args:
        prefix: Two-character hex string (e.g., '5d') identifying the bucket file.

    Returns:
        Dictionary mapping 30-character MD5 hash suffixes to relative frequency floats.
    """
    if prefix not in _cache:
        module = importlib.import_module(f'bnc_lookup.rf.rf_{prefix}')
        _cache[prefix] = getattr(module, f'frequencies_{prefix}')
    return _cache[prefix]


def _calculate_md5(input_text: str) -> str:
    """Compute the MD5 hex digest of a normalized word.

    Normalization includes apostrophe variant conversion, lowercase,
    and whitespace stripping.

    Args:
        input_text: The word to hash.

    Returns:
        32-character hexadecimal MD5 digest string.
    """
    return hashlib.md5(normalize(input_text).encode()).hexdigest()


def _lookup_rf(input_text: str) -> float | None:
    """Look up the relative frequency for a single word form.

    Args:
        input_text: The word to look up (should already be normalized).

    Returns:
        Relative frequency as a float in (0, 1) if found, None otherwise.
    """
    if not input_text:
        return None
    h = _calculate_md5(input_text)
    prefix, suffix = h[:2], h[2:]
    try:
        return _get_rf_dict(prefix).get(suffix)
    except ModuleNotFoundError:
        return None


class FindRF:
    """O(1) relative frequency lookup for BNC words.

    Provides precise per-word frequency data derived from the BNC corpus
    (100,106,029 tokens). Supports computing expected occurrence counts
    for any target text length.

    Includes automatic plural fallback: if a word ending in 's' is not
    found, the singular form is also checked.
    """

    def __init__(self):
        pass

    def relative_frequency(self, input_text: str) -> float | None:
        """Relative frequency of word in BNC (raw_count / corpus_size).

        Performs case-insensitive lookup with automatic plural fallback.

        Args:
            input_text: The word to look up.

        Returns:
            Float in range (0, 1), or None if word not in BNC.
        """
        input_text = normalize(input_text)

        direct = _lookup_rf(input_text)

        # Contraction split: prefer higher frequency
        parts = _split_contraction(input_text)
        if parts:
            stem, suffix = parts
            stem_rf = _lookup_rf(stem)
            suffix_rf = _lookup_rf(suffix)
            if stem_rf is not None and suffix_rf is not None:
                split_rf = min(stem_rf, suffix_rf)
                if direct is None or split_rf > direct:
                    return split_rf

        if direct is not None:
            return direct

        # Try singular form if plural
        if input_text.endswith('s') and len(input_text) > 3:
            result = _lookup_rf(input_text[:-1])
            if result is not None:
                return result

        return None

    def expected_count(self, input_text: str, text_length: int, rounded: bool = False) -> float | int | None:
        """Expected number of occurrences of a word in a text of given length.

        Computes ``relative_frequency(word) * text_length`` to estimate how
        many times a word would appear in a text of the given token count,
        assuming BNC-like frequency distribution.

        Args:
            input_text: The word to look up.
            text_length: Length of the target text in tokens.
            rounded: If True, return a rounded integer (e.g., 0.04 -> 0, 3090.7 -> 3091).

        Returns:
            Expected count as a float (or int if rounded), or None if word not in BNC.
        """
        rf = self.relative_frequency(input_text)
        if rf is None:
            return None
        result = rf * text_length
        if rounded:
            return round(result)
        return result
