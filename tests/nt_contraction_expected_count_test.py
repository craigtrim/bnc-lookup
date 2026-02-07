# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Expected counts for n't contractions should reflect stem frequency.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestNtContractionExpectedCount:

    def test_dont_ec_50k(self):
        ec = bnc.expected_count("don't", 50000)
        assert ec is not None
        assert ec > 1.0

    def test_cant_ec_50k(self):
        ec = bnc.expected_count("can't", 50000)
        assert ec is not None
        assert ec > 1.0

    def test_arent_ec_50k(self):
        ec = bnc.expected_count("aren't", 50000)
        assert ec is not None
        assert ec > 1.0

    def test_dont_ec_rounded(self):
        ec = bnc.expected_count("don't", 50000, rounded=True)
        assert ec is not None
        assert ec >= 1
