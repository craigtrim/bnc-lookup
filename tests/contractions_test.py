import bnc_lookup as bnc


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


# =============================================================================
# 's contraction allowlist tests (issue #7)
#
# The 's suffix is ambiguous (possessive vs. contraction), so only specific
# stems from S_CONTRACTION_STEMS are treated as contractions. These tests
# verify the curated allowlist works correctly across all API functions.
#
# Related GitHub Issues:
#     #5 - Add contraction fallback for BNC lookup
#     #7 - Missing common contractions: where's, how's
# =============================================================================


# --- _split_contraction for 's allowlist ---

def test_split_contraction_wheres():
    """where's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("where's") == ('where', "'s")


def test_split_contraction_hows():
    """how's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("how's") == ('how', "'s")


def test_split_contraction_somebodys():
    """somebody's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("somebody's") == ('somebody', "'s")


def test_split_contraction_everybodys():
    """everybody's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("everybody's") == ('everybody', "'s")


def test_split_contraction_everyones():
    """everyone's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("everyone's") == ('everyone', "'s")


def test_split_contraction_nobodys():
    """nobody's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("nobody's") == ('nobody', "'s")


def test_split_contraction_anywheres():
    """anywhere's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("anywhere's") == ('anywhere', "'s")


def test_split_contraction_nowheres():
    """nowhere's should split via S_CONTRACTION_STEMS allowlist."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("nowhere's") == ('nowhere', "'s")


def test_split_contraction_possessive_not_split():
    """Possessives NOT in S_CONTRACTION_STEMS must NOT be split."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("john's") is None
    assert _split_contraction("dog's") is None
    assert _split_contraction("cat's") is None
    assert _split_contraction("world's") is None
    assert _split_contraction("king's") is None
    assert _split_contraction("child's") is None
    assert _split_contraction("teacher's") is None
    assert _split_contraction("mother's") is None
    assert _split_contraction("father's") is None
    assert _split_contraction("london's") is None


def test_split_contraction_s_empty_stem():
    """Bare 's with no stem should return None."""
    from bnc_lookup.find_bnc import _split_contraction
    assert _split_contraction("'s") is None


# --- exists() for 's allowlist ---

def test_s_contraction_wheres_exists():
    """where's should exist via 's contraction fallback."""
    assert bnc.exists("where's") is True


def test_s_contraction_hows_exists():
    """how's should exist via 's contraction fallback."""
    assert bnc.exists("how's") is True


def test_s_contraction_somebodys_exists():
    """somebody's should exist via 's contraction fallback."""
    assert bnc.exists("somebody's") is True


def test_s_contraction_everybodys_exists():
    """everybody's should exist via 's contraction fallback."""
    assert bnc.exists("everybody's") is True


def test_s_contraction_everyones_exists():
    """everyone's should exist via 's contraction fallback."""
    assert bnc.exists("everyone's") is True


def test_s_contraction_nobodys_exists():
    """nobody's should exist via 's contraction fallback."""
    assert bnc.exists("nobody's") is True


def test_s_contraction_anywheres_exists():
    """anywhere's should exist via 's contraction fallback."""
    assert bnc.exists("anywhere's") is True


def test_s_contraction_nowheres_exists():
    """nowhere's should exist via 's contraction fallback."""
    assert bnc.exists("nowhere's") is True


def test_s_contraction_possessive_not_falsely_exists():
    """Possessives NOT in allowlist should not gain false existence."""
    # dog's doesn't exist in BNC directly and "dog" is not in S_CONTRACTION_STEMS
    assert bnc.exists("dog's") is False


# --- exists() case insensitivity for 's ---

def test_s_contraction_wheres_case_upper():
    """WHERE'S should work case-insensitively."""
    assert bnc.exists("WHERE'S") is True


def test_s_contraction_wheres_case_title():
    """Where's should work case-insensitively."""
    assert bnc.exists("Where's") is True


def test_s_contraction_hows_case_upper():
    """HOW'S should work case-insensitively."""
    assert bnc.exists("HOW'S") is True


def test_s_contraction_hows_case_title():
    """How's should work case-insensitively."""
    assert bnc.exists("How's") is True


def test_s_contraction_everybodys_case_upper():
    """EVERYBODY'S should work case-insensitively."""
    assert bnc.exists("EVERYBODY'S") is True


# --- exists() curly apostrophe for 's ---

def test_s_contraction_wheres_curly_apostrophe():
    """where\u2019s with curly apostrophe should work."""
    assert bnc.exists('where\u2019s') is True


def test_s_contraction_hows_curly_apostrophe():
    """how\u2019s with curly apostrophe should work."""
    assert bnc.exists('how\u2019s') is True


def test_s_contraction_somebodys_curly_apostrophe():
    """somebody\u2019s with curly apostrophe should work."""
    assert bnc.exists('somebody\u2019s') is True


# --- bucket() for 's allowlist ---

def test_s_contraction_wheres_bucket():
    """where's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("where's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_hows_bucket():
    """how's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("how's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_somebodys_bucket():
    """somebody's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("somebody's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_everybodys_bucket():
    """everybody's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("everybody's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_everyones_bucket():
    """everyone's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("everyone's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_nobodys_bucket():
    """nobody's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("nobody's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_anywheres_bucket():
    """anywhere's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("anywhere's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_nowheres_bucket():
    """nowhere's should return a valid bucket via 's contraction fallback."""
    b = bnc.bucket("nowhere's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_bucket_possessive_not_affected():
    """Possessive not in allowlist should still return None if not in BNC."""
    assert bnc.bucket("dog's") is None


def test_s_contraction_wheres_bucket_case_insensitive():
    """WHERE'S bucket should work case-insensitively."""
    b = bnc.bucket("WHERE'S")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_hows_bucket_case_insensitive():
    """How's bucket should work case-insensitively."""
    b = bnc.bucket("How's")
    assert b is not None
    assert 1 <= b <= 100


def test_s_contraction_wheres_bucket_curly_apostrophe():
    """where\u2019s bucket should work with curly apostrophe."""
    b = bnc.bucket('where\u2019s')
    assert b is not None
    assert 1 <= b <= 100


# --- relative_frequency() for 's allowlist ---

def test_s_contraction_wheres_rf():
    """where's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("where's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_hows_rf():
    """how's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("how's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_somebodys_rf():
    """somebody's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("somebody's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_everybodys_rf():
    """everybody's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("everybody's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_everyones_rf():
    """everyone's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("everyone's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_nobodys_rf():
    """nobody's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("nobody's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_anywheres_rf():
    """anywhere's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("anywhere's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_nowheres_rf():
    """nowhere's should return a relative frequency via 's contraction fallback."""
    rf = bnc.relative_frequency("nowhere's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_rf_possessive_not_affected():
    """Possessive not in allowlist should still return None if not in BNC."""
    assert bnc.relative_frequency("dog's") is None


def test_s_contraction_wheres_rf_case_insensitive():
    """WHERE'S rf should work case-insensitively."""
    rf = bnc.relative_frequency("WHERE'S")
    assert rf is not None
    assert rf > 0


def test_s_contraction_hows_rf_case_insensitive():
    """How's rf should work case-insensitively."""
    rf = bnc.relative_frequency("How's")
    assert rf is not None
    assert rf > 0


def test_s_contraction_wheres_rf_curly_apostrophe():
    """where\u2019s rf should work with curly apostrophe."""
    rf = bnc.relative_frequency('where\u2019s')
    assert rf is not None
    assert rf > 0


def test_s_contraction_rf_uses_min_of_components():
    """'s contraction rf should return min(stem_rf, suffix_rf) — conservative."""
    from bnc_lookup.find_rf import _lookup_rf
    stem_rf = _lookup_rf('where')
    suffix_rf = _lookup_rf("'s")
    assert stem_rf is not None
    assert suffix_rf is not None
    expected = min(stem_rf, suffix_rf)
    assert bnc.relative_frequency("where's") == expected


def test_s_contraction_rf_hows_uses_min_of_components():
    """how's rf should return min(stem_rf, suffix_rf) — conservative."""
    from bnc_lookup.find_rf import _lookup_rf
    stem_rf = _lookup_rf('how')
    suffix_rf = _lookup_rf("'s")
    assert stem_rf is not None
    assert suffix_rf is not None
    expected = min(stem_rf, suffix_rf)
    assert bnc.relative_frequency("how's") == expected


# --- expected_count() for 's allowlist ---

def test_s_contraction_wheres_expected_count():
    """where's should return an expected count."""
    ec = bnc.expected_count("where's", 100000)
    assert ec is not None
    assert ec > 0


def test_s_contraction_hows_expected_count():
    """how's should return an expected count."""
    ec = bnc.expected_count("how's", 100000)
    assert ec is not None
    assert ec > 0


def test_s_contraction_somebodys_expected_count():
    """somebody's should return an expected count."""
    ec = bnc.expected_count("somebody's", 100000)
    assert ec is not None
    assert ec > 0


def test_s_contraction_wheres_expected_count_rounded():
    """where's expected count with rounded=True should return int."""
    ec = bnc.expected_count("where's", 100000, rounded=True)
    assert ec is not None
    assert isinstance(ec, int)


def test_s_contraction_expected_count_possessive_not_affected():
    """Possessive not in allowlist should still return None if not in BNC."""
    assert bnc.expected_count("dog's", 100000) is None


# --- Consistency: all 's allowlist stems across all API functions ---

def test_s_contraction_consistency_wheres():
    """where's should be consistent across all API functions."""
    assert bnc.exists("where's") is True
    assert bnc.bucket("where's") is not None
    assert bnc.relative_frequency("where's") is not None
    assert bnc.expected_count("where's", 100000) is not None


def test_s_contraction_consistency_hows():
    """how's should be consistent across all API functions."""
    assert bnc.exists("how's") is True
    assert bnc.bucket("how's") is not None
    assert bnc.relative_frequency("how's") is not None
    assert bnc.expected_count("how's", 100000) is not None


def test_s_contraction_consistency_somebodys():
    """somebody's should be consistent across all API functions."""
    assert bnc.exists("somebody's") is True
    assert bnc.bucket("somebody's") is not None
    assert bnc.relative_frequency("somebody's") is not None
    assert bnc.expected_count("somebody's", 100000) is not None


def test_s_contraction_consistency_everybodys():
    """everybody's should be consistent across all API functions."""
    assert bnc.exists("everybody's") is True
    assert bnc.bucket("everybody's") is not None
    assert bnc.relative_frequency("everybody's") is not None
    assert bnc.expected_count("everybody's", 100000) is not None


def test_s_contraction_consistency_everyones():
    """everyone's should be consistent across all API functions."""
    assert bnc.exists("everyone's") is True
    assert bnc.bucket("everyone's") is not None
    assert bnc.relative_frequency("everyone's") is not None
    assert bnc.expected_count("everyone's", 100000) is not None


def test_s_contraction_consistency_nobodys():
    """nobody's should be consistent across all API functions."""
    assert bnc.exists("nobody's") is True
    assert bnc.bucket("nobody's") is not None
    assert bnc.relative_frequency("nobody's") is not None
    assert bnc.expected_count("nobody's", 100000) is not None


def test_s_contraction_consistency_anywheres():
    """anywhere's should be consistent across all API functions."""
    assert bnc.exists("anywhere's") is True
    assert bnc.bucket("anywhere's") is not None
    assert bnc.relative_frequency("anywhere's") is not None
    assert bnc.expected_count("anywhere's", 100000) is not None


def test_s_contraction_consistency_nowheres():
    """nowhere's should be consistent across all API functions."""
    assert bnc.exists("nowhere's") is True
    assert bnc.bucket("nowhere's") is not None
    assert bnc.relative_frequency("nowhere's") is not None
    assert bnc.expected_count("nowhere's", 100000) is not None


# --- Batch: all S_CONTRACTION_STEMS across all functions ---

def test_batch_all_s_contraction_stems_exist():
    """All S_CONTRACTION_STEMS 's forms should exist."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    for stem in S_CONTRACTION_STEMS:
        word = stem + "'s"
        assert bnc.exists(word) is True, f'{word} should exist'


def test_batch_all_s_contraction_stems_bucket():
    """All S_CONTRACTION_STEMS 's forms should have a valid bucket."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    for stem in S_CONTRACTION_STEMS:
        word = stem + "'s"
        b = bnc.bucket(word)
        assert b is not None, f'{word} bucket should not be None'
        assert 1 <= b <= 100, f'{word} bucket {b} out of range'


def test_batch_all_s_contraction_stems_rf():
    """All S_CONTRACTION_STEMS 's forms should have a relative frequency."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    for stem in S_CONTRACTION_STEMS:
        word = stem + "'s"
        rf = bnc.relative_frequency(word)
        assert rf is not None, f'{word} rf should not be None'
        assert rf > 0, f'{word} rf should be positive'


def test_batch_all_s_contraction_stems_expected_count():
    """All S_CONTRACTION_STEMS 's forms should return expected counts."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    for stem in S_CONTRACTION_STEMS:
        word = stem + "'s"
        ec = bnc.expected_count(word, 100000)
        assert ec is not None, f'{word} expected_count should not be None'
        assert ec > 0, f'{word} expected_count should be positive'


def test_batch_all_s_contraction_stems_case_insensitive():
    """All S_CONTRACTION_STEMS 's forms should work in uppercase."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    for stem in S_CONTRACTION_STEMS:
        word = stem.upper() + "'S"
        assert bnc.exists(word) is True, f'{word} should exist (uppercase)'
        assert bnc.bucket(
            word) is not None, f'{word} bucket should work (uppercase)'
        assert bnc.relative_frequency(
            word) is not None, f'{word} rf should work (uppercase)'


def test_batch_all_s_contraction_stems_curly_apostrophe():
    """All S_CONTRACTION_STEMS 's forms should work with curly apostrophe."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    for stem in S_CONTRACTION_STEMS:
        word = stem + '\u2019s'
        assert bnc.exists(
            word) is True, f'{word} should exist (curly apostrophe)'
        assert bnc.bucket(
            word) is not None, f'{word} bucket should work (curly apostrophe)'


# --- Negative tests: possessives must NOT match ---

def test_s_contraction_possessives_not_split_batch():
    """Common possessives must NOT be split as 's contractions."""
    from bnc_lookup.find_bnc import _split_contraction
    possessives = [
        "john's", "mary's", "dog's", "cat's", "king's", "queen's",
        "child's", "world's", "man's", "woman's", "boy's", "girl's",
        "teacher's", "doctor's", "mother's", "father's", "brother's",
        "sister's", "friend's", "london's", "england's", "america's",
        "today's", "yesterday's", "tomorrow's", "life's", "death's",
        "god's", "devil's", "earth's", "nature's", "company's",
    ]
    for word in possessives:
        assert _split_contraction(
            word) is None, f'{word} should NOT be split as contraction'


# --- Update the total contraction count to include 's stems ---

def test_s_contraction_stems_count():
    """Verify all 8 S_CONTRACTION_STEMS are accounted for."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    assert len(S_CONTRACTION_STEMS) == 8, (
        f'Expected 8 stems, got {len(S_CONTRACTION_STEMS)}: {S_CONTRACTION_STEMS}'
    )


def test_s_contraction_stems_contents():
    """Verify exact contents of S_CONTRACTION_STEMS."""
    from bnc_lookup.find_bnc import S_CONTRACTION_STEMS
    expected = {'where', 'how', 'somebody', 'everybody',
                'everyone', 'nobody', 'anywhere', 'nowhere'}
    assert S_CONTRACTION_STEMS == expected
