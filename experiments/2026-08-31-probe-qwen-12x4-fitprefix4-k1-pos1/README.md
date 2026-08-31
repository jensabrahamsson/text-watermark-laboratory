# Qwen 12×4 last-1 opening, token 0 skipped

`--fit-prefix 4 --context-len 1 --pos-bucket 1`. No `--include-first`.

| Method | wins | AUC |
|---|---|---|
| hits | 6/12 | 0.549 |
| poshits | 10/12 | 0.624 |

Last-1 of tokens 1–3 is not the Qwen 12/12. That ranking needs token 0.
