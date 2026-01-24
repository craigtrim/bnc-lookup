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
