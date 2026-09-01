# 2026-09-01 — DistilGPT2 100 prompts × 4 draws × 128 tokens

Phase B of [../../research/PROTOCOL-next.md](../../research/PROTOCOL-next.md).
Same seeds as `../2026-09-01-prompts-100/` (committed before GPT-2 `pair`).
Native DistilGPT2 + public DeepMind 30. Shared GPT-2 tokenizer.

Seed `20260901`. `n_samples=4`. `results.json` stores **first-draw** official
scores only; extras live on disk as `*-marked-2.txt` … `-4`.

## Official lamp (first draw)

**70/100** marked mean > unmarked mean. Min marked mean ≈ 0.433. Max unmarked
mean ≈ 0.560. Mean marked ≈ 0.559, mean unmarked ≈ 0.496. Instance
`public-deepmind-30`. The mixin is weaker here than GPT-2 Phase A (**100/100**).
Ground truth for key-free probes remains mixin on/off, not this lamp.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-distil-100x4
```

Opening probes (locks B and C only):
[../2026-09-01-probe-distil-100x4-opening-poshits/](../2026-09-01-probe-distil-100x4-opening-poshits/),
[../2026-09-01-probe-distil-100x4-opening-rankpath/](../2026-09-01-probe-distil-100x4-opening-rankpath/).
