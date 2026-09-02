# 2026-08-31 — GPT-2 12×4 control-shuffled-30 twins

Same 12 Grok seeds as `experiments/2026-08-17-pair-12x4`. Mixin on with
`control_keys()` (`control-shuffled-30`), **not** the public DeepMind 30.
Four independent draws × 128 new tokens. Seed **20260931**.

There is no `*-marked.txt`. `blind` / `indicate fit` ignore these files.

| File | Sampler |
|---|---|
| `*-prompt.txt` | Seed (not stamped) |
| `*-control-gen.txt` plus `-2`/`-3`/`-4` | GPT-2 + `control_keys()` |

## Official lamp

48 files, `n_tokens=128`.

| Keys | Mean range | Mean of means |
|---|---|---|
| `public-deepmind-30` | **0.483–0.526** | **0.501** |
| matching `control-shuffled-30` | **0.604–0.641** | **0.624** |

Every file scores higher on the matching control keys than on the public
keys. Different instance, not “GPT-2 style”. Same pattern as the 12×1×700
pile in `experiments/2026-08-17-pair-limit/`.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --control-only --n-samples 4 --max-new-tokens 128 --seed 20260931 \
  --out-dir experiments/2026-08-31-pair-12x4-controlkeys
```

Key-free instance contrast: [../2026-08-31-contrast-36x4-to-12x4-fitprefix4/](../2026-08-31-contrast-36x4-to-12x4-fitprefix4/).
