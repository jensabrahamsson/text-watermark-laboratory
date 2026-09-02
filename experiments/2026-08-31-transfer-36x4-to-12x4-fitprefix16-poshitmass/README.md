# New-topic matched 16-token poshits / poshitmass, bucket 4

Train 24 new 36×4 stems, score the original 12×4 files.
`--fit-prefix 16 --pos-bucket 4`. Nested Youden / 10% FPR from
leave-one-prompt-out on the **training** stems, then frozen on test.
`used_keys=false`. Shared stems dropped.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | Nested-by-stem |
|---|---|---|---|---|---|
| Full-file hits (published) | **12/12** | 0.793 | **42/48** | 24/48 | train-LOO Youden 26/48 vs 44/48 |
| Matched 16-token poshits, bucket 4 | **11/12** | 0.820 | 39/48 | 33/48 | **39/48 vs 38/48** |
| **Matched 16-token poshitmass, bucket 4** | **11/12** | **0.831** | 39/48 | 33/48 | **39/48 vs 38/48** |

Train-LOO nested Youden is conservative here (**16/48** vs **45/48**):
in-domain Youden sets a high threshold. Nested 10% FPR recovers
**39/48 vs 38/48**, matching nested-by-stem. Quote nested FPR10 / t=0,
not nested Youden, as the isolated-file gate on this split.

Do not replace 10/12, 29/48, or 36/36.
