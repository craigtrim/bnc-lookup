# Morphological Analysis

API reference for the morphological suffix analysis functions: `get_suffixes()`, `get_inflections()`, and `get_morphology()`.

## Table of Contents

- [Overview](#overview)
- [get_suffixes](#get_suffixes)
- [get_inflections](#get_inflections)
- [get_morphology](#get_morphology)
- [Morphology Dataclass](#morphology-dataclass)
- [How Inflectional Detection Works](#how-inflectional-detection-works)
- [Design Decisions](#design-decisions)

## Overview

The library provides two layers of morphological suffix analysis:

| Function | Type | Performance | Source |
|----------|------|-------------|--------|
| `get_suffixes()` | Derivational | O(1) static lookup | Pre-computed by morphroot |
| `get_inflections()` | Inflectional | Runtime detection | Closed set of English endings |
| `get_morphology()` | Both | O(1) + runtime | Combines both into a single result |

**Derivational suffixes** change the word's part of speech or core meaning (e.g., "happy" + "-ness" = "happiness"). These are pre-computed from the morphroot segmentation engine and stored in 256 hash-bucketed files under `bnc_lookup/sx/`, following the same architecture as the existence and frequency data.

**Inflectional suffixes** express grammatical features without changing the word class (e.g., "cat" + "-s" = "cats"). These are detected at runtime by stripping candidate endings and checking whether the resulting stem exists in the BNC corpus.

## get_suffixes

```python
bnc.get_suffixes(word: str) -> list[str] | None
```

Returns the derivational suffixes for a BNC word via O(1) static lookup.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | `str` | Any English word. Case-insensitive. |

### Return Value

| Return | Meaning |
|--------|---------|
| `list[str]` | Suffixes in derivation order (innermost first), e.g. `['ful', 'ly']` |
| `[]` | Word is in the BNC but is monomorphemic (no derivational suffixes) |
| `None` | Word is not in the BNC at all |

### Examples

```python
import bnc_lookup as bnc

# Derivational suffixes in innermost-first order
bnc.get_suffixes('happiness')       # ['ness']
bnc.get_suffixes('beautifully')     # ['ful', 'ly']
bnc.get_suffixes('nationalization') # ['ize', 'tion', 'al']
bnc.get_suffixes('cheerfully')      # ['ful', 'ly']

# Monomorphemic words return empty list
bnc.get_suffixes('cat')             # []
bnc.get_suffixes('the')             # []
bnc.get_suffixes('danger')          # []

# Unknown words return None
bnc.get_suffixes('xyz123')          # None
```

### How It Works

Derivational suffix data is pre-computed by the [morphroot](https://github.com/craigtrim/morphroot) segmentation engine and stored in 256 hash-bucketed Python modules under `bnc_lookup/sx/`. Each module maps a 30-character MD5 hash suffix to a pipe-delimited suffix string (e.g., `"ful|ly"`).

At lookup time:
1. The word is normalized to lowercase
2. Its MD5 hash is computed
3. The first 2 hex characters select the bucket file (lazy-loaded and cached)
4. The remaining 30 characters are used as the lookup key
5. If found, the pipe-delimited string is split into a list
6. If not found but the word exists in BNC (via `FindBnc.exists()`), returns `[]`
7. If the word is not in the BNC at all, returns `None`

## get_inflections

```python
bnc.get_inflections(word: str) -> list[str] | None
```

Returns the inflectional suffixes for a word by runtime detection against the closed set of English inflectional endings.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | `str` | Any English word. Case-insensitive. |

### Return Value

| Return | Meaning |
|--------|---------|
| `list[str]` | Inflectional suffix detected, e.g. `['s']`, `['ing']`, `['ed']`, `['est']` |
| `[]` | Word is itself a BNC base form (no inflectional ending) |
| `None` | No BNC base form can be recovered |

### Inflectional Suffixes Handled

| Suffix | Grammatical Function | Example |
|--------|---------------------|---------|
| `-s` | Plural noun, 3rd-person singular verb | cats, runs |
| `-es` | Plural noun, 3rd-person singular verb | boxes, watches |
| `-ing` | Present participle, gerund | running, walking |
| `-ed` | Past tense, past participle | walked, played |
| `-est` | Superlative adjective | fastest, tallest |

Suffixes are tried longest-first: `-est`, `-ing`, `-ed`, `-es`, `-s`.

### Examples

```python
import bnc_lookup as bnc

# Plural / 3rd-person singular
bnc.get_inflections('cats')         # ['s']
bnc.get_inflections('boxes')        # ['es']

# Present participle
bnc.get_inflections('running')      # ['ing']
bnc.get_inflections('walking')      # ['ing']
bnc.get_inflections('hoping')       # ['ing']  (e-drop: hope → hop + ing)

# Past tense
bnc.get_inflections('walked')       # ['ed']
bnc.get_inflections('hoped')        # ['ed']  (e-drop: hope → hop + ed)
bnc.get_inflections('stopped')      # ['ed']  (double consonant: stop → stopp + ed)
bnc.get_inflections('carried')      # ['ed']  (y-restore: carry → carri + ed)

# Superlative
bnc.get_inflections('fastest')      # ['est']
bnc.get_inflections('happiest')     # ['est']  (y-restore: happy → happi + est)

# Base form (no inflection)
bnc.get_inflections('cat')          # []
bnc.get_inflections('walk')         # []

# Unknown word
bnc.get_inflections('xyz123')       # None
```

### Allomorphic Restoration Logic

When a suffix is stripped from the input word, the raw stem may not match the dictionary base form. The function applies four allomorphic restoration strategies to recover the base:

| Strategy | Raw Stem | Restored | Example Word |
|----------|----------|----------|-------------|
| **Direct** | walk | walk | walked |
| **E-restore** | hop | hope | hoped, hoping |
| **Double-consonant reduction** | runn | run | running |
| **Y-restore** | happi | happy | happiest, carried |

These are applied in order. The first candidate that exists in the BNC corpus is accepted.

**E-restore** is only applied for suffixes that trigger e-drop in English orthography: `-ing`, `-ed`, `-er`, `-est`. It is not applied for `-s` or `-es` (no English word drops a final -e before adding -s).

**Double-consonant reduction** checks whether the last two characters of the stem are identical (e.g., "runn", "stopp") and tries removing the final duplicate.

**Y-restore** checks whether the stem ends in "i" and tries replacing it with "y" (e.g., "happi" becomes "happy").

**Minimum stem length**: A stem must be at least 2 characters after stripping. This prevents false positives on very short words.

## get_morphology

```python
bnc.get_morphology(word: str) -> Morphology | None
```

Returns the full morphological suffix analysis by combining derivational lookup with runtime inflectional detection.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `word` | `str` | Any English word. Case-insensitive. |

### Return Value

| Return | Meaning |
|--------|---------|
| `Morphology` | Dataclass with `.derivational` and `.inflectional` lists |
| `None` | Word is not in the BNC and no inflected base form can be found |

### Examples

```python
import bnc_lookup as bnc

# Derivational only
m = bnc.get_morphology('happiness')
# Morphology(derivational=['ness'], inflectional=[])
m.derivational   # ['ness']
m.inflectional   # []

# Inflectional only
m = bnc.get_morphology('cats')
# Morphology(derivational=[], inflectional=['s'])
m.derivational   # []
m.inflectional   # ['s']

# Both derivational and inflectional
# (word has derivational suffixes from get_suffixes,
#  and is also a base form in BNC so inflectional is [])
m = bnc.get_morphology('beautifully')
# Morphology(derivational=['ful', 'ly'], inflectional=[])

# Neither (monomorphemic base form)
m = bnc.get_morphology('cat')
# Morphology(derivational=[], inflectional=[])
m.derivational   # []
m.inflectional   # []

# Unknown word
m = bnc.get_morphology('xyz123')
# None

# Flat suffix list if needed
m = bnc.get_morphology('happiness')
m.derivational + m.inflectional   # ['ness']
```

### Logic

`get_morphology()` calls both `get_suffixes()` and `get_inflections()` independently:

1. If both return `None`, returns `None` (word completely unknown).
2. Otherwise, returns a `Morphology` dataclass where each field defaults to `[]` if its respective function returned `None`.

This means a word can have derivational suffixes, inflectional suffixes, both, or neither -- and the `Morphology` result always has two well-typed list fields.

## Morphology Dataclass

```python
from bnc_lookup import Morphology

@dataclass(frozen=True)
class Morphology:
    derivational: list[str]   # Derivational suffixes, innermost-first
    inflectional: list[str]   # Inflectional suffixes detected at runtime
```

The dataclass is frozen (immutable). Both fields are always lists (never `None`).

### Field Details

| Field | Type | Description |
|-------|------|-------------|
| `derivational` | `list[str]` | Derivational suffixes in innermost-first order. Empty if monomorphemic or if `get_suffixes()` returned `None`. |
| `inflectional` | `list[str]` | Inflectional suffixes. Typically a single-element list (e.g., `['s']`, `['ing']`). Empty if the word is a base form or if `get_inflections()` returned `None`. |

## How Inflectional Detection Works

### Runtime vs Pre-Computed

Derivational suffixes (`get_suffixes()`) are pre-computed at build time by the morphroot segmentation engine and stored as static data in `bnc_lookup/sx/`. This gives O(1) lookup at the cost of a build step.

Inflectional suffixes (`get_inflections()`) are detected at runtime. For each candidate suffix in the closed set (`-est`, `-ing`, `-ed`, `-es`, `-s`), the function:

1. Checks if the input word ends with the suffix
2. Strips the suffix to get the raw stem
3. Generates allomorphic candidate base forms (direct, e-restore, double-consonant, y-restore)
4. Checks each candidate against the BNC corpus via `FindBnc.exists()`
5. Returns the first match

This design was chosen because:
- The inflectional suffix set is closed and small (5 endings)
- Allomorphic restoration is straightforward
- Runtime detection avoids storing a second pre-computed dataset
- The BNC existence check is O(1), so the overall cost is low

### The Closed Set

English has a finite, closed set of inflectional suffixes. Unlike derivational morphology (where new suffixes can be productive in complex ways), inflectional endings are fixed:

| Suffix | Grammar |
|--------|---------|
| `-s` / `-es` | Plural, 3rd-person singular |
| `-ing` | Progressive aspect |
| `-ed` | Past tense, past participle |
| `-est` | Superlative |

The function tries suffixes longest-first to avoid ambiguity (e.g., "boxes" should match `-es` before `-s`).

## Design Decisions

### Why -er Comparative Is Excluded

The comparative suffix `-er` (e.g., "faster", "taller") is intentionally excluded from inflectional detection. Without part-of-speech data, comparative `-er` is indistinguishable from agentive `-er` (e.g., "teacher", "runner"), which is a derivational suffix.

Agentive `-er` is already handled by `get_suffixes()` as a derivational suffix. Including `-er` in inflectional detection would cause false positives: "teacher" would be reported as having inflectional `-er` (comparative of "teach"), which is incorrect.

The tradeoff: genuine comparatives like "faster" and "taller" are not detected as inflectional. They can still appear in `get_suffixes()` if the derivational data includes them.

### Why get_inflections Returns [] vs None

The three-way return (`list`, `[]`, `None`) mirrors `get_suffixes()` and carries distinct meaning:

- `['s']`, `['ing']`, etc.: The word is an inflected form of a BNC base
- `[]`: The word is itself a BNC base form (no inflection to strip)
- `None`: The word cannot be anchored to any BNC entry at all

This distinction matters for downstream consumers. An empty list means "known word, no suffixes" while `None` means "unknown word."
