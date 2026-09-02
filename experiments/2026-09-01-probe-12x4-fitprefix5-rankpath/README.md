# In-domain prefix-5 rankpath (12×4 LOO)

`--fit-prefix 5 --pos-bucket 1 --rankpath --windows 3:4`.
`used_keys=false`. Four rank symbols, last row = generated token 4
(the first official 5-gram).

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| postokbackoff | 12/12 | 0.756 | 23/48 | 47/48 |
| **rankpath** | **11/12** | 0.767 | **30/48** | **36/48** |
| rankuni | 11/12 | 0.738 | 34/48 | 32/48 |

Prefix-4 opening rankpath on the same twins is **12/12**, **41/48 vs
39/48**. Prefix-5 does **not** beat it. Letter d2 stays `lr<0`
(−1.208). Window `3:4` rankuni (the official 5-gram token alone) is
**4/12**, AUC **0.406**. Do not sell 30/48 as beating **29/48** or
prefix-4 **41/48**.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md),
[../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
