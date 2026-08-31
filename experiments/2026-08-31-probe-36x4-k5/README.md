# Mixin `ngram_len=5` ablation on 36×4 GPT-2 twins

Public SynthID-Text uses `ngram_len=5` (four previous tokens plus the
candidate). The laboratory default `context_len=4` is the four-token
suffix of that window. This run uses `--context-len 5` on the same
36×4 GPT-2 pairs (`hits` and `hashpool` only).

## Last-5 vs last-4 (in-domain 36×4)

| Method | Context | Prompts marked > unmarked | Isolated marked `lr > 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|---|
| Hits | last-4 (published) | **36/36** | 134/144 | **0.934** | 119/144 vs 134/144 |
| Hits | last-5 | 35/36 | 130/144 | 0.912 | 124/144 vs 130/144 |
| Hashpool | last-4 (published) | 36/36 | 128/144 | 0.909 | 111/144 vs 128/144 |
| Hashpool | last-5 | 34/36 | 125/144 | 0.891 | 113/144 vs 126/144 |

Matching the mixin's `ngram_len=5` does **not** beat last-4. Keep the
default `context_len=4`.
