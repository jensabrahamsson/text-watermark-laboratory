# DistilGPT2 native opening rankpath (12×4 LOO)

`--fit-prefix 4 --pos-bucket 1`, Distil unmarked LM, Distil twins.
Official lamp on this pile is **12/12**. `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| rankpath | **8/12** | **0.579** | 28/48 | 32/48 | 0.132 |
| rankuni | 5/12 | 0.451 | 25/48 | 25/48 | 0.876 |

Chance. Distil in-domain token hits on the same twins is **9/12**,
AUC 0.705. A working mixin is not enough: Distil unmarked-LM five-symbol
bins do not carry the GPT-2 opening rank-path. Rank-path is **not** a
universal tournament detector across GPT-2-family generators.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
