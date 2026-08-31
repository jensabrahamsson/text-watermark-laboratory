# 2026-08-31 — Qwen2-1.5B 12 prompts × 4 draws × 128 tokens

Same 12 Grok seeds as `experiments/2026-08-17-pair-qwen`. New sample
(`--seed 20260831`). Generator: Qwen2-1.5B-Instruct + public DeepMind 30.
This is **not** a replacement of the original 12×1 corpus.

## Official lamp (first draw)

**12/12** marked mean > unmarked mean. Min marked ≈ 0.557. Max unmarked ≈
0.523. Score with `--model Qwen/Qwen2-1.5B-Instruct`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260831 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --out-dir experiments/2026-08-31-pair-qwen-12x4
```

Key-free: [../2026-08-31-probe-qwen-12x4/](../2026-08-31-probe-qwen-12x4/).
GPT-2 tables on this sample:
[../2026-08-31-transfer-gpt2-to-qwen-12x4/](../2026-08-31-transfer-gpt2-to-qwen-12x4/).
