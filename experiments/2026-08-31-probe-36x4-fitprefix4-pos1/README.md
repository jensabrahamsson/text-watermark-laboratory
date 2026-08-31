# Matched 4-token fit with position buckets (36×4)

`--fit-prefix 4` clips every draw before fit and score. `--pos-bucket 1`
namespaces last-k by exact token index. `used_keys=false`.

Scoring a 0:4 **slice** of a 128-token table already ranks 34/36. Fitting
on those four tokens is the matched protocol. Position namespacing
balances t=0.

| Method | Prompt wins | Marked `> 0` | Unmarked `≤ 0` | AUC | Nested-by-stem |
|---|---|---|---|---|---|
| Window 0:4 hits (fit-full) | **34/36** | 129/144 | 92/144 | 0.917 | 117/144 vs 126/144 |
| **Matched 4-token hits** | **34/36** | 132/144 | 114/144 | **0.935** | 121/144 vs 129/144 |
| **Matched 4-token poshits, bucket 1** | **34/36** | 131/144 | **132/144** | **0.935** | 121/144 vs 132/144 |
| Matched 16-token poshits, bucket 1 | **34/36** | 132/144 | **132/144** | 0.938 | 124/144 vs 132/144 |

Four tokens plus position namespace recover the 16-token bucket-1 t=0
balance. Prompt grain stays 34/36. Do not replace 36/36.
