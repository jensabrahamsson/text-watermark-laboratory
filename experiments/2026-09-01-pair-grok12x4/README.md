# 2026-09-01 — 12 Grok-register prompts × 4 draws × 128 tokens

Register-matched train for
[../../research/PROTOCOL-isolated-register.md](../../research/PROTOCOL-isolated-register.md).
Seeds: `../2026-09-01-prompts-grok12/` (committed at SHA `07ce009` before
this `pair`). Generator: GPT-2 + public DeepMind 30 mixin.

Seed `20260904`. `n_samples=4`. `results.json` stores **first-draw**
official scores only; extras live on disk as `*-marked-2.txt` … `-4`
and matching `*-unmarked-gen-*.txt`.

## Official lamp (first draw)

**12/12** marked mean > unmarked mean. Min marked mean ≈ 0.613. Max
unmarked mean ≈ 0.513. Instance `public-deepmind-30`. This is the
key-based reference check, not the key-free indicator.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-grok12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 \
  --out-dir experiments/2026-09-01-pair-grok12x4
```

Frozen key-free analysis (do not change flags): see
[PROTOCOL-isolated-register.md](../../research/PROTOCOL-isolated-register.md).
Do not look at those LRs until those commands have been run once.
