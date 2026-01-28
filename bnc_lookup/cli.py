#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Command-line interface for BNC Lookup.

Provides CLI access to all major API operations:
    bnc-exists <word>              Check if a word exists in BNC
    bnc-bucket <word>              Get frequency bucket (1-100)
    bnc-freq <word>                Get relative frequency
    bnc-expected <word> <length>   Get expected count in text of given length

All commands print results to stdout and exit with code 0 on success,
1 if the word is not found in BNC.
"""

import sys

import bnc_lookup as bnc


def exists():
    """CLI entry point: check if a word exists in BNC."""
    if len(sys.argv) < 2:
        print('Usage: bnc-exists <word>', file=sys.stderr)
        sys.exit(2)
    word = sys.argv[1]
    result = bnc.exists(word)
    print(str(result))
    sys.exit(0 if result else 1)


def bucket():
    """CLI entry point: get frequency bucket for a word."""
    if len(sys.argv) < 2:
        print('Usage: bnc-bucket <word>', file=sys.stderr)
        sys.exit(2)
    word = sys.argv[1]
    result = bnc.bucket(word)
    if result is None:
        print('None')
        sys.exit(1)
    print(result)


def freq():
    """CLI entry point: get relative frequency for a word."""
    if len(sys.argv) < 2:
        print('Usage: bnc-freq <word>', file=sys.stderr)
        sys.exit(2)
    word = sys.argv[1]
    result = bnc.relative_frequency(word)
    if result is None:
        print('None')
        sys.exit(1)
    print(f'{result:.6e}')


def expected():
    """CLI entry point: get expected count for a word in a text of given length."""
    if len(sys.argv) < 3:
        print(
            'Usage: bnc-expected <word> <text_length> [--rounded]', file=sys.stderr)
        sys.exit(2)
    word = sys.argv[1]
    try:
        text_length = int(sys.argv[2])
    except ValueError:
        print(
            f"Error: text_length must be an integer, got '{sys.argv[2]}'", file=sys.stderr)
        sys.exit(2)
    rounded = '--rounded' in sys.argv
    result = bnc.expected_count(word, text_length, rounded=rounded)
    if result is None:
        print('None')
        sys.exit(1)
    if rounded:
        print(result)
    else:
        print(f'{result:.4f}')
