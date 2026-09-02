# Matched 4-token last-1 poshits

36×4 leave-one-out. `--fit-prefix 4 --context-len 1 --pos-bucket 1`.
`used_keys=false`. Last-4 at the opening is already truncated to last-1
at i=1, last-2 at i=2, last-3 at i=3. This run asks that question
explicitly.

| Method | wins | AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| hits | 34/36 | 0.936 | 132/144 | 106/144 |
| **poshits** | **34/36** | **0.940** | 132/144 | **128/144** |
| first (token 0 only) | 34/36 | 0.687 | 114/144 | 92/144 |

Out of family this last-1 poshits reader copies the published 4-token
last-4 gate. Token 0 alone is weaker in-domain ranking (AUC 0.687).
Do not replace 10/12, 29/48, or 36/36.
