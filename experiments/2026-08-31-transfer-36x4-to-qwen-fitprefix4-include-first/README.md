# GPT-2 36×4 → Qwen, 4-token include-first (chance)

Train 24 new GPT-2 stems, score the new Qwen 12×4 sample through the
GPT-2 tokenizer. `--fit-prefix 4 --include-first`. Overlapping stems
dropped. `used_keys=false`.

| Method | Prompt wins | File AUC | t=0 |
|---|---|---|---|
| poshits | 8/12 | 0.584 | 0/48 vs 48/48 |
| first | 7/12 | 0.561 | 0/48 vs 48/48 |

Qwen has an in-domain first-token indicator. GPT-2 tables do not
read it. Same conclusion as the 16-token bucket-1 transfer.
