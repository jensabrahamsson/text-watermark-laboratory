# Opening-only unmarked-LM geometry (in-domain 12×4, no prompt)

Leave-one-of-12-out, `--fit-prefix 4 --pos-bucket 1`. Isolated-file
pivot: generated tokens only (token 0 unscored). `used_keys=false`.

Opening pivot-lda **10/12**, AUC **0.672**, isolated **27/48**. That
beats the published 128-token pivot-lda (10/12, 0.599, 17/48). The
geometry mark is front-loaded. Entropy weighting does not beat
uniform LDA here. postokbackoff is **12/12** / 23/48. Cascade combined
36/48 spends unmarked FPs on the fallback. Not a universal detector.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokbackoff --skip-hashpool \
  --pivot --pivot-weight uniform,entropy --cascade postokbackoff \
  --out-dir experiments/2026-08-31-probe-12x4-fitprefix4-cascade-isolated
```
