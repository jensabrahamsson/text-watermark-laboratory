# 2026-09-01 — Qwen2-1.5B-Instruct 100 prompts × 4 draws × 128 tokens

Phase B of [../../research/PROTOCOL-next.md](../../research/PROTOCOL-next.md).
Same seeds as `../2026-09-01-prompts-100/` (committed before GPT-2 `pair`).
Native `Qwen/Qwen2-1.5B-Instruct` + public DeepMind 30. Local Hugging Face,
not Dashscope `qwen-plus`.

Seed `20260901`. `n_samples=4`. `results.json` stores **first-draw** official
scores only; extras live on disk as `*-marked-2.txt` … `-4`.

## Official lamp (first draw)

**100/100** marked mean > unmarked mean. Min marked mean ≈ 0.518. Max unmarked
mean ≈ 0.520. Mean marked ≈ 0.580, mean unmarked ≈ 0.500. Instance
`public-deepmind-30`. The mixin is on here, unlike Distil Phase B (**70/100**).
Ground truth for key-free probes remains mixin on/off, not this lamp.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model Qwen/Qwen2-1.5B-Instruct --n-samples 4 --max-new-tokens 128 \
  --seed 20260901 --out-dir experiments/2026-09-01-pair-qwen-100x4
```

Opening probes (locks B and C only):
[../2026-09-01-probe-qwen-100x4-opening-poshits/](../2026-09-01-probe-qwen-100x4-opening-poshits/),
[../2026-09-01-probe-qwen-100x4-opening-rankpath/](../2026-09-01-probe-qwen-100x4-opening-rankpath/).
