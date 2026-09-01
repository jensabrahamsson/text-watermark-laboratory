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
  it reads occupancy.

Keep exact `postokhits` when the claim is observed-token preference.
Keep `hashpool` only if occupancy of empty cells is an acceptable
regulariser, and say so. `hashtok` is the occupancy-free hashed
reader.
