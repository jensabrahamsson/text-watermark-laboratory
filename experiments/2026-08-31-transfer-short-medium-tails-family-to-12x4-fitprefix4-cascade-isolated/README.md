# Cascade after short+medium+tails+neighborhood train (no prompt)

Sixty training stems, 12×4 test, `--fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Isolated generated-only pivot.

postokbackoff **covers 42/48** and marks **34/48** (`lr>0`); eight
covered files have a negative observed-token LR. Precision among
decided files is still **1.000** (0 unmarked FP). Pivot fallback on
the six leftover zeros is 5/6 marked and 15 unmarked FPs. Combined
39/48, precision 0.722. Do not sell 39/48 cascade as beating poshits
39/48.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --extra-train experiments/2026-08-31-pair-long12x4 \
  --extra-train experiments/2026-08-31-pair-tails12x4 \
  --extra-train experiments/2026-08-31-pair-family12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokbackoff \
  --pivot --pivot-weight uniform,entropy --cascade postokbackoff \
  --out-dir experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-isolated
```
