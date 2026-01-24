# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Lookup frequency bucket for BNC words """

import hashlib
import importlib

_cache = {}


def _get_bucket_dict(prefix: str) -> dict:
    if prefix not in _cache:
        module = importlib.import_module(f'bnc_lookup.freq.f_{prefix}')
        _cache[prefix] = getattr(module, f'buckets_{prefix}')
    return _cache[prefix]


def _calculate_md5(input_text: str) -> str:
    return hashlib.md5(input_text.lower().strip().encode()).hexdigest()


def _lookup_bucket(input_text: str) -> int | None:
    if not input_text:
        return None
    h = _calculate_md5(input_text)
    prefix, suffix = h[:2], h[2:]
    try:
        return _get_bucket_dict(prefix).get(suffix)
    except ModuleNotFoundError:
        return None


class FindFreq:
    """ Lookup frequency bucket for BNC words """

    def __init__(self):
        pass

    def bucket(self, input_text: str) -> int | None:
        """
        Get frequency bucket for a word.

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
