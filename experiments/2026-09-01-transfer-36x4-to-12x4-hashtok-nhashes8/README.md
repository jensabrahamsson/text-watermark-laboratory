# Transfer hashtok mixer width: default n=8 wins OOD

Train on `experiments/2026-08-31-pair-36x4` after dropping the twelve
overlapping 12×4 stems. Score every file in
`experiments/2026-08-17-pair-12x4`. Occupancy-free `hashtok`, last-4,
full 128-token files. Nested Youden / 10% FPR from leave-one-prompt-out
on the 24 training stems, then frozen on the test files. Still no keys.

In-domain 12×4 LOO preferred n=2 / n=4 over the CLI default n=8
([../2026-09-01-probe-12x4-hashtok-nhashes2/](../2026-09-01-probe-12x4-hashtok-nhashes2/)).
This is the transfer gate that decides whether to change the default.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 8 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8
```

| n_hashes | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | nested FPR10 |
|---|---|---|---|---|---|---|
| 2 | 10/12 | 0.704 | 29/48 | 32/48 | 17/48 vs 44/48 | 13/48 vs 46/48 |
| 4 | 9/12 | 0.679 | **31/48** | 30/48 | **19/48 vs 41/48** | 15/48 vs 46/48 |
| **8 (default, this dir)** | **11/12** | **0.707** | 29/48 | **35/48** | **17/48 vs 46/48** | **17/48 vs 46/48** |

Default n=8 wins prompt ranking, file AUC, t=0 unmarked spec, nested
Youden spec, and nested FPR10 recall. n=4 is densest at t=0 and nested
recall, with the worst nested spec. The in-domain n=2 / n=4 win did
**not** transfer. Keep the CLI default at 8.

t=0 marked **29/48** here is not the headline hard last-4 **29/48**:
different scorer, different split. Nested 17/48 is below hits nested
Youden **26/48 vs 44/48** on this same 24→12 gate. Letter d2 stays
negative at all three widths. Do **not** sell 31/48, 19/48, or 17/48
as beating poshits **39/48** or replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
