# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""'s contractions (allowlisted) should get stem-based bucket.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestSContractionBuckets:

    def test_its_bucket(self):
        assert bnc.bucket("it's") == 1

    def test_hes_bucket(self):
        assert bnc.bucket("he's") == 1

    def test_shes_bucket(self):
        assert bnc.bucket("she's") == 1

    def test_thats_bucket(self):
        assert bnc.bucket("that's") == 1

    def test_whats_bucket(self):
        assert bnc.bucket("what's") == 1

    def test_theres_bucket(self):
        assert bnc.bucket("there's") == 1

    def test_lets_bucket(self):
        assert bnc.bucket("let's") == 1
