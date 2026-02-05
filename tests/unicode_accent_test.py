"""Tests for unicode accent normalization (issue #8).

Words with accented characters (e.g., protégé, phaéton, outré) should match
their ASCII-normalized equivalents in the BNC corpus. The original accented
form is preserved in output — only the lookup normalizes.

Related GitHub Issue:
    #8 - Normalize unicode accents before lookup
    https://github.com/craigtrim/bnc-lookup/issues/8
"""

import bnc_lookup as bnc
from bnc_lookup.normalize import normalize, normalize_unicode_accents


# ========================================================================
# Known affected words from issue #8
# ========================================================================

class TestIssue8KnownAffectedExists:
    """Verify exists() works for the three words cited in issue #8."""

    def test_protege_accented(self):
        assert bnc.exists('protégé') is True

    def test_phaeton_accented(self):
        assert bnc.exists('phaéton') is True

    def test_outre_accented(self):
        assert bnc.exists('outré') is True


class TestIssue8KnownAffectedBucket:
    """Verify bucket() returns correct values for issue #8 words."""

    def test_protege_bucket_matches(self):
        assert bnc.bucket('protégé') == bnc.bucket('protege')

    def test_phaeton_bucket_matches(self):
        assert bnc.bucket('phaéton') == bnc.bucket('phaeton')

    def test_outre_bucket_matches(self):
        assert bnc.bucket('outré') == bnc.bucket('outre')


class TestIssue8KnownAffectedRelativeFrequency:
    """Verify relative_frequency() works for issue #8 words."""

    def test_protege_rf_matches(self):
        assert bnc.relative_frequency(
            'protégé') == bnc.relative_frequency('protege')

    def test_phaeton_rf_matches(self):
        assert bnc.relative_frequency(
            'phaéton') == bnc.relative_frequency('phaeton')

    def test_outre_rf_matches(self):
        assert bnc.relative_frequency(
            'outré') == bnc.relative_frequency('outre')


class TestIssue8KnownAffectedExpectedCount:
    """Verify expected_count() works for issue #8 words."""

    def test_protege_ec_matches(self):
        assert bnc.expected_count(
            'protégé', 50000) == bnc.expected_count('protege', 50000)

    def test_phaeton_ec_matches(self):
        assert bnc.expected_count(
            'phaéton', 50000) == bnc.expected_count('phaeton', 50000)

    def test_outre_ec_matches(self):
        assert bnc.expected_count(
            'outré', 50000) == bnc.expected_count('outre', 50000)

    def test_protege_ec_rounded_matches(self):
        assert bnc.expected_count('protégé', 50000, rounded=True) == bnc.expected_count(
            'protege', 50000, rounded=True)

    def test_phaeton_ec_rounded_matches(self):
        assert bnc.expected_count('phaéton', 50000, rounded=True) == bnc.expected_count(
            'phaeton', 50000, rounded=True)

    def test_outre_ec_rounded_matches(self):
        assert bnc.expected_count('outré', 50000, rounded=True) == bnc.expected_count(
            'outre', 50000, rounded=True)


# ========================================================================
# Additional accented words known to exist in BNC (ASCII form)
# ========================================================================

class TestAdditionalAccentedWordsExists:
    """Additional accented words that should match ASCII forms in BNC."""

    def test_cafe_accented(self):
        assert bnc.exists('café') is True

    def test_resume_accented(self):
        assert bnc.exists('résumé') is True

    def test_naive_accented(self):
        assert bnc.exists('naïve') is True

    def test_cliche_accented(self):
        assert bnc.exists('cliché') is True


class TestAdditionalAccentedWordsBucket:
    """Additional accented words should produce same buckets as ASCII."""

    def test_cafe_bucket(self):
        assert bnc.bucket('café') == bnc.bucket('cafe')

    def test_resume_bucket(self):
        assert bnc.bucket('résumé') == bnc.bucket('resume')

    def test_naive_bucket(self):
        assert bnc.bucket('naïve') == bnc.bucket('naive')

    def test_cliche_bucket(self):
        assert bnc.bucket('cliché') == bnc.bucket('cliche')


class TestAdditionalAccentedWordsRF:
    """Additional accented words should produce same relative frequency as ASCII."""

    def test_cafe_rf(self):
        assert bnc.relative_frequency('café') == bnc.relative_frequency('cafe')

    def test_resume_rf(self):
        assert bnc.relative_frequency(
            'résumé') == bnc.relative_frequency('resume')

    def test_naive_rf(self):
        assert bnc.relative_frequency(
            'naïve') == bnc.relative_frequency('naive')

    def test_cliche_rf(self):
        assert bnc.relative_frequency(
            'cliché') == bnc.relative_frequency('cliche')


class TestAdditionalAccentedWordsEC:
    """Additional accented words should produce same expected count as ASCII."""

    def test_cafe_ec(self):
        assert bnc.expected_count(
            'café', 100000) == bnc.expected_count('cafe', 100000)

    def test_resume_ec(self):
        assert bnc.expected_count(
            'résumé', 100000) == bnc.expected_count('resume', 100000)

    def test_naive_ec(self):
        assert bnc.expected_count(
            'naïve', 100000) == bnc.expected_count('naive', 100000)

    def test_cliche_ec(self):
        assert bnc.expected_count(
            'cliché', 100000) == bnc.expected_count('cliche', 100000)


# ========================================================================
# normalize_unicode_accents() unit tests
# ========================================================================

class TestNormalizeUnicodeAccentsFunction:
    """Unit tests for the normalize_unicode_accents() function."""

    def test_acute_e(self):
        assert normalize_unicode_accents('café') == 'cafe'

    def test_grave_e(self):
        assert normalize_unicode_accents('è') == 'e'

    def test_circumflex_o(self):
        assert normalize_unicode_accents('rôle') == 'role'

    def test_umlaut_i(self):
        """Diaeresis (umlaut) should be stripped."""
        assert normalize_unicode_accents('naïve') == 'naive'

    def test_cedilla_c(self):
        assert normalize_unicode_accents('façade') == 'facade'

    def test_tilde_n(self):
        assert normalize_unicode_accents('señor') == 'senor'

    def test_multiple_accents(self):
        """Multiple accented characters in one word."""
        assert normalize_unicode_accents('résumé') == 'resume'

    def test_all_accented_chars(self):
        """Comprehensive accent types."""
        assert normalize_unicode_accents('protégé') == 'protege'

    def test_ascii_passthrough(self):
        """Plain ASCII should pass through unchanged."""
        assert normalize_unicode_accents('hello') == 'hello'

    def test_empty_string(self):
        assert normalize_unicode_accents('') == ''

    def test_numbers_passthrough(self):
        assert normalize_unicode_accents('abc123') == 'abc123'

    def test_punctuation_passthrough(self):
        assert normalize_unicode_accents("don't") == "don't"

    def test_hyphen_passthrough(self):
        assert normalize_unicode_accents('self-esteem') == 'self-esteem'

    def test_mixed_ascii_and_accented(self):
        """Mix of accented and plain characters."""
        assert normalize_unicode_accents('phaéton') == 'phaeton'

    def test_uppercase_accented(self):
        """Uppercase accented chars should also be normalized."""
        assert normalize_unicode_accents('CAFÉ') == 'CAFE'

    def test_combining_acute_accent(self):
        """Combining acute accent (U+0301) should be stripped."""
        # 'e' + combining acute = é (decomposed form)
        assert normalize_unicode_accents('e\u0301') == 'e'

    def test_combining_grave_accent(self):
        """Combining grave accent (U+0300) should be stripped."""
        assert normalize_unicode_accents('e\u0300') == 'e'

    def test_combining_circumflex(self):
        """Combining circumflex (U+0302) should be stripped."""
        assert normalize_unicode_accents('o\u0302') == 'o'

    def test_combining_diaeresis(self):
        """Combining diaeresis (U+0308) should be stripped."""
        assert normalize_unicode_accents('i\u0308') == 'i'

    def test_combining_tilde(self):
        """Combining tilde (U+0303) should be stripped."""
        assert normalize_unicode_accents('n\u0303') == 'n'

    def test_combining_cedilla(self):
        """Combining cedilla (U+0327) should be stripped."""
        assert normalize_unicode_accents('c\u0327') == 'c'

    def test_precomposed_and_decomposed_same_result(self):
        """Both precomposed (NFC) and decomposed (NFD) forms should give same result."""
        import unicodedata
        precomposed = 'café'
        decomposed = unicodedata.normalize('NFD', 'café')
        assert normalize_unicode_accents(
            precomposed) == normalize_unicode_accents(decomposed)

    def test_scandinavian_a_ring(self):
        """å (a with ring above) should normalize to a."""
        assert normalize_unicode_accents('å') == 'a'

    def test_german_umlaut_u(self):
        """ü should normalize to u."""
        assert normalize_unicode_accents('über') == 'uber'

    def test_german_umlaut_o(self):
        """ö should normalize to o."""
        assert normalize_unicode_accents('schön') == 'schon'

    def test_german_umlaut_a(self):
        """ä should normalize to a."""
        assert normalize_unicode_accents('Märchen') == 'Marchen'

    def test_polish_l_stroke(self):
        """ł (L with stroke) - special case, may or may not normalize."""
        # NFKD + ASCII ignore will drop ł entirely since it's a base character
        # that doesn't decompose to l + combining mark.
        # This is acceptable behavior - we test that it doesn't crash.
        result = normalize_unicode_accents('łódź')
        assert isinstance(result, str)

    def test_ligature_ae(self):
        """æ ligature - doesn't decompose to ae under NFKD, gets dropped."""
        result = normalize_unicode_accents('æ')
        assert isinstance(result, str)

    def test_ligature_oe(self):
        """œ ligature - doesn't decompose to oe under NFKD, gets dropped."""
        result = normalize_unicode_accents('œ')
        assert isinstance(result, str)


# ========================================================================
# Full normalize() pipeline with accents
# ========================================================================

class TestNormalizePipelineWithAccents:
    """Test the full normalize() pipeline handles accents + other normalization."""

    def test_accent_plus_lowercase(self):
        """Accented uppercase should normalize to ASCII lowercase."""
        assert normalize('CAFÉ') == 'cafe'

    def test_accent_plus_strip(self):
        """Whitespace + accents should both be handled."""
        assert normalize('  café  ') == 'cafe'

    def test_accent_plus_apostrophe(self):
        """Accented word with curly apostrophe should normalize both."""
        # naïve with curly apostrophe somewhere
        word = 'na\u00efve\u2019s'
        result = normalize(word)
        assert result == "naive's"

    def test_accent_plus_uppercase_plus_strip(self):
        """All normalization steps combined."""
        assert normalize('  PROTÉGÉ  ') == 'protege'

    def test_accent_plus_curly_apostrophe(self):
        """Accented text with curly apostrophe variant."""
        word = 'caf\u00e9\u2019s'
        assert normalize(word) == "cafe's"

    def test_accent_normalize_idempotent(self):
        """Normalizing already-ASCII text should be idempotent."""
        assert normalize('protege') == 'protege'
        assert normalize('cafe') == 'cafe'

    def test_normalize_preserves_apostrophe(self):
        """ASCII apostrophe should survive accent normalization."""
        assert normalize("don't") == "don't"

    def test_normalize_preserves_hyphen(self):
        """Hyphen should survive accent normalization."""
        assert normalize('self-esteem') == 'self-esteem'


# ========================================================================
# Case variants of accented words
# ========================================================================

class TestAccentedCaseVariants:
    """Accented words in various case forms should all normalize correctly."""

    def test_cafe_uppercase(self):
        assert bnc.exists('CAFÉ') is True

    def test_cafe_titlecase(self):
        assert bnc.exists('Café') is True

    def test_cafe_lowercase(self):
        assert bnc.exists('café') is True

    def test_protege_uppercase(self):
        assert bnc.exists('PROTÉGÉ') is True

    def test_protege_titlecase(self):
        assert bnc.exists('Protégé') is True

    def test_naive_uppercase(self):
        assert bnc.exists('NAÏVE') is True

    def test_naive_titlecase(self):
        assert bnc.exists('Naïve') is True

    def test_resume_uppercase(self):
        assert bnc.exists('RÉSUMÉ') is True

    def test_resume_titlecase(self):
        assert bnc.exists('Résumé') is True

    def test_cliche_uppercase(self):
        assert bnc.exists('CLICHÉ') is True

    def test_outre_uppercase(self):
        assert bnc.exists('OUTRÉ') is True

    def test_phaeton_uppercase(self):
        assert bnc.exists('PHAÉTON') is True

    def test_cafe_uppercase_bucket(self):
        """Uppercase accented should give same bucket as lowercase ASCII."""
        assert bnc.bucket('CAFÉ') == bnc.bucket('cafe')

    def test_protege_titlecase_bucket(self):
        assert bnc.bucket('Protégé') == bnc.bucket('protege')

    def test_naive_uppercase_rf(self):
        assert bnc.relative_frequency(
            'NAÏVE') == bnc.relative_frequency('naive')


# ========================================================================
# Accented words with plural fallback
# ========================================================================

class TestAccentedPluralFallback:
    """Accented words with 's' plural suffix should use plural fallback."""

    def test_cafes_accented(self):
        """cafés should match cafes or cafe via plural fallback."""
        assert bnc.exists('cafés') is True

    def test_cliches_accented(self):
        """clichés should match cliches or cliche via plural fallback."""
        assert bnc.exists('clichés') is True

    def test_proteges_accented(self):
        """protégés should match via plural fallback to protege."""
        assert bnc.exists('protégés') is True

    def test_resumes_accented(self):
        """résumés should match via plural fallback to resume."""
        assert bnc.exists('résumés') is True

    def test_cafes_accented_bucket(self):
        """Accented plural should produce a bucket."""
        assert bnc.bucket('cafés') is not None

    def test_proteges_accented_bucket(self):
        assert bnc.bucket('protégés') is not None


# ========================================================================
# Accented words with whitespace
# ========================================================================

class TestAccentedWithWhitespace:
    """Accented words with whitespace should normalize both."""

    def test_cafe_leading_space(self):
        assert bnc.exists(' café') is True

    def test_cafe_trailing_space(self):
        assert bnc.exists('café ') is True

    def test_cafe_both_spaces(self):
        assert bnc.exists(' café ') is True

    def test_protege_with_tab(self):
        assert bnc.exists('\tprotégé\t') is True

    def test_cafe_spaces_bucket(self):
        assert bnc.bucket(' café ') == bnc.bucket('cafe')

    def test_protege_spaces_rf(self):
        assert bnc.relative_frequency(
            ' protégé ') == bnc.relative_frequency('protege')


# ========================================================================
# Various accent types (comprehensive Unicode coverage)
# ========================================================================

class TestVariousAccentTypes:
    """Test different types of Unicode accents/diacritics."""

    def test_acute_accent_e(self):
        """é (U+00E9) — acute accent."""
        assert normalize('café') == 'cafe'

    def test_grave_accent_e(self):
        """è (U+00E8) — grave accent."""
        assert normalize('crème') == 'creme'

    def test_circumflex_e(self):
        """ê (U+00EA) — circumflex."""
        assert normalize('fête') == 'fete'

    def test_diaeresis_i(self):
        """ï (U+00EF) — diaeresis."""
        assert normalize('naïve') == 'naive'

    def test_cedilla_c(self):
        """ç (U+00E7) — cedilla."""
        assert normalize('façade') == 'facade'

    def test_tilde_n(self):
        """ñ (U+00F1) — tilde."""
        assert normalize('señor') == 'senor'

    def test_ring_a(self):
        """å (U+00E5) — ring above."""
        assert normalize('åland') == 'aland'

    def test_umlaut_u(self):
        """ü (U+00FC) — umlaut."""
        assert normalize('über') == 'uber'

    def test_circumflex_o(self):
        """ô (U+00F4) — circumflex."""
        assert normalize('rôle') == 'role'

    def test_acute_a(self):
        """á (U+00E1) — acute accent."""
        assert normalize('á') == 'a'

    def test_acute_i(self):
        """í (U+00ED) — acute accent."""
        assert normalize('í') == 'i'

    def test_acute_o(self):
        """ó (U+00F3) — acute accent."""
        assert normalize('ó') == 'o'

    def test_acute_u(self):
        """ú (U+00FA) — acute accent."""
        assert normalize('ú') == 'u'

    def test_grave_a(self):
        """à (U+00E0) — grave accent."""
        assert normalize('à') == 'a'

    def test_circumflex_a(self):
        """â (U+00E2) — circumflex."""
        assert normalize('â') == 'a'

    def test_circumflex_i(self):
        """î (U+00EE) — circumflex."""
        assert normalize('î') == 'i'

    def test_circumflex_u(self):
        """û (U+00FB) — circumflex."""
        assert normalize('û') == 'u'

    def test_diaeresis_e(self):
        """ë (U+00EB) — diaeresis."""
        assert normalize('ë') == 'e'

    def test_diaeresis_u(self):
        """ü (U+00FC) — diaeresis."""
        assert normalize('ü') == 'u'

    def test_umlaut_o(self):
        """ö (U+00F6) — umlaut."""
        assert normalize('ö') == 'o'


# ========================================================================
# Edge cases
# ========================================================================

class TestAccentEdgeCases:
    """Edge cases for accent normalization."""

    def test_empty_string(self):
        assert normalize('') == ''

    def test_single_accented_char(self):
        assert normalize('é') == 'e'

    def test_all_accented_chars(self):
        """Word made entirely of accented characters."""
        assert normalize('éèêë') == 'eeee'

    def test_non_latin_unaffected(self):
        """Non-Latin scripts should not crash (they may produce empty strings)."""
        result = normalize('你好')
        assert isinstance(result, str)

    def test_emoji_unaffected(self):
        """Emoji should not crash."""
        result = normalize('hello 👋')
        assert isinstance(result, str)

    def test_already_ascii_word(self):
        """Words that are already ASCII should be unchanged after normalize."""
        assert normalize('the') == 'the'
        assert normalize('computer') == 'computer'
        assert normalize("don't") == "don't"

    def test_very_long_accented_word(self):
        """Long strings with accents should still work."""
        long_word = 'café' * 100
        result = normalize(long_word)
        assert result == 'cafe' * 100

    def test_none_type_not_accepted(self):
        """None should raise an error, not silently pass."""
        import pytest
        with pytest.raises((TypeError, AttributeError)):
            normalize(None)

    def test_numeric_string_with_accent(self):
        """Numbers mixed with accented characters."""
        assert normalize('café123') == 'cafe123'

    def test_whitespace_only(self):
        """Whitespace-only strings should normalize to empty."""
        assert normalize('   ') == ''

    def test_accent_on_uppercase(self):
        """Uppercase accented chars should lowercase and strip accent."""
        assert normalize('É') == 'e'
        assert normalize('À') == 'a'
        assert normalize('Ü') == 'u'

    def test_double_accent_word(self):
        """Word with two different accent types."""
        assert normalize('résumé') == 'resume'

    def test_nfkd_compatibility_decomposition(self):
        """NFKD should handle compatibility decompositions."""
        # ﬁ (U+FB01) ligature fi should decompose to 'fi' under NFKD
        assert normalize('ﬁ') == 'fi'

    def test_superscript_digits_nfkd(self):
        """NFKD decomposes superscript digits to regular digits."""
        assert normalize('²') == '2'
        assert normalize('³') == '3'


# ========================================================================
# Regression: existing behavior should not be broken
# ========================================================================

class TestAccentNormalizationRegression:
    """Ensure accent normalization doesn't break existing functionality."""

    def test_common_words_still_exist(self):
        assert bnc.exists('the') is True
        assert bnc.exists('and') is True
        assert bnc.exists('of') is True

    def test_apostrophe_words_still_work(self):
        assert bnc.exists("don't") is True
        assert bnc.exists("won't") is True
        assert bnc.exists("can't") is True

    def test_curly_apostrophe_still_works(self):
        curly_dont = 'don\u2019t'
        assert bnc.exists(curly_dont) is True

    def test_bucket_common_words(self):
        assert bnc.bucket('the') == 1
        assert bnc.bucket('of') == 1

    def test_rf_common_words(self):
        rf = bnc.relative_frequency('the')
        assert rf is not None
        assert rf > 0

    def test_ec_common_words(self):
        ec = bnc.expected_count('the', 50000)
        assert ec is not None
        assert ec > 2000

    def test_nonexistent_word_still_false(self):
        assert bnc.exists('xyznotarealword999') is False
        assert bnc.bucket('xyznotarealword999') is None

    def test_plural_fallback_still_works(self):
        assert bnc.exists('computers') is True
        assert bnc.bucket('computers') is not None

    def test_empty_string_still_works(self):
        assert bnc.exists('') is False
        assert bnc.bucket('') is None

    def test_whitespace_normalization_still_works(self):
        assert bnc.exists(' the ') is True

    def test_case_insensitivity_still_works(self):
        assert bnc.exists('THE') is True
        assert bnc.bucket('THE') == bnc.bucket('the')
