# Cascade on the 24-short OOD 4-token gate (no prompt)

Train 24 other 36×4 stems, score 12×4. `--fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Isolated generated-only pivot.

postokbackoff copies **16/48**, precision **1.000**, **12/12**. Opening
LDA does not transfer (4/12, AUC 0.422). Rank+entropy keeps 10/12 with
32/48 and 22 unmarked FPs. Cascade fallback is 2/32 and drops prompt
ranking to 6/12. Do not sell 18/48 or 32/48 as beating 39/48.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods postokbackoff \
  --pivot --pivot-weight uniform,entropy --cascade postokbackoff \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-cascade-isolated
```
