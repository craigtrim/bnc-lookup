# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""n't contractions should return bucket based on stem, not ghost entry.

Ghost entries give buckets like 11-88; stems are all bucket 1.
The fix should prefer the contraction-split result (max of stem
and suffix buckets) when it indicates higher frequency.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestNtContractionBuckets:

    def test_dont_bucket(self):
        assert bnc.bucket("don't") == 1

    def test_cant_bucket(self):
        assert bnc.bucket("can't") == 1

    def test_wont_bucket(self):
        assert bnc.bucket("won't") == 1

    def test_couldnt_bucket(self):
        assert bnc.bucket("couldn't") == 1

    def test_didnt_bucket(self):
        assert bnc.bucket("didn't") == 1

    def test_isnt_bucket(self):
        assert bnc.bucket("isn't") == 1

    def test_arent_bucket(self):
        assert bnc.bucket("aren't") == 1

    def test_havent_bucket(self):
        assert bnc.bucket("haven't") == 1

    def test_doesnt_bucket(self):
        assert bnc.bucket("doesn't") == 1

    def test_hasnt_bucket(self):
        assert bnc.bucket("hasn't") == 1

    def test_wouldnt_bucket(self):
        assert bnc.bucket("wouldn't") == 1

    def test_shouldnt_bucket(self):
        assert bnc.bucket("shouldn't") == 1

    def test_wasnt_bucket(self):
        assert bnc.bucket("wasn't") == 1

    def test_werent_bucket(self):
        assert bnc.bucket("weren't") == 1

    def test_neednt_bucket(self):
        assert bnc.bucket("needn't") == 1
