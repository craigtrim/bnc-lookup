# BNC Lookup

[![PyPI version](https://badge.fury.io/py/bnc-lookup.svg)](https://badge.fury.io/py/bnc-lookup)
[![Downloads](https://pepy.tech/badge/bnc-lookup)](https://pepy.tech/project/bnc-lookup)
[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-19%20passed-brightgreen)]()

**Is this token a word? O(1) answer. No setup. No dependencies.**

A simple question deserves a simple answer. This library gives you instant yes/no validation against 669,000 word forms from the British National Corpus, plus frequency ranking.

## Quick Start

```bash
pip install bnc-lookup
```

```python
import bnc_lookup as bnc

# Check if a word exists
bnc.exists('the')          # True
bnc.exists('however')      # True
bnc.exists('xyzabc123')    # False

# Get frequency bucket (1=most common, 100=least common)
bnc.bucket('the')          # 1
bnc.bucket('python')       # 4
bnc.bucket('qwerty')       # 12
bnc.bucket('xyzabc123')    # None (not found)

# Handles plurals automatically
bnc.exists('computers')    # True
bnc.bucket('computers')    # 1

# Case insensitive
bnc.exists('THE')          # True
```

## Features

- **Zero Dependencies** - Pure Python, no external packages
- **Zero I/O** - No filesystem access, no database queries
- **Zero Setup** - No corpus downloads or configuration
- **Microsecond Lookups** - O(1) dictionary access
- **Smart Plurals** - Automatically checks singular forms
- **Frequency Ranking** - 100 buckets from most to least common
- **Simple API** - Two functions: `exists()` and `bucket()`

## The Problem This Solves

In NLP, you frequently need to answer the question: **"Is this token a real word?"**

Not "what does it mean?" Not "give me synonyms." Just: is this a word?

<table>
<tr>
<td align="center"><code>bnc.exists('computer')</code></td>
<td align="center"><code>bnc.exists('asdfgh')</code></td>
</tr>
<tr>
<td align="center"><img src="https://raw.githubusercontent.com/craigtrim/bnc-lookup/master/docs/images/yes-hot-dog.png" width="180"></td>
<td align="center"><img src="https://raw.githubusercontent.com/craigtrim/bnc-lookup/master/docs/images/not-hot-dog.png" width="180"></td>
</tr>
<tr>
<td align="center"><code>True</code></td>
<td align="center"><code>False</code></td>
</tr>
</table>

That's it. O(1) response. No ambiguity.

## Frequency Buckets

Words are ranked into 100 buckets based on their frequency in the BNC corpus:

| Bucket | Description | Examples |
|--------|-------------|----------|
| 1 | Most frequent (~6,700 words) | the, of, and, is, computer |
| 2-10 | Very common | algorithm, python, beautiful |
| 11-50 | Common | qwerty, specialized terms |
| 51-99 | Less common | Rare but valid words |
| 100 | Least frequent | Obscure terms |

```python
import bnc_lookup as bnc

# Filter by frequency
def is_common_word(word):
    bucket = bnc.bucket(word)
    return bucket is not None and bucket <= 10
```

## Why BNC?

The British National Corpus isn't an academic wordlist (too narrow). It's not a web scrape (too noisy). It's not slang (too ephemeral).

It's a **100-million-word corpus of real British English** collected from written and spoken sources between 1991-1994. Books, newspapers, academic papers, conversations. The BNC frequency list captures ~669,000 unique word forms actually used by native speakers.

If a token passes the BNC test, you can be confident it's a word that real people actually use.

## Real Words vs Dictionary Words

How much of real-world English is in the dictionary? We compared BNC against WordNet:

![BNC Vocabulary Zones by WordNet Coverage](https://raw.githubusercontent.com/craigtrim/bnc-lookup/master/docs/images/vocabulary_zones.png)

**93%** of common words (bucket 1-10) are in WordNet. But dictionaries miss proper nouns, technical terms, compounds, and domain jargon that appear constantly in real text.

That's the gap BNC fills. [Full analysis](https://github.com/craigtrim/bnc-lookup/issues/1)

## When to Use This

- **Tokenization filtering**: Keep real words, discard garbage
- **Input validation**: Reject nonsense in user input
- **NLP preprocessing**: Filter candidates before expensive operations
- **Spell-check pre-filtering**: Quick reject obvious non-words before fuzzy matching
- **Data cleaning**: Identify malformed or corrupted text
- **Frequency-based filtering**: Prefer common words over obscure ones

## What This Doesn't Do

- No definitions, synonyms, or semantic relationships (use spaCy for that)
- No spell-checking or suggestions (just existence check)
- No irregular plural handling ("mice" → "mouse")

## Documentation

For detailed usage, performance benchmarks, and advanced features, see the [API Documentation](https://github.com/craigtrim/bnc-lookup/blob/master/docs/API.md).

## Development

```bash
git clone https://github.com/craigtrim/bnc-lookup.git
cd bnc-lookup
make install  # Install dependencies
make test     # Run tests
make all      # Full build pipeline
```

See [API Documentation](https://github.com/craigtrim/bnc-lookup/blob/master/docs/API.md) for detailed development information.

## License

This package is dual-licensed:
- **Software**: MIT License
- **BNC Data**: BNC User Licence

See [LICENSE](https://github.com/craigtrim/bnc-lookup/blob/master/LICENSE) for complete terms.

## Attribution

This package contains data derived from the British National Corpus frequency lists:

> BNC frequency lists compiled by Adam Kilgarriff.
> Source: https://www.kilgarriff.co.uk/BNClists/all.num.gz
>
> The British National Corpus, version 3 (BNC XML Edition). 2007. Distributed by Bodleian Libraries, University of Oxford, on behalf of the BNC Consortium.

**Note:** This is a static snapshot of BNC frequency data. The data is not automatically updated.

## See Also

- **[wordnet-lookup](https://github.com/craigtrim/wordnet-lookup)** - Similar O(1) lookup using the WordNet lexicon
- **[BNC vs WordNet Analysis](https://github.com/craigtrim/bnc-lookup/issues/1)** - Deep dive on what each captures

## Links

- **Repository**: [github.com/craigtrim/bnc-lookup](https://github.com/craigtrim/bnc-lookup)
- **PyPI**: [pypi.org/project/bnc-lookup](https://pypi.org/project/bnc-lookup)
- **BNC**: [natcorp.ox.ac.uk](http://www.natcorp.ox.ac.uk)
- **Author**: Craig Trim ([craigtrim@gmail.com](mailto:craigtrim@gmail.com))
