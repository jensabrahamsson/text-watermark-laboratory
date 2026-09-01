# 2026-09-01 — 100 GPT-2 prompts × 4 draws × 128 tokens

Confirmatory corpus for [../../research/PROTOCOL-next.md](../../research/PROTOCOL-next.md).
Seeds: `../2026-09-01-prompts-100/` (committed before this `pair`).
Generator: GPT-2 + public DeepMind 30 mixin. Length-matched to the original
12×4 corpus (128 tokens).

Seed `20260901`. `n_samples=4`. `results.json` stores **first-draw** official
scores only; extras live on disk as `*-marked-2.txt` … `-4` and matching
`*-unmarked-gen-*.txt`.

## Official lamp (first draw)

**100/100** marked mean > unmarked mean. Min marked mean ≈ 0.576. Max unmarked
mean ≈ 0.519. Instance `public-deepmind-30`. This is the key-based reference
check, not the key-free indicator.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-100x4
```

Frozen key-free analysis (do not change flags):

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods interpolate --context-len 4 \
  --out-dir experiments/2026-09-01-probe-100x4-hard-last4
```
