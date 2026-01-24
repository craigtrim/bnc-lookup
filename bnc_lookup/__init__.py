from bnc_lookup.find_bnc import FindBnc
from bnc_lookup.find_freq import FindFreq


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
