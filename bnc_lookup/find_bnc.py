# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Facade to find BNC Data on Disk """

import hashlib
import importlib

_cache = {}


def _get_hash_set(prefix: str) -> frozenset:
    if prefix not in _cache:
        module = importlib.import_module(f'bnc_lookup.hs.h_{prefix}')
        _cache[prefix] = getattr(module, f'hashes_{prefix}')
    return _cache[prefix]


def _calculate_md5(input_text: str) -> str:
    return hashlib.md5(input_text.lower().strip().encode()).hexdigest()


def _hash_exists(input_text: str) -> bool:
    if not input_text:
        return False
    h = _calculate_md5(input_text)
    prefix, suffix = h[:2], h[2:]
    try:
        return suffix in _get_hash_set(prefix)
    except ModuleNotFoundError:
        return False


class FindBnc:
    """ Facade to find BNC Data on Disk """

    def __init__(self):
        pass

    def exists(self, input_text: str) -> bool:
        input_text = input_text.lower().strip()

        if _hash_exists(input_text):
            return True

        if input_text.endswith('s') and len(input_text) > 3:
            if _hash_exists(input_text[:-1]):
                return True

        return False
