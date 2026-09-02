# In-domain hashtok2 reshuffles signs; not a singleton core

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. `hashtok2` is unbucketed hashtok with
`min_count=2`: skip a hash unless the observed next token appeared at
least twice in that bucket. Same mixer as hashtok, not exact-length
`hashtoklen2`. Occupancy-free. Still no keys.

Prefix-5 OOD `hashtoklen2` collapsed 21 TPs to a 10-file singleton-free
core. This full-file in-domain check asks whether hashtok's 33 TPs
were the same kind of singleton pile.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok2,hashtok \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok2
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| hashtok | 9/12 | 0.664 | **33/48** | **22/48** | 22/48 vs 30/48 |
| **hashtok2** | 8/12 | 0.602 | **34/48** | 21/48 | **19/48 vs 35/48** |

Skipping singletons **reshuffles** t=0 signs (lost 3, gained 4). It
does not peel a robust core. Combined t=0 stays **55/96**. Nested
recall drops (19 vs 22) while spec rises (35 vs 30), still worse than
hits **22/48 vs 39/48**. Letter d2 stays negative and is more negative
than hashtok. Prompt misses: night-bus, library, market, letter.

Lost versus hashtok: harbour d2, night-bus d4, station d1. Gained:
night-bus d3, library d1/d2, ferry-queue d4. Do **not** sell 34/48 as
replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
