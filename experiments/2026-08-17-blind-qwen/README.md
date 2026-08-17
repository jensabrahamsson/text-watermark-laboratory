# 2026-08-17 — key-free blind on Qwen2 twins

Twins: [../2026-08-17-pair-qwen/](../2026-08-17-pair-qwen/). Token counts from the Qwen tokenizer.

| Corpus | Generator | New tokens | Marked higher |
|---|---|---|---|
| `2026-08-17-blind` | GPT-2 | 128 | **8/12** |
| `2026-08-17-blind-limit` | GPT-2 | 700 | **6/12** |
| **this run** | Qwen2-1.5B-Instruct | 128 | **4/12** |

Official lamp on these twins is still 12/12. Last-1 counts did not travel. `used_keys=false`.

```bash
python -m text_watermark_tools blind experiments/2026-08-17-pair-qwen \
  --model Qwen/Qwen2-1.5B-Instruct --out-dir experiments/2026-08-17-blind-qwen
```
