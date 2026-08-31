# tokbackoff on the short-train 4-token OOD gate

Train 24 new 36×4 stems, score 12×4. `--fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

`postokbackoff` **copies** `postokhits` here: **12/12**, isolated **16/48**,
precision **1.000** among decided. Shrinking last-k does not cover the
nine After / Closing / Now / While zeros when the extra train seeds are
10–12 word one-liners. Do not sell 16/48 as beating 39/48.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | precision |
|---|---|---|---|---|---|---|---|
| poshits | **12/12** | **0.873** | **39/48** | **41/48** | 9/33 | 39/0 | 0.848 |
| postokhits | **12/12** | 0.694 | **16/48** | **48/48** | 32/44 | **16/0** | **1.000** |
| **postokbackoff** | **12/12** | 0.694 | **16/48** | **48/48** | 32/44 | **16/0** | **1.000** |

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,postokbackoff \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff
```
