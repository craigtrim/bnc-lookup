# API Documentation

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Relative Frequency](#relative-frequency)
- [Expected Count](#expected-count)
- [Frequency Buckets](#frequency-buckets)
- [Command-Line Interface](#command-line-interface)
- [Advanced Usage](#advanced-usage)
- [Performance](#performance)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Development](#development)

## Installation

```bash
pip install bnc-lookup
```

## Basic Usage

Import the module and use the main functions:

```python
import bnc_lookup as bnc

# Check if a word exists in BNC
bnc.exists('the')          # True
bnc.exists('however')      # True
bnc.exists('xyzabc123')    # False

# Get frequency bucket (1=most common, 100=least common)
bnc.bucket('the')          # 1
bnc.bucket('python')       # 4
bnc.bucket('xyzabc123')    # None

# Works with various forms
bnc.exists('computers')    # Handles plurals automatically
bnc.bucket('computers')    # Returns bucket for singular form
```

### Case Handling

All lookups are case-insensitive:

```python
bnc.exists('THE')     # True
bnc.exists('The')     # True
bnc.exists('the')     # True

bnc.bucket('THE')     # 1
bnc.bucket('The')     # 1
```

### Plural Detection

The library automatically handles common plural forms:

```python
# If 'computers' isn't found directly, checks 'computer'
bnc.exists('computers')    # True
bnc.bucket('computers')    # 1

# Works for most regular plurals
bnc.exists('databases')    # True
```

### Contraction Handling

The BNC corpus splits contractions into separate tokens ("don't" becomes "do" + "n't"). The joined forms exist as ghost entries with near-zero frequency. The library detects contractions and returns frequency data based on the stem components instead:

```python
# Without contraction fix, "don't" would return bucket 88 (ghost entry)
bnc.bucket("don't")     # 1 (based on "do" + "n't")
bnc.bucket("can't")     # 1
bnc.bucket("won't")     # 1
bnc.bucket("it's")      # 1 (based on "it" + "'s")

# Relative frequency reflects the stem, not the ghost entry
bnc.relative_frequency("don't")   # ~0.003 (not 1e-08)
```

Supported suffixes: `n't`, `'ll`, `'re`, `'ve`, `'m`, `'d`, `'s`.

The `'s` suffix is only split for known contractions (it's, he's, she's, that's, what's, etc.), not possessives (dog's, cat's). See [IMPLEMENTATION.md](IMPLEMENTATION.md) for the full allowlist and technical details.

## Relative Frequency

Get the precise relative frequency of a word in the BNC corpus (raw count / 100,106,029 total tokens):

```python
import bnc_lookup as bnc

bnc.relative_frequency('the')        # 0.0618 (6.18% of all tokens)
bnc.relative_frequency('python')     # 3.69e-06
bnc.relative_frequency('shimmered')  # 9.79e-07
bnc.relative_frequency('xyzabc123')  # None (not found)
```

This provides per-word precision for quantitative analysis, unlike `bucket()` which groups words into coarse tiers.

## Expected Count

Estimate how many times a word would appear in a text of a given length:

```python
import bnc_lookup as bnc

# How many times would "the" appear in a 50,000-word text?
bnc.expected_count('the', 50000)                  # 3090.7

# Rare words have fractional expected counts
bnc.expected_count('shimmered', 50000)             # 0.0489

# Use rounded=True for whole numbers
bnc.expected_count('the', 50000, rounded=True)     # 3091
bnc.expected_count('shimmered', 50000, rounded=True)  # 0

# Not found returns None
bnc.expected_count('xyzabc123', 50000)             # None
```

### Use Case: Stylometry

```python
import bnc_lookup as bnc

def overuse_ratio(word, observed_count, text_length):
    """How much more/less a word is used vs. expected."""
    expected = bnc.expected_count(word, text_length)
    if expected is None or expected == 0:
        return None
    return observed_count / expected

# Author uses "however" 15 times in a 10,000-word essay
overuse_ratio('however', 15, 10000)  # ~2.5x overuse
```

## Frequency Buckets

Words are ranked into 100 buckets based on corpus frequency:

| Bucket | Description | Word Count |
|--------|-------------|------------|
| 1 | Most frequent | ~6,700 |
| 2-10 | Very common | ~6,700 each |
| 11-50 | Common | ~6,700 each |
| 51-99 | Less common | ~6,700 each |
| 100 | Least frequent | ~6,700 |

### Usage Examples

```python
import bnc_lookup as bnc

# Filter by frequency
def is_common_word(word):
    bucket = bnc.bucket(word)
    return bucket is not None and bucket <= 10

# Prefer common words
def rank_words(words):
    return sorted(words, key=lambda w: bnc.bucket(w) or 101)

# Exclude rare words
tokens = ['the', 'computer', 'qwerty', 'xyzabc']
common = [t for t in tokens if (b := bnc.bucket(t)) and b <= 50]
```

### Words by Bucket

Retrieve all words in a given bucket or sample from it:

```python
import bnc_lookup as bnc

# Get all words in bucket 1 (most frequent)
words = bnc.words(1)       # tuple of ~6,700 words, sorted alphabetically

# Random sample from a bucket
sample = bnc.sample(1, 5)  # list of 5 random words from bucket 1
```

### How Buckets Are Calculated

1. All 669,417 unique words are sorted by corpus frequency
2. Words are divided into 100 equal groups (~6,694 per bucket)
3. Bucket 1 contains the top 1% most frequent words
4. Bucket 100 contains the bottom 1% least frequent words

## Command-Line Interface

After installation, four CLI commands are available:

```bash
# Check if a word exists (exit code 0=yes, 1=no)
bnc-exists the
# True

bnc-exists xyzabc123
# False

# Get frequency bucket
bnc-bucket python
# 4

# Get relative frequency
bnc-freq the
# 6.181373e-02

# Get expected count in a text of given length
bnc-expected the 50000
# 3090.6865

# With rounding
bnc-expected the 50000 --rounded
# 3091
```

## Advanced Usage

For more control, you can use the classes directly:

```python
from bnc_lookup import FindBnc, FindFreq, FindRF

# Existence checking
finder = FindBnc()
exists = finder.exists('however')

# Frequency lookup
freq = FindFreq()
bucket = freq.bucket('however')

# Relative frequency
rf = FindRF()
rel_freq = rf.relative_frequency('however')
expected = rf.expected_count('however', 50000)
```

### Batch Validation

```python
import bnc_lookup as bnc

words = ['alpha', 'beta', 'gamma', 'notaword']
valid_words = [word for word in words if bnc.exists(word)]
print(valid_words)  # ['alpha', 'beta', 'gamma']

# With frequency info
word_buckets = [(w, bnc.bucket(w)) for w in words]
# [('alpha', 1), ('beta', 1), ('gamma', 1), ('notaword', None)]
```

## Performance

The library is optimized for speed with zero I/O overhead:

### Benchmark Example

```python
import time
import bnc_lookup as bnc

# Single lookup benchmark
start = time.perf_counter()
result = bnc.exists('nonetheless')
elapsed = time.perf_counter() - start
print(f"Lookup time: {elapsed*1000:.6f}ms")  # Typically microseconds

# Batch lookup benchmark
words = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
start = time.perf_counter()
results = [bnc.exists(word) for word in words]
elapsed = time.perf_counter() - start
print(f"Batch lookup time: {elapsed*1000:.6f}ms for {len(words)} words")
```

### Performance Characteristics

- **Lookup Complexity**: O(1) - Direct dictionary access
- **Memory**: Lazy loading - only imports buckets when accessed
- **I/O Operations**: Zero - No file system or database access
- **Typical Latency**: Microseconds per lookup

## How It Works

### Architecture

1. **Hash-Based Storage**: BNC terms are stored as MD5 hash suffixes in 256 buckets
2. **Bucket Routing**: The first 2 hex characters of the hash determine the bucket (00-ff)
3. **Lazy Loading**: Hash modules are imported on-demand and cached
4. **Contraction Handling**: Contractions are split into components for accurate frequency data
5. **Plural Handling**: If a word isn't found and ends with 's', the singular form is checked
6. **Case Insensitive**: All inputs are normalized to lowercase

### Storage Structure

**Existence checking** (`bnc_lookup/hs/`):
- 256 files (h_00.py through h_ff.py)
- Each contains a `frozenset` of hash suffixes
- O(1) membership testing

**Frequency buckets** (`bnc_lookup/freq/`):
- 256 files (f_00.py through f_ff.py)
- Each contains a `dict` mapping hash suffix → bucket number
- O(1) lookup

**Relative frequencies** (`bnc_lookup/rf/`):
- 256 files (rf_00.py through rf_ff.py)
- Each contains a `dict` mapping hash suffix → relative frequency float
- O(1) lookup

**Bucket word lists** (`bnc_lookup/bw/`):
- 100 files (bw_01.py through bw_100.py)
- Each contains a sorted `tuple` of words in that bucket

### Lookup Flow

```
bnc.exists('Hello')

1. Normalize: 'Hello' -> 'hello'
2. Hash: MD5('hello') -> '5d4...592'
3. Split: prefix='5d', suffix='4...592'
4. Load bucket: import h_5d.py (if not cached)
5. Check: suffix in hashes_5d  # O(1) frozenset lookup
6. If not found and ends with 's':
   - Repeat for singular form
7. Return: True/False
```

### Data Source

The hash files are pre-compiled from the BNC frequency list (669,417 unique word forms across 100,106,029 tokens).

For detailed implementation notes, see [IMPLEMENTATION.md](IMPLEMENTATION.md).

## Project Structure

```
bnc-lookup/
├── bnc_lookup/
│   ├── __init__.py           # Public API
│   ├── cli.py                # Command-line interface
│   ├── find_bnc.py           # Word existence lookup
│   ├── find_freq.py          # Frequency bucket lookup
│   ├── find_rf.py            # Relative frequency lookup
│   ├── find_words.py         # Bucket-to-words reverse lookup
│   ├── hs/                   # Hash storage (256 files)
│   ├── freq/                 # Frequency buckets (256 files)
│   ├── rf/                   # Relative frequencies (256 files)
│   └── bw/                   # Bucket word lists (100 files)
├── builder/
│   ├── build_hash_files.py           # Generates hs/ files
│   ├── build_frequency_buckets.py    # Generates freq/ files
│   ├── build_relative_frequencies.py # Generates rf/ files
│   ├── build_bucket_words.py         # Generates bw/ files
│   └── all.num                       # Source BNC frequency list
├── tests/
│   └── bnc_lookup_test.py
├── docs/
│   ├── API.md                # This file
│   ├── IMPLEMENTATION.md     # Technical deep-dive
│   ├── FREQUENCY_EXAMPLES.md # Example words per bucket
│   └── WORDNET_COVERAGE.md   # BNC vs WordNet analysis
├── pyproject.toml            # Poetry configuration
├── Makefile                  # Build commands
└── README.md                 # Quick start guide
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/craigtrim/bnc-lookup.git
cd bnc-lookup

# Install dependencies
make install
```

### Running Tests

```bash
# Run tests
make test

# Run full build (install, test, lint, build)
make all
```

### Regenerating Data Files

```bash
python builder/build_hash_files.py            # Existence hashes
python builder/build_frequency_buckets.py     # Frequency buckets
python builder/build_bucket_words.py          # Bucket word lists
python builder/build_relative_frequencies.py  # Relative frequencies
```

### Code Quality

The project uses modern Python tooling:

- **Ruff**: Fast Python linter
- **Pre-commit**: Git hooks for code quality
- **Autopep8**: Code formatting
- **Pytest**: Testing framework

```bash
# Run linters
make linters

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

### Makefile Targets

```bash
make install   # Install dependencies
make test      # Run pytest
make linters   # Run ruff and autopep8
make build     # Build distribution
make publish   # Publish to PyPI
make all       # Full build pipeline
```

## Requirements

- Python 3.7+
- No external dependencies

## License

This package is dual-licensed:
- **Software**: MIT License
- **BNC Data**: BNC User Licence

See [LICENSE](../LICENSE) for complete terms.

### Attribution

This package contains data derived from the British National Corpus frequency lists:

> BNC frequency lists compiled by Adam Kilgarriff.
> Source: https://www.kilgarriff.co.uk/BNClists/all.num.gz
>
> The British National Corpus, version 3 (BNC XML Edition). 2007. Distributed by Bodleian Libraries, University of Oxford, on behalf of the BNC Consortium.

For more information about the BNC, visit [natcorp.ox.ac.uk](http://www.natcorp.ox.ac.uk)
