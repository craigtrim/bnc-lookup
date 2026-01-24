# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Retrieve words by frequency bucket """

import importlib
import random

_cache = {}


def _get_bucket_words(bucket: int) -> tuple:
    if bucket not in _cache:
        module = importlib.import_module(f'bnc_lookup.bw.bw_{bucket:02d}')
        _cache[bucket] = getattr(module, f'words_{bucket:02d}')
    return _cache[bucket]


class FindWords:
    """ Retrieve words by frequency bucket """

    def __init__(self):
        pass

    def by_bucket(self, bucket: int) -> tuple:
        """
        Get all words in a frequency bucket.

        Args:
            bucket: Bucket number 1-100 (1=most frequent, 100=least frequent)

        Returns:
            Tuple of words in that bucket (alphabetically sorted)
        """
        if not 1 <= bucket <= 100:
            raise ValueError(f'Bucket must be 1-100, got {bucket}')
        return _get_bucket_words(bucket)

    def sample(self, bucket: int, n: int = 10) -> list:
        """
        Get random sample of words from a bucket.

        Args:
            bucket: Bucket number 1-100
            n: Number of words to return (default 10)

        Returns:
            List of randomly sampled words
        """
        words = self.by_bucket(bucket)
        n = min(n, len(words))
        return random.sample(words, n)
