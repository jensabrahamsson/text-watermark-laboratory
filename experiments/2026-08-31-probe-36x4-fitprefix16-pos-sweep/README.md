# Matched 16-token poshits bucket sweep (36×4)

`--fit-prefix 16` clips every draw before fit and score. `--pos-bucket N`
prepends `i // N` to last-4. That namespace is not a watermark key.
Bucket 16 on a 16-token prefix is a no-op (every token sits in bucket 0).
`used_keys=false`.

| bucket | prompt wins | file AUC | marked `> 0` | unmarked `≤ 0` | nested-by-stem |
|---|---|---|---|---|---|
| **1** | **34/36** | **0.938** | 132/144 | **132/144** | 124/144 vs 132/144 |
| 2 | **34/36** | **0.938** | 132/144 | **132/144** | 124/144 vs 132/144 |
| 4 | **34/36** | **0.937** | **133/144** | 114/144 | 122/144 vs 127/144 |
| 8 | **34/36** | 0.936 | 133/144 | 114/144 | 122/144 vs 127/144 |

Bucket 1 and bucket 2 produce **identical** leave-one-out LRs on this
prefix: no last-4 repeats across odd/even neighbouring offsets here.
Finest namespace (bucket ≤ 2) balances t=0 **132/144 vs 132/144**. Prompt
grain stays 34/36. Do not replace 36/36.

Out of family, the same bucket-1 reader is
[`../2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos1/`](../2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos1/).
