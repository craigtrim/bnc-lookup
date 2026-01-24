# Frequency Bucket Examples

One example word from each of the 100 frequency buckets, showing how word commonality decreases from bucket 1 (most frequent) to bucket 100 (least frequent).

## Overview

| Range | Description | Typical Frequency |
|-------|-------------|-------------------|
| 1-10 | Very common words | 30+ occurrences |
| 11-30 | Common words | 3-30 occurrences |
| 31-50 | Uncommon words | 2-3 occurrences |
| 51-100 | Rare words | 1 occurrence |

## All 100 Buckets

| Bucket | Example Word | Corpus Frequency |
|--------|--------------|------------------|
| 1 | people | 124,158 |
| 2 | algorithm | 556 |
| 3 | entrepreneur | 289 |
| 4 | metaphysics | 148 |
| 5 | kangaroo | 115 |
| 6 | saxophone | 89 |
| 7 | samurai | 61 |
| 8 | etymology | 47 |
| 9 | croissant | 33 |
| 10 | espresso | 30 |
| 11 | origami | 24 |
| 12 | hengist | 21 |
| 13 | otton | 17 |
| 14 | froebel | 15 |
| 15 | torgyan | 13 |
| 16 | enterectomy | 11 |
| 17 | sandwiching | 10 |
| 18 | hamo | 9 |
| 19 | gammy | 8 |
| 20 | detrusor | 7 |
| 21 | odile | 7 |
| 22 | zvereva | 6 |
| 23 | withamshaw | 5 |
| 24 | zydeco | 5 |
| 25 | osburn | 5 |
| 26 | pylyshyn | 4 |
| 27 | boughey | 4 |
| 28 | natros | 4 |
| 29 | espiritu | 4 |
| 30 | rheindalen | 3 |
| 31 | ilam | 3 |
| 32 | belud | 3 |
| 33 | zwolle | 3 |
| 34 | macmanus | 3 |
| 35 | tregian | 3 |
| 36 | transfluent | 2 |
| 37 | sbcb | 2 |
| 38 | pauncefoot | 2 |
| 39 | marxiste | 2 |
| 40 | hominas | 2 |
| 41 | epilimnion | 2 |
| 42 | cdre | 2 |
| 43 | afrodite | 2 |
| 44 | 24-game | 2 |
| 45 | zzzzzzzz | 2 |
| 46 | repapering | 2 |
| 47 | hendryx | 2 |
| 48 | anklebiters | 2 |
| 49 | wombling | 1 |
| 50 | wahlenbergii | 1 |
| 51 | uray | 1 |
| 52 | truden | 1 |
| 53 | thines | 1 |
| 54 | swiftitude | 1 |
| 55 | statuesquely | 1 |
| 56 | slummery | 1 |
| 57 | seshed | 1 |
| 58 | samin | 1 |
| 59 | ricards | 1 |
| 60 | randak | 1 |
| 61 | prntd | 1 |
| 62 | plumosa | 1 |
| 63 | pathnames | 1 |
| 64 | orpoagation | 1 |
| 65 | nonantola | 1 |
| 66 | nargis | 1 |
| 67 | mlib | 1 |
| 68 | mccarren | 1 |
| 69 | ltcl | 1 |
| 70 | leada | 1 |
| 71 | kiathas | 1 |
| 72 | isamatec | 1 |
| 73 | hywell | 1 |
| 74 | hemorrhoids | 1 |
| 75 | gtgc | 1 |
| 76 | gelatinously | 1 |
| 77 | fomula | 1 |
| 78 | fadoul | 1 |
| 79 | enchytraeids | 1 |
| 80 | dreadheads | 1 |
| 81 | densitron | 1 |
| 82 | crucifiction | 1 |
| 83 | cometabolism | 1 |
| 84 | charrismo | 1 |
| 85 | bzzzzzzzzzzz | 1 |
| 86 | bolstadr | 1 |
| 87 | bayyud | 1 |
| 88 | assaad | 1 |
| 89 | altamura | 1 |
| 90 | a.m.m. | 1 |
| 91 | 74w | 1 |
| 92 | 520e. | 1 |
| 93 | 38493 | 1 |
| 94 | 29000s | 1 |
| 95 | 2,569 | 1 |
| 96 | 1800–1948 | 1 |
| 97 | 13.625% | 1 |
| 98 | 1,000ft | 1 |
| 99 | 's_old | 1 |
| 100 | £120.8m | 1 |

## Observations

**Bucket 1** is large—it contains ~6,700 words including nearly all common English words (the, and, people, time, work, computer, beautiful, etc.).

**Buckets 2-11** contain recognizable but less common words: algorithm, entrepreneur, kangaroo, saxophone, espresso, origami.

**Buckets 12-48** contain increasingly obscure terms: proper nouns, technical jargon, foreign words, and specialized vocabulary.

**Buckets 49-100** contain words that appear only once in the 100-million-word corpus: typos, rare proper nouns, technical codes, and corpus artifacts.

## Usage

```python
import bnc_lookup as bnc

# Common words are in bucket 1
bnc.bucket('people')       # 1
bnc.bucket('computer')     # 1
bnc.bucket('beautiful')    # 1

# Less common words in higher buckets
bnc.bucket('algorithm')    # 2
bnc.bucket('saxophone')    # 6
bnc.bucket('origami')      # 11

# Filter for common words only
def is_common(word):
    bucket = bnc.bucket(word)
    return bucket is not None and bucket <= 10
```

## Notes

- Each bucket contains approximately **6,694 words**
- The BNC corpus was collected 1991-1994, so some modern terms may be absent
- Bucket assignment is based on **percentile ranking**, not raw frequency
