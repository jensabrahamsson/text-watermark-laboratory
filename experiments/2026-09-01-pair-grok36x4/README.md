# 2026-09-01 — 36 Grok-register prompts × 4 draws × 128 tokens

Scale train for
[../../research/PROTOCOL-isolated-scale.md](../../research/PROTOCOL-isolated-scale.md).
Seeds: `../2026-09-01-prompts-grok36/` (committed at SHA `e537d71` before
this `pair`). Generator: GPT-2 + public DeepMind 30 mixin.

Seed `20260905`. `n_samples=4`. `results.json` stores **first-draw**
official scores only; extras live on disk as `*-marked-2.txt` … `-4`
and matching `*-unmarked-gen-*.txt`.

## Official lamp (first draw)

**36/36** marked mean > unmarked mean. Min marked mean ≈ 0.608. Max
unmarked mean ≈ 0.516. Instance `public-deepmind-30`. This is the
key-based reference check, not the key-free indicator.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-grok36 \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --out-dir experiments/2026-09-01-pair-grok36x4
```

Frozen key-free analysis (do not change flags): see
[PROTOCOL-isolated-scale.md](../../research/PROTOCOL-isolated-scale.md).
Do not look at those LRs until the frozen commands have been run once.
Does not replace **25/48**.
