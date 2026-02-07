# !/usr/bin/env python
# -*- coding: UTF-8 -*-
"""exists() should continue to return True for all contractions.

Related GitHub Issue:
    #9 - Contraction frequency data is wrong
    https://github.com/craigtrim/bnc-lookup/issues/9
"""

import bnc_lookup as bnc


class TestExistsUnchanged:

    def test_dont_exists(self):
        assert bnc.exists("don't") is True

    def test_cant_exists(self):
        assert bnc.exists("can't") is True

    def test_its_exists(self):
        assert bnc.exists("it's") is True

    def test_hes_exists(self):
        assert bnc.exists("he's") is True

    def test_well_exists(self):
        assert bnc.exists("we'll") is True

    def test_youre_exists(self):
        assert bnc.exists("you're") is True

    def test_im_exists(self):
        assert bnc.exists("i'm") is True

    def test_hed_exists(self):
        assert bnc.exists("he'd") is True
