# New-topic tokhits: occupancy Laplace vs observed next tokens

Train 24 new 36×4 stems, score 12×4. `--fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

poshits on this gate is **12/12**, AUC **0.873**, t=0 **39/48 vs 41/48**.
That 39/48 includes The-Laplace occupancy (δ = 0.330103 for every novel
continuation after `'The'`). `postokhits` keeps only next tokens seen in
train: **12/12**, isolated **16/48**, precision **1.000** among decided
files (16 TP, 0 FP). Do not sell 16/48 as beating 39/48.

Not a universal detector. Not keys. Do not replace 10/12, 29/48, or 36/36.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|---|---|---|
| poshits | **12/12** | **0.873** | **39/48** | **41/48** | 9/33 | 39/0 | 7/8 | 0.848 |
| **postokhits** | **12/12** | 0.694 | **16/48** | **48/48** | 32/44 | **16/0** | **0/4** | **1.000** |
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 9/22 | 39/0 | 15/11 | 0.722 |
| tokhits | 11/12 | 0.674 | 16/48 | 45/48 | 32/39 | 16/0 | 3/6 | 0.842 |

Atom dump: [`atoms.json`](atoms.json) (26 types; unseen-next mass 34,
seen-next 33). Rebuild with `text_watermark_tools.atoms.dump_opening_atoms`.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,hits,tokhits \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits
```
