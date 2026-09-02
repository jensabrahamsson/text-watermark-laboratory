# UTF-8 surface hashpool on Qwen2-1.5B leave-one-out

Same twins as `../2026-08-31-probe-qwen/`. Byte hashpool only; no Qwen
tokenizer in the scorer. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | perm p |
|---|---|---|---|---|---|
| surface | **9/12** | **0.674** | 9/12 | 3/12 | 0.046 |
| Qwen-tokenizer hashpool (prior) | **10/12** | **0.750** | 11/12 | 6/12 | 0.017 |

Surface works on this generator without its tokenizer. Token hashpool on
the Qwen vocabulary is still stronger. Isolated sign at 0 is sensitive
(unmarked ≤0 only 3/12).
