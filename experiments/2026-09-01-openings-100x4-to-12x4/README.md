# Opening-overlap bound: 100 families → original 12×4

Observed-token isolated recall on the frozen lock B tables equals
train opening-atom overlap. Not a new `probe --methods` name.

`postokhits` covers **18/48** marked files (exact 4-token copy
**14/48**). Decided precision **1.000** (16 TP, 0 FP). Occupancy-free
t=0 on those tables is **16/48 vs 48/48**: two covered files have
non-positive observed-token LR.

The 30 unmarked-style zeros are the original Grok openings the 100
one-line scenes do not produce (`The ferry`, `Closing`, `The dog`,
`The printer`). Does not replace **25/48**.

```bash
python -m text_watermark_tools openings experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-100x4-to-12x4
```
