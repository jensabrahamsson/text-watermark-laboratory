# Leave-one-prompt LDA stack of hits + hashpool (12×4)

Post-hoc Fisher LDA on the already-saved 12×4 `hits` and `hashpool` file
scores. Weights are fit without the held prompt. No new generation, no
keys.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hits (source) | 11/12 | 0.737 | 28/48 | 30/48 |
| hashpool (source) | 11/12 | 0.716 | 35/48 | 29/48 |
| **stack** | **11/12** | **0.732** | 23/48 | **44/48** |

The stack does not beat hits on AUC or hashpool on isolated recall. It
moves the decision toward specificity (44/48 unmarked ≤ 0). Complementary
prompt misses are recorded in the probe note; this is not a 12/12 ensemble
claim.
