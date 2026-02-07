# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""'s contractions (allowlisted) should get stem-based RF.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestSContractionRF:

    def test_its_rf_above_ghost(self):
        rf = bnc.relative_frequency("it's")
        assert rf is not None
        assert rf > 1e-04

    def test_hes_rf_above_ghost(self):
        rf = bnc.relative_frequency("he's")
        assert rf is not None
        assert rf > 1e-04

    def test_thats_rf_above_ghost(self):
        rf = bnc.relative_frequency("that's")
        assert rf is not None
        assert rf > 1e-04

    def test_whats_rf_above_ghost(self):
        rf = bnc.relative_frequency("what's")
        assert rf is not None
        assert rf > 1e-04

    def test_theres_rf_above_ghost(self):
        rf = bnc.relative_frequency("there's")
        assert rf is not None
        assert rf > 1e-04
