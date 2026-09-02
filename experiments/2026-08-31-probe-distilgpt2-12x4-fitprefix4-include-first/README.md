# DistilGPT2 12×4 opening with include-first

`--fit-prefix 4 --pos-bucket 1 --include-first`.

| Method | wins | AUC |
|---|---|---|
| hits / poshits | 6/12 | 0.65 |
| first | 8/12 | 0.676 |

Distil does **not** copy Qwen's first-token 12/12. The opening is
weaker than full-file hits 9/12.
