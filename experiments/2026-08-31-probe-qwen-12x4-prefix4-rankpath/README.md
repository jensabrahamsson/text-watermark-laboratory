# Qwen2-1.5B native prefix-4 rankpath (12×4 LOO)

`--fit-prefix 5 --pos-bucket 0`, Qwen unmarked LM. Four isolated
choice-matrix rows (generated tokens 1–4). `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| rankpath | **9/12** | **0.662** | 25/48 | 33/48 | 0.0035 |
| rankuni | 8/12 | 0.561 | 25/48 | 24/48 | 0.331 |

File AUC is weakly above chance. Ranking 9/12 and isolated 25/48 is
**not** Qwen first-token **12/12**, AUC **0.901**. Do not score Qwen ids
with GPT-2 tables.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
