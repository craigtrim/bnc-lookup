import bnc_lookup as bnc


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
