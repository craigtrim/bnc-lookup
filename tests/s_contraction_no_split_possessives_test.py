# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Possessive 's should NOT be split (stems not in allowlist).

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

from bnc_lookup.find_bnc import _split_contraction


class TestSContractionNoSplitPossessives:

    def test_dogs_no_split(self):
        result = _split_contraction("dog's")
        assert result is None

    def test_cats_no_split(self):
        result = _split_contraction("cat's")
        assert result is None

    def test_johns_no_split(self):
        result = _split_contraction("john's")
        assert result is None

    def test_mans_no_split(self):
        result = _split_contraction("man's")
        assert result is None

    def test_worlds_no_split(self):
        result = _split_contraction("world's")
        assert result is None

    def test_childs_no_split(self):
        result = _split_contraction("child's")
        assert result is None
