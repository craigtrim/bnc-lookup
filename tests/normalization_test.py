import bnc_lookup as bnc


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
