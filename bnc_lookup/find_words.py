# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Reverse lookup: retrieve words by frequency bucket.

Provides the inverse of find_freq.py: given a bucket number (1-100),
returns all words assigned to that bucket. Words are stored as sorted
tuples in 100 files (bw_01.py through bw_100.py), one per bucket.

Supports random sampling for applications that need representative
words from a frequency tier without loading the full list.
"""

import importlib
import random

_cache = {}


def _get_bucket_words(bucket: int) -> tuple:
    """Load and cache the word tuple for a given bucket number.

    Args:
        bucket: Bucket number (1-100).

    Returns:
        Tuple of words in that bucket, sorted alphabetically.
    """
    if bucket not in _cache:
        module = importlib.import_module(f'bnc_lookup.bw.bw_{bucket:02d}')
        _cache[bucket] = getattr(module, f'words_{bucket:02d}')
    return _cache[bucket]


class FindWords:
    """Reverse lookup from frequency bucket to word list.

    Each bucket contains ~6,694 words sorted alphabetically. Bucket 1
    holds the most frequent words, bucket 100 the least frequent.
    """

    def __init__(self):
        pass

    def by_bucket(self, bucket: int) -> tuple:
        """Get all words in a frequency bucket.

        Args:
            bucket: Bucket number 1-100 (1=most frequent, 100=least frequent).

        Returns:
            Tuple of words in that bucket (alphabetically sorted).

        Raises:
            ValueError: If bucket is not in range 1-100.
        """
        if not 1 <= bucket <= 100:
            raise ValueError(f'Bucket must be 1-100, got {bucket}')
        return _get_bucket_words(bucket)

    def sample(self, bucket: int, n: int = 10) -> list:
        """Get random sample of words from a bucket.

        Args:
            bucket: Bucket number 1-100.
            n: Number of words to return (default 10). Clamped to bucket size.

        Returns:
            List of randomly sampled words from the bucket.

        Raises:
            ValueError: If bucket is not in range 1-100.
        """
        words = self.by_bucket(bucket)
        n = min(n, len(words))
        return random.sample(words, n)
