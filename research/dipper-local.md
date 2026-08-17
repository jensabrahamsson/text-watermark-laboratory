# DIPPER locally

**Decision 2026-08-15:** do not download. No official 7B exists. The 11B checkpoint is out of scope for Phase 0.

## What DIPPER is

[DIPPER](https://arxiv.org/abs/2303.13408) (Krishna et al., NeurIPS 2023) is an **11B** T5-XXL, fine-tuned for paragraph paraphrase with knobs `lex_diversity` / `order_diversity`. That is the paraphraser ETH and Nature follow-ups use against SynthID.

Official weights: [`kalpeshk2011/dipper-paraphraser-xxl`](https://huggingface.co/kalpeshk2011/dipper-paraphraser-xxl)

- 11 266 928 640 parameters, **F32**
- Weight files ≈ **45 GB** on disk
- Authors: *GPU with at least 40 GB* to reproduce paper runs
- Reference code does `.cuda()`. No MPS support
- Ablation without context: the same 11B (`…-xxl-no-context`)

There is **no** official 7B, 3B, or 770M DIPPER. A random 7B paraphraser is not DIPPER and does not give comparable numbers.

## Why not here

F32 load ≈ 45 GB weights. Authors ask for a GPU with at least 40 GB. Reference code does `.cuda()`. bitsandbytes-8bit is CUDA in practice. This lab does not download that checkpoint.

## Is it needed?

| Step | Need DIPPER? |
|---|---|
| Detector Phase 0 (score) | No |
| Measure *our* mark before/after rewrite | No — Sonnet 5 / Grok is enough. We already have 0.617 → 0.502 |
| A number comparable to ETH/Nature (DIPPER lex=60, ~1000 tokens) | Yes, then you need exactly that 11B model |

The next implementation is Phase 0. Therefore: no download.

## If a 40 GB+ CUDA GPU is available later

```text
huggingface-cli download kalpeshk2011/dipper-paraphraser-xxl \
  --local-dir models/dipper-paraphraser-xxl
# + google/t5-v1_1-xxl tokenizer
# inference: official DipperParaphraser, lex=60, order=0 or 20
```

Weights belong in `models/` (gitignored). Not in the `synthid-text` checkout.
