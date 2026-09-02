# 2026-08-31 — key-free probe on Qwen2-1.5B twins (12×1)

Leave-one-prompt-out on `experiments/2026-08-17-pair-qwen` with the Qwen tokenizer. `context_len=4`. No keys.

Published key-free last-2 on this corpus was **10/12**. Hard last-4 here is only **6/12**.

| Method | Prompt wins | File AUC | Marked `> 0` | perm p |
|---|---|---|---|---|
| unigram | 7/12 | 0.590 | 4/12 | 0.12 |
| hard last-4 | 6/12 | 0.625 | 4/12 | 0.11 |
| **hits / gated / shrinkage** | 8/12 | **0.417** | 1/12 | 0.89 |
| **hashpool** | **10/12** | **0.750** | **11/12** | 0.017 |

Exact shared 4-grams are too sparse on 12 prompts × 1 draw with a 151k-piece tokenizer: `hits` prompt-wins can still look decent while file AUC goes **below** 0.5. Hash pooling is what transfers. Isolated hashpool sign 11/12 has binomial p ≈ 0.003; unmarked specificity is only 6/12.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-qwen \
  --model Qwen/Qwen2-1.5B-Instruct \
  --out-dir experiments/2026-08-31-probe-qwen
```
