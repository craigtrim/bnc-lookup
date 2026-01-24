# Implementation Notes

Technical deep-dive into the hash-based lookup system.

## Why Hashes?

A naive implementation might use alphabetically organized lists. This has two problems:

1. **O(n) lookups**: `in` on a Python list scans linearly
2. **Uneven distribution**: Some letters have far more entries than others

Hashing solves both: MD5 distributes uniformly across 256 buckets, and `frozenset` provides O(1) membership testing.

## Why MD5?

MD5 is:
- **Fast**: ~300ns per hash on modern hardware
- **Uniform**: Excellent distribution for non-cryptographic use
- **Sufficient**: Cryptographic weakness irrelevant for lookup tables

We only store the suffix (30 chars) after splitting on the 2-char prefix, saving ~6% space per entry.

## Why frozenset?

| Data Structure | Lookup | Memory | Mutability |
|---------------|--------|--------|------------|
| list | O(n) | Lower | Mutable |
| set | O(1) | Higher | Mutable |
| frozenset | O(1) | Higher | Immutable |

`frozenset` wins because:
- O(1) average-case lookup via hash table
- Immutability allows Python to optimize memory layout
- Hashable (can be used as dict keys if needed)

## Why 256 Buckets?

Two hex characters = 16 × 16 = 256 possible prefixes. This gives:
- ~2,615 entries per bucket on average (669,417 ÷ 256)
- Small enough files for fast imports
- Uniform distribution (MD5 property)

One hex character (16 buckets) = ~41,800 entries each = slower imports.
Three hex characters (4,096 buckets) = too many tiny files.

## Why Lazy Loading?

Eager loading imports all 256 modules at startup:
```python
from bnc_lookup.hs import hashes_00, hashes_01, ...  # 256 imports
```

Problems:
- Slow startup (~2s to load 669k strings)
- Memory for all 256 sets even if only a few are used

Lazy loading with caching:
```python
def _get_hash_set(prefix: str) -> frozenset:
    if prefix not in _cache:
        module = importlib.import_module(f'bnc_lookup.hs.h_{prefix}')
        _cache[prefix] = getattr(module, f'hashes_{prefix}')
    return _cache[prefix]
```

Benefits:
- Fast startup (near-zero)
- Only loads buckets actually accessed
- Cached after first access per prefix

## Hash Function

```python
def _calculate_md5(input_text: str) -> str:
    return hashlib.md5(input_text.lower().strip().encode()).hexdigest()
```

Input normalization:
- `.lower()`: Case-insensitive matching
- `.strip()`: Ignore leading/trailing whitespace
- `.encode()`: UTF-8 bytes for hashing

The same normalization is applied at build time and lookup time.

## Existence Lookup Flow

```
Input: "Hello"
    │
    ▼
Normalize: "hello"
    │
    ▼
MD5: "5d41402abc4b2a76b9719d911017c592"
    │
    ▼
Split: prefix="5d", suffix="41402abc4b2a76b9719d911017c592"
    │
    ▼
Load: importlib.import_module('bnc_lookup.hs.h_5d')
    │
    ▼
Check: "41402abc4b2a76b9719d911017c592" in hashes_5d
    │
    ▼
Return: True/False
```

## Frequency Bucket System

### Architecture

The frequency system uses the same 256-bucket pattern but stores bucket numbers (1-100) instead of just membership:

**Storage** (`bnc_lookup/freq/`):
- 256 files (f_00.py through f_ff.py)
- Each contains a `dict` mapping hash suffix → bucket number
- Same lazy loading pattern as existence checking

### Bucket Calculation

```python
# During build:
word_freqs.sort(key=lambda x: x[1], reverse=True)  # Sort by frequency
bucket_size = total_words / 100  # ~6,694 words per bucket

for idx, (word, freq) in enumerate(word_freqs):
    bucket = min(int(idx / bucket_size) + 1, 100)
    # Store: hash(word) -> bucket
```

This creates a percentile-based ranking:
- Bucket 1: Top 1% most frequent words
- Bucket 100: Bottom 1% least frequent words

### Why Percentile Buckets?

Word frequencies follow a Zipfian distribution (extremely skewed):
- "the": 6,187,927 occurrences
- Median word: ~100 occurrences
- Many words: 1 occurrence

Linear bucketing would put 99% of words in bucket 100. Percentile bucketing ensures:
- Equal word count per bucket (~6,694)
- Meaningful differentiation across the frequency spectrum

### Frequency Lookup Flow

```
Input: "python"
    │
    ▼
Normalize: "python"
    │
    ▼
MD5: "23eeeb4347bdd26bfc6b7ee9a3b755dd"
    │
    ▼
Split: prefix="23", suffix="eeeb4347bdd26bfc6b7ee9a3b755dd"
    │
    ▼
Load: importlib.import_module('bnc_lookup.freq.f_23')
    │
    ▼
Lookup: buckets_23.get(suffix)  # Returns 4
    │
    ▼
Return: 4
```

## Plural Handling

If the word ends with 's' and isn't found, try the singular:

```python
if input_text.endswith('s') and len(input_text) > 3:
    if _hash_exists(input_text[:-1]):
        return True
```

This catches regular plurals like "computers" → "computer".

Limitation: Doesn't handle irregular plurals ("mice" → "mouse").

## Build Process

### Existence Hash Files

The `builder/build_hash_files.py` script:

1. Reads `all.num` (BNC frequency list, space-delimited)
2. Extracts the word from each line (second column)
3. Hashes each word with MD5
4. Groups by first 2 hex chars of hash
5. Writes 256 Python files with `frozenset` literals
6. Generates `__init__.py` with imports

```python
# Example generated file: h_5d.py
hashes_5d = frozenset({
    '41402abc4b2a76b9719d911017c592',
    '8f14e45fceea167a5a36dedd4bea254',
    ...
})
```

### Frequency Bucket Files

The `builder/build_frequency_buckets.py` script:

1. Reads `all.num` and aggregates frequencies per word
2. Sorts by frequency (descending)
3. Assigns buckets 1-100 based on percentile
4. Hashes each word and groups by prefix
5. Writes 256 Python files with `dict` literals

```python
# Example generated file: f_5d.py
buckets_5d = {
    '41402abc4b2a76b9719d911017c592': 1,
    '8f14e45fceea167a5a36dedd4bea254': 23,
    ...
}
```

## Performance Characteristics

| Operation | Complexity | Typical Time |
|-----------|------------|--------------|
| Hash computation | O(n) string length | ~300ns |
| Bucket lookup | O(1) dict access | ~50ns |
| Set membership | O(1) average | ~50ns |
| Module import (cold) | O(n) entries | ~5ms |
| Module import (cached) | O(1) | ~50ns |

Total lookup time: ~400ns warm, ~5ms cold (first access to a bucket).

## Memory Usage

- Each hash suffix: 30 chars = ~80 bytes (Python string overhead)
- 669,417 entries × 80 bytes ≈ 53 MB if all loaded
- Lazy loading: Only used buckets in memory
- Typical usage: 10-50 buckets = 2-13 MB

### Frequency Storage Overhead

Each frequency bucket file stores suffix → int mappings:
- Same 30-char suffix keys
- Integer values (1-100): 28 bytes each in Python
- Total additional: ~19 MB if all loaded
- Same lazy loading benefits apply

## Collision Resistance

MD5 collision probability for 669k entries:

```
P(collision) ≈ n² / 2^129
            ≈ (669000)² / 2^129
            ≈ 10^-27
```

Effectively zero. And collisions would only cause false positives (saying a non-word exists), not false negatives.

## Why Not Bloom Filters?

Bloom filters are space-efficient probabilistic sets with false positives. They'd work here, but:

1. `frozenset` is fast enough
2. Zero false positives with sets
3. Simpler implementation
4. No bit manipulation or multiple hash functions

For 669k entries, the space savings aren't worth the complexity.

## Data Source

The BNC frequency list (`all.num`) is derived from:

- **Source**: Adam Kilgarriff's BNC frequency lists
- **URL**: https://www.kilgarriff.co.uk/BNClists/all.num.gz
- **Format**: Space-delimited (frequency, word, POS tag, document count)
- **Entries**: 938,971 lines, 669,417 unique word forms (after aggregation)

## Future Optimizations

Potential improvements (not implemented):

1. **Single binary file**: Pack all hashes into one file, memory-map it
2. **Perfect hashing**: Eliminate collision chains entirely
3. **Compile to C extension**: For extreme performance needs

Current implementation is fast enough for most use cases.
