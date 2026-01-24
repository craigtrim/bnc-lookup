from bnc_lookup.find_bnc import FindBnc
from bnc_lookup.find_freq import FindFreq
from bnc_lookup.find_words import FindWords


def exists(input_text: str) -> bool:
    """Check if a word exists in the BNC corpus."""
    return FindBnc().exists(input_text)


def bucket(input_text: str) -> int | None:
    """
    Get frequency bucket for a word.

    Returns:
        1-100: Bucket number (1=most frequent, 100=least frequent)
        None: Word not found in BNC
    """
    return FindFreq().bucket(input_text)


def words(bucket: int) -> tuple:
    """
    Get all words in a frequency bucket.

    Args:
        bucket: Bucket number 1-100 (1=most frequent, 100=least frequent)

    Returns:
        Tuple of words in that bucket (alphabetically sorted)
    """
    return FindWords().by_bucket(bucket)


def sample(bucket: int, n: int = 10) -> list:
    """
    Get random sample of words from a bucket.

    Args:
        bucket: Bucket number 1-100
        n: Number of words to return (default 10)

    Returns:
        List of randomly sampled words
    """
    return FindWords().sample(bucket, n)
