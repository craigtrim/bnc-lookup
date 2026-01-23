# API Documentation

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)
- [Direct Dictionary Access](#direct-dictionary-access)
- [Performance](#performance)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Development](#development)

## Installation

```bash
pip install bnc-lookup
```

## Basic Usage

The main interface is the `is_bnc_term()` function:

```python
from bnc_lookup import is_bnc_term

# Check if a word exists in BNC
is_bnc_term('the')          # True
is_bnc_term('however')      # True
is_bnc_term('nonetheless')  # True
is_bnc_term('xyzabc123')    # False

# Validate words
if is_bnc_term('according'):
    print("Valid BNC term")

# Works with various forms
is_bnc_term('computers')    # Handles plurals automatically
```

## Advanced Usage

For more control, you can use the `FindBnc` class directly:

```python
from bnc_lookup import FindBnc

finder = FindBnc()
exists = finder.exists('however')
```

### Batch Validation

```python
from bnc_lookup import is_bnc_term

words = ['alpha', 'beta', 'gamma', 'notaword']
valid_words = [word for word in words if is_bnc_term(word)]
print(valid_words)  # ['alpha', 'beta', 'gamma']
```

### Case Handling

All lookups are case-insensitive:

```python
is_bnc_term('THE')     # True
is_bnc_term('The')     # True
is_bnc_term('the')     # True
```

### Plural Detection

The library automatically handles common plural forms:

```python
# If 'computers' isn't found directly, checks 'computer'
is_bnc_term('computers')    # True

# Works for most regular plurals
is_bnc_term('databases')    # True
```

## Performance

The library is optimized for speed with zero I/O overhead. All lookups are performed against pre-compiled dictionaries:

### Benchmark Example

```python
import time
from bnc_lookup import is_bnc_term

# Single lookup benchmark
start = time.perf_counter()
result = is_bnc_term('nonetheless')
elapsed = time.perf_counter() - start
print(f"Lookup time: {elapsed*1000:.6f}ms")  # Typically microseconds

# Batch lookup benchmark
words = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
start = time.perf_counter()
results = [is_bnc_term(word) for word in words]
elapsed = time.perf_counter() - start
print(f"Batch lookup time: {elapsed*1000:.6f}ms for {len(words)} words")
```

### Performance Characteristics

- **Lookup Complexity**: O(1) - Direct dictionary access
- **Memory**: All dictionaries loaded at import (one-time cost)
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

1. **Hash-Based Storage**: BNC terms are stored as MD5 hash suffixes in 256 `frozenset` buckets
2. **Bucket Routing**: The first 2 hex characters of the hash determine the bucket (00-ff)
3. **Lazy Loading**: Hash modules are imported on-demand and cached
4. **Plural Handling**: If a word isn't found and ends with 's', the singular form is checked
5. **Case Insensitive**: All inputs are normalized to lowercase

### Lookup Flow

```python
# When you call: is_bnc_term('Hello')

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

The hash files are pre-compiled from the BNC frequency list (669,418 unique word forms).

For detailed implementation notes, see [IMPLEMENTATION.md](IMPLEMENTATION.md).

## Project Structure

```
bnc-lookup/
├── bnc_lookup/
│   ├── __init__.py           # Main API exports
│   ├── find_bnc.py           # Core lookup logic
│   └── hs/
│       ├── __init__.py       # Hash module exports
│       ├── h_00.py           # Hashes with prefix '00'
│       ├── h_01.py           # Hashes with prefix '01'
│       └── ...               # Through 'ff' (256 files)
├── builder/
│   ├── build_hash_files.py   # Generates hash files
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
