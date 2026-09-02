# DistilGPT2 native prefix-4 rankpath (12×4 LOO)

`--fit-prefix 5 --pos-bucket 0`, Distil unmarked LM. Four isolated
choice-matrix rows (generated tokens 1–4). `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| rankpath | **7/12** | **0.563** | 23/48 | 26/48 | 0.099 |
| rankuni | 4/12 | 0.431 | 21/48 | 21/48 | 0.885 |

Same chance result as the opening protocol. Official lamp is still
12/12. See the opening Distil rankpath README.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
