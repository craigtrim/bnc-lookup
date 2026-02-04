"""BNC Lookup - O(1) word validation and frequency data from the British National Corpus.

Provides instant word existence checking, frequency bucket ranking, and
per-word relative frequency data for 669,417 word forms from the BNC
(100,106,029 tokens across 4,124 documents).

Public API:
    exists(word)                          -> bool
    bucket(word)                          -> int | None
    words(bucket)                         -> tuple
    sample(bucket, n)                     -> list
    relative_frequency(word)              -> float | None
    expected_count(word, length, rounded) -> float | int | None

All lookups are case-insensitive with automatic plural fallback.
"""

from bnc_lookup.find_bnc import FindBnc
from bnc_lookup.find_freq import FindFreq
from bnc_lookup.find_rf import FindRF
from bnc_lookup.find_words import FindWords


def exists(input_text: str) -> bool:
    """Check if a word exists in the BNC corpus.

    Includes automatic fallbacks:
    - Plural fallback: "computers" → tries "computer"
    - Contraction fallback: "we'll" → checks "we" + "'ll" exist

    Args:
        input_text: The word to check.

    Returns:
        True if the word exists in the BNC (directly or via fallback).
    """
    return FindBnc().exists(input_text)


def bucket(input_text: str) -> int | None:
    """Get frequency bucket for a word.

    Args:
        input_text: The word to look up.

    Returns:
        1-100: Bucket number (1=most frequent, 100=least frequent)
        None: Word not found in BNC
    """
    return FindFreq().bucket(input_text)


def words(bucket: int) -> tuple:
    """Get all words in a frequency bucket.

    Args:
        bucket: Bucket number 1-100 (1=most frequent, 100=least frequent).

    Returns:
        Tuple of words in that bucket (alphabetically sorted).

    Raises:
        ValueError: If bucket is not in range 1-100.
    """
    return FindWords().by_bucket(bucket)


def sample(bucket: int, n: int = 10) -> list:
    """Get random sample of words from a bucket.

    Args:
        bucket: Bucket number 1-100.
        n: Number of words to return (default 10).

    Returns:
        List of randomly sampled words.

    Raises:
        ValueError: If bucket is not in range 1-100.
    """
    return FindWords().sample(bucket, n)


def relative_frequency(word: str) -> float | None:
    """Relative frequency of word in BNC (raw_count / corpus_size).

    Args:
        word: The word to look up.

    Returns:
        Float in range (0, 1), or None if word not in BNC.
    """
    return FindRF().relative_frequency(word)


def expected_count(word: str, text_length: int, rounded: bool = False) -> float | int | None:
    """Expected number of occurrences of a word in a text of given length.

    Based on the word's observed relative frequency in the BNC
    (100,106,029 tokens across 4,124 documents).

    Args:
        word: The word to look up.
        text_length: Length of the target text in tokens.
        rounded: If True, return a rounded integer.

    Returns:
        Expected count as a float (or int if rounded), or None if word not in BNC.
    """
    return FindRF().expected_count(word, text_length, rounded=rounded)
