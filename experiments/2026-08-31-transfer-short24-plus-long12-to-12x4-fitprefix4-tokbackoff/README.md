# tokbackoff, 24 short + 12 medium → 12×4

`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

`postokbackoff` **12/12**, isolated **22/48**, precision **1.000** among
decided. Same two extra files as medium-only (harbour draws 3 and 4).
The nine zeros remain. Do not sell 22/48 as beating 39/48.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | precision |
|---|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.639 | 20/48 | **48/48** | 9/33 | 20/19 | 1.000 |
| postokhits | **12/12** | 0.739 | **20/48** | **48/48** | 28/43 | **20/0** | **1.000** |
| **postokbackoff** | **12/12** | 0.757 | **22/48** | **48/48** | 26/43 | **22/0** | **1.000** |
