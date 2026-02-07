# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Contractions with curly/smart quotes should also get correct frequency.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestSmartQuoteContractions:

    def test_dont_smart_quote_bucket(self):
        assert bnc.bucket('don\u2019t') == 1

    def test_its_smart_quote_bucket(self):
        assert bnc.bucket('it\u2019s') == 1

    def test_well_smart_quote_bucket(self):
        assert bnc.bucket('we\u2019ll') == 1

    def test_dont_smart_quote_rf(self):
        rf = bnc.relative_frequency('don\u2019t')
        assert rf is not None
        assert rf > 1e-04
