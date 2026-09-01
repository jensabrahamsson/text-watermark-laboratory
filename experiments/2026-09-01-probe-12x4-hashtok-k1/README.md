# In-domain hashtok last-k ablation (`--context-len`)

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files. Occupancy-free `hashtok` while varying n-gram order.
Frozen mixer: `--n-hashes 8`, seed **20260831** (not SynthID
`hash_iv`). Same mixer as
[../2026-09-01-probe-12x4-hashtok/](../2026-09-01-probe-12x4-hashtok/)
(CLI default **last-4**). Still no keys.

This directory is **last-1**. Sibling runs: last-2, last-3.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 1 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-k1
```

| context_len | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| **1 (this dir)** | **5/12** | **0.507** | 22/48 | 22/48 | **9/48 vs 42/48** |
| 2 | 9/12 | 0.585 | 27/48 | 28/48 | 19/48 vs 32/48 |
| 3 | **11/12** | 0.666 | 24/48 | **36/48** | **22/48 vs 40/48** |
| 4 (default) | 9/12 | 0.664 | **33/48** | 22/48 | 22/48 vs 30/48 |

Last-1 is chance (permutation p = 0.45). Last-3 has the best prompt
ranking and nested spec here, with sparser t=0 marked recall (**24/48**
is below default **33/48** and below hard last-4 **29/48**). Last-2
ranking is not a 5% test (p ≈ 0.097). Letter d2 stays negative at
last-1/2/4 and flips positive at last-3; the letter *prompt* still
loses at last-1/2 and wins at last-3/4. Do not sell that flip as the
official 5-gram.

Keep `--context-len 4`. Order is a knob, like mixer width and seed.
Do **not** sell 24/48, nested 22/48, or last-3 prompt **11/12** as
replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
