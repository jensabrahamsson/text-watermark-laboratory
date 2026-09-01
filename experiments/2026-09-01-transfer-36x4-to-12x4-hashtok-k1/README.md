# Transfer hashtok last-k: last-1 is not last-4

Train on `experiments/2026-08-31-pair-36x4` after dropping the twelve
overlapping 12×4 stems. Score every file in
`experiments/2026-08-17-pair-12x4`. Occupancy-free `hashtok`. Frozen
mixer: `--n-hashes 8`, seed **20260831** (not `hash_iv`). Nested
Youden / 10% FPR from leave-one-prompt-out on the 24 training stems,
then frozen on the test files. Still no keys.

This directory is **last-1**. Sibling runs: last-2, last-3. Default
last-4: [../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/](../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 1 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-k1
```

| context_len | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | nested FPR10 |
|---|---|---|---|---|---|---|
| **1 (this dir)** | 7/12 | 0.651 | 25/48 | 35/48 | **18/48 vs 45/48** | 8/48 vs 46/48 |
| 2 | 10/12 | **0.738** | **29/48** | **36/48** | 15/48 vs 45/48 | 13/48 vs 47/48 |
| 3 | 10/12 | 0.667 | 25/48 | 34/48 | 11/48 vs 47/48 | 12/48 vs 47/48 |
| 4 (default) | **11/12** | 0.707 | **29/48** | 35/48 | 17/48 vs 46/48 | **17/48 vs 46/48** |

In-domain last-1 was chance. This transfer last-1 has ranking signal
(AUC 0.651) and the highest nested-Youden recall among the four
orders, with collapsed prompt ranking (**7/12**) and nested FPR10
(**8/48**). That is not a reason to change `--context-len`. Letter d2
stays negative. Do **not** sell nested 18/48 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
