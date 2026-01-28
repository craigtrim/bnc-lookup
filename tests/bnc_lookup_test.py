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
