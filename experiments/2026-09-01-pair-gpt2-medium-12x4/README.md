# 2026-09-01 — gpt2-medium original-12 prompts × 4 draws × 128 tokens

In-generator occupancy-free analog of
[../../research/PROTOCOL-isolated-m12.md](../../research/PROTOCOL-isolated-m12.md)
(protocol SHA `5be70f3`, named `3610cef`). Same seeds as
`../2026-08-17-grok-prompts/` (disjoint from the 100 confirmatory
prompts). Native `gpt2-medium` + public DeepMind 30. Same BPE as GPT-2
(`is_gpt2_name` is true). Not leftover-15. Not leftover targeting.

Seed `20260901`. `n_samples=4`. `results.json` stores **first-draw** official
scores only; extras live on disk as `*-marked-2.txt` … `-4`.

## Official lamp (first draw)

**12/12** marked mean > unmarked mean. Instance `public-deepmind-30`.
The mixin is on. This is a keyed positive control, not a key-free
endpoint. Do not sell **12/12** as replacing **25/48**.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model gpt2-medium --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-gpt2-medium-12x4
```

Do not mix these twins into the 100×4 train. Do not apply leftover-15
GPT-2 keys here. Opened occupancy-free transfer:
[../2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/](../2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits/),
[../2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/](../2026-09-01-openings-gpt2-medium-100x4-to-medium12x4/).
Occupancy-free t=0 **10/48**. Coverage **13/48**. Do not sell those
counts as replacing **25/48**.
