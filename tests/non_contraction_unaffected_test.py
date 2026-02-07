# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Regular words should return the same results as before.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestNonContractionUnaffected:

    def test_the_bucket(self):
        assert bnc.bucket('the') == 1

    def test_hello_bucket(self):
        b = bnc.bucket('hello')
        assert b is not None
        assert b > 0

    def test_the_rf(self):
        rf = bnc.relative_frequency('the')
        assert rf is not None
        assert rf > 0.01

    def test_nonexistent_word(self):
        assert bnc.bucket('xyzzyplugh') is None
        assert bnc.relative_frequency('xyzzyplugh') is None
