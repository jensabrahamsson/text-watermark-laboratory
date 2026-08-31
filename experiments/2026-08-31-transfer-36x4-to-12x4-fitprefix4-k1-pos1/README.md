# New-topic matched 4-token last-1

Train 24 new 36×4 stems, score 12×4. `--fit-prefix 4 --context-len 1
--pos-bucket 1`. Nested Youden from training-stem leave-one-out.
`used_keys=false`.

| Method | Prompt wins | File AUC | t=0 | Nested Youden |
|---|---|---|---|---|
| hits | 11/12 | 0.846 | 39/48 vs 38/48 | 16 vs 45 (conservative) |
| **poshits** | **12/12** | **0.873** | **39/48 vs 41/48** | 16 vs 48 (conservative) |
| first | 6/12 | 0.555 | 16/48 vs 40/48 | chance |

Last-1 poshits on four tokens is the same OOD ranking and t=0 as last-4
poshits on four tokens (12/12, 0.873, 39 vs 41). Nested Youden on last-1
is conservative; quote t=0 / nested FPR10. First-token-only does not
transfer. Still GPT-2, new topics. Not a universal detector.
