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
  hashpool reads occupancy. Mixed hashed backoff's fifth-token hit is
  last-1 unmarked, and two of its earlier hits are short prefixes in
  longer-order tables. Exact-length backoff2 is last-2
  `'Now in' → ' the'`, still not token 4.

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

## Exact-length hashing (`hashtoklen`)

`_scored_ctx` returns fewer than k tokens at the start of a string.
Hashing that short prefix into an order-k table is not a k-gram: it
collides last-1/last-2 English with real 4-grams in the same buckets.
On the mixed prefix-5 backoff traces, library ×4 and letter d3 win at
order 4 on i=3 (`order > i`). Letter d2 backoff2 lr=0.694 is i=1
order 3 and i=2 order 4, both illegal.

`hashtoklen` / `hashtoklenbackoff` / `hashtoklenbackoff2` fit and
score only when `len(ctx) == order`. Same laboratory mixer. Still no
keys. Instance `key-free-hashtoklen` / `key-free-hashtoklenbackoff`.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashtok,hashtoklen,hashtoklenbackoff,hashtoklenbackoff2,postokbackoff2 \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen
```

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen/).
Letter d2 atoms: [../experiments/2026-09-01-letter-d2-first-ngram/hashtoklen-trace.json](../experiments/2026-09-01-letter-d2-first-ngram/hashtoklen-trace.json).

## Prefix-5 isolated files (exact length)

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtok | 9/12 | 0.761 | **30/48** | 36/48 | 26/48 vs 42/48 | 0.714 |
| **hashtoklen** | **12/12** | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** | 0.875 |
| **hashtoklenbackoff** | 11/12 | 0.822 | **36/48** | 34/48 | **33/48 vs 42/48** | 0.720 |
| **hashtoklenbackoff2** | 10/12 | 0.769 | **36/48** | 35/48 | **28/48 vs 43/48** | 0.735 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 15/48 vs 46/48 | 0.882 |

`hashtoklen` scores only the official 5-gram slot (i=4). 27 marked
files abstain. Prompt ranking **12/12** is not isolated-file density.

Letter d2 under exact backoff:

| i | token | winning order | δ | notes |
|---|---|---|---|---|
| 1 | ` in` | none | abstain | order 3 no longer eligible (`ctx_len=1`) |
| 2 | ` the` | **2** | +0.797 | last-2 `'Now in' → ' the'` |
| 3 | ` second` | none | abstain | all exact orders unseen |
| 4 | ` I` | **1** | **−1.100** | last-4/3/2 unseen; last-1 unmarked |

hashtoklen `n_used=0`. hashtoklenbackoff `n_used=2`, lr=**−0.152**.
hashtoklenbackoff2 `n_used=1`, lr=**0.797** from last-2, **not** the
official 5-gram. Library ×4 survive as a legal last-3
`'Cl' 'osing' ' is' → ' the'` (i=3, order 3). Letter d3's illegal
order-4 extra is gone. Office d4 is last-3 `' at'` at i=4.

Nested Youden **33/48 vs 42/48** is the honest isolated-file number
for exact hashed backoff. Mixed backoff nested **30/48** was the
short-prefix mixer plus last-1. Do not sell 36/48 or 33/48 as beating
poshits **39/48** or replacing **29/48**.

## Harbour d2 is a hashed 5-gram collision, not occupancy

Twenty of hashtoklen's 21 TPs are exact `postokhits`. The extra is
harbour d2 (`01-harbour-marked-2.txt`): `The ferry was over ,` (ids
`[464, 26450, 373, 625, 11]`). Exact last-4 of the comma is
unmarked-like (`postokhits` lr=**−2.65**, `n_used=1`). Occupancy-free
hashtoklen is marked-like (lr=**+0.618**) because **one of eight**
laboratory hashes (bucket 178) collided with other last-4s that
continue with comma marked-only (c_m=11, c_u=0). That is an observed
next-token collision, not Laplace of an empty cell.

Mixed `tables-hashpool` (short prefixes hashed into the 4-gram mixer)
plus score-time `exact_len` is a **different** mixer (lr=+2.18, 2/8
hashes, c_u=1) and is not the holdout number. Persist exact-length
tables as `tables-hashtoklen`. Letter d2's official `I` still has
`n_used=0`. In-domain 12×4 LOO hashtoklen is **7/48 vs 48/48**
(precision 1.0 among decided); harbour d2 is already a TP there;
letter d2 is not. Unique openings stay unseen.

JSON: [../experiments/2026-09-01-letter-d2-first-ngram/harbour-d2-hashtoklen-trace.json](../experiments/2026-09-01-letter-d2-first-ngram/harbour-d2-hashtoklen-trace.json),
[../experiments/2026-09-01-probe-12x4-fitprefix5-hashtoklen/](../experiments/2026-09-01-probe-12x4-fitprefix5-hashtoklen/).

## Prefix-4 exact-length backoff no longer hurts

On a 4-token prefix, `hashtoklen` (order 4) abstains everywhere: there
is no 4-token context. Prompt **12/12** on that run is all-zero ties,
not a ranking. Exact `hashtoklenbackoff` uses legal last-3/2/1:

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| hashtok | 10/12 | 0.844 | **35/48** | 39/48 | **33/48 vs 45/48** |
| hashtoklen | 12/12† | 0.500 | **0/48** | 48/48 | 0/48 vs 48/48 |
| **hashtoklenbackoff** | 11/12 | 0.826 | **35/48** | 38/48 | **35/48 vs 40/48** |

† Ties. Mixed hashed backoff on this window was **31/48**. Exact
backoff matches hashtok's t=0 density. Keep prefix-4 `hashtok`.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtoklen/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtoklen/).

## Hashed 5-gram + opening rankpath cascade

`--cascade hashtoklen --cascade-fallback rankpath` puts the
occupancy-free official 5-gram reader on the count channel. Rebound
from saved prefix-4 rankpath rows (no new GPT-2 forwards):

| Rule | marked>0 | unmarked≤0 |
|---|---|---|
| hashtoklen decided | **21/48** | **45/48** |
| coverage / positive-when | **33/48** | **37/48** |

hashtoklen has no covered-negative marked files, so the two when-rules
match. Combined **70/96** vs prefix-4 count **82/96**. Leftover eight
stay misses. Do not sell 33/48.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen-cascade-rankpath/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen-cascade-rankpath/).

## Distil: same tokenizer, not the same 5-grams

DistilGPT2 12×4 is officially **12/12**. Native Distil opening
rankpath is chance. Native Distil prefix-5 hashtoklen is **7/48 vs
48/48** (same sparse in-domain grain as GPT-2). GPT-2 60-stem tables
scored on Distil prefix-5:

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| hashtoklen | 9/12 | **0.571** | **10/48** | 43/48 | 0.041 |
| hashtoklenbackoff | 4/12 | **0.470** | 17/48 | 26/48 | 0.794 |
| postokhits | 9/12 | 0.591 | 10/48 | 42/48 | 0.017 |

Occupancy-free official-grain hashing does not become a Distil
detector. Same BPE is not the same generator footprint. Do not sell
10/48.

JSON: [../experiments/2026-09-01-probe-distilgpt2-12x4-fitprefix5-hashtoklen/](../experiments/2026-09-01-probe-distilgpt2-12x4-fitprefix5-hashtoklen/),
[../experiments/2026-09-01-transfer-short-medium-tails-family-to-distil-prefix5-hashtoklen/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-distil-prefix5-hashtoklen/).

## Drop-one skip-grams (`hashskip`) are denser at t=0 and worse nested

`hashskip` hashes exact last-k with one token dropped. Views are
tagged `(SKIP_TAG, drop_index, *kept)` so they are not last-(k-1).
Same occupancy-free mixer. Instance `key-free-hashskip`. Still no
keys.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashtoklen,hashskip \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashskip
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| hashtoklen | 12/12† | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** |
| **hashskip** | 8/12 | 0.663 | **25/48** | 35/48 | **16/48 vs 41/48** |

† Ties among zeros. t=0 extras: harbour d3/d4, night-bus d2/d4,
workshop d4. Thirteen unmarked FPs. Nested Youden **16/48** is the
honest isolated-file number.

Letter d2 `Now in the second I`: drop-2 and drop-3 **see** `I`, both
unmarked-only (c_m=0, c_u=1, lr=−0.847). The coarsened official
5-gram that exists in train votes unmarked, the same way last-1 did.
Leftover eight: 2/8 at t=0 (tiny harbour d3/d4); nested leftover
fill-in **0/8**. Do not sell 25/48.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashskip/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashskip/),
[../experiments/2026-09-01-letter-d2-first-ngram/letter-d2-hashskip-trace.json](../experiments/2026-09-01-letter-d2-first-ngram/letter-d2-hashskip-trace.json).

Coverage-then-hashskip on saved holdouts is **worse** than hashtoklen
alone: **26/48 vs 35/48**, 13 FPs, combined **61/96** vs hashtoklen
**66/96**. Do not add hashskip as a cascade fallback.

## Singleton collisions (`hashtoklen2`)

Occupancy-free default is `c_m + c_u ≥ 1`. `hashtoklen2` /
`hashskip2` raise that floor to **2** at score time on the same
frozen tables. Not a new mixer. Still no keys. Instance
`key-free-hashtoklen2` / `key-free-hashskip2`.
`indicate score --score-mode hashtoklen2`.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashtoklen,hashtoklen2,hashskip,hashskip2 \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtoklen | 12/12† | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** | 0.875 |
| **hashtoklen2** | 12/12† | 0.604 | **10/48** | **48/48** | **10/48 vs 48/48** | **1.000** |
| hashskip | 8/12 | 0.663 | **25/48** | 35/48 | **16/48 vs 41/48** | 0.658 |
| **hashskip2** | 8/12 | 0.641 | **22/48** | 39/48 | **15/48 vs 41/48** | 0.710 |

† Ties among zeros. **11 of 21** hashtoklen TPs are singleton hash
collisions. min_count=2 is the robust occupancy-free 5-gram core:
precision 1.0, nested matching t=0.

Harbour d2 survives (c_m=11, same lr=+0.618). Letter d2 still
abstains. Lost: night-bus d3, market ×4, kitchen d2, station d1/d3,
rain d2, garden d1/d4. Leftover eight stay zeros.

hashskip2 zeros letter d2's unmarked singleton votes but still has
9 unmarked FPs. Nested leftover fill-in **0/8**. Do not sell 10/48,
22/48, or 15/48 as beating poshits **39/48** or replacing **29/48**.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2/).

## Count-weighting hashes does nothing at this grain

Occupancy-free default averages the hashes that saw the observed next
token. Weighting those hashes by `c_m+c_u` or `log(1+n)` **copies**
uniform hashtoklen (**21/48 vs 45/48**) on the frozen prefix-5
`tables-hashtoklen`. No marked file mixes a singleton hash with a
dense one on the official 5-gram slot. Rain d1 mixes n=7 with n=8
(both dense); that shifts LR by 0.005 and does not flip the sign.
Weight `n-1` (skip n=1) copies `min_count=2` (**10/48 vs 48/48**). Not a product scorer. The test
`test_prefix5_hashtoklen_count_weighting_copies_uniform` rescores the
saved tables.

## hashtoklen2 + prefix-4 rankpath is not complementary

Rebound saved prefix-4 rankpath rows with `hashtoklen2` as the count
channel (no new GPT-2). Coverage cascade **28/48 vs 40/48** copies
standalone 60-stem prefix-4 rankpath. All 10 robust hashed 5-gram TPs
are already rankpath TPs. Leftover fill-in **0/8**. Combined **68/96**
vs hashtoklen cascade **70/96** vs prefix-4 count **82/96**.
`hashtoklen2` is not in `HASH_CASCADE_READERS`. Do not add it as a
cascade count channel on this number. Do not sell 28/48.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2-cascade-rankpath/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2-cascade-rankpath/).

## MASK replace (`hashmask`) is denser coverage and worse nested

`hashmask` hashes exact last-k with one token replaced by
`MASK_TAG=-4`. Length stays k: a masked 4-gram is not a last-3 and not
a tagged skip-gram. Occupancy-free. Instance `key-free-hashmask`.
Persist `tables-hashmask/` (`mask_one=true`, `drop_one=false`,
`exact_len=true`). Refuse score-time `hashmask` on a non-mask mixer.
`hashmask2` is `min_count=2` on the same tables.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 5 --pos-bucket 0 \
  --methods hashtoklen,hashmask,hashmask2 \
  --out-dir experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashmask
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtoklen | 12/12† | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** | 0.875 |
| **hashmask** | 11/12 | 0.704 | **21/48** | **42/48** | **19/48 vs 45/48** | 0.778 |
| **hashmask2** | 10/12 | 0.642 | **15/48** | 44/48 | **11/48 vs 45/48** | 0.789 |

† Ties among zeros. Same 21 TPs at t=0 as hashtoklen: extras harbour
d3/d4, letter d2, workshop d4; lost market ×4. Six unmarked FPs.
Nested Youden **19/48 vs 45/48** is worse than exact hashtoklen.
Keep prefix-5 `hashtoklen` / robust `hashtoklen2`.

Letter d2 `Now in the second I`: only `mask_i=3` (`Now in the MASK` →
`I`) sees the continuation. Two opposing singleton hashes (bucket
hashes c_m=1 and c_u=1) average to file lr=**+0.240**, and that **is**
the official slot (`n_used=1`). `hashmask2` skips both (`n_used=0`).
Nested t=0.778 throws letter d2 out. Leftover t=0 is harbour d3/d4
and letter d2; nested leftover is harbour d3/d4 only. Not 8/8. Do not
sell 21/48, 19/48, 15/48, or letter d2 +0.240.

JSON: [../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashmask/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashmask/),
[../experiments/2026-09-01-letter-d2-first-ngram/letter-d2-hashmask-trace.json](../experiments/2026-09-01-letter-d2-first-ngram/letter-d2-hashmask-trace.json).

## In-domain full-file hashtok is denser at t=0 and noisier nested

Leave-one-prompt-out on the published 12×4 twins, full 128-token files.
Unbucketed last-4. Hashpool matches the published **35/48 vs 29/48**.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashpool,hashtok,hashtoklen,hits,postokhits \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| hits | 11/12 | 0.737 | 28/48 | 30/48 | **22/48 vs 39/48** |
| hashpool | 11/12 | 0.716 | **35/48** | **29/48** | 23/48 vs 36/48 |
| **hashtok** | 9/12 | 0.664 | **33/48** | **22/48** | **22/48 vs 30/48** |
| hashtoklen | 8/12 | 0.592 | 33/48 | 23/48 | 30/48 vs 20/48 |

Occupancy-free hashing is four files denser than hard last-4 **29/48**
at t=0, with 26 unmarked FPs. Nested-by-stem spec is worse than hits.
Hashpool occupancy and hashtok disagree on six files (hashpool-only
night-bus d3, library d2, market d1, ferry-queue d4; hashtok-only
night-bus d4, market d3). Letter d2 stays negative. Do not sell 33/48
or 35/48 as replacing **29/48**.

JSON: [../experiments/2026-09-01-probe-12x4-hashtok/](../experiments/2026-09-01-probe-12x4-hashtok/).

## Mixer width: n=2/4 beat n=8 at seed 20260831

The CLI default is `--n-hashes 8`. That is a random-feature width, not
SynthID’s secret hash. Leave-one-prompt-out on the same 12×4 full-file
twins while changing only that width, at mixer seed **20260831**:

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 2 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-nhashes2
```

| n_hashes | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| **2** | **11/12** | **0.764** | 34/48 | **31/48** | **28/48 vs 37/48** |
| 4 | **11/12** | 0.733 | **36/48** | 30/48 | **35/48 vs 30/48** |
| 8 (default) | 9/12 | 0.664 | 33/48 | 22/48 | 22/48 vs 30/48 |
| 16 | **11/12** | 0.662 | **36/48** | 22/48 | 29/48 vs 24/48 |
| 32 | 10/12 | 0.622 | 30/48 | 26/48 | 21/48 vs 38/48 |

Fewer hashes are denser *and* better nested than n=8 **at this seed**.
n=2 has the best file AUC and the best nested spec among the dense
widths. n=4 is the densest t=0 / nested recall (mean nested t ≈ 0).
Wider mixers dilute the mean gap: n=16 nested spec is **24/48**; n=32
nested recall **21/48** is below n=8. Letter d2 stays negative at
n=2/4/8/32. n=16 is the only width here with letter d2 `lr>0`; the
letter prompt still loses. Do not sell that as reading the official
5-gram.

This is not hits nested **22/48 vs 39/48**, not poshits **39/48**, and
not hard last-4 **29/48**. Combined t=0 at n=2 is **65/96**. Do not
sell 36/48, 35/48, or 34/48 as replacing **29/48**.

JSON: [../experiments/2026-09-01-probe-12x4-hashtok-nhashes2/](../experiments/2026-09-01-probe-12x4-hashtok-nhashes2/),
[../experiments/2026-09-01-probe-12x4-hashtok-nhashes4/](../experiments/2026-09-01-probe-12x4-hashtok-nhashes4/),
[../experiments/2026-09-01-probe-12x4-hashtok-nhashes16/](../experiments/2026-09-01-probe-12x4-hashtok-nhashes16/),
[../experiments/2026-09-01-probe-12x4-hashtok-nhashes32/](../experiments/2026-09-01-probe-12x4-hashtok-nhashes32/).

## Mixer seed confounds the in-domain n=2 width win

`fit_hashpool_twins` / `rotate_hashpool` take a feature-hash `seed`
(default **20260831**). That is not SynthID `hash_iv`. Same 12×4
hashtok n=2 LOO at other seeds:

| n_hashes | seed | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|---|
| 2 | **20260831** | **11/12** | **0.764** | 34/48 | **31/48** | **28/48 vs 37/48** |
| 2 | 0 | 9/12 | 0.637 | 34/48 | 21/48 | 28/48 vs 30/48 |
| 2 | 1 | **11/12** | 0.687 | 33/48 | 25/48 | 29/48 vs 36/48 |
| 2 | 7 | **11/12** | 0.695 | 30/48 | 28/48 | 27/48 vs 34/48 |
| 2 | 42 | 10/12 | 0.743 | 34/48 | 30/48 | **34/48 vs 25/48** |
| 2 | 12345 | 10/12 | 0.712 | 31/48 | 25/48 | 25/48 vs 37/48 |
| 8 | 0 | 9/12 | 0.658 | 33/48 | **32/48** | **32/48 vs 33/48** |
| 8 | 7 | **11/12** | 0.719 | 31/48 | 29/48 | **28/48 vs 37/48** |

n=2 unmarked spec ranges **21–31/48**; nested spec **25–37/48**. Default
seed 20260831 is among the best n=2 mixers here, not a typical one.
Seed 0 keeps 34 TPs and collapses spec to **21/48**. n=8 seed 7 nested
**28/48 vs 37/48** matches the advertised n=2 default. Letter d2 flips
sign at n=2 seeds 0 and 12345. The in-domain n=2 vs n=8 table is
seed-confounded. Keep CLI `n_hashes=8` and seed `20260831`. Do not
sell 34/48 as a width law.

JSON: [../experiments/2026-09-01-probe-12x4-hashtok-nhashes2-seeds/](../experiments/2026-09-01-probe-12x4-hashtok-nhashes2-seeds/).

## Mixer width does not transfer: keep default n=8

The honest isolated-file gate is nested Youden on 24 new 36×4 stems,
frozen on the original 12×4 files. Same occupancy-free `hashtok`,
full-file last-4, `drop-from-train`.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 8 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8
```

| n_hashes | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | nested FPR10 |
|---|---|---|---|---|---|---|
| 2 | 10/12 | 0.704 | 29/48 | 32/48 | 17/48 vs 44/48 | 13/48 vs 46/48 |
| 4 | 9/12 | 0.679 | **31/48** | 30/48 | **19/48 vs 41/48** | 15/48 vs 46/48 |
| **8 (default)** | **11/12** | **0.707** | 29/48 | **35/48** | **17/48 vs 46/48** | **17/48 vs 46/48** |

Default n=8 wins prompt ranking, file AUC, t=0 spec, nested Youden
spec, and nested FPR10 recall **at mixer seed 20260831**. The
in-domain n=2 / n=4 win did not transfer at that seed, and both
comparisons are seed-confounded. Keep the published protocol frozen. t=0 marked 29/48 here is not the
headline hard last-4 **29/48**. Nested 17/48 is below hits nested
Youden **26/48 vs 44/48** on this same split. Letter d2 stays
negative. Do not sell 31/48, 19/48, or 17/48 as beating poshits
**39/48** or replacing **29/48**.

JSON: [../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/](../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/),
[../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes2/](../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes2/),
[../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes4/](../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes4/).

## Transfer n=8 win is also seed-confounded

Same 24→12 hashtok gate at other feature-hash seeds (not `hash_iv`):

| n_hashes | seed | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|---|
| 8 | **20260831** | **11/12** | 0.707 | 29/48 | 35/48 | 17/48 vs 46/48 |
| 8 | 0 | 10/12 | 0.709 | 27/48 | 36/48 | 14/48 vs 46/48 |
| 8 | 7 | 10/12 | 0.705 | 25/48 | **37/48** | 16/48 vs 45/48 |
| 2 | 7 | 9/12 | **0.740** | 29/48 | 36/48 | **19/48 vs 47/48** |

Default seed 20260831 is the best n=8 prompt ranking here. n=2 seed 7
nested **19/48 vs 47/48** beats that default on nested recall and spec,
with worse prompt ranking. Letter d2 flips at seed 0. Keep the
published protocol frozen (`n_hashes=8`, seed `20260831`). Do not fish
a seed. Do not sell 19/48 or 17/48 as replacing **29/48**.

JSON: [../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-seeds/](../experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-seeds/).

## OR with hard last-4 is complementary TPs, not a detector

Saved 12×4 LOO holdouts, no new GPT-2. Hard last-4 indicate is still
**29/48 vs 23/48** (combined **52/96**). Occupancy-free full-file
hashtok is **33/48 vs 22/48**. OR at t=0 (either `lr>0`) is
**39/48 vs 12/48**, combined **51/96**. That 39 matches poshits on the
TP side only; 36 unmarked false positives make the combined gate
**worse** than indicate. Coverage (use the primary LR when it is
nonzero, else the other channel) is not leftover fill-in:
postokhits-then-hashtok is **35/48 vs 22/48** (combined **57/96**)
versus postokhits standalone **24/48 vs 45/48** (**69/96**).

hashtok recovers 10 of 19 indicate misses: harbour d1, night-bus d1,
market d3, kitchen d3, station d1/d2, office d1, garden d2/d3/d4.
Indicate recovers 6 of 15 hashtok misses: library d1/d3/d4, market d1,
station d4, rain d1. Both miss 9 files, including letter d2/d3/d4.

Honest nested fusion on the same LOO scores throws those extra TPs
away. Leave-one-stem Fisher LDA of indicate+hashtok is **28/48 vs
27/48** at t=0 and nested-by-stem **21/48 vs 37/48**. Nested Youden on
`max(indicate, hashtok)` is **21/48 vs 39/48**. Nested 2D Youden OR is
**37/48 vs 18/48** (still 30 unmarked FPs). Do not sell 39/48. This is
not a 12/12 ensemble; the published hits+hashpool stack stays **11/12**.

JSON: [../experiments/2026-09-01-probe-12x4-hashtok-indicate-or/](../experiments/2026-09-01-probe-12x4-hashtok-indicate-or/).

## tokhybrid copies hashtok isolated; poshashtok is a specificity knob

In-domain 12×4 LOO, full 128-token last-4. `tokhybrid` uses exact
tokhits when the n-gram and next token were seen, else hashtok.
That is token-level occupancy-free hybrid, not file-level OR.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods tokhybrid,poshashtok,hashtok,hybrid \
  --out-dir experiments/2026-09-01-probe-12x4-tokhybrid-poshashtok
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| poshashtok | 11/12 | 0.621 | **28/48** | 25/48 | **14/48 vs 38/48** |
| hashtok | 9/12 | 0.664 | **33/48** | 22/48 | 22/48 vs 30/48 |
| hybrid | 11/12 | 0.725 | **35/48** | 28/48 | 24/48 vs 41/48 |
| **tokhybrid** | **11/12** | 0.683 | **33/48** | 22/48 | **23/48 vs 35/48** |

`tokhybrid` copies hashtok's 33 true positives. No isolated-file sign
flips. Prompt ranking rises to **11/12** (station remains). Nested
spec is still worse than hits **22/48 vs 39/48**. Occupancy hybrid
extras versus tokhybrid are the same four files as hashpool versus
hashtok. Letter d2 stays negative. `poshashtok` (`i // 16`) is a
specificity knob, not a denser isolated-file reader. Do not sell
33/48, 35/48, 28/48, or tokhybrid 11/12 as replacing **29/48**.

JSON: [../experiments/2026-09-01-probe-12x4-tokhybrid-poshashtok/](../experiments/2026-09-01-probe-12x4-tokhybrid-poshashtok/).

## hashtokgap is weaker than hashtok (strict subset)

In-domain 12×4 LOO, full 128-token last-4. `hashtokgap` hashes only
where exact tokhits abstains (the residual of unseen n-grams). That is
the opposite of tokhybrid, still occupancy-free, still no keys.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtokgap,hashtok,tokhybrid \
  --out-dir experiments/2026-09-01-probe-12x4-hashtokgap
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| hashtok | 9/12 | 0.664 | **33/48** | **22/48** | 22/48 vs 30/48 |
| tokhybrid | **11/12** | 0.683 | **33/48** | 22/48 | 23/48 vs 35/48 |
| **hashtokgap** | 8/12 | 0.586 | **27/48** | 21/48 | **17/48 vs 31/48** |

True positives are a strict subset of hashtok. Lost six files, gained
none: harbour d2, kitchen d1, station d1/d2/d3, rain d3. Combined t=0
**48/96** versus hashtok **55/96**. Nested spec is still worse than
hits **22/48 vs 39/48**. Letter d2 stays negative and copies the
hashtok LR. Dropping tokhits-scorable positions does not isolate a
complementary hashed signal; those positions were carrying the six
lost signs when hashed. Do not sell 27/48, 33/48, or tokhybrid 11/12
as replacing **29/48**.

JSON: [../experiments/2026-09-01-probe-12x4-hashtokgap/](../experiments/2026-09-01-probe-12x4-hashtokgap/).

## hashtok2 reshuffles full-file signs; not a singleton core

In-domain 12×4 LOO, full 128-token last-4. `hashtok2` is unbucketed
hashtok with `min_count=2`. Prefix-5 OOD `hashtoklen2` collapsed 21 TPs
to a 10-file singleton-free core. Full-file in-domain does not.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok2,hashtok \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok2
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| hashtok | 9/12 | 0.664 | **33/48** | **22/48** | 22/48 vs 30/48 |
| **hashtok2** | 8/12 | 0.602 | **34/48** | 21/48 | **19/48 vs 35/48** |

Lost three hashtok TPs (harbour d2, night-bus d4, station d1) and
gained four (night-bus d3, library d1/d2, ferry-queue d4). Combined t=0
stays **55/96**. Nested recall drops (19 vs 22) while spec rises
(35 vs 30), still worse than hits **22/48 vs 39/48**. Letter d2 stays
negative. Do not sell 34/48 as replacing **29/48**.

JSON: [../experiments/2026-09-01-probe-12x4-hashtok2/](../experiments/2026-09-01-probe-12x4-hashtok2/).

## Opening-grain hashtok copies tokhits density (24/48)

In-domain 12×4 LOO, matched `--fit-prefix 4`. Opening rankpath on these
twins is **41/48**. Hashed token identity at the same grain is not that
dense.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --methods hits,tokhits,hashtok,hashtok2 \
  --out-dir experiments/2026-09-01-probe-12x4-fitprefix4-hashtok
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem | precision |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.691 | 23/48 | 48/48 | 23/48 vs 48/48 | 1.000 |
| tokhits | **12/12** | 0.772 | 23/48 | 48/48 | 23/48 vs 48/48 | 1.000 |
| **hashtok** | **12/12** | 0.796 | **24/48** | 47/48 | 23/48 vs 47/48 | 0.960 |
| hashtok2 | **12/12** | 0.729 | 22/48 | 48/48 | 22/48 vs 48/48 | 1.000 |

tokhits: 25/48 marked zeros; decided 23/0. tokhits ⊂ hashtok at t=0.
Extra hashtok TP: **letter d3 only**. One unmarked FP: kitchen d4.
Nested Youden drops letter d3 (mean t ≈ 0.065). hashtok2 versus tokhits
gains letter d3 and loses kitchen d4 and rain d1. Letter **d2 is zero**
on all four readers (not the full-file negative LR). Opening hashed
readers copy tokhits density, not rankpath **41/48**. Marked isolated
`lr>0` is **24/48**, below hard last-4 **29/48**. Prompt **12/12** and
unmarked ≤0 **47/48** do not make 24 a denser isolated-file detector.
Do not sell 24/48, 23/48, or tokhits **12/12** as replacing **29/48**.

JSON: [../experiments/2026-09-01-probe-12x4-fitprefix4-hashtok/](../experiments/2026-09-01-probe-12x4-fitprefix4-hashtok/).

