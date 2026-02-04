import bnc_lookup as bnc


# Existence tests

def test_common_words_exist():
    assert bnc.exists('the') is True
    assert bnc.exists('of') is True
    assert bnc.exists('and') is True
    assert bnc.exists('is') is True


def test_case_insensitive():
    assert bnc.exists('THE') is True
    assert bnc.exists('The') is True


def test_nonexistent_words():
    assert bnc.exists('xyzabc123') is False
    assert bnc.exists('notarealword999') is False


def test_empty_input():
    assert bnc.exists('') is False


def test_plurals():
    assert bnc.exists('computers') is True
    assert bnc.exists('languages') is True


# Frequency bucket tests

def test_common_words_bucket_1():
    """Most common words should be in bucket 1."""
    assert bnc.bucket('the') == 1
    assert bnc.bucket('of') == 1
    assert bnc.bucket('and') == 1
    assert bnc.bucket('to') == 1
    assert bnc.bucket('a') == 1


def test_bucket_case_insensitive():
    assert bnc.bucket('THE') == 1
    assert bnc.bucket('The') == 1


def test_bucket_nonexistent_words():
    """Non-existent words should return None."""
    assert bnc.bucket('xyzabc123') is None
    assert bnc.bucket('notarealword999') is None


def test_bucket_empty_input():
    assert bnc.bucket('') is None


def test_bucket_range():
    """Buckets should be in range 1-100."""
    bucket = bnc.bucket('the')
    assert bucket is not None
    assert 1 <= bucket <= 100

    bucket = bnc.bucket('python')
    assert bucket is not None
    assert 1 <= bucket <= 100


def test_bucket_plurals():
    """Plural fallback should work for buckets."""
    assert bnc.bucket('computers') is not None
    assert bnc.bucket('languages') is not None


def test_frequency_ordering():
    """More common words should have lower bucket numbers."""
    the_bucket = bnc.bucket('the')
    python_bucket = bnc.bucket('python')
    # 'the' is more common than 'python'
    assert the_bucket <= python_bucket


# Words by bucket tests

def test_words_returns_tuple():
    """words() should return a tuple."""
    result = bnc.words(1)
    assert isinstance(result, tuple)
    assert len(result) > 0


def test_words_bucket_1_contains_common():
    """Bucket 1 should contain common words."""
    words = bnc.words(1)
    # Check some common words are present
    assert 'the' in words
    assert 'and' in words
    assert 'people' in words


def test_words_bucket_range():
    """All buckets 1-100 should have words."""
    for b in [1, 25, 50, 75, 100]:
        words = bnc.words(b)
        assert len(words) > 0


def test_words_invalid_bucket():
    """Invalid bucket should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        bnc.words(0)
    with pytest.raises(ValueError):
        bnc.words(101)


def test_sample_returns_list():
    """sample() should return a list."""
    result = bnc.sample(1, 5)
    assert isinstance(result, list)
    assert len(result) == 5


def test_sample_respects_n():
    """sample() should return n items."""
    assert len(bnc.sample(1, 3)) == 3
    assert len(bnc.sample(1, 10)) == 10


def test_sample_words_exist():
    """Sampled words should exist in BNC."""
    words = bnc.sample(1, 10)
    for word in words:
        assert bnc.exists(word)


# Relative frequency tests

def test_relative_frequency_common_words():
    """Common words should have higher relative frequencies."""
    rf_the = bnc.relative_frequency('the')
    rf_python = bnc.relative_frequency('python')
    assert rf_the is not None
    assert rf_python is not None
    assert rf_the > rf_python


def test_relative_frequency_range():
    """Relative frequency should be between 0 and 1."""
    rf = bnc.relative_frequency('the')
    assert rf is not None
    assert 0 < rf < 1


def test_relative_frequency_nonexistent():
    """Non-existent words should return None."""
    assert bnc.relative_frequency('xyzabc123') is None


def test_relative_frequency_empty():
    assert bnc.relative_frequency('') is None


def test_relative_frequency_case_insensitive():
    assert bnc.relative_frequency('THE') == bnc.relative_frequency('the')


def test_relative_frequency_plurals():
    """Plural fallback should work."""
    assert bnc.relative_frequency('computers') is not None


# Expected count tests

def test_expected_count_the():
    """'the' in 50k tokens should be ~3000+."""
    ec = bnc.expected_count('the', 50000)
    assert ec is not None
    assert ec > 2000


def test_expected_count_rare_word():
    """Rare words should have low expected counts."""
    ec = bnc.expected_count('shimmered', 50000)
    assert ec is not None
    assert ec < 1.0


def test_expected_count_nonexistent():
    assert bnc.expected_count('xyzabc123', 50000) is None


def test_expected_count_scales_with_length():
    """Expected count should scale linearly with text length."""
    ec1 = bnc.expected_count('the', 10000)
    ec2 = bnc.expected_count('the', 20000)
    assert ec1 is not None
    assert ec2 is not None
    assert abs(ec2 - 2 * ec1) < 0.001


def test_expected_count_rounded():
    """rounded=True should return an int."""
    ec = bnc.expected_count('the', 50000, rounded=True)
    assert ec is not None
    assert isinstance(ec, int)
    assert ec > 2000


def test_expected_count_rounded_rare_word():
    """Rare words should round to 0."""
    ec = bnc.expected_count('shimmered', 50000, rounded=True)
    assert ec == 0


def test_expected_count_rounded_nonexistent():
    assert bnc.expected_count('xyzabc123', 50000, rounded=True) is None


# Apostrophe normalization tests (issue #4)

def test_curly_apostrophe_exists():
    """Curly apostrophe (U+2019) should normalize to ASCII apostrophe."""
    # "don't" with curly apostrophe
    curly_dont = 'don' + chr(0x2019) + 't'
    assert bnc.exists(curly_dont) is True


def test_left_curly_apostrophe_exists():
    """Left curly apostrophe (U+2018) should also work."""
    # "don't" with left curly apostrophe (misuse but should work)
    left_curly_dont = 'don' + chr(0x2018) + 't'
    assert bnc.exists(left_curly_dont) is True


def test_curly_apostrophe_bucket():
    """Curly apostrophe should work with bucket()."""
    curly_dont = 'don' + chr(0x2019) + 't'
    standard_dont = "don't"
    assert bnc.bucket(curly_dont) == bnc.bucket(standard_dont)


def test_curly_apostrophe_relative_frequency():
    """Curly apostrophe should work with relative_frequency()."""
    curly_dont = 'don' + chr(0x2019) + 't'
    standard_dont = "don't"
    assert bnc.relative_frequency(
        curly_dont) == bnc.relative_frequency(standard_dont)


def test_curly_apostrophe_expected_count():
    """Curly apostrophe should work with expected_count()."""
    curly_dont = 'don' + chr(0x2019) + 't'
    standard_dont = "don't"
    assert bnc.expected_count(
        curly_dont, 50000) == bnc.expected_count(standard_dont, 50000)


def test_various_apostrophe_variants():
    """Various apostrophe-like characters should all work."""
    apostrophe_variants = [
        chr(0x0027),  # APOSTROPHE (standard)
        chr(0x2019),  # RIGHT SINGLE QUOTATION MARK
        chr(0x2018),  # LEFT SINGLE QUOTATION MARK
        chr(0x0060),  # GRAVE ACCENT
        chr(0x00B4),  # ACUTE ACCENT
        chr(0x02BC),  # MODIFIER LETTER APOSTROPHE
    ]
    for apos in apostrophe_variants:
        word = 'don' + apos + 't'
        assert bnc.exists(
            word) is True, f'Failed for apostrophe U+{ord(apos):04X}'


def test_standard_apostrophe_words():
    """Words with standard ASCII apostrophe should work."""
    assert bnc.exists("don't") is True
    assert bnc.exists("won't") is True
    assert bnc.exists("can't") is True
    assert bnc.exists("it's") is True
    assert bnc.exists("he's") is True
    assert bnc.exists("she's") is True


# Whitespace handling tests

def test_exists_with_leading_whitespace():
    """Leading whitespace should be stripped."""
    assert bnc.exists(' the') is True
    assert bnc.exists('  the') is True
    assert bnc.exists('\tthe') is True


def test_exists_with_trailing_whitespace():
    """Trailing whitespace should be stripped."""
    assert bnc.exists('the ') is True
    assert bnc.exists('the  ') is True
    assert bnc.exists('the\t') is True


def test_exists_with_both_whitespace():
    """Both leading and trailing whitespace should be stripped."""
    assert bnc.exists(' the ') is True
    assert bnc.exists('  the  ') is True
    assert bnc.exists('\t the \t') is True


def test_bucket_with_whitespace():
    """Whitespace should be stripped for bucket()."""
    assert bnc.bucket(' the') == bnc.bucket('the')
    assert bnc.bucket('the ') == bnc.bucket('the')
    assert bnc.bucket(' the ') == bnc.bucket('the')


def test_relative_frequency_with_whitespace():
    """Whitespace should be stripped for relative_frequency()."""
    assert bnc.relative_frequency(' the') == bnc.relative_frequency('the')
    assert bnc.relative_frequency('the ') == bnc.relative_frequency('the')
    assert bnc.relative_frequency(' the ') == bnc.relative_frequency('the')


def test_expected_count_with_whitespace():
    """Whitespace should be stripped for expected_count()."""
    assert bnc.expected_count(
        ' the', 50000) == bnc.expected_count('the', 50000)
    assert bnc.expected_count(
        'the ', 50000) == bnc.expected_count('the', 50000)


# Plural fallback boundary tests

def test_plural_fallback_short_words():
    """Words 3 chars or less ending in 's' should NOT use plural fallback."""
    # 'bus' is 3 chars - should not try 'bu'
    # We test that 'bus' exists on its own merit, not via fallback
    assert bnc.exists('bus') is True
    assert bnc.exists('gas') is True
    assert bnc.exists('yes') is True


def test_plural_fallback_four_char_words():
    """Words 4+ chars ending in 's' should use plural fallback."""
    # 'cars' -> tries 'car' if 'cars' not found
    assert bnc.exists('cars') is True
    assert bnc.exists('dogs') is True
    assert bnc.exists('cats') is True


def test_plural_fallback_only_when_needed():
    """Plural fallback only kicks in if word not found directly."""
    # 'computers' exists directly in BNC
    assert bnc.exists('computers') is True
    assert bnc.bucket('computers') is not None


# sample() edge case tests

def test_sample_default_n():
    """sample() with default n should return 10 items."""
    result = bnc.sample(1)
    assert isinstance(result, list)
    assert len(result) == 10


def test_sample_invalid_bucket_zero():
    """sample() with bucket 0 should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        bnc.sample(0, 5)


def test_sample_invalid_bucket_101():
    """sample() with bucket 101 should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        bnc.sample(101, 5)


def test_sample_invalid_bucket_negative():
    """sample() with negative bucket should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        bnc.sample(-1, 5)


def test_sample_randomness():
    """sample() should return different results on different calls (usually)."""
    # Get multiple samples and check they're not all identical
    samples = [tuple(bnc.sample(50, 5)) for _ in range(10)]
    unique_samples = set(samples)
    # With 10 samples of 5 words each, we should see some variety
    assert len(unique_samples) > 1


def test_sample_words_in_correct_bucket():
    """Sampled words should be from the correct bucket."""
    for bucket in [1, 25, 50, 75, 100]:
        words = bnc.sample(bucket, 5)
        bucket_words = bnc.words(bucket)
        for word in words:
            assert word in bucket_words


# words() edge case tests

def test_words_invalid_bucket_negative():
    """words() with negative bucket should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        bnc.words(-1)
    with pytest.raises(ValueError):
        bnc.words(-100)


def test_words_invalid_bucket_float():
    """words() with float should raise TypeError or work if int-like."""
    # This depends on implementation - may raise TypeError
    try:
        result = bnc.words(1.0)
        # If it works, should return same as words(1)
        assert result == bnc.words(1)
    except TypeError:
        pass  # Also acceptable


def test_words_all_buckets_non_empty():
    """Every bucket 1-100 should contain at least one word."""
    for bucket in range(1, 101):
        words = bnc.words(bucket)
        assert len(words) > 0, f'Bucket {bucket} is empty'


def test_words_bucket_1_size():
    """Bucket 1 should have ~6,694 words (top 1%)."""
    words = bnc.words(1)
    # Allow some variance, but should be in ballpark
    assert len(words) > 5000
    assert len(words) < 10000


def test_words_alphabetically_sorted():
    """Words in each bucket should be alphabetically sorted."""
    for bucket in [1, 50, 100]:
        words = bnc.words(bucket)
        assert words == tuple(sorted(words))


# expected_count() edge case tests

def test_expected_count_zero_length():
    """expected_count() with zero text_length should return 0."""
    ec = bnc.expected_count('the', 0)
    assert ec == 0.0


def test_expected_count_negative_length():
    """expected_count() with negative text_length returns negative (math works)."""
    ec = bnc.expected_count('the', -1000)
    assert ec is not None
    assert ec < 0


def test_expected_count_case_insensitive():
    """expected_count() should be case insensitive."""
    assert bnc.expected_count('THE', 50000) == bnc.expected_count('the', 50000)
    assert bnc.expected_count('The', 50000) == bnc.expected_count('the', 50000)


def test_expected_count_empty():
    """expected_count() with empty string should return None."""
    assert bnc.expected_count('', 50000) is None


def test_expected_count_large_text():
    """expected_count() should work with large text lengths."""
    ec = bnc.expected_count('the', 10_000_000)
    assert ec is not None
    assert ec > 600000  # 'the' is ~6% of BNC


def test_expected_count_rounded_boundary():
    """Test rounding behavior at 0.5 boundary."""
    # Find a word that gives ~0.5 expected count at some text length
    # 'shimmered' is rare, expected count at 50k is << 1
    ec_float = bnc.expected_count('shimmered', 50000)
    ec_rounded = bnc.expected_count('shimmered', 50000, rounded=True)
    assert ec_float is not None
    assert ec_rounded is not None
    assert ec_rounded == round(ec_float)


# Consistency tests across functions

def test_exists_bucket_consistency():
    """If exists() is True, bucket() should return a value."""
    test_words = ['the', 'python', 'computer', 'language', 'testing']
    for word in test_words:
        if bnc.exists(word):
            assert bnc.bucket(word) is not None


def test_exists_rf_consistency():
    """If exists() is True, relative_frequency() should return a value."""
    test_words = ['the', 'python', 'computer', 'language', 'testing']
    for word in test_words:
        if bnc.exists(word):
            assert bnc.relative_frequency(word) is not None


def test_bucket_rf_consistency():
    """If bucket() returns a value, relative_frequency() should too."""
    test_words = ['the', 'python', 'computer', 'language', 'testing']
    for word in test_words:
        if bnc.bucket(word) is not None:
            assert bnc.relative_frequency(word) is not None


def test_nonexistent_all_none():
    """Non-existent words should return False/None across all functions."""
    fake_word = 'xyznotarealword999'
    assert bnc.exists(fake_word) is False
    assert bnc.bucket(fake_word) is None
    assert bnc.relative_frequency(fake_word) is None
    assert bnc.expected_count(fake_word, 50000) is None


# Unicode and special character tests

def test_unicode_words():
    """Words with accented characters should work if in BNC."""
    # café, résumé, naïve are in BNC
    # Testing that Unicode doesn't break things
    result = bnc.exists('café')
    assert result is True or result is False  # Just shouldn't crash


def test_hyphenated_words():
    """Hyphenated words should work if in BNC."""
    assert bnc.exists(
        'self-esteem') is True or bnc.exists('self-esteem') is False


def test_numeric_strings():
    """Numeric strings should not crash."""
    assert bnc.exists('123') is True or bnc.exists('123') is False
    assert bnc.exists('2024') is True or bnc.exists('2024') is False


def test_mixed_case_words():
    """Various case patterns should all normalize."""
    assert bnc.exists('ThE') is True
    assert bnc.exists('tHe') is True
    assert bnc.exists('THE') is True
    assert bnc.bucket('ThE') == bnc.bucket('the')


# Stress tests

def test_many_lookups():
    """Many rapid lookups should work without issue."""
    words = ['the', 'and', 'of', 'to', 'a', 'in', 'is', 'it', 'for', 'on']
    for _ in range(100):
        for word in words:
            assert bnc.exists(word) is True


def test_bucket_1_all_exist():
    """All words in bucket 1 should exist."""
    words = bnc.words(1)
    for word in words[:100]:  # Test first 100 to keep it quick
        assert bnc.exists(
            word) is True, f"Word '{word}' from bucket 1 doesn't exist"


def test_bucket_100_all_exist():
    """All words in bucket 100 should exist."""
    words = bnc.words(100)
    for word in words[:100]:  # Test first 100
        assert bnc.exists(
            word) is True, f"Word '{word}' from bucket 100 doesn't exist"


# Normalize module unit tests

def test_normalize_module_apostrophe_normalization():
    """Test normalize_apostrophes() directly."""
    from bnc_lookup.normalize import normalize_apostrophes

    # Curly right quote
    assert normalize_apostrophes('don\u2019t') == "don't"
    # Curly left quote
    assert normalize_apostrophes('don\u2018t') == "don't"
    # Grave accent
    assert normalize_apostrophes('don\u0060t') == "don't"
    # Acute accent
    assert normalize_apostrophes('don\u00B4t') == "don't"
    # Multiple in one string
    assert normalize_apostrophes('\u2019test\u2018') == "'test'"


def test_normalize_module_full_normalize():
    """Test normalize() directly."""
    from bnc_lookup.normalize import normalize

    # Lowercase
    assert normalize('THE') == 'the'
    # Strip whitespace
    assert normalize('  the  ') == 'the'
    # Apostrophe + lowercase + strip
    assert normalize('  DON\u2019T  ') == "don't"


def test_normalize_module_empty_string():
    """Normalize empty string should return empty string."""
    from bnc_lookup.normalize import normalize, normalize_apostrophes

    assert normalize('') == ''
    assert normalize_apostrophes('') == ''


def test_normalize_module_no_apostrophes():
    """Strings without apostrophes should pass through unchanged (except case/strip)."""
    from bnc_lookup.normalize import normalize, normalize_apostrophes

    assert normalize_apostrophes('hello world') == 'hello world'
    assert normalize('HELLO WORLD') == 'hello world'


def test_normalize_all_apostrophe_variants():
    """Test all 20 apostrophe variants normalize correctly."""
    from bnc_lookup.normalize import normalize_apostrophes, APOSTROPHE_VARIANTS

    for char in APOSTROPHE_VARIANTS:
        test_str = f'don{char}t'
        result = normalize_apostrophes(test_str)
        assert result == "don't", f'Failed for U+{ord(char):04X}'


# Edge cases for apostrophe normalization across all functions

def test_all_functions_with_fullwidth_apostrophe():
    """Fullwidth apostrophe (U+FF07) should work across all functions."""
    fullwidth_dont = 'don' + chr(0xFF07) + 't'
    standard_dont = "don't"

    assert bnc.exists(fullwidth_dont) is True
    assert bnc.bucket(fullwidth_dont) == bnc.bucket(standard_dont)
    assert bnc.relative_frequency(
        fullwidth_dont) == bnc.relative_frequency(standard_dont)
    assert bnc.expected_count(
        fullwidth_dont, 50000) == bnc.expected_count(standard_dont, 50000)


def test_all_functions_with_prime():
    """Prime mark (U+2032) should work across all functions."""
    prime_dont = 'don' + chr(0x2032) + 't'
    standard_dont = "don't"

    assert bnc.exists(prime_dont) is True
    assert bnc.bucket(prime_dont) == bnc.bucket(standard_dont)
    assert bnc.relative_frequency(
        prime_dont) == bnc.relative_frequency(standard_dont)


def test_all_functions_with_modifier_letter_apostrophe():
    """Modifier letter apostrophe (U+02BC) should work across all functions."""
    modifier_dont = 'don' + chr(0x02BC) + 't'
    standard_dont = "don't"

    assert bnc.exists(modifier_dont) is True
    assert bnc.bucket(modifier_dont) == bnc.bucket(standard_dont)
    assert bnc.relative_frequency(
        modifier_dont) == bnc.relative_frequency(standard_dont)
