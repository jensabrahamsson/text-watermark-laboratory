# 2026-08-17 — key-free blind on 12 × 700-token twins

Same protocol as [../2026-08-17-blind/](../2026-08-17-blind/). Twins: [../2026-08-17-pair-limit/](../2026-08-17-pair-limit/).

## Baseline vs this run

| Corpus | New tokens | Marked higher | Accuracy | context_len |
|---|---|---|---|---|
| `2026-08-17-blind` (dress rehearsal) | 128 | **8/12** | 0.67 | 1 |
| **this run** | **700** | **6/12** | 0.50 | 1 |

`used_keys=false` `hash_iv=false` `g_values=false`.

Longer twins did **not** raise last-1 accuracy. Six of twelve held-out prompts lean the right way — chance on this n. The official lamp on the same files is still 12/12 (marked 0.61–0.63). Indication from 8/12 @ 128 did not grow with length on this blunt counter.

```bash
python -m text_watermark_tools blind experiments/2026-08-17-pair-limit \
  --out-dir experiments/2026-08-17-blind-limit
```
