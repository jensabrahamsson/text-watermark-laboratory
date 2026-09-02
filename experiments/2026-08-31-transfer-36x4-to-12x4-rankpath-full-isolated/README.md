# Full-file rank-path transfer (24 short 36×4 stems → 12×4)

`--rankpath --rankpath-full --rankpath-pos-bucket 0`. `used_keys=false`.
Overlap dropped from train.

Full path **6/12**, AUC 0.534. Matched prefix of four rank symbols:
**11/12**, AUC **0.759**, isolated **25/48 vs 43/48** (5 unmarked FPs,
precision 0.833). Window 16:32 is chance. Full-file rankuni 41/48 spends
31 unmarked FPs. Not 29/48 and not poshits 39/48.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
