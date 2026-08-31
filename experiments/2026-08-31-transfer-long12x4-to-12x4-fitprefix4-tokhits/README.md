# Medium-length new-topic transfer onto 12×4

Train 12 new ~40-word scene stems × 4, score original 12×4.
`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

Official lamp on the train pile is **12/12**. Generated token 0 is only
`"` and `The` — no After / Closing / Now / While.

`postokhits` stays **12/12** with isolated **19/48** and precision
**1.000** among decided files (19 TP, 0 FP). That is +3 files versus
the 24 short one-liner train (**16/48**), all four *market* draws
(`The dog`, seen in canal-lock train). The same nine zeros remain.

`poshits` on this train is **8/12** and 20 marked **wrong-sign** files.
Unseen-after-The Laplace **flips** (δ ≈ −0.365) because these medium
seeds use `The` on the marked side. The 39/48 poshits number on the
short-seed train is occupancy-specific. Do not replace 10/12, 29/48,
16/48, or 39/48.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | precision |
|---|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.621 | 19/48 | **48/48** | 9/33 | 19/20 | 1.000 |
| **postokhits** | **12/12** | 0.729 | **19/48** | **48/48** | 29/43 | **19/0** | **1.000** |

```bash
python -m text_watermark_tools pair experiments/2026-08-31-prompts-long12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-08-31-pair-long12x4

python -m text_watermark_tools probe experiments/2026-08-31-pair-long12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits \
  --out-dir experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits
```
