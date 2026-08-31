# New GPT-2 topics → Qwen 12×1 (negative)

Train 24 stems `13`–`36` from `../2026-08-17-pair-36/`. Score Qwen
`01`–`12`. Drop overlapping stems from train. GPT-2 probe tokenizer plus
UTF-8 surface. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | perm p |
|---|---|---|---|---|
| hits | 6/12 | 0.524 | 4/12 | 0.29 |
| hashpool | 8/12 | 0.500 | 7/12 | 0.38 |
| surface | 8/12 | 0.514 | 9/12 | 0.55 |
| logit | 8/12 | 0.542 | 0/12 | 0.30 |

Different prompt families **and** a different generator leave no usable
key-free signal in these tables. Compare with same-topic GPT-2→Qwen
(`../2026-08-31-transfer-gpt2-to-qwen/`, hits **11/12** paired) and with
in-domain Qwen hashpool (`../2026-08-31-probe-qwen/`, **10/12**).
