# API Documentation

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Frequency Buckets](#frequency-buckets)
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

Import the module and use the two main functions:

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

### How Buckets Are Calculated

1. All 669,417 unique words are sorted by corpus frequency
2. Words are divided into 100 equal groups (~6,694 per bucket)
3. Bucket 1 contains the top 1% most frequent words
4. Bucket 100 contains the bottom 1% least frequent words

## Advanced Usage

For more control, you can use the classes directly:

```python
from bnc_lookup import FindBnc, FindFreq

# Existence checking
finder = FindBnc()
exists = finder.exists('however')

# Frequency lookup
freq = FindFreq()
bucket = freq.bucket('however')
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

### Comparison with Traditional Corpus Access

Traditional corpus interfaces require:
- Database connections or file I/O
- NLTK corpus downloads
- Multiple filesystem lookups
- Parsing overhead

`bnc-lookup` eliminates all of these by using pre-compiled static dictionaries.

## How It Works

### Architecture

1. **Hash-Based Storage**: BNC terms are stored as MD5 hash suffixes in 256 buckets
2. **Bucket Routing**: The first 2 hex characters of the hash determine the bucket (00-ff)
3. **Lazy Loading**: Hash modules are imported on-demand and cached
4. **Plural Handling**: If a word isn't found and ends with 's', the singular form is checked
5. **Case Insensitive**: All inputs are normalized to lowercase

### Storage Structure

**Existence checking** (`bnc_lookup/hs/`):
- 256 files (h_00.py through h_ff.py)
- Each contains a `frozenset` of hash suffixes
- O(1) membership testing

**Frequency buckets** (`bnc_lookup/freq/`):
- 256 files (f_00.py through f_ff.py)
- Each contains a `dict` mapping hash suffix → bucket number
- O(1) lookup

### Lookup Flow

```python
# When you call: bnc.exists('Hello')

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

The hash files are pre-compiled from the BNC frequency list (669,417 unique word forms).

For detailed implementation notes, see [IMPLEMENTATION.md](IMPLEMENTATION.md).

## Project Structure

```
bnc-lookup/
├── bnc_lookup/
│   ├── __init__.py           # Main API: exists(), bucket()
│   ├── find_bnc.py           # Existence lookup logic
│   ├── find_freq.py          # Frequency bucket lookup logic
│   ├── hs/                   # Hash storage (256 files)
│   │   ├── __init__.py
│   │   ├── h_00.py           # Hashes with prefix '00'
│   │   └── ...               # Through 'ff'
│   └── freq/                 # Frequency buckets (256 files)
│       ├── __init__.py
│       ├── f_00.py           # Buckets with prefix '00'
│       └── ...               # Through 'ff'
├── builder/
│   ├── build_hash_files.py   # Generates hash files
│   ├── build_frequency_buckets.py  # Generates frequency files
│   └── all.num               # Source frequency list
├── tests/
│   └── bnc_lookup_test.py
├── docs/
│   ├── API.md                # This file
│   └── IMPLEMENTATION.md     # Technical deep-dive
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
# Regenerate hash files from BNC data
python builder/build_hash_files.py

# Regenerate frequency bucket files
python builder/build_frequency_buckets.py
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

## Contributing

Contributions are welcome! Please ensure:

1. All tests pass: `make test`
2. Code passes linting: `make linters`
3. Pre-commit hooks are satisfied

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
