# Transfer hashtok last-k: last-2 AUC is not last-4 nested

Train on `experiments/2026-08-31-pair-36x4` after dropping the twelve
overlapping 12×4 stems. Score every file in
`experiments/2026-08-17-pair-12x4`. Occupancy-free `hashtok`. Frozen
mixer: `--n-hashes 8`, seed **20260831** (not `hash_iv`). Nested
Youden / 10% FPR from leave-one-prompt-out on the 24 training stems,
then frozen on the test files. Still no keys.

This directory is **last-2**. Sibling runs: last-1, last-3. Default
last-4: [../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/](../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 2 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-k2
```

| context_len | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | nested FPR10 |
|---|---|---|---|---|---|---|
| 1 | 7/12 | 0.651 | 25/48 | 35/48 | 18/48 vs 45/48 | 8/48 vs 46/48 |
| **2 (this dir)** | 10/12 | **0.738** | **29/48** | **36/48** | 15/48 vs 45/48 | 13/48 vs 47/48 |
| 3 | 10/12 | 0.667 | 25/48 | 34/48 | 11/48 vs 47/48 | 12/48 vs 47/48 |
| 4 (default) | **11/12** | 0.707 | **29/48** | 35/48 | 17/48 vs 46/48 | **17/48 vs 46/48** |

Last-2 has the best file AUC and t=0 unmarked spec on this split.
t=0 marked **29/48** copies default last-4 and is **not** the headline
hard last-4 **29/48**. Nested Youden recall **15/48** and nested FPR10
**13/48** are below last-4. Prompt ranking is **10/12**, not **11/12**.
Letter d2 stays negative. Keep `--context-len 4`. Do **not** sell
AUC 0.738 or t=0 29/48 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
