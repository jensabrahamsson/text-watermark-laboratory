# In-domain hashtok `--n-hashes 4`

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. Occupancy-free `hashtok` with four mixer
hashes. Comparison table:
[../2026-09-01-probe-12x4-hashtok-nhashes2/](../2026-09-01-probe-12x4-hashtok-nhashes2/).

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 4 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-nhashes4
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| **hashtok n=4** | **11/12** | 0.733 | **36/48** | 30/48 | **35/48 vs 30/48** |

Densest t=0 marked recall in the width sweep. Nested mean t ≈ 0, so
nested **35/48 vs 30/48** is almost the t=0 gate (spec still 30/48,
same as default n=8 nested spec). Prompt miss: letter. Letter d2 stays
negative. Do **not** sell 36/48 or 35/48 as replacing **29/48** or
beating poshits **39/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
