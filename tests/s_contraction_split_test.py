# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""_split_contraction() should handle 's for allowlisted stems.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

from bnc_lookup.find_bnc import _split_contraction


class TestSContractionSplit:

    def test_its_splits(self):
        result = _split_contraction("it's")
        assert result is not None

    def test_hes_splits(self):
        result = _split_contraction("he's")
        assert result is not None

    def test_shes_splits(self):
        result = _split_contraction("she's")
        assert result is not None

    def test_thats_splits(self):
        result = _split_contraction("that's")
        assert result is not None

    def test_whats_splits(self):
        result = _split_contraction("what's")
        assert result is not None

    def test_theres_splits(self):
        result = _split_contraction("there's")
        assert result is not None

    def test_heres_splits(self):
        result = _split_contraction("here's")
        assert result is not None

    def test_wheres_splits(self):
        result = _split_contraction("where's")
        assert result is not None

    def test_whos_splits(self):
        result = _split_contraction("who's")
        assert result is not None

    def test_hows_splits(self):
        result = _split_contraction("how's")
        assert result is not None

    def test_lets_splits(self):
        result = _split_contraction("let's")
        assert result is not None

    def test_ones_splits(self):
        result = _split_contraction("one's")
        assert result is not None

    def test_everybodys_splits(self):
        result = _split_contraction("everybody's")
        assert result is not None

    def test_everyones_splits(self):
        result = _split_contraction("everyone's")
        assert result is not None

    def test_everythings_splits(self):
        result = _split_contraction("everything's")
        assert result is not None

    def test_nobodys_splits(self):
        result = _split_contraction("nobody's")
        assert result is not None

    def test_nothings_splits(self):
        result = _split_contraction("nothing's")
        assert result is not None

    def test_someones_splits(self):
        result = _split_contraction("someone's")
        assert result is not None

    def test_somethings_splits(self):
        result = _split_contraction("something's")
        assert result is not None
