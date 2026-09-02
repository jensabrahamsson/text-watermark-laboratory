# 60-stem prefix-5 occupancy-free drop-one skip-grams → 12×4

Same train as prefix-5 `hashtoklen`. `hashskip` hashes exact last-4
with one token dropped. Each view is tagged `(SKIP_TAG, drop_index,
*kept)` so a drop-one 4-gram is **not** a last-3. Occupancy-free: a
hash votes only if that skip-bucket produced the observed next token.
Still no keys. Instance `key-free-hashskip`.

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

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtoklen | 12/12† | 0.701 | **21/48** | 45/48 | **21/48 vs 45/48** | 0.875 |
| **hashskip** | 8/12 | 0.663 | **25/48** | 35/48 | **16/48 vs 41/48** | 0.658 |

† Ranking of 27 marked zeros plus 21 decided files. Not isolated-file density.

t=0 extras versus hashtoklen: harbour d3/d4, night-bus d2/d4, workshop
d4. Lost rain d2. Thirteen unmarked FPs (hashtoklen had three). Nested
Youden **16/48** is the honest isolated-file number: the extra density
is low-precision skip collisions, so the training-stem threshold
(0.867) throws most of them out.

Leftover eight (prefix-4 cascade-when-positive misses): harbour d3/d4
sign at t=0 (tiny +0.120); letter d2 is **negative** (lr=−0.847);
station d4, letter d3, office d1/d3, ferry-queue d4 still abstain.
Nested leftover fill-in **0/8**.

Letter d2 official 5-gram `Now in the second I`: drop-2 and drop-3
skip views **see** `I`, both unmarked-only (c_m=0, c_u=1). Coarsening
finds the same unmarked preference last-1 already had. It is not a
rescue of an unseen 5-gram. JSON:
[../2026-09-01-letter-d2-first-ngram/letter-d2-hashskip-trace.json](../2026-09-01-letter-d2-first-ngram/letter-d2-hashskip-trace.json).

Do **not** sell 25/48 or 16/48 as beating poshits **39/48** or
replacing **29/48**. Persist exact skip tables as `tables-hashskip/`
(`drop_one=true`). Do not score mixed `tables-hashpool` with
`--score-mode hashskip`.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
