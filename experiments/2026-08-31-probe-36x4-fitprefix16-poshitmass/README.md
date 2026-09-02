# Matched 16-token poshits and poshitmass, bucket 4 (36×4)

Same `--fit-prefix 16 --pos-bucket 4` protocol as
[`../2026-08-31-probe-36x4-fitprefix16-pos4/`](../2026-08-31-probe-36x4-fitprefix16-pos4/).
`poshitmass` is hits log-ratio × fraction of positions that hit, on
those bucketed tables. `used_keys=false`.

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden |
|---|---|---|---|---|---|
| Full 128-token hits (published) | **36/36** | 134/144 | 76/144 | 0.934 | 119/144 vs 134/144 |
| Full 128-token hitmass (published) | **36/36** | 134/144 | 76/144 | **0.938** | 116/144 vs 134/144 |
| Matched 16-token poshits, bucket 4 | **34/36** | 133/144 | **114/144** | 0.937 | 122/144 vs 127/144 |
| **Matched 16-token poshitmass, bucket 4** | **34/36** | 133/144 | **114/144** | **0.943** | 121/144 vs 130/144 |

poshitmass keeps the same t=0 counts as poshits and raises file AUC.
That 0.943 is a **16-token** reader; do not quote it as beating
full-file hitmass 0.938 like-for-like. Unmarked `≤ 0` is **114/144**
rather than 76/144. Prompt grain stays 34/36.

Do not replace 36/36 or 29/48.
