# Qwen2-1.5B native opening rankpath (12×4 LOO)

`--fit-prefix 4 --pos-bucket 1`, Qwen unmarked LM, Qwen tokenizer.
Official lamp on this pile is **12/12**. Rankpath scores generated
tokens 1…, not token 0. `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| rankpath | **8/12** | **0.590** | 24/48 | 32/48 | 0.029 |
| rankuni | 8/12 | 0.597 | 26/48 | 33/48 | 0.246 |

Qwen’s in-domain opening **is token 0 identity** (`first` **12/12**,
AUC **0.901**). Rank-path on later opening ranks does not recover that.
Do not score Qwen ids with GPT-2 tables.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
