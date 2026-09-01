# Prefix-4 rank-path cascade fallback (60-stem train → 12×4)

Count tables: `--fit-prefix 4 --pos-bucket 1` postokbackoff.
Fallback: unbucketed first four rank symbols (`--cascade-rankpath-end 4
--rankpath-pos-bucket 0`). Not the full file. `used_keys=false`.

postokbackoff still **42 covered / 34 `lr>0`**, precision **1.000**.
Prefix-4 rankpath signs **1/6** leftover zeros (`The printer worked
better`) and 5 of 42 uncovered unmarked files. Combined cascade
**35/48 vs 43/48**, precision **0.875**. Uncovered FPR10 is the same
1/6 leftover with 4 unmarked FPs.

That is higher precision than opening rankuni (2/6 leftover, 15
unmarked FPs, cascade 36/48) and than full-file rankpath (4/6 leftover,
17 unmarked FPs, cascade 38/48). Do not sell 35/48 as beating poshits
39/48. Mixed AUC 0.825 is not a detector.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).

See [results.md](results.md).
