# New-topic matched 4-token poshits, bucket 1

Train 24 new 36×4 stems, score 12×4. `--fit-prefix 4 --pos-bucket 1`.
Nested Youden / 10% FPR from training-stem leave-one-out. `used_keys=false`.

This is the same isolated-file operating point as matched 16-token
bucket 1, on a shorter clip. Nested Youden is **not** conservative here.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | Nested Youden | Nested FPR10 |
|---|---|---|---|---|---|---|
| Full-file hits (published) | **12/12** | 0.793 | **42/48** | 24/48 | 26/48 vs 44/48 | 21/48 vs 45/48 |
| Window 0:4 hits (fit-full) | 11/12 | 0.752 | 40/48 | 23/48 | — | — |
| Matched 4-token hits | 11/12 | 0.820 | 39/48 | 33/48 | **39/48 vs 38/48** | **39/48 vs 38/48** |
| **Matched 4-token poshits, bucket 1** | **12/12** | **0.873** | 39/48 | **41/48** | **39/48 vs 41/48** | **39/48 vs 41/48** |
| Matched 16-token poshits, bucket 1 | **12/12** | **0.873** | 39/48 | **41/48** | 16/48 vs 48/48 | **39/48 vs 41/48** |

Four tokens, position-namespaced, trained on other GPT-2 topics: prompt
ranking **12/12**, file AUC **0.873**, isolated t=0 **39/48 vs 41/48**,
and the train-LOO nested Youden matches t=0. The 16-token finest-bucket
reader copies the ranking and t=0 numbers; its nested Youden overfits
the longer in-domain window.

Still GPT-2, same generator, new topics. Not a universal detector. Not
keys. Do not replace 10/12, 29/48, or 36/36.
