# Rank-path opening probe (12×4 LOO, isolated)

`--fit-prefix 4 --pos-bucket 1 --rankpath --cascade postokbackoff --cascade-fallback rankuni`.
`used_keys=false`.

Rankpath **12/12**, AUC **0.797**, isolated **41/48** vs 39/48 unmarked ≤0
(precision 0.820). Opening LDA on the same files is 27/48. Not 29/48.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
