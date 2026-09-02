# 2026-08-31 — 12 medium-length GPT-2 prompts × 4 draws × 128 tokens

Seeds: [`../2026-08-31-prompts-long12/`](../2026-08-31-prompts-long12/).
~41–51 words, matching `04-market` … `12-ferry-queue`, not the 10–12 word
one-liners. New topics. Not copies of the original twelve stems. Not Claude.

Seed `20260901`. `n_samples=4`. Official first-draw lamp **12/12**.
Min marked mean ≈ 0.576. Max unmarked mean ≈ 0.512.

```bash
python -m text_watermark_tools pair experiments/2026-08-31-prompts-long12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-08-31-pair-long12x4
```

Generated token 0 on the 48 marked files is only `"` (26) and `The` (22).
No `After` / `Closing` / `Now` / `While`. Medium seed length alone does
not copy those 12×4 zeros.
