# In-domain hashtok `--n-hashes 16`

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. Occupancy-free `hashtok` with sixteen mixer
hashes. Comparison table:
[../2026-09-01-probe-12x4-hashtok-nhashes2/](../2026-09-01-probe-12x4-hashtok-nhashes2/).

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods hashtok --n-hashes 16 \
  --out-dir experiments/2026-09-01-probe-12x4-hashtok-nhashes16
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| **hashtok n=16** | **11/12** | 0.662 | **36/48** | 22/48 | **29/48 vs 24/48** |

Same t=0 marked count as n=4 (**36/48**) with default-like unmarked
spec (**22/48**). Nested spec **24/48** is a coin flip. File AUC
matches default n=8, not n=2. Prompt miss: letter. This is the only
width in the sweep with letter d2 `lr>0`; the letter prompt still
loses. Do not sell that as reading the official 5-gram. Do **not**
sell 36/48 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
