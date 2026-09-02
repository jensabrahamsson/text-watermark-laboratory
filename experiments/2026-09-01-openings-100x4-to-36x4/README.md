# Opening-overlap bound: 100 families → 36×4

Observed-token isolated recall equals train opening-atom overlap.
`postokhits` covers **117/144** marked files (exact 4-token **103/144**).
Decided precision **0.958** (114 TP, 5 FP). Occupancy-free t=0 on the
frozen lock B tables is **114/144 vs 139/144**.

Same-register overlap, not a universal detector. Does not replace
**25/48**.

```bash
python -m text_watermark_tools openings experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokhits --skip-stem-curve \
  --out-dir experiments/2026-09-01-openings-100x4-to-36x4
```
