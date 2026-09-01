# Transfer hashtok last-k: last-3 nested is sparse

Train on `experiments/2026-08-31-pair-36x4` after dropping the twelve
overlapping 12×4 stems. Score every file in
`experiments/2026-08-17-pair-12x4`. Occupancy-free `hashtok`. Frozen
mixer: `--n-hashes 8`, seed **20260831** (not `hash_iv`). Nested
Youden / 10% FPR from leave-one-prompt-out on the 24 training stems,
then frozen on the test files. Still no keys.

This directory is **last-3**. Sibling runs: last-1, last-2. Default
last-4: [../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/](../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --context-len 3 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-k3
```

| context_len | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | nested FPR10 |
|---|---|---|---|---|---|---|
| 1 | 7/12 | 0.651 | 25/48 | 35/48 | 18/48 vs 45/48 | 8/48 vs 46/48 |
| 2 | 10/12 | **0.738** | **29/48** | **36/48** | 15/48 vs 45/48 | 13/48 vs 47/48 |
| **3 (this dir)** | 10/12 | 0.667 | 25/48 | 34/48 | **11/48 vs 47/48** | 12/48 vs 47/48 |
| 4 (default) | **11/12** | 0.707 | **29/48** | 35/48 | 17/48 vs 46/48 | **17/48 vs 46/48** |

In-domain last-3 was the best prompt ranking (**11/12**) and nested
spec. That win does **not** transfer: nested Youden recall drops to
**11/48**, t=0 marked **25/48**, prompt **10/12**. Letter d2 is
negative here (in-domain last-3 had flipped positive). Keep
`--context-len 4`. Do **not** sell 11/48 nested or in-domain last-3
**11/12** as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
