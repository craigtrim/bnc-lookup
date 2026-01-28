# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Frequency bucket lookup for BNC words.

Maps each word to a frequency bucket (1-100) based on its rank in the
BNC corpus. Bucket 1 contains the top 1% most frequent words (~6,694 words),
bucket 100 contains the bottom 1%.

Uses the same MD5-based hash distribution as find_bnc.py, but stores
bucket assignments (int) instead of existence flags. Each of the 256
bucket files (f_00.py through f_ff.py) maps hash suffixes to bucket numbers.
"""

import hashlib
import importlib

_cache = {}


def _get_bucket_dict(prefix: str) -> dict:
    """Load and cache the bucket dictionary for a given 2-char hex prefix.

    Args:
        prefix: Two-character hex string (e.g., '5d') identifying the bucket file.

    Returns:
        Dictionary mapping 30-character MD5 hash suffixes to bucket numbers (1-100).
    """
    if prefix not in _cache:
        module = importlib.import_module(f'bnc_lookup.freq.f_{prefix}')
        _cache[prefix] = getattr(module, f'buckets_{prefix}')
    return _cache[prefix]


def _calculate_md5(input_text: str) -> str:
    """Compute the MD5 hex digest of a normalized (lowercase, stripped) word.

    Args:
        input_text: The word to hash.

    Returns:
        32-character hexadecimal MD5 digest string.
    """
    return hashlib.md5(input_text.lower().strip().encode()).hexdigest()


def _lookup_bucket(input_text: str) -> int | None:
    """Look up the frequency bucket for a single word form.

    Args:
        input_text: The word to look up (should already be normalized).

    Returns:
        Bucket number (1-100) if found, None otherwise.
    """
    if not input_text:
        return None
    h = _calculate_md5(input_text)
    prefix, suffix = h[:2], h[2:]
    try:
        return _get_bucket_dict(prefix).get(suffix)
    except ModuleNotFoundError:
        return None


class FindFreq:
    """O(1) frequency bucket lookup for BNC words.

    Words are ranked by corpus frequency and divided into 100 equal-sized
    buckets. Bucket 1 = most frequent (the, of, and, ...), bucket 100 =
    least frequent.

    Includes automatic plural fallback: if a word ending in 's' is not
    found, the singular form is also checked.
    """

    def __init__(self):
        pass

    def bucket(self, input_text: str) -> int | None:
        """Get frequency bucket for a word.

        Performs case-insensitive lookup with automatic plural fallback.

        Args:
            input_text: The word to look up.

        Returns:
            1-100: Bucket number (1=most frequent, 100=least frequent)
            None: Word not found in BNC
        """
        input_text = input_text.lower().strip()

        result = _lookup_bucket(input_text)
        if result is not None:
            return result

        # Try singular form if plural
        if input_text.endswith('s') and len(input_text) > 3:
            result = _lookup_bucket(input_text[:-1])
            if result is not None:
                return result

        return None
