from bnc_lookup import is_bnc_term


def test_common_words_exist():
    assert is_bnc_term('the') is True
    assert is_bnc_term('of') is True
    assert is_bnc_term('and') is True
    assert is_bnc_term('is') is True


def test_case_insensitive():
    assert is_bnc_term('THE') is True
    assert is_bnc_term('The') is True


def test_nonexistent_words():
    assert is_bnc_term('xyzabc123') is False
    assert is_bnc_term('notarealword999') is False


def test_empty_input():
    assert is_bnc_term('') is False
