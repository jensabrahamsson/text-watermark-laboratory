# 60-stem prefix-5 occupancy-free MASK replace → 12×4

Same train as prefix-5 `hashtoklen`. `hashmask` hashes exact last-4 with
one token replaced by `MASK_TAG=-4`. Length stays 4, so a masked 4-gram
is **not** a last-3 and **not** a tagged skip-gram (`SKIP_TAG=-3`).
Occupancy-free: a hash votes only if that MASK-bucket produced the
observed next token. Still no keys. Instance `key-free-hashmask`.
`hashmask2` is score-time `min_count=2` on the same tables.

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

† Ranking of 27 marked zeros plus 21 decided files. Not isolated-file density.

Same 21 true positives at t=0 as hashtoklen, not denser: extras harbour
d3/d4, letter d2, workshop d4; lost market ×4. Six unmarked FPs
(hashtoklen had three). Nested Youden **19/48 vs 45/48** is **worse**
than exact hashtoklen **21/48 vs 45/48**. Keep prefix-5 `hashtoklen`.

Leftover eight at t=0: harbour d3/d4 and letter d2. Nested threshold
0.778 keeps harbour d3/d4 (`+0.861`) and throws letter d2 (`+0.240`).
`hashmask2` leftover TPs are empty. Nested leftover fill-in is **not**
8/8.

Letter d2 official 5-gram `Now in the second I`: only `mask_i=3`
(`Now in the MASK` → `I`) sees the continuation. Two opposing
singleton hashes (c_m=1 vs c_u=1) average to file lr=`+0.240`, which
**is** that official slot (`n_used=1`). `hashmask2` skips both
singletons (`n_used=0`). This is not a dense marked 5-gram. JSON:
[../2026-09-01-letter-d2-first-ngram/letter-d2-hashmask-trace.json](../2026-09-01-letter-d2-first-ngram/letter-d2-hashmask-trace.json).

Do **not** sell 21/48, 19/48, 15/48, or letter d2 `+0.240` as beating
poshits **39/48** or replacing **29/48**. Persist MASK tables as
`tables-hashmask/` (`mask_one=true`, `drop_one=false`,
`exact_len=true`). Do not score mixed `tables-hashpool` or skip tables
with `--score-mode hashmask`.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
