# Full-file rank-path probe (12×4 LOO, isolated)

`--rankpath --rankpath-full --rankpath-pos-bucket 0` with matched prefixes
and windows. `used_keys=false`.

Full 128-token path is chance: **8/12**, AUC **0.559**, perm p=0.145.
Prefix of four rank symbols is **10/12**, AUC **0.718**, isolated 30/48
vs 35/48. Window 16:32 is chance (6/12, AUC 0.506). The opening reader
(`--fit-prefix 4 --pos-bucket 1`) remains **12/12 / 41/48**.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
