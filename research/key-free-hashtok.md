# Occupancy-free hashpool (`hashtok`)

`hashpool` feature-hashes last-k contexts into shared buckets so a
held-out prompt can still be scored. That mixer is not SynthID's
secret hash. It still scores **every** hashed continuation with
Dirichlet/Laplace, including a next token that never appeared in the
bucket. That is the same occupancy artifact as poshits on `'The'`
([key-free-tokhits.md](key-free-tokhits.md)).

`hashtok` is the tokhits analog on collisions: skip a hash unless the
observed next token appeared in that bucket (`c_m + c_u ≥ 1`). Average
only the hashes that hit. Abstain when none did (`n_used=0`). Same
frozen tables; `indicate score --score-mode hashtok`. Still no keys,
`hash_iv`, or g-values.

## Protocol

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashpool,hashtok,hybrid,postokhits,postokbackoff2 \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok
```

Sixty other stems. Score 12×4 files, first **5** generated tokens
(official `ngram_len=5` grain). Last-4 context. Token 4 is the first
official tournament. Isolated `indicate score` of a lone file still
cannot reconstruct the prompt.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok/).
Letter d2 atoms: [../experiments/2026-09-01-letter-d2-first-ngram/hashtok-trace.json](../experiments/2026-09-01-letter-d2-first-ngram/hashtok-trace.json).

## Prefix-5 isolated files

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | marked zeros | precision |
|---|---|---|---|---|---|---|
| hashpool | **11/12** | 0.841 | **34/48** | **34/48** | 0/48 | 0.708 |
| **hashtok** | 9/12 | 0.761 | **30/48** | **36/48** | 5/48 | 0.714 |
| hybrid | 9/12 | 0.808 | 31/48 | 33/48 | 0/48 | 0.674 |
| postokhits | **10/12** | 0.762 | **30/48** | **45/48** | 10/48 | **0.909** |
| postokbackoff2 | **12/12** | 0.642 | 15/48 | 46/48 | 33/48 | 0.882 |

Nested Youden (train stems only): hashpool **30/48 vs 43/48**; hashtok
**26/48 vs 42/48**; postokhits **30/48 vs 45/48**.

Hashpool's four extra marked signs versus hashtok:

| File | hashpool | hashtok |
|---|---:|---:|
| harbour d2 | 0.059 | −0.233 |
| harbour d3 | 0.152 | −0.203 |
| harbour d4 | 0.152 | −0.203 |
| **letter d2** | **0.372** | **0.000** (`n_used=0`) |

Those four are occupancy, not colliding observed tokens. hashtok's 30
true positives are **exactly** postokhits' 30. Feature hashing did not
recover a next token that exact last-k missed. It did add unmarked
false positives (12 vs 3).

Do not sell 34/48 or 30/48 as beating poshits **39/48** (that 39/48
includes The-Laplace occupancy) or replacing isolated **29/48**.

## Letter d2's official 5-gram

File `08-letter-marked-2.txt`. Isolated prefix-5:
`Now in the second I` (ids `[3844, 287, 262, 1218, 314]`). Official
`public-deepmind-30` mean on that 5-gram is **0.733**. That path uses
keys. Isolated rankpath never sees this tournament at `--fit-prefix 4`
and ranks token 4 as a top-k miss under the isolated LM context
([key-free-cascade.md](key-free-cascade.md)).

hashtok on the frozen 60-stem prefix-5 tables:

| i | context → token | hashes that saw it | hashtok | hashpool |
|---|---|---:|---|---:|
| 1 | `Now` → ` in` | 0/8 | abstain | 0.000 |
| 2 | `Now in` → ` the` | 0/8 | abstain | 0.662 |
| 3 | `Now in the` → ` second` | 0/8 | abstain | 0.512 |
| 4 | `Now in the second` → ` I` | **0/8** | **abstain** | **0.314** |

The official 5-gram continuation `I` is unseen in every colliding
bucket. hashpool still emits a positive occupancy score. hybrid copies
it (exact last-k also misses). hashtok abstains on the whole file.

Prefix-8 `postokbackoff` also fails this 5-gram: last-4/3/2 unseen,
and `' second'` never continues with `' I'`. Its letter d2 score is
last-1 `' in' → ' the'`. Hashing the 4-gram does not create that
missing continuation.

## What this is not

- Not a universal isolated-file detector.
- Not key recovery. The mixer is a laboratory splitmix of token ids.
- Not a reason to replace the 12×4 last-4 headline **10/12** / **29/48**.
- Not evidence that hashing reads official 5-grams. On this leftover
  hashpool reads occupancy, and hashed backoff's fifth-token hit is
  last-1 unmarked.

Keep exact `postokhits` when the claim is observed-token preference.
Keep `hashpool` only if occupancy of empty cells is an acceptable
regulariser, and say so. `hashtok` is the occupancy-free hashed
reader. On the published opening, keep prefix-4 `hashtok` rather than
hashed backoff. Nested Youden, not t=0 38/48, is the honest isolated
gate for prefix-5 hashed backoff.

## Hashed backoff (`hashtokbackoff`)

Count-table `tokbackoff` can shrink last-k because `_add_sequence`
stores every suffix order 1..k in the same tables. Hashpool
`_add_hash_seq` hashes only `context_len`. Do **not** hash a shorter
prefix into a 4-gram pool: that is a different mixer, not backoff.

`hashtokbackoff` / `hashtokbackoff2` fit **separate** hashpool tables
per order `(1,2,3,4)` (`HASHBACKOFF_ORDERS`). At each position they
try longest→shortest `hashtok_token_lr` and keep the first occupancy-free
hit. `min_order=2` refuses last-1. Same laboratory mixer. Still no
keys, `hash_iv`, or g-values. Instance `key-free-hashtokbackoff` /
`key-free-hashtokbackoff2`.

A short generated prefix hashed into a longer-order table is not that
order's n-gram. At letter d2 position i=1, the winning "order 3" is
the one-token prefix `Now` hashed into the order-3 tables.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashpool,hashtok,hashtokbackoff,hashtokbackoff2,postokbackoff,postokbackoff2 \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtokbackoff
```

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtokbackoff/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtokbackoff/).
Opening window: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtokbackoff/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtokbackoff/).
Letter d2 atoms: [../experiments/2026-09-01-letter-d2-first-ngram/hashtokbackoff-trace.json](../experiments/2026-09-01-letter-d2-first-ngram/hashtokbackoff-trace.json).

## Prefix-5 isolated files (hashed backoff)

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashpool | 11/12 | 0.841 | **34/48** | 34/48 | 30/48 vs 43/48 | 0.708 |
| hashtok | 9/12 | 0.761 | **30/48** | 36/48 | 26/48 vs 42/48 | 0.714 |
| **hashtokbackoff** | 10/12 | 0.836 | **38/48** | 35/48 | **30/48 vs 40/48** | 0.745 |
| **hashtokbackoff2** | 10/12 | 0.818 | **36/48** | 34/48 | **30/48 vs 42/48** | 0.720 |
| postokbackoff | 10/12 | 0.782 | 34/48 | 40/48 | 33/48 vs 42/48 | 0.810 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 15/48 vs 46/48 | 0.882 |

hashtokbackoff's eight extra marked signs versus hashtok: harbour d3/d4,
library ×4, letter d2/d3, office d4. hashtokbackoff2 drops harbour
(those two need last-1). Library ×4 and letter d3 win at **order 4**
hashed observed-token hits. Station d4 and office d1/d3 stay zeros.

Nested Youden **30/48** is the honest isolated-file number. Do not sell
38/48 or 36/48 as beating poshits **39/48** (that 39/48 includes
The-Laplace occupancy) or replacing **29/48**.

## Letter d2 under hashed backoff

Isolated prefix-5 `Now in the second I`. hashtok still abstains
(`n_used=0`). hashtokbackoff:

| i | token | winning order | δ | last-4/3/2 saw it? |
|---|---|---|---|---|
| 1 | ` in` | 3 | +1.110 | order 3: 1 hash, c_m=1 c_u=0 (short prefix into order-3 tables) |
| 2 | ` the` | 4 | +0.277 | order 4: 2 hashes, c_m=0 c_u=2 |
| 3 | ` second` | none | abstain | all orders unseen |
| 4 | ` I` (official 5-gram) | **1** | **−1.100** | last-4/3/2 **0 hashes**; last-1: 2 hashes, **c_m=0 c_u=2** |

hashtokbackoff `n_used=3`, lr=**0.096** (last-1 of `I` dilutes).
hashtokbackoff2 `n_used=2`, lr=**0.694** from tokens 1–2, **not**
token 4. The official 5-gram continuation is still unseen at last-2+.
Last-1 saw `I` unmarked only. This is not a 5-gram reader.

## Prefix-4 opening (hashed backoff hurts)

Same 60-stem train, generated tokens 0–3 (published opening).

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashpool | 10/12 | 0.887 | **38/48** | 37/48 | **35/48 vs 46/48** | 0.776 |
| **hashtok** | 10/12 | 0.844 | **35/48** | 39/48 | **33/48 vs 45/48** | 0.795 |
| hashtokbackoff | 10/12 | 0.780 | 31/48 | 33/48 | 31/48 vs 42/48 | 0.674 |
| hashtokbackoff2 | 10/12 | 0.760 | 31/48 | 33/48 | 31/48 vs 42/48 | 0.674 |
| postokbackoff | 10/12 | 0.800 | 34/48 | 43/48 | 34/48 vs 45/48 | 0.872 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 15/48 vs 46/48 | 0.882 |

Hashpool's three extra TPs versus hashtok are occupancy. Shrinking
hashed orders on this window **hurts** (31/48, 15 FPs) relative to
plain hashtok. Keep prefix-4 `hashtok` as the occupancy-free hashed
reader; keep exact `postokbackoff` when overlap precision is the
point. Do not sell 38/48 or 35/48 as beating poshits **39/48**.
