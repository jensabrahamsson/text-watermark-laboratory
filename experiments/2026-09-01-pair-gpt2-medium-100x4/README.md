# 2026-09-01 — gpt2-medium 100 prompts × 4 draws × 128 tokens

Occupancy-free leftover-15 analog of
[../../research/PROTOCOL-isolated-mgen.md](../../research/PROTOCOL-isolated-mgen.md)
(protocol SHA `cc9c4ca`, named `883532b`). Same seeds as
`../2026-09-01-prompts-100/` (committed before leftover membership).
Native `gpt2-medium` + public DeepMind 30. Same BPE as GPT-2
(`is_gpt2_name` is true). Not more GPT-2 scenes. Not leftover targeting.

Seed `20260901`. `n_samples=4`. `results.json` stores **first-draw** official
scores only; extras live on disk as `*-marked-2.txt` … `-4`.

## Official lamp (first draw)

**100/100** marked mean > unmarked mean. Instance `public-deepmind-30`.
The mixin is on. This is a keyed positive control, not a key-free
endpoint. Do not sell **100/100** as replacing **25/48**.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --model gpt2-medium --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-gpt2-medium-100x4
```

Opened occupancy-free transfer:
[../2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/](../2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits/),
[../2026-09-01-openings-gpt2-medium-100x4-to-12x4/](../2026-09-01-openings-gpt2-medium-100x4-to-12x4/),
[../2026-09-01-isolated-mgen-leftover-15/](../2026-09-01-isolated-mgen-leftover-15/).
Occupancy-free t=0 **16/48**. Leftover-15 coverage **0/15**. Do not sell
those counts as replacing **25/48**.
