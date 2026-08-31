# 2026-08-31 — 36 GPT-2 prompts × 4 draws × 128 tokens

Same 36 seeds as `experiments/2026-08-17-prompts-36`. Generator: GPT-2 + public
DeepMind 30 mixin. Length-matched to the original 12×4 corpus (128 tokens),
unlike the historical `experiments/2026-08-17-pair-36` (one draw × 256 tokens).

Seed `20260831`. `n_samples=4`. `results.json` stores **first-draw** official
scores only; extras live on disk as `*-marked-2.txt` … `-4` and matching
`*-unmarked-gen-*.txt`.

## Official lamp (first draw)

**36/36** marked mean > unmarked mean. Min marked mean ≈ 0.590. Max unmarked
mean ≈ 0.521. Instance `public-deepmind-30`. This is the key-based reference
check, not the key-free indicator.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-prompts-36 \
  --n-samples 4 --max-new-tokens 128 --seed 20260831 \
  --out-dir experiments/2026-08-31-pair-36x4
```

Key-free leave-one-out: [../2026-08-31-probe-36x4/](../2026-08-31-probe-36x4/).
Draw-count ablation: [../2026-08-31-probe-36x4-draws1/](../2026-08-31-probe-36x4-draws1/),
[../2026-08-31-probe-36x4-draws2/](../2026-08-31-probe-36x4-draws2/).
