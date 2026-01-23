from bnc_lookup.find_bnc import FindBnc


def is_bnc_term(input_text: str) -> bool:
    return FindBnc().exists(input_text)
