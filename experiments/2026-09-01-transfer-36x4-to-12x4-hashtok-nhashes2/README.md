# Transfer hashtok `--n-hashes 2`

24 new 36×4 stems → original 12×4 files. Occupancy-free `hashtok` with
two mixer hashes. Comparison table:
[../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/](../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 2 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes2
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| **hashtok n=2** | 10/12 | 0.704 | 29/48 | 32/48 | **17/48 vs 44/48** |

In-domain n=2 beat default n=8. This OOD gate does not: prompt 10/12
vs n=8 **11/12**, nested spec 44 vs **46**. t=0 marked 29/48 is not
the headline hard last-4 **29/48**. Keep the CLI default at 8. Do not
sell 29/48 or 17/48 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
