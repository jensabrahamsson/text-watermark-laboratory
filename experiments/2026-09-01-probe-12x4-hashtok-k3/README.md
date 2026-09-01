# In-domain hashtok last-k ablation (`--context-len`)

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files. Occupancy-free `hashtok` while varying n-gram order.
Frozen mixer: `--n-hashes 8`, seed **20260831** (not SynthID
`hash_iv`). Same mixer as
[../2026-09-01-probe-12x4-hashtok/](../2026-09-01-probe-12x4-hashtok/)
(CLI default **last-4**). Still no keys.

This directory is **last-3**. Sibling runs: last-1, last-2.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 3 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-k3
```

| context_len | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| 1 | 5/12 | 0.507 | 22/48 | 22/48 | 9/48 vs 42/48 |
| 2 | 9/12 | 0.585 | 27/48 | 28/48 | 19/48 vs 32/48 |
| **3 (this dir)** | **11/12** | 0.666 | 24/48 | **36/48** | **22/48 vs 40/48** |
| 4 (default) | 9/12 | 0.664 | **33/48** | 22/48 | 22/48 vs 30/48 |

Last-3 is the best *prompt ranking* and nested spec on this in-domain
gate. Marked t=0 **24/48** is below default last-4 **33/48** and below
hard last-4 **29/48**. Nested recall **22/48** copies default last-4
and is not denser. Letter d2 is positive here; that is an order flip
like n=16, not the official 5-gram. Combined t=0 **60/96** is a
specificity knob, not a calibrated detector.

Keep `--context-len 4`. Do **not** sell 24/48, nested 22/48, or prompt
**11/12** as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
