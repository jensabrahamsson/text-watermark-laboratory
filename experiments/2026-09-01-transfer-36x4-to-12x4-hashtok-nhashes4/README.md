# Transfer hashtok `--n-hashes 4`

24 new 36×4 stems → original 12×4 files. Occupancy-free `hashtok` with
four mixer hashes. Comparison table:
[../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/](../2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8/).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 4 \
  --out-dir experiments/2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes4
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| **hashtok n=4** | 9/12 | 0.679 | **31/48** | 30/48 | **19/48 vs 41/48** |

Densest t=0 and nested recall in this width sweep, worst nested spec
and prompt ranking. The in-domain n=4 win did **not** transfer. Keep
the CLI default at 8. Do **not** sell 31/48 or 19/48 as beating
poshits **39/48** or replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
