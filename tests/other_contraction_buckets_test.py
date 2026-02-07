# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Other contractions ('ll, 're, 've, 'm, 'd) should prefer stem-based frequency.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestOtherContractionBuckets:

    def test_well_bucket(self):
        assert bnc.bucket("we'll") == 1

    def test_youll_bucket(self):
        assert bnc.bucket("you'll") == 1

    def test_theyll_bucket(self):
        assert bnc.bucket("they'll") == 1

    def test_were_bucket(self):
        assert bnc.bucket("we're") == 1

    def test_youre_bucket(self):
        assert bnc.bucket("you're") == 1

    def test_theyre_bucket(self):
        assert bnc.bucket("they're") == 1

    def test_weve_bucket(self):
        assert bnc.bucket("we've") == 1

    def test_youve_bucket(self):
        assert bnc.bucket("you've") == 1

    def test_theyve_bucket(self):
        assert bnc.bucket("they've") == 1

    def test_im_bucket(self):
        assert bnc.bucket("i'm") == 1

    def test_hed_bucket(self):
        assert bnc.bucket("he'd") == 1

    def test_shed_bucket(self):
        assert bnc.bucket("she'd") == 1

    def test_theyd_bucket(self):
        assert bnc.bucket("they'd") == 1

    def test_youd_bucket(self):
        assert bnc.bucket("you'd") == 1

    def test_wed_bucket(self):
        assert bnc.bucket("we'd") == 1

    def test_id_bucket(self):
        assert bnc.bucket("i'd") == 1
