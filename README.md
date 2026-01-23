# BNC Lookup

[![PyPI version](https://img.shields.io/pypi/v/bnc-lookup.svg)](https://pypi.org/project/bnc-lookup/)
[![PyPI downloads](https://img.shields.io/pypi/dm/bnc-lookup.svg)](https://pypi.org/project/bnc-lookup/)
[![Python versions](https://img.shields.io/pypi/pyversions/bnc-lookup.svg)](https://pypi.org/project/bnc-lookup/)
[![License](https://img.shields.io/badge/License-MIT%20%2B%20BNC-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/craigtrim/bnc-lookup)

**Is this token a word? O(1) answer. No setup. No dependencies.**

A simple question deserves a simple answer. This library gives you instant yes/no validation against 669,000 word forms from the British National Corpus.

## Quick Start

```bash
pip install bnc-lookup
```

```python
from bnc_lookup import is_bnc_term

# That's it. Start validating.
is_bnc_term('the')          # True
is_bnc_term('however')      # True
is_bnc_term('nonetheless')  # True
is_bnc_term('xyzabc123')    # False

# Handles plurals automatically
is_bnc_term('computers')    # True

# Case insensitive
is_bnc_term('THE')          # True
```

## Features

- **Zero Dependencies** - Pure Python, no external packages
- **Zero I/O** - No filesystem access, no database queries
- **Zero Setup** - No corpus downloads or configuration
- **Microsecond Lookups** - O(1) dictionary access
- **Smart Plurals** - Automatically checks singular forms
- **Simple API** - One function does it all

## The Problem This Solves

In NLP, you frequently need to answer the question: **"Is this token a real word?"**

Not "what does it mean?" Not "give me synonyms." Just: is this a word?

<table>
<tr>
<td align="center"><code>is_bnc_term('computer')</code></td>
<td align="center"><code>is_bnc_term('asdfgh')</code></td>
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

## Why BNC?

The British National Corpus isn't an academic wordlist (too narrow). It's not a web scrape (too noisy). It's not slang (too ephemeral).

It's a **100-million-word corpus of real British English** collected from written and spoken sources between 1991-1994. Books, newspapers, academic papers, conversations. The BNC frequency list captures ~669,000 unique word forms actually used by native speakers.

If a token passes the BNC test, you can be confident it's a word that real people actually use.

## When to Use This

- **Tokenization filtering**: Keep real words, discard garbage
- **Input validation**: Reject nonsense in user input
- **NLP preprocessing**: Filter candidates before expensive operations
- **Spell-check pre-filtering**: Quick reject obvious non-words before fuzzy matching
- **Data cleaning**: Identify malformed or corrupted text

## What This Doesn't Do

- No definitions, synonyms, or semantic relationships (use spaCy for that)
- No frequency counts or rankings (just yes/no)
- No spell-checking or suggestions (just existence check)

## Documentation

For detailed usage, performance benchmarks, and advanced features, see the [API Documentation](docs/API.md).

## Development

```bash
git clone https://github.com/craigtrim/bnc-lookup.git
cd bnc-lookup
make install  # Install dependencies
make test     # Run tests
make all      # Full build pipeline
```

See [API Documentation](docs/API.md) for detailed development information.

## License

This package is dual-licensed:
- **Software**: MIT License
- **BNC Data**: BNC User Licence

See [LICENSE](LICENSE) for complete terms.

## Attribution

This package contains data derived from the British National Corpus frequency lists:

> BNC frequency lists compiled by Adam Kilgarriff.
> Source: https://www.kilgarriff.co.uk/BNClists/all.num.gz
>
> The British National Corpus, version 3 (BNC XML Edition). 2007. Distributed by Bodleian Libraries, University of Oxford, on behalf of the BNC Consortium.

**Note:** This is a static snapshot of BNC frequency data. The data is not automatically updated.

## See Also

- **[wordnet-lookup](https://github.com/craigtrim/wordnet-lookup)** - Similar O(1) lookup using the WordNet lexicon

## Links

- **Repository**: [github.com/craigtrim/bnc-lookup](https://github.com/craigtrim/bnc-lookup)
- **PyPI**: [pypi.org/project/bnc-lookup](https://pypi.org/project/bnc-lookup)
- **BNC**: [natcorp.ox.ac.uk](http://www.natcorp.ox.ac.uk)
- **Author**: Craig Trim ([craigtrim@gmail.com](mailto:craigtrim@gmail.com))
