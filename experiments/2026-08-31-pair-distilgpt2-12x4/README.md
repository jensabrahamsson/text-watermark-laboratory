# 2026-08-31 — DistilGPT2 12 prompts × 4 draws × 128 tokens

Same 12 Grok seeds. `--model distilgpt2 --n-samples 4 --max-new-tokens 128
--seed 20260831`. GPT-2 tokenizer (shared with `gpt2`). Public DeepMind 30.

## Official lamp (first draw)

**12/12** marked mean > unmarked mean. Marked means ≈ 0.62. Unmarked ≈ 0.50.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260831 \
  --out-dir experiments/2026-08-31-pair-distilgpt2-12x4
```

This is a tokenizer-matched third generator, not a replacement of GPT-2
12×4. Key-free: [../2026-08-31-probe-distilgpt2-12x4/](../2026-08-31-probe-distilgpt2-12x4/).
GPT-2 36×4 → this sample:
[../2026-08-31-transfer-36x4-to-distilgpt2-12x4/](../2026-08-31-transfer-36x4-to-distilgpt2-12x4/).
