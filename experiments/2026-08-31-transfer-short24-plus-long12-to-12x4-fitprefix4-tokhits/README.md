# 24 short one-liners plus 12 medium scenes → 12×4

Train stems 13–36 (short) and 37–48 (medium). Score original 12×4.
`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

`postokhits` **12/12**, isolated **20/48**, precision **1.000** among
decided (20 TP, 0 FP). The extra file versus medium-only is rain draw 2.
The nine After / Closing / Now / While zeros remain. poshits is still
8/12 with 19 wrong-sign marked files. Do not replace 16/48 or 39/48.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | precision |
|---|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.639 | 20/48 | **48/48** | 9/33 | 20/19 | 1.000 |
| **postokhits** | **12/12** | 0.739 | **20/48** | **48/48** | 28/43 | **20/0** | **1.000** |
