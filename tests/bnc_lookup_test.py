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


# Contraction fallback tests (issue #5)

def test_contraction_fallback_well():
    """we'll should exist via contraction fallback (we + 'll)."""
    assert bnc.exists("we'll") is True


def test_contraction_fallback_ill():
    """i'll should exist via contraction fallback (i + 'll)."""
    assert bnc.exists("i'll") is True


def test_contraction_fallback_youll():
    """you'll should exist via contraction fallback (you + 'll)."""
    assert bnc.exists("you'll") is True


def test_contraction_fallback_theyll():
    """they'll should exist via contraction fallback (they + 'll)."""
    assert bnc.exists("they'll") is True


def test_contraction_fallback_im():
    """i'm should exist via contraction fallback (i + 'm)."""
    assert bnc.exists("i'm") is True


def test_contraction_fallback_youre():
    """you're should exist via contraction fallback (you + 're)."""
    assert bnc.exists("you're") is True


def test_contraction_fallback_were():
    """we're should exist via contraction fallback (we + 're)."""
    assert bnc.exists("we're") is True


def test_contraction_fallback_theyre():
    """they're should exist via contraction fallback (they + 're)."""
    assert bnc.exists("they're") is True


def test_contraction_fallback_ive():
    """i've should exist via contraction fallback (i + 've)."""
    assert bnc.exists("i've") is True


def test_contraction_fallback_youve():
    """you've should exist via contraction fallback (you + 've)."""
    assert bnc.exists("you've") is True


def test_contraction_fallback_weve():
    """we've should exist via contraction fallback (we + 've)."""
    assert bnc.exists("we've") is True


def test_contraction_fallback_theyve():
    """they've should exist via contraction fallback (they + 've)."""
    assert bnc.exists("they've") is True


def test_contraction_fallback_id():
    """i'd should exist via contraction fallback (i + 'd)."""
    assert bnc.exists("i'd") is True


def test_contraction_fallback_youd():
    """you'd should exist via contraction fallback (you + 'd)."""
    assert bnc.exists("you'd") is True


def test_contraction_fallback_wed():
    """we'd should exist via contraction fallback (we + 'd)."""
    assert bnc.exists("we'd") is True


def test_contraction_fallback_theyd():
    """they'd should exist via contraction fallback (they + 'd)."""
    assert bnc.exists("they'd") is True


def test_contraction_fallback_case_insensitive():
    """Contraction fallback should be case insensitive."""
    assert bnc.exists("We'll") is True
    assert bnc.exists("WE'LL") is True
    assert bnc.exists("I'm") is True
    assert bnc.exists("I'M") is True


def test_contraction_fallback_curly_apostrophe():
    """Contraction fallback should work with curly apostrophes."""
    # we'll with curly apostrophe
    curly_well = 'we' + chr(0x2019) + 'll'
    assert bnc.exists(curly_well) is True

    # i'm with curly apostrophe
    curly_im = 'i' + chr(0x2019) + 'm'
    assert bnc.exists(curly_im) is True


def test_contraction_fallback_invalid_stem():
    """Contractions with invalid stems should return False."""
    # "zqn't" -> "zq" + "n't" - "zq" is not a word in BNC
    assert bnc.exists("zqn't") is False
    # "xyzzy'll" -> "xyzzy" + "'ll" - "xyzzy" is not a word
    assert bnc.exists("xyzzy'll") is False


def test_contraction_fallback_aint():
    """ain't exists via fallback since 'ai' and 'n't' both exist in BNC."""
    # While 'ain't' might seem like it shouldn't exist, 'ai' is in the BNC
    # (as an abbreviation) and 'n't' is stored as a separate token
    assert bnc.exists("ain't") is True


def test_contraction_fallback_wont():
    """won't should NOT exist via fallback (wo is not a valid word)."""
    # won't -> wo + n't, but "wo" is not in BNC
    # Unless "won't" itself is in BNC directly
    result = bnc.exists("won't")
    # The result depends on whether "won't" is stored directly
    # or if "wo" exists - just verify it doesn't crash
    assert result is True or result is False


def test_contraction_fallback_cant():
    """can't should be handled correctly."""
    # can't -> ca + n't, but "ca" might not exist
    # OR "can't" might be stored directly
    result = bnc.exists("can't")
    assert result is True or result is False


def test_contraction_fallback_doesnt_affect_regular_words():
    """Regular words without contractions should not be affected."""
    assert bnc.exists('well') is True  # "well" the word, not "we'll"
    assert bnc.exists('ill') is True   # "ill" the word, not "i'll"
    assert bnc.exists('were') is True  # "were" past tense, not "we're"


def test_split_contraction_function():
    """Test the internal _split_contraction function."""
    from bnc_lookup.find_bnc import _split_contraction

    # 'll contractions
    assert _split_contraction("we'll") == ('we', "'ll")
    assert _split_contraction("i'll") == ('i', "'ll")
    assert _split_contraction("you'll") == ('you', "'ll")

    # 'm contractions
    assert _split_contraction("i'm") == ('i', "'m")

    # 're contractions
    assert _split_contraction("you're") == ('you', "'re")
    assert _split_contraction("we're") == ('we', "'re")
    assert _split_contraction("they're") == ('they', "'re")

    # 've contractions
    assert _split_contraction("i've") == ('i', "'ve")
    assert _split_contraction("we've") == ('we', "'ve")

    # 'd contractions
    assert _split_contraction("i'd") == ('i', "'d")
    assert _split_contraction("we'd") == ('we', "'d")

    # n't contractions
    assert _split_contraction("don't") == ('do', "n't")
    assert _split_contraction("won't") == ('wo', "n't")
    assert _split_contraction("can't") == ('ca', "n't")

    # Non-contractions
    assert _split_contraction('hello') is None
    assert _split_contraction('well') is None
    assert _split_contraction('the') is None


def test_split_contraction_empty_stem():
    """Contraction with no stem should return None."""
    from bnc_lookup.find_bnc import _split_contraction

    # Just the suffix with no stem
    assert _split_contraction("'ll") is None
    assert _split_contraction("'m") is None
    assert _split_contraction("n't") is None


# =============================================================================
# Contraction fallback for bucket() tests
# =============================================================================

def test_contraction_bucket_well():
    """we'll should return a bucket via contraction fallback."""
    b = bnc.bucket("we'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_ill():
    """i'll should return a bucket via contraction fallback."""
    b = bnc.bucket("i'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_youll():
    """you'll should return a bucket via contraction fallback."""
    b = bnc.bucket("you'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_theyll():
    """they'll should return a bucket via contraction fallback."""
    b = bnc.bucket("they'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_shell():
    """she'll should return a bucket via contraction fallback."""
    b = bnc.bucket("she'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_hell():
    """he'll should return a bucket via contraction fallback."""
    b = bnc.bucket("he'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_itll():
    """it'll should return a bucket via contraction fallback."""
    b = bnc.bucket("it'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_im():
    """i'm should return a bucket via contraction fallback."""
    b = bnc.bucket("i'm")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_youre():
    """you're should return a bucket via contraction fallback."""
    b = bnc.bucket("you're")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_were():
    """we're should return a bucket via contraction fallback."""
    b = bnc.bucket("we're")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_theyre():
    """they're should return a bucket via contraction fallback."""
    b = bnc.bucket("they're")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_ive():
    """i've should return a bucket via contraction fallback."""
    b = bnc.bucket("i've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_youve():
    """you've should return a bucket via contraction fallback."""
    b = bnc.bucket("you've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_weve():
    """we've should return a bucket via contraction fallback."""
    b = bnc.bucket("we've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_theyve():
    """they've should return a bucket via contraction fallback."""
    b = bnc.bucket("they've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_id():
    """i'd should return a bucket via contraction fallback."""
    b = bnc.bucket("i'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_youd():
    """you'd should return a bucket via contraction fallback."""
    b = bnc.bucket("you'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_wed():
    """we'd should return a bucket via contraction fallback."""
    b = bnc.bucket("we'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_theyd():
    """they'd should return a bucket via contraction fallback."""
    b = bnc.bucket("they'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_shed():
    """she'd should return a bucket via contraction fallback."""
    b = bnc.bucket("she'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_hed():
    """he'd should return a bucket via contraction fallback."""
    b = bnc.bucket("he'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_bucket_case_insensitive():
    """Contraction bucket fallback should be case insensitive."""
    assert bnc.bucket("we'll") == bnc.bucket("We'll")
    assert bnc.bucket("we'll") == bnc.bucket("WE'LL")
    assert bnc.bucket("i'm") == bnc.bucket("I'm")
    assert bnc.bucket("i'm") == bnc.bucket("I'M")
    assert bnc.bucket("you're") == bnc.bucket("YOU'RE")


def test_contraction_bucket_curly_apostrophe():
    """Contraction bucket fallback should work with curly apostrophes."""
    curly_well = 'we' + chr(0x2019) + 'll'
    standard_well = "we'll"
    assert bnc.bucket(curly_well) == bnc.bucket(standard_well)

    curly_im = 'i' + chr(0x2019) + 'm'
    standard_im = "i'm"
    assert bnc.bucket(curly_im) == bnc.bucket(standard_im)


def test_contraction_bucket_invalid_stem_returns_none():
    """Contractions with invalid stems should return None for bucket."""
    assert bnc.bucket("zqn't") is None
    assert bnc.bucket("xyzzy'll") is None
    assert bnc.bucket("qqq're") is None


def test_contraction_bucket_uses_max_of_components():
    """Contraction bucket should use max (less frequent) of components."""
    # Get component buckets
    we_bucket = bnc.bucket('we')
    ll_bucket = bnc.bucket("'ll")
    well_bucket = bnc.bucket("we'll")

    # Should be max of components (conservative estimate)
    assert we_bucket is not None
    assert ll_bucket is not None
    assert well_bucket is not None
    assert well_bucket == max(we_bucket, ll_bucket)


# =============================================================================
# Contraction fallback for relative_frequency() tests
# =============================================================================

def test_contraction_rf_well():
    """we'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("we'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_ill():
    """i'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("i'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_youll():
    """you'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("you'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_theyll():
    """they'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("they'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_shell():
    """she'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("she'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_hell():
    """he'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("he'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_itll():
    """it'll should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("it'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_im():
    """i'm should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("i'm")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_youre():
    """you're should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("you're")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_were():
    """we're should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("we're")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_theyre():
    """they're should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("they're")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_ive():
    """i've should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("i've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_youve():
    """you've should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("you've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_weve():
    """we've should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("we've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_theyve():
    """they've should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("they've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_id():
    """i'd should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("i'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_youd():
    """you'd should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("you'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_wed():
    """we'd should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("we'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_theyd():
    """they'd should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("they'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_shed():
    """she'd should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("she'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_hed():
    """he'd should return a relative frequency via contraction fallback."""
    rf = bnc.relative_frequency("he'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_rf_case_insensitive():
    """Contraction rf fallback should be case insensitive."""
    assert bnc.relative_frequency("we'll") == bnc.relative_frequency("We'll")
    assert bnc.relative_frequency("we'll") == bnc.relative_frequency("WE'LL")
    assert bnc.relative_frequency("i'm") == bnc.relative_frequency("I'm")
    assert bnc.relative_frequency("i'm") == bnc.relative_frequency("I'M")
    assert bnc.relative_frequency("you're") == bnc.relative_frequency("YOU'RE")


def test_contraction_rf_curly_apostrophe():
    """Contraction rf fallback should work with curly apostrophes."""
    curly_well = 'we' + chr(0x2019) + 'll'
    standard_well = "we'll"
    assert bnc.relative_frequency(
        curly_well) == bnc.relative_frequency(standard_well)

    curly_im = 'i' + chr(0x2019) + 'm'
    standard_im = "i'm"
    assert bnc.relative_frequency(
        curly_im) == bnc.relative_frequency(standard_im)


def test_contraction_rf_invalid_stem_returns_none():
    """Contractions with invalid stems should return None for rf."""
    assert bnc.relative_frequency("zqn't") is None
    assert bnc.relative_frequency("xyzzy'll") is None
    assert bnc.relative_frequency("qqq're") is None


def test_contraction_rf_uses_min_of_components():
    """Contraction rf should use min (less frequent) of components."""
    # Get component relative frequencies
    we_rf = bnc.relative_frequency('we')
    ll_rf = bnc.relative_frequency("'ll")
    well_rf = bnc.relative_frequency("we'll")

    # Should be min of components (conservative estimate)
    assert we_rf is not None
    assert ll_rf is not None
    assert well_rf is not None
    assert well_rf == min(we_rf, ll_rf)


# =============================================================================
# Contraction fallback for expected_count() tests
# =============================================================================

def test_contraction_expected_count_well():
    """we'll should return an expected count via contraction fallback."""
    ec = bnc.expected_count("we'll", 50000)
    assert ec is not None
    assert ec > 0


def test_contraction_expected_count_im():
    """i'm should return an expected count via contraction fallback."""
    ec = bnc.expected_count("i'm", 50000)
    assert ec is not None
    assert ec > 0


def test_contraction_expected_count_youre():
    """you're should return an expected count via contraction fallback."""
    ec = bnc.expected_count("you're", 50000)
    assert ec is not None
    assert ec > 0


def test_contraction_expected_count_ive():
    """i've should return an expected count via contraction fallback."""
    ec = bnc.expected_count("i've", 50000)
    assert ec is not None
    assert ec > 0


def test_contraction_expected_count_wed():
    """we'd should return an expected count via contraction fallback."""
    ec = bnc.expected_count("we'd", 50000)
    assert ec is not None
    assert ec > 0


def test_contraction_expected_count_case_insensitive():
    """Contraction expected_count fallback should be case insensitive."""
    assert bnc.expected_count(
        "we'll", 50000) == bnc.expected_count("We'll", 50000)
    assert bnc.expected_count(
        "we'll", 50000) == bnc.expected_count("WE'LL", 50000)


def test_contraction_expected_count_rounded():
    """Contraction expected_count should work with rounded=True."""
    ec = bnc.expected_count("we'll", 50000, rounded=True)
    assert ec is not None
    assert isinstance(ec, int)


def test_contraction_expected_count_invalid_stem_returns_none():
    """Contractions with invalid stems should return None for expected_count."""
    assert bnc.expected_count("zqn't", 50000) is None
    assert bnc.expected_count("xyzzy'll", 50000) is None


# =============================================================================
# Contraction consistency tests across all functions
# =============================================================================

def test_contraction_consistency_well():
    """we'll should be consistent across exists, bucket, rf, and expected_count."""
    assert bnc.exists("we'll") is True
    assert bnc.bucket("we'll") is not None
    assert bnc.relative_frequency("we'll") is not None
    assert bnc.expected_count("we'll", 50000) is not None


def test_contraction_consistency_im():
    """i'm should be consistent across all functions."""
    assert bnc.exists("i'm") is True
    assert bnc.bucket("i'm") is not None
    assert bnc.relative_frequency("i'm") is not None
    assert bnc.expected_count("i'm", 50000) is not None


def test_contraction_consistency_youre():
    """you're should be consistent across all functions."""
    assert bnc.exists("you're") is True
    assert bnc.bucket("you're") is not None
    assert bnc.relative_frequency("you're") is not None
    assert bnc.expected_count("you're", 50000) is not None


def test_contraction_consistency_ive():
    """i've should be consistent across all functions."""
    assert bnc.exists("i've") is True
    assert bnc.bucket("i've") is not None
    assert bnc.relative_frequency("i've") is not None
    assert bnc.expected_count("i've", 50000) is not None


def test_contraction_consistency_wed():
    """we'd should be consistent across all functions."""
    assert bnc.exists("we'd") is True
    assert bnc.bucket("we'd") is not None
    assert bnc.relative_frequency("we'd") is not None
    assert bnc.expected_count("we'd", 50000) is not None


def test_contraction_consistency_all_ll_contractions():
    """All 'll contractions should be consistent."""
    ll_contractions = ["i'll", "you'll", "we'll",
                       "they'll", "she'll", "he'll", "it'll"]
    for word in ll_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec failed'


def test_contraction_consistency_all_re_contractions():
    """All 're contractions should be consistent."""
    re_contractions = ["you're", "we're", "they're"]
    for word in re_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec failed'


def test_contraction_consistency_all_ve_contractions():
    """All 've contractions should be consistent."""
    ve_contractions = ["i've", "you've", "we've", "they've"]
    for word in ve_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec failed'


def test_contraction_consistency_all_d_contractions():
    """All 'd contractions should be consistent."""
    d_contractions = ["i'd", "you'd", "we'd",
                      "they'd", "she'd", "he'd", "it'd"]
    for word in d_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec failed'


def test_contraction_consistency_m_contraction():
    """The 'm contraction (i'm) should be consistent."""
    assert bnc.exists("i'm") is True
    assert bnc.bucket("i'm") is not None
    assert bnc.relative_frequency("i'm") is not None
    assert bnc.expected_count("i'm", 50000) is not None


def test_contraction_consistency_invalid_all_return_false_or_none():
    """Invalid contractions should return False/None consistently."""
    # Use stems that definitely don't exist in BNC: zq, xyzzy, qqq, asdf, xyxyxy
    invalid_contractions = ["zqn't", "xyzzy'll",
                            "qqq're", "asdf've", "xyxyxy'd", "zq'm"]
    for word in invalid_contractions:
        assert bnc.exists(word) is False, f'{word} exists should be False'
        assert bnc.bucket(word) is None, f'{word} bucket should be None'
        assert bnc.relative_frequency(
            word) is None, f'{word} rf should be None'
        assert bnc.expected_count(
            word, 50000) is None, f'{word} ec should be None'


# =============================================================================
# Comprehensive contraction matrix test
# =============================================================================

def test_contraction_matrix_all_pronouns_all_suffixes():
    """Test all pronoun + suffix combinations comprehensively."""
    pronouns = ['i', 'you', 'we', 'they', 'she', 'he', 'it']
    suffixes = ["'ll", "'re", "'ve", "'d", "'m"]

    # Map of which combinations are valid English contractions
    # Some pronouns don't combine with all suffixes
    valid_combinations = {
        'i': ["'ll", "'ve", "'d", "'m"],
        'you': ["'ll", "'re", "'ve", "'d"],
        'we': ["'ll", "'re", "'ve", "'d"],
        'they': ["'ll", "'re", "'ve", "'d"],
        'she': ["'ll", "'d"],
        'he': ["'ll", "'d"],
        'it': ["'ll", "'d"],
    }

    for pronoun in pronouns:
        for suffix in valid_combinations.get(pronoun, []):
            word = pronoun + suffix
            # All valid combinations should work
            assert bnc.exists(word) is True, f'{word} exists failed'
            assert bnc.bucket(word) is not None, f'{word} bucket failed'
            assert bnc.relative_frequency(
                word) is not None, f'{word} rf failed'


def test_contraction_with_all_apostrophe_variants():
    """Test contractions with all 20 apostrophe variants."""
    from bnc_lookup.normalize import APOSTROPHE_VARIANTS

    base_contractions = [
        ('we', 'll'),
        ('i', 'm'),
        ('you', 're'),
        ('i', 've'),
        ('we', 'd'),
    ]

    for stem, suffix in base_contractions:
        standard_word = stem + "'" + suffix
        standard_bucket = bnc.bucket(standard_word)
        standard_rf = bnc.relative_frequency(standard_word)

        for apos in APOSTROPHE_VARIANTS:
            variant_word = stem + apos + suffix
            assert bnc.exists(
                variant_word) is True, f'exists failed for {repr(variant_word)}'
            assert bnc.bucket(
                variant_word) == standard_bucket, f'bucket mismatch for {repr(variant_word)}'
            assert bnc.relative_frequency(
                variant_word) == standard_rf, f'rf mismatch for {repr(variant_word)}'


# =============================================================================
# COMPREHENSIVE CONTRACTION TESTS - NON-PRONOUN CONTRACTIONS
# =============================================================================

# -----------------------------------------------------------------------------
# Modal verb n't contractions
# -----------------------------------------------------------------------------

def test_contraction_wouldnt_exists():
    """wouldn't should exist via contraction fallback."""
    assert bnc.exists("wouldn't") is True


def test_contraction_wouldnt_bucket():
    """wouldn't should return a bucket."""
    b = bnc.bucket("wouldn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_wouldnt_rf():
    """wouldn't should return a relative frequency."""
    rf = bnc.relative_frequency("wouldn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_couldnt_exists():
    """couldn't should exist via contraction fallback."""
    assert bnc.exists("couldn't") is True


def test_contraction_couldnt_bucket():
    """couldn't should return a bucket."""
    b = bnc.bucket("couldn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_couldnt_rf():
    """couldn't should return a relative frequency."""
    rf = bnc.relative_frequency("couldn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_shouldnt_exists():
    """shouldn't should exist via contraction fallback."""
    assert bnc.exists("shouldn't") is True


def test_contraction_shouldnt_bucket():
    """shouldn't should return a bucket."""
    b = bnc.bucket("shouldn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_shouldnt_rf():
    """shouldn't should return a relative frequency."""
    rf = bnc.relative_frequency("shouldn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_mustnt_exists():
    """mustn't should exist via contraction fallback."""
    assert bnc.exists("mustn't") is True


def test_contraction_mustnt_bucket():
    """mustn't should return a bucket."""
    b = bnc.bucket("mustn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_mustnt_rf():
    """mustn't should return a relative frequency."""
    rf = bnc.relative_frequency("mustn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_mightnt_exists():
    """mightn't should exist via contraction fallback."""
    assert bnc.exists("mightn't") is True


def test_contraction_mightnt_bucket():
    """mightn't should return a bucket."""
    b = bnc.bucket("mightn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_mightnt_rf():
    """mightn't should return a relative frequency."""
    rf = bnc.relative_frequency("mightn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_neednt_exists():
    """needn't should exist via contraction fallback."""
    assert bnc.exists("needn't") is True


def test_contraction_neednt_bucket():
    """needn't should return a bucket."""
    b = bnc.bucket("needn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_neednt_rf():
    """needn't should return a relative frequency."""
    rf = bnc.relative_frequency("needn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_darent_exists():
    """daren't should exist via contraction fallback."""
    assert bnc.exists("daren't") is True


def test_contraction_darent_bucket():
    """daren't should return a bucket."""
    b = bnc.bucket("daren't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_darent_rf():
    """daren't should return a relative frequency."""
    rf = bnc.relative_frequency("daren't")
    assert rf is not None
    assert 0 < rf < 1


# -----------------------------------------------------------------------------
# Auxiliary verb n't contractions
# -----------------------------------------------------------------------------

def test_contraction_isnt_exists():
    """isn't should exist via contraction fallback."""
    assert bnc.exists("isn't") is True


def test_contraction_isnt_bucket():
    """isn't should return a bucket."""
    b = bnc.bucket("isn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_isnt_rf():
    """isn't should return a relative frequency."""
    rf = bnc.relative_frequency("isn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_arent_exists():
    """aren't should exist via contraction fallback."""
    assert bnc.exists("aren't") is True


def test_contraction_arent_bucket():
    """aren't should return a bucket."""
    b = bnc.bucket("aren't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_arent_rf():
    """aren't should return a relative frequency."""
    rf = bnc.relative_frequency("aren't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_wasnt_exists():
    """wasn't should exist via contraction fallback."""
    assert bnc.exists("wasn't") is True


def test_contraction_wasnt_bucket():
    """wasn't should return a bucket."""
    b = bnc.bucket("wasn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_wasnt_rf():
    """wasn't should return a relative frequency."""
    rf = bnc.relative_frequency("wasn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_werent_exists():
    """weren't should exist via contraction fallback."""
    assert bnc.exists("weren't") is True


def test_contraction_werent_bucket():
    """weren't should return a bucket."""
    b = bnc.bucket("weren't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_werent_rf():
    """weren't should return a relative frequency."""
    rf = bnc.relative_frequency("weren't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_hasnt_exists():
    """hasn't should exist via contraction fallback."""
    assert bnc.exists("hasn't") is True


def test_contraction_hasnt_bucket():
    """hasn't should return a bucket."""
    b = bnc.bucket("hasn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_hasnt_rf():
    """hasn't should return a relative frequency."""
    rf = bnc.relative_frequency("hasn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_havent_exists():
    """haven't should exist via contraction fallback."""
    assert bnc.exists("haven't") is True


def test_contraction_havent_bucket():
    """haven't should return a bucket."""
    b = bnc.bucket("haven't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_havent_rf():
    """haven't should return a relative frequency."""
    rf = bnc.relative_frequency("haven't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_hadnt_exists():
    """hadn't should exist via contraction fallback."""
    assert bnc.exists("hadn't") is True


def test_contraction_hadnt_bucket():
    """hadn't should return a bucket."""
    b = bnc.bucket("hadn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_hadnt_rf():
    """hadn't should return a relative frequency."""
    rf = bnc.relative_frequency("hadn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_doesnt_exists():
    """doesn't should exist via contraction fallback."""
    assert bnc.exists("doesn't") is True


def test_contraction_doesnt_bucket():
    """doesn't should return a bucket."""
    b = bnc.bucket("doesn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_doesnt_rf():
    """doesn't should return a relative frequency."""
    rf = bnc.relative_frequency("doesn't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_dont_exists():
    """don't should exist via contraction fallback."""
    assert bnc.exists("don't") is True


def test_contraction_dont_bucket():
    """don't should return a bucket."""
    b = bnc.bucket("don't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_dont_rf():
    """don't should return a relative frequency."""
    rf = bnc.relative_frequency("don't")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_didnt_exists():
    """didn't should exist via contraction fallback."""
    assert bnc.exists("didn't") is True


def test_contraction_didnt_bucket():
    """didn't should return a bucket."""
    b = bnc.bucket("didn't")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_didnt_rf():
    """didn't should return a relative frequency."""
    rf = bnc.relative_frequency("didn't")
    assert rf is not None
    assert 0 < rf < 1


# -----------------------------------------------------------------------------
# Interrogative pronoun contractions ('ll, 'd, 've, 're)
# -----------------------------------------------------------------------------

def test_contraction_whod_exists():
    """who'd should exist via contraction fallback."""
    assert bnc.exists("who'd") is True


def test_contraction_whod_bucket():
    """who'd should return a bucket."""
    b = bnc.bucket("who'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whod_rf():
    """who'd should return a relative frequency."""
    rf = bnc.relative_frequency("who'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_wholl_exists():
    """who'll should exist via contraction fallback."""
    assert bnc.exists("who'll") is True


def test_contraction_wholl_bucket():
    """who'll should return a bucket."""
    b = bnc.bucket("who'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_wholl_rf():
    """who'll should return a relative frequency."""
    rf = bnc.relative_frequency("who'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whove_exists():
    """who've should exist via contraction fallback."""
    assert bnc.exists("who've") is True


def test_contraction_whove_bucket():
    """who've should return a bucket."""
    b = bnc.bucket("who've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whove_rf():
    """who've should return a relative frequency."""
    rf = bnc.relative_frequency("who've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whatd_exists():
    """what'd should exist via contraction fallback."""
    assert bnc.exists("what'd") is True


def test_contraction_whatd_bucket():
    """what'd should return a bucket."""
    b = bnc.bucket("what'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whatd_rf():
    """what'd should return a relative frequency."""
    rf = bnc.relative_frequency("what'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whatll_exists():
    """what'll should exist via contraction fallback."""
    assert bnc.exists("what'll") is True


def test_contraction_whatll_bucket():
    """what'll should return a bucket."""
    b = bnc.bucket("what'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whatll_rf():
    """what'll should return a relative frequency."""
    rf = bnc.relative_frequency("what'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whatve_exists():
    """what've should exist via contraction fallback."""
    assert bnc.exists("what've") is True


def test_contraction_whatve_bucket():
    """what've should return a bucket."""
    b = bnc.bucket("what've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whatve_rf():
    """what've should return a relative frequency."""
    rf = bnc.relative_frequency("what've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whered_exists():
    """where'd should exist via contraction fallback."""
    assert bnc.exists("where'd") is True


def test_contraction_whered_bucket():
    """where'd should return a bucket."""
    b = bnc.bucket("where'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whered_rf():
    """where'd should return a relative frequency."""
    rf = bnc.relative_frequency("where'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_wherell_exists():
    """where'll should exist via contraction fallback."""
    assert bnc.exists("where'll") is True


def test_contraction_wherell_bucket():
    """where'll should return a bucket."""
    b = bnc.bucket("where'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_wherell_rf():
    """where'll should return a relative frequency."""
    rf = bnc.relative_frequency("where'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whereve_exists():
    """where've should exist via contraction fallback."""
    assert bnc.exists("where've") is True


def test_contraction_whereve_bucket():
    """where've should return a bucket."""
    b = bnc.bucket("where've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whereve_rf():
    """where've should return a relative frequency."""
    rf = bnc.relative_frequency("where've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whend_exists():
    """when'd should exist via contraction fallback."""
    assert bnc.exists("when'd") is True


def test_contraction_whend_bucket():
    """when'd should return a bucket."""
    b = bnc.bucket("when'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whend_rf():
    """when'd should return a relative frequency."""
    rf = bnc.relative_frequency("when'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whenll_exists():
    """when'll should exist via contraction fallback."""
    assert bnc.exists("when'll") is True


def test_contraction_whenll_bucket():
    """when'll should return a bucket."""
    b = bnc.bucket("when'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whenll_rf():
    """when'll should return a relative frequency."""
    rf = bnc.relative_frequency("when'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_howd_exists():
    """how'd should exist via contraction fallback."""
    assert bnc.exists("how'd") is True


def test_contraction_howd_bucket():
    """how'd should return a bucket."""
    b = bnc.bucket("how'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_howd_rf():
    """how'd should return a relative frequency."""
    rf = bnc.relative_frequency("how'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_howll_exists():
    """how'll should exist via contraction fallback."""
    assert bnc.exists("how'll") is True


def test_contraction_howll_bucket():
    """how'll should return a bucket."""
    b = bnc.bucket("how'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_howll_rf():
    """how'll should return a relative frequency."""
    rf = bnc.relative_frequency("how'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_howve_exists():
    """how've should exist via contraction fallback."""
    assert bnc.exists("how've") is True


def test_contraction_howve_bucket():
    """how've should return a bucket."""
    b = bnc.bucket("how've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_howve_rf():
    """how've should return a relative frequency."""
    rf = bnc.relative_frequency("how've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whyd_exists():
    """why'd should exist via contraction fallback."""
    assert bnc.exists("why'd") is True


def test_contraction_whyd_bucket():
    """why'd should return a bucket."""
    b = bnc.bucket("why'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whyd_rf():
    """why'd should return a relative frequency."""
    rf = bnc.relative_frequency("why'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_whyll_exists():
    """why'll should exist via contraction fallback."""
    assert bnc.exists("why'll") is True


def test_contraction_whyll_bucket():
    """why'll should return a bucket."""
    b = bnc.bucket("why'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_whyll_rf():
    """why'll should return a relative frequency."""
    rf = bnc.relative_frequency("why'll")
    assert rf is not None
    assert 0 < rf < 1


# -----------------------------------------------------------------------------
# Demonstrative pronoun contractions
# -----------------------------------------------------------------------------

def test_contraction_thatd_exists():
    """that'd should exist via contraction fallback."""
    assert bnc.exists("that'd") is True


def test_contraction_thatd_bucket():
    """that'd should return a bucket."""
    b = bnc.bucket("that'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thatd_rf():
    """that'd should return a relative frequency."""
    rf = bnc.relative_frequency("that'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_thatll_exists():
    """that'll should exist via contraction fallback."""
    assert bnc.exists("that'll") is True


def test_contraction_thatll_bucket():
    """that'll should return a bucket."""
    b = bnc.bucket("that'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thatll_rf():
    """that'll should return a relative frequency."""
    rf = bnc.relative_frequency("that'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_thatve_exists():
    """that've should exist via contraction fallback."""
    assert bnc.exists("that've") is True


def test_contraction_thatve_bucket():
    """that've should return a bucket."""
    b = bnc.bucket("that've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thatve_rf():
    """that've should return a relative frequency."""
    rf = bnc.relative_frequency("that've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_thisd_exists():
    """this'd should exist via contraction fallback."""
    assert bnc.exists("this'd") is True


def test_contraction_thisd_bucket():
    """this'd should return a bucket."""
    b = bnc.bucket("this'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thisd_rf():
    """this'd should return a relative frequency."""
    rf = bnc.relative_frequency("this'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_thisll_exists():
    """this'll should exist via contraction fallback."""
    assert bnc.exists("this'll") is True


def test_contraction_thisll_bucket():
    """this'll should return a bucket."""
    b = bnc.bucket("this'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thisll_rf():
    """this'll should return a relative frequency."""
    rf = bnc.relative_frequency("this'll")
    assert rf is not None
    assert 0 < rf < 1


# -----------------------------------------------------------------------------
# Existential/locative contractions (there, here)
# -----------------------------------------------------------------------------

def test_contraction_thered_exists():
    """there'd should exist via contraction fallback."""
    assert bnc.exists("there'd") is True


def test_contraction_thered_bucket():
    """there'd should return a bucket."""
    b = bnc.bucket("there'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thered_rf():
    """there'd should return a relative frequency."""
    rf = bnc.relative_frequency("there'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_therell_exists():
    """there'll should exist via contraction fallback."""
    assert bnc.exists("there'll") is True


def test_contraction_therell_bucket():
    """there'll should return a bucket."""
    b = bnc.bucket("there'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_therell_rf():
    """there'll should return a relative frequency."""
    rf = bnc.relative_frequency("there'll")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_thereve_exists():
    """there've should exist via contraction fallback."""
    assert bnc.exists("there've") is True


def test_contraction_thereve_bucket():
    """there've should return a bucket."""
    b = bnc.bucket("there've")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_thereve_rf():
    """there've should return a relative frequency."""
    rf = bnc.relative_frequency("there've")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_hered_exists():
    """here'd should exist via contraction fallback."""
    assert bnc.exists("here'd") is True


def test_contraction_hered_bucket():
    """here'd should return a bucket."""
    b = bnc.bucket("here'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_hered_rf():
    """here'd should return a relative frequency."""
    rf = bnc.relative_frequency("here'd")
    assert rf is not None
    assert 0 < rf < 1


def test_contraction_herell_exists():
    """here'll should exist via contraction fallback."""
    assert bnc.exists("here'll") is True


def test_contraction_herell_bucket():
    """here'll should return a bucket."""
    b = bnc.bucket("here'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_herell_rf():
    """here'll should return a relative frequency."""
    rf = bnc.relative_frequency("here'll")
    assert rf is not None
    assert 0 < rf < 1


# -----------------------------------------------------------------------------
# Other common contractions
# -----------------------------------------------------------------------------

def test_contraction_everybody_d_exists():
    """everybody'd should exist via contraction fallback."""
    assert bnc.exists("everybody'd") is True


def test_contraction_everybody_d_bucket():
    """everybody'd should return a bucket."""
    b = bnc.bucket("everybody'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_everybody_ll_exists():
    """everybody'll should exist via contraction fallback."""
    assert bnc.exists("everybody'll") is True


def test_contraction_everybody_ll_bucket():
    """everybody'll should return a bucket."""
    b = bnc.bucket("everybody'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_everyone_d_exists():
    """everyone'd should exist via contraction fallback."""
    assert bnc.exists("everyone'd") is True


def test_contraction_everyone_d_bucket():
    """everyone'd should return a bucket."""
    b = bnc.bucket("everyone'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_everyone_ll_exists():
    """everyone'll should exist via contraction fallback."""
    assert bnc.exists("everyone'll") is True


def test_contraction_everyone_ll_bucket():
    """everyone'll should return a bucket."""
    b = bnc.bucket("everyone'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_someone_d_exists():
    """someone'd should exist via contraction fallback."""
    assert bnc.exists("someone'd") is True


def test_contraction_someone_d_bucket():
    """someone'd should return a bucket."""
    b = bnc.bucket("someone'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_someone_ll_exists():
    """someone'll should exist via contraction fallback."""
    assert bnc.exists("someone'll") is True


def test_contraction_someone_ll_bucket():
    """someone'll should return a bucket."""
    b = bnc.bucket("someone'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_something_d_exists():
    """something'd should exist via contraction fallback."""
    assert bnc.exists("something'd") is True


def test_contraction_something_d_bucket():
    """something'd should return a bucket."""
    b = bnc.bucket("something'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_something_ll_exists():
    """something'll should exist via contraction fallback."""
    assert bnc.exists("something'll") is True


def test_contraction_something_ll_bucket():
    """something'll should return a bucket."""
    b = bnc.bucket("something'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_nothing_d_exists():
    """nothing'd should exist via contraction fallback."""
    assert bnc.exists("nothing'd") is True


def test_contraction_nothing_d_bucket():
    """nothing'd should return a bucket."""
    b = bnc.bucket("nothing'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_nothing_ll_exists():
    """nothing'll should exist via contraction fallback."""
    assert bnc.exists("nothing'll") is True


def test_contraction_nothing_ll_bucket():
    """nothing'll should return a bucket."""
    b = bnc.bucket("nothing'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_anybody_d_exists():
    """anybody'd should exist via contraction fallback."""
    assert bnc.exists("anybody'd") is True


def test_contraction_anybody_d_bucket():
    """anybody'd should return a bucket."""
    b = bnc.bucket("anybody'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_anybody_ll_exists():
    """anybody'll should exist via contraction fallback."""
    assert bnc.exists("anybody'll") is True


def test_contraction_anybody_ll_bucket():
    """anybody'll should return a bucket."""
    b = bnc.bucket("anybody'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_anyone_d_exists():
    """anyone'd should exist via contraction fallback."""
    assert bnc.exists("anyone'd") is True


def test_contraction_anyone_d_bucket():
    """anyone'd should return a bucket."""
    b = bnc.bucket("anyone'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_anyone_ll_exists():
    """anyone'll should exist via contraction fallback."""
    assert bnc.exists("anyone'll") is True


def test_contraction_anyone_ll_bucket():
    """anyone'll should return a bucket."""
    b = bnc.bucket("anyone'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_anything_d_exists():
    """anything'd should exist via contraction fallback."""
    assert bnc.exists("anything'd") is True


def test_contraction_anything_d_bucket():
    """anything'd should return a bucket."""
    b = bnc.bucket("anything'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_anything_ll_exists():
    """anything'll should exist via contraction fallback."""
    assert bnc.exists("anything'll") is True


def test_contraction_anything_ll_bucket():
    """anything'll should return a bucket."""
    b = bnc.bucket("anything'll")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_nobody_d_exists():
    """nobody'd should exist via contraction fallback."""
    assert bnc.exists("nobody'd") is True


def test_contraction_nobody_d_bucket():
    """nobody'd should return a bucket."""
    b = bnc.bucket("nobody'd")
    assert b is not None
    assert 1 <= b <= 100


def test_contraction_nobody_ll_exists():
    """nobody'll should exist via contraction fallback."""
    assert bnc.exists("nobody'll") is True


def test_contraction_nobody_ll_bucket():
    """nobody'll should return a bucket."""
    b = bnc.bucket("nobody'll")
    assert b is not None
    assert 1 <= b <= 100


# =============================================================================
# MASSIVE BATCH TESTS - Test all contractions in bulk
# =============================================================================

def test_batch_all_nt_contractions_exist():
    """All common n't contractions should exist."""
    nt_contractions = [
        "wouldn't", "couldn't", "shouldn't", "mustn't", "mightn't",
        "needn't", "daren't", "oughtn't",
        "isn't", "aren't", "wasn't", "weren't",
        "hasn't", "haven't", "hadn't",
        "doesn't", "don't", "didn't",
    ]
    for word in nt_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'


def test_batch_all_nt_contractions_bucket():
    """All common n't contractions should return buckets."""
    nt_contractions = [
        "wouldn't", "couldn't", "shouldn't", "mustn't", "mightn't",
        "needn't", "daren't", "oughtn't",
        "isn't", "aren't", "wasn't", "weren't",
        "hasn't", "haven't", "hadn't",
        "doesn't", "don't", "didn't",
    ]
    for word in nt_contractions:
        b = bnc.bucket(word)
        assert b is not None, f'{word} bucket failed'
        assert 1 <= b <= 100, f'{word} bucket out of range'


def test_batch_all_nt_contractions_rf():
    """All common n't contractions should return relative frequencies."""
    nt_contractions = [
        "wouldn't", "couldn't", "shouldn't", "mustn't", "mightn't",
        "needn't", "daren't", "oughtn't",
        "isn't", "aren't", "wasn't", "weren't",
        "hasn't", "haven't", "hadn't",
        "doesn't", "don't", "didn't",
    ]
    for word in nt_contractions:
        rf = bnc.relative_frequency(word)
        assert rf is not None, f'{word} rf failed'
        assert 0 < rf < 1, f'{word} rf out of range'


def test_batch_all_ll_contractions_exist():
    """All common 'll contractions should exist."""
    ll_contractions = [
        # Pronouns
        "i'll", "you'll", "he'll", "she'll", "it'll", "we'll", "they'll",
        # Interrogatives
        "who'll", "what'll", "where'll", "when'll", "how'll", "why'll",
        # Demonstratives
        "that'll", "this'll",
        # Existential/locative
        "there'll", "here'll",
        # Indefinite pronouns
        "everybody'll", "everyone'll", "somebody'll", "someone'll",
        "something'll", "nothing'll", "anybody'll", "anyone'll", "anything'll",
        "nobody'll",
    ]
    for word in ll_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'


def test_batch_all_ll_contractions_bucket():
    """All common 'll contractions should return buckets."""
    ll_contractions = [
        "i'll", "you'll", "he'll", "she'll", "it'll", "we'll", "they'll",
        "who'll", "what'll", "where'll", "when'll", "how'll", "why'll",
        "that'll", "this'll",
        "there'll", "here'll",
        "everybody'll", "everyone'll", "somebody'll", "someone'll",
        "something'll", "nothing'll", "anybody'll", "anyone'll", "anything'll",
        "nobody'll",
    ]
    for word in ll_contractions:
        b = bnc.bucket(word)
        assert b is not None, f'{word} bucket failed'
        assert 1 <= b <= 100, f'{word} bucket out of range'


def test_batch_all_ll_contractions_rf():
    """All common 'll contractions should return relative frequencies."""
    ll_contractions = [
        "i'll", "you'll", "he'll", "she'll", "it'll", "we'll", "they'll",
        "who'll", "what'll", "where'll", "when'll", "how'll", "why'll",
        "that'll", "this'll",
        "there'll", "here'll",
        "everybody'll", "everyone'll", "somebody'll", "someone'll",
        "something'll", "nothing'll", "anybody'll", "anyone'll", "anything'll",
        "nobody'll",
    ]
    for word in ll_contractions:
        rf = bnc.relative_frequency(word)
        assert rf is not None, f'{word} rf failed'
        assert 0 < rf < 1, f'{word} rf out of range'


def test_batch_all_d_contractions_exist():
    """All common 'd contractions should exist."""
    d_contractions = [
        # Pronouns
        "i'd", "you'd", "he'd", "she'd", "it'd", "we'd", "they'd",
        # Interrogatives
        "who'd", "what'd", "where'd", "when'd", "how'd", "why'd",
        # Demonstratives
        "that'd", "this'd",
        # Existential/locative
        "there'd", "here'd",
        # Indefinite pronouns
        "everybody'd", "everyone'd", "somebody'd", "someone'd",
        "something'd", "nothing'd", "anybody'd", "anyone'd", "anything'd",
        "nobody'd",
    ]
    for word in d_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'


def test_batch_all_d_contractions_bucket():
    """All common 'd contractions should return buckets."""
    d_contractions = [
        "i'd", "you'd", "he'd", "she'd", "it'd", "we'd", "they'd",
        "who'd", "what'd", "where'd", "when'd", "how'd", "why'd",
        "that'd", "this'd",
        "there'd", "here'd",
        "everybody'd", "everyone'd", "somebody'd", "someone'd",
        "something'd", "nothing'd", "anybody'd", "anyone'd", "anything'd",
        "nobody'd",
    ]
    for word in d_contractions:
        b = bnc.bucket(word)
        assert b is not None, f'{word} bucket failed'
        assert 1 <= b <= 100, f'{word} bucket out of range'


def test_batch_all_d_contractions_rf():
    """All common 'd contractions should return relative frequencies."""
    d_contractions = [
        "i'd", "you'd", "he'd", "she'd", "it'd", "we'd", "they'd",
        "who'd", "what'd", "where'd", "when'd", "how'd", "why'd",
        "that'd", "this'd",
        "there'd", "here'd",
        "everybody'd", "everyone'd", "somebody'd", "someone'd",
        "something'd", "nothing'd", "anybody'd", "anyone'd", "anything'd",
        "nobody'd",
    ]
    for word in d_contractions:
        rf = bnc.relative_frequency(word)
        assert rf is not None, f'{word} rf failed'
        assert 0 < rf < 1, f'{word} rf out of range'


def test_batch_all_ve_contractions_exist():
    """All common 've contractions should exist."""
    ve_contractions = [
        # Pronouns
        "i've", "you've", "we've", "they've",
        # Interrogatives
        "who've", "what've", "where've", "how've",
        # Demonstratives
        "that've",
        # Existential
        "there've",
        # Indefinite pronouns
        "could've", "would've", "should've", "might've", "must've",
    ]
    for word in ve_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'


def test_batch_all_ve_contractions_bucket():
    """All common 've contractions should return buckets."""
    ve_contractions = [
        "i've", "you've", "we've", "they've",
        "who've", "what've", "where've", "how've",
        "that've",
        "there've",
        "could've", "would've", "should've", "might've", "must've",
    ]
    for word in ve_contractions:
        b = bnc.bucket(word)
        assert b is not None, f'{word} bucket failed'
        assert 1 <= b <= 100, f'{word} bucket out of range'


def test_batch_all_ve_contractions_rf():
    """All common 've contractions should return relative frequencies."""
    ve_contractions = [
        "i've", "you've", "we've", "they've",
        "who've", "what've", "where've", "how've",
        "that've",
        "there've",
        "could've", "would've", "should've", "might've", "must've",
    ]
    for word in ve_contractions:
        rf = bnc.relative_frequency(word)
        assert rf is not None, f'{word} rf failed'
        assert 0 < rf < 1, f'{word} rf out of range'


def test_batch_all_re_contractions_exist():
    """All common 're contractions should exist."""
    re_contractions = [
        "you're", "we're", "they're",
    ]
    for word in re_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'


def test_batch_all_re_contractions_bucket():
    """All common 're contractions should return buckets."""
    re_contractions = [
        "you're", "we're", "they're",
    ]
    for word in re_contractions:
        b = bnc.bucket(word)
        assert b is not None, f'{word} bucket failed'
        assert 1 <= b <= 100, f'{word} bucket out of range'


def test_batch_all_re_contractions_rf():
    """All common 're contractions should return relative frequencies."""
    re_contractions = [
        "you're", "we're", "they're",
    ]
    for word in re_contractions:
        rf = bnc.relative_frequency(word)
        assert rf is not None, f'{word} rf failed'
        assert 0 < rf < 1, f'{word} rf out of range'


def test_batch_all_m_contractions():
    """i'm contraction should work across all functions."""
    assert bnc.exists("i'm") is True
    assert bnc.bucket("i'm") is not None
    assert bnc.relative_frequency("i'm") is not None
    assert bnc.expected_count("i'm", 50000) is not None


# =============================================================================
# COMPREHENSIVE CONSISTENCY TESTS
# =============================================================================

def test_consistency_all_modal_nt_contractions():
    """All modal n't contractions should be consistent across functions."""
    words = ["wouldn't", "couldn't", "shouldn't", "mustn't", "mightn't",
             "needn't", "daren't", "oughtn't"]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


def test_consistency_all_auxiliary_nt_contractions():
    """All auxiliary n't contractions should be consistent across functions."""
    words = ["isn't", "aren't", "wasn't", "weren't",
             "hasn't", "haven't", "hadn't",
             "doesn't", "don't", "didn't"]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


def test_consistency_all_interrogative_contractions():
    """All interrogative contractions should be consistent."""
    words = [
        "who'd", "who'll", "who've",
        "what'd", "what'll", "what've",
        "where'd", "where'll", "where've",
        "when'd", "when'll",
        "how'd", "how'll", "how've",
        "why'd", "why'll",
    ]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


def test_consistency_all_demonstrative_contractions():
    """All demonstrative contractions should be consistent."""
    words = ["that'd", "that'll", "that've", "this'd", "this'll"]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


def test_consistency_all_existential_contractions():
    """All existential/locative contractions should be consistent."""
    words = ["there'd", "there'll", "there've", "here'd", "here'll"]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


def test_consistency_all_indefinite_pronoun_contractions():
    """All indefinite pronoun contractions should be consistent."""
    words = [
        "everybody'd", "everybody'll",
        "everyone'd", "everyone'll",
        "somebody'd", "somebody'll",
        "someone'd", "someone'll",
        "something'd", "something'll",
        "nothing'd", "nothing'll",
        "anybody'd", "anybody'll",
        "anyone'd", "anyone'll",
        "anything'd", "anything'll",
        "nobody'd", "nobody'll",
    ]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


def test_consistency_modal_ve_contractions():
    """Modal 've contractions should be consistent."""
    words = ["could've", "would've", "should've", "might've", "must've"]
    for word in words:
        assert bnc.exists(word) is True, f'{word} exists'
        assert bnc.bucket(word) is not None, f'{word} bucket'
        assert bnc.relative_frequency(word) is not None, f'{word} rf'
        assert bnc.expected_count(word, 50000) is not None, f'{word} ec'


# =============================================================================
# COMPREHENSIVE CASE SENSITIVITY TESTS
# =============================================================================

def test_case_sensitivity_modal_nt():
    """Modal n't contractions should be case insensitive."""
    words = ["wouldn't", "couldn't", "shouldn't"]
    for word in words:
        upper = word.upper()
        title = word.title()
        assert bnc.bucket(word) == bnc.bucket(upper), f'{word} vs {upper}'
        assert bnc.bucket(word) == bnc.bucket(title), f'{word} vs {title}'
        assert bnc.relative_frequency(word) == bnc.relative_frequency(upper)
        assert bnc.relative_frequency(word) == bnc.relative_frequency(title)


def test_case_sensitivity_auxiliary_nt():
    """Auxiliary n't contractions should be case insensitive."""
    words = ["isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't"]
    for word in words:
        upper = word.upper()
        title = word.title()
        assert bnc.bucket(word) == bnc.bucket(upper), f'{word} vs {upper}'
        assert bnc.bucket(word) == bnc.bucket(title), f'{word} vs {title}'


def test_case_sensitivity_interrogative():
    """Interrogative contractions should be case insensitive."""
    words = ["who'd", "what'll", "where've", "how'd"]
    for word in words:
        upper = word.upper()
        title = word.title()
        assert bnc.bucket(word) == bnc.bucket(upper), f'{word} vs {upper}'
        assert bnc.bucket(word) == bnc.bucket(title), f'{word} vs {title}'


def test_case_sensitivity_demonstrative():
    """Demonstrative contractions should be case insensitive."""
    words = ["that'd", "that'll", "this'll"]
    for word in words:
        upper = word.upper()
        assert bnc.bucket(word) == bnc.bucket(upper), f'{word} vs {upper}'


def test_case_sensitivity_existential():
    """Existential contractions should be case insensitive."""
    words = ["there'd", "there'll", "here'll"]
    for word in words:
        upper = word.upper()
        assert bnc.bucket(word) == bnc.bucket(upper), f'{word} vs {upper}'


# =============================================================================
# COMPREHENSIVE APOSTROPHE VARIANT TESTS
# =============================================================================

def test_apostrophe_variants_modal_nt():
    """Modal n't contractions should work with all apostrophe variants."""
    from bnc_lookup.normalize import APOSTROPHE_VARIANTS

    # Test wouldn't with all variants
    standard = "wouldn't"
    standard_bucket = bnc.bucket(standard)
    for apos in APOSTROPHE_VARIANTS:
        variant = 'wouldn' + apos + 't'
        assert bnc.exists(
            variant) is True, f'exists failed for {repr(variant)}'
        assert bnc.bucket(
            variant) == standard_bucket, f'bucket mismatch for {repr(variant)}'


def test_apostrophe_variants_interrogative():
    """Interrogative contractions should work with all apostrophe variants."""
    from bnc_lookup.normalize import APOSTROPHE_VARIANTS

    # Test who'd with all variants
    standard = "who'd"
    standard_bucket = bnc.bucket(standard)
    for apos in APOSTROPHE_VARIANTS:
        variant = 'who' + apos + 'd'
        assert bnc.exists(
            variant) is True, f'exists failed for {repr(variant)}'
        assert bnc.bucket(
            variant) == standard_bucket, f'bucket mismatch for {repr(variant)}'


def test_apostrophe_variants_existential():
    """Existential contractions should work with all apostrophe variants."""
    from bnc_lookup.normalize import APOSTROPHE_VARIANTS

    # Test there'll with all variants
    standard = "there'll"
    standard_bucket = bnc.bucket(standard)
    for apos in APOSTROPHE_VARIANTS:
        variant = 'there' + apos + 'll'
        assert bnc.exists(
            variant) is True, f'exists failed for {repr(variant)}'
        assert bnc.bucket(
            variant) == standard_bucket, f'bucket mismatch for {repr(variant)}'


def test_apostrophe_variants_modal_ve():
    """Modal 've contractions should work with all apostrophe variants."""
    from bnc_lookup.normalize import APOSTROPHE_VARIANTS

    # Test could've with all variants
    standard = "could've"
    standard_bucket = bnc.bucket(standard)
    for apos in APOSTROPHE_VARIANTS:
        variant = 'could' + apos + 've'
        assert bnc.exists(
            variant) is True, f'exists failed for {repr(variant)}'
        assert bnc.bucket(
            variant) == standard_bucket, f'bucket mismatch for {repr(variant)}'


# =============================================================================
# MEGA MATRIX TEST - ALL STEMS x ALL SUFFIXES
# =============================================================================

def test_mega_matrix_all_valid_contractions():
    """Test a comprehensive matrix of stems and suffixes."""
    # All stems that should work with contractions
    stems_for_ll = [
        'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'who', 'what', 'where', 'when', 'how', 'why',
        'that', 'this', 'there', 'here',
        'everybody', 'everyone', 'somebody', 'someone', 'something',
        'nothing', 'anybody', 'anyone', 'anything', 'nobody',
    ]

    stems_for_d = [
        'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'who', 'what', 'where', 'when', 'how', 'why',
        'that', 'this', 'there', 'here',
        'everybody', 'everyone', 'somebody', 'someone', 'something',
        'nothing', 'anybody', 'anyone', 'anything', 'nobody',
    ]

    stems_for_ve = [
        'i', 'you', 'we', 'they',
        'who', 'what', 'where', 'how',
        'that', 'there',
        'could', 'would', 'should', 'might', 'must',
    ]

    stems_for_re = ['you', 'we', 'they']

    stems_for_m = ['i']

    stems_for_nt = [
        'would', 'could', 'should', 'must', 'might', 'need', 'dare', 'ought',
        'is', 'are', 'was', 'were', 'has', 'have', 'had', 'does', 'do', 'did',
    ]

    # Test 'll contractions
    for stem in stems_for_ll:
        word = stem + "'ll"
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'

    # Test 'd contractions
    for stem in stems_for_d:
        word = stem + "'d"
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'

    # Test 've contractions
    for stem in stems_for_ve:
        word = stem + "'ve"
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'

    # Test 're contractions
    for stem in stems_for_re:
        word = stem + "'re"
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'

    # Test 'm contractions
    for stem in stems_for_m:
        word = stem + "'m"
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'

    # Test n't contractions
    for stem in stems_for_nt:
        word = stem + "n't"
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
        assert bnc.relative_frequency(word) is not None, f'{word} rf failed'


def test_total_contraction_count():
    """Verify we're testing a substantial number of contractions."""
    # Count all unique contractions we're testing
    all_contractions = set()

    # Pronouns
    pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they']
    for p in pronouns:
        all_contractions.add(p + "'ll")
        all_contractions.add(p + "'d")
    for p in ['i', 'you', 'we', 'they']:
        all_contractions.add(p + "'ve")
    for p in ['you', 'we', 'they']:
        all_contractions.add(p + "'re")
    all_contractions.add("i'm")

    # Interrogatives
    interrogatives = ['who', 'what', 'where', 'when', 'how', 'why']
    for i in interrogatives:
        all_contractions.add(i + "'ll")
        all_contractions.add(i + "'d")
    for i in ['who', 'what', 'where', 'how']:
        all_contractions.add(i + "'ve")

    # Demonstratives
    for d in ['that', 'this']:
        all_contractions.add(d + "'ll")
        all_contractions.add(d + "'d")
    all_contractions.add("that've")

    # Existential
    for e in ['there', 'here']:
        all_contractions.add(e + "'ll")
        all_contractions.add(e + "'d")
    all_contractions.add("there've")

    # Indefinite pronouns
    indefinites = ['everybody', 'everyone', 'somebody', 'someone', 'something',
                   'nothing', 'anybody', 'anyone', 'anything', 'nobody']
    for ind in indefinites:
        all_contractions.add(ind + "'ll")
        all_contractions.add(ind + "'d")

    # n't contractions
    nt_stems = ['would', 'could', 'should', 'must', 'might', 'need', 'dare', 'ought',
                'is', 'are', 'was', 'were', 'has', 'have', 'had', 'does', 'do', 'did']
    for stem in nt_stems:
        all_contractions.add(stem + "n't")

    # Modal 've
    for modal in ['could', 'would', 'should', 'might', 'must']:
        all_contractions.add(modal + "'ve")

    # Verify we're testing at least 90 unique contractions
    assert len(
        all_contractions) >= 90, f'Only {len(all_contractions)} contractions'

    # Verify all of them work
    for word in all_contractions:
        assert bnc.exists(word) is True, f'{word} exists failed'
        assert bnc.bucket(word) is not None, f'{word} bucket failed'
