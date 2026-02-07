# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Word existence checking against the British National Corpus.

Uses MD5-based hash distribution across 256 bucket files for O(1) lookup.
Each word is hashed, and the first 2 hex characters of the hash determine
which bucket file (h_00.py through h_ff.py) contains the hash suffix.
Bucket files are lazy-loaded on first access and cached in memory.

Includes automatic plural fallback: if a word ending in 's' is not found,
the singular form (with trailing 's' removed) is also checked.

Includes contraction fallback: if a contraction like "we'll" is not found,
the components ("we" and "'ll") are checked separately. This accounts for
the BNC's tokenization of contractions into separate parts.
"""

import hashlib
import importlib

from bnc_lookup.normalize import normalize

_cache = {}

# Contraction suffixes stored as separate tokens in the BNC corpus
# Order matters: longer suffixes must be checked before shorter ones
CONTRACTION_SUFFIXES = ("n't", "'ll", "'re", "'ve", "'m", "'d", "'s")

# Stems where 's is a contraction (is/has), not a possessive.
# "dog's" = possessive (no split), "it's" = "it is" (split).
S_CONTRACTION_STEMS = frozenset({
    'it', 'he', 'she', 'that', 'what', 'there', 'here', 'where',
    'who', 'how', 'everybody', 'everyone', 'everything', 'nobody',
    'nothing', 'someone', 'something', 'let', 'one',
})


def _get_hash_set(prefix: str) -> frozenset:
    """Load and cache the hash suffix frozenset for a given 2-char hex prefix.

    Args:
        prefix: Two-character hex string (e.g., '5d') identifying the bucket file.

    Returns:
        Frozenset of 30-character MD5 hash suffixes for words in this bucket.
    """
    if prefix not in _cache:
        module = importlib.import_module(f'bnc_lookup.hs.h_{prefix}')
        _cache[prefix] = getattr(module, f'hashes_{prefix}')
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


def _hash_exists(input_text: str) -> bool:
    """Check whether a word's hash suffix exists in its corresponding bucket.

    Args:
        input_text: The word to look up (should already be normalized).

    Returns:
        True if the word's hash suffix is found in its bucket frozenset.
    """
    if not input_text:
        return False
    h = _calculate_md5(input_text)
    prefix, suffix = h[:2], h[2:]
    try:
        return suffix in _get_hash_set(prefix)
    except ModuleNotFoundError:
        return False


def _split_contraction(word: str) -> tuple[str, str] | None:
    """Split a contraction into its component parts if possible.

    The BNC tokenizes contractions separately (e.g., "we'll" → "we" + "'ll").
    This function reverses that split for fallback lookup.

    Args:
        word: A normalized word that may be a contraction.

    Returns:
        Tuple of (stem, suffix) if the word matches a contraction pattern,
        or None if no contraction pattern matches.

    Examples:
        >>> _split_contraction("we'll")
        ("we", "'ll")
        >>> _split_contraction("don't")
        ("do", "n't")
        >>> _split_contraction("hello")
        None
    """
    for suffix in CONTRACTION_SUFFIXES:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if not stem:
                continue
            # For 's, only split if stem is a known contraction (not possessive)
            if suffix == "'s" and stem not in S_CONTRACTION_STEMS:
                continue
            return (stem, suffix)
    return None


class FindBnc:
    """O(1) word existence checker against 669,417 BNC word forms.

    Lookup flow:
        1. Normalize input to lowercase
        2. Compute MD5 hash
        3. Use first 2 hex chars as bucket prefix, remaining 30 as suffix
        4. Check suffix membership in the bucket's frozenset
        5. If not found and word ends with 's', retry with singular form
    """

    def __init__(self):
        pass

    def exists(self, input_text: str) -> bool:
        """Check if a word exists in the BNC corpus.

        Performs case-insensitive lookup with automatic fallbacks:
        1. Direct lookup of the normalized word
        2. Plural fallback: if word ends with 's' (length > 3), try singular
        3. Contraction fallback: if word is a contraction, check if both
           components exist (e.g., "we'll" → "we" + "'ll")

        Args:
            input_text: The word to check.

        Returns:
            True if the word exists in the BNC (directly or via fallback).
        """
        input_text = normalize(input_text)

        if _hash_exists(input_text):
            return True

        if input_text.endswith('s') and len(input_text) > 3:
            if _hash_exists(input_text[:-1]):
                return True

        # Contraction fallback: check if both parts exist separately
        parts = _split_contraction(input_text)
        if parts:
            stem, suffix = parts
            if _hash_exists(stem) and _hash_exists(suffix):
                return True

        return False
