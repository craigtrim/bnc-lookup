# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Other contractions ('ll, 're, 've, 'm, 'd) should prefer stem-based RF.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestOtherContractionRF:

    def test_well_rf(self):
        rf = bnc.relative_frequency("we'll")
        assert rf is not None
        assert rf > 1e-04

    def test_youre_rf(self):
        rf = bnc.relative_frequency("you're")
        assert rf is not None
        assert rf > 1e-04

    def test_weve_rf(self):
        rf = bnc.relative_frequency("we've")
        assert rf is not None
        assert rf > 1e-04

    def test_im_rf(self):
        rf = bnc.relative_frequency("i'm")
        assert rf is not None
        assert rf > 1e-04
