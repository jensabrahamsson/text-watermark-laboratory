# tokbackoff, 12 medium scenes → 12×4

Train 12 new ~40-word stems × 4. `--fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

`postokbackoff` **12/12**, isolated **21/48**, precision **1.000** among
decided (21 TP, 0 FP). That is +2 files versus `postokhits` **19/48** on
the same train: harbour draws 3 and 4, `The ferry was in`. Full last-3
never saw `in`; last-1 `' was' → ' in'` did (2 marked / 0 unmarked).
The nine After / Closing / Now / While zeros remain. Do not sell 21/48
as beating 39/48.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | precision |
|---|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.621 | 19/48 | **48/48** | 9/33 | 19/20 | 1.000 |
| postokhits | **12/12** | 0.729 | **19/48** | **48/48** | 29/43 | **19/0** | **1.000** |
| **postokbackoff** | **12/12** | 0.748 | **21/48** | **48/48** | 27/43 | **21/0** | **1.000** |
