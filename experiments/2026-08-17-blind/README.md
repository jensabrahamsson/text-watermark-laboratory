# 2026-08-17 — key-free blind on 12 pairs

The same 12 prompts → GPT-2 with mixin and GPT-2 without. Ground truth is how the file was **created**. The blind detector sees only token counts (last-1), never keys / `hash_iv` / g-values.

This is the measurement that does **not** know the key. Protocol and both lamps: [research/key-free-twins.md](../../research/key-free-twins.md). Twins: [../2026-08-17-blind-pairs/](../2026-08-17-blind-pairs/).

## Oracle (keys, `score`)

All 12 marked twins: mean **0.61–0.65**. All 12 unmarked: **≈ 0.50**. The lamp with the key sees everything.

## Blind (no keys, leave-one-prompt-out)

| context_len | Marked higher | Accuracy |
|---|---|---|
| 1 | 8/12 | 0.67 |
| 2 | 4/12 | 0.33 |
| 3 | 4/12 | 0.33 |

8/12 is an indication the idea is promising: eight held-out prompts lean the right way, four do not. Last-2/3 go the other way — too sparse. The key is what makes the clean 12/12.

```bash
python -m text_watermark_tools blind experiments/2026-08-17-blind-pairs \
  --out-dir experiments/2026-08-17-blind
```
