# In-domain hashtok last-k ablation (`--context-len`)

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files. Occupancy-free `hashtok` while varying n-gram order.
Frozen mixer: `--n-hashes 8`, seed **20260831** (not SynthID
`hash_iv`). Same mixer as
[../2026-09-01-probe-12x4-hashtok/](../2026-09-01-probe-12x4-hashtok/)
(CLI default **last-4**). Still no keys.

This directory is **last-2**. Sibling runs: last-1, last-3.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 2 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-k2
```

| context_len | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| 1 | 5/12 | 0.507 | 22/48 | 22/48 | 9/48 vs 42/48 |
| **2 (this dir)** | 9/12 | 0.585 | 27/48 | 28/48 | 19/48 vs 32/48 |
| 3 | **11/12** | 0.666 | 24/48 | **36/48** | **22/48 vs 40/48** |
| 4 (default) | 9/12 | 0.664 | **33/48** | 22/48 | 22/48 vs 30/48 |

Last-2 is between chance last-1 and default last-4. Ranking is not a
5% test (permutation p ≈ 0.097). Letter d2 stays negative. Combined
t=0 **55/96** matches default last-4's combined count with a different
split of signs, not a denser isolated-file detector.

Keep `--context-len 4`. Do **not** sell 27/48 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
