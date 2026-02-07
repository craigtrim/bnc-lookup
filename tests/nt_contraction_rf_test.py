# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""n't contractions should return RF based on stem, not ghost entry.

Ghost entries give RF ~1e-08; stems give RF ~1e-03 or higher.
The fix should prefer the contraction-split result (min of stem
and suffix RFs) when it indicates higher frequency.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestNtContractionRF:

    def test_dont_rf_above_ghost(self):
        rf = bnc.relative_frequency("don't")
        assert rf is not None
        assert rf > 1e-04

    def test_cant_rf_above_ghost(self):
        rf = bnc.relative_frequency("can't")
        assert rf is not None
        assert rf > 1e-04

    def test_wont_rf_above_ghost(self):
        rf = bnc.relative_frequency("won't")
        assert rf is not None
        assert rf > 1e-05

    def test_couldnt_rf_above_ghost(self):
        rf = bnc.relative_frequency("couldn't")
        assert rf is not None
        assert rf > 1e-04

    def test_didnt_rf_above_ghost(self):
        rf = bnc.relative_frequency("didn't")
        assert rf is not None
        assert rf > 1e-04

    def test_isnt_rf_above_ghost(self):
        rf = bnc.relative_frequency("isn't")
        assert rf is not None
        assert rf > 1e-04

    def test_arent_rf_above_ghost(self):
        rf = bnc.relative_frequency("aren't")
        assert rf is not None
        assert rf > 1e-04

    def test_havent_rf_above_ghost(self):
        rf = bnc.relative_frequency("haven't")
        assert rf is not None
        assert rf > 1e-04

    def test_doesnt_rf_above_ghost(self):
        rf = bnc.relative_frequency("doesn't")
        assert rf is not None
        assert rf > 1e-04

    def test_hasnt_rf_above_ghost(self):
        rf = bnc.relative_frequency("hasn't")
        assert rf is not None
        assert rf > 1e-04
