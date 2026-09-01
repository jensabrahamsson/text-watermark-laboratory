# In-domain hashtokgap is weaker than hashtok

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. `hashtokgap` is the occupancy-free residual of
`tokhybrid`: skip positions whose exact last-k and next token were
seen, and average hashtok only on the rest. Laplace cannot vote.
Still no keys.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtokgap,hashtok,tokhybrid \
  --out-dir experiments/2026-09-01-probe-12x4-hashtokgap
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| hashtok | 9/12 | 0.664 | **33/48** | **22/48** | 22/48 vs 30/48 |
| tokhybrid | **11/12** | 0.683 | **33/48** | **22/48** | 23/48 vs 35/48 |
| **hashtokgap** | 8/12 | 0.586 | **27/48** | 21/48 | **17/48 vs 31/48** |

`hashtokgap` true positives are a strict subset of hashtok's 33. It
loses six files and gains none: harbour d2, kitchen d1, station
d1/d2/d3, rain d3. Combined t=0 is **48/96** (chance) versus hashtok
**55/96**. Nested spec is still worse than hits **22/48 vs 39/48**.
Letter d2 stays negative and copies the hashtok LR. Prompt misses are
market, station, office, ferry-queue.

Dropping tokhits-scorable positions does not isolate a complementary
hashed signal. Those positions were carrying the six lost file signs
when hashed. Token-level tokhybrid still copies hashtok **33/48**.
Do **not** sell 27/48, 33/48, or tokhybrid 11/12 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
