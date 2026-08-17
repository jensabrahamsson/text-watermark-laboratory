# 2026-08-15 — known-mark mixin experiment

GPT-2 + SynthID mixin (temp 1.0). Surrogate fitted only from `generate()` queries (no keys, no `hash_iv`, no g-values). Rewrite uses the surrogate plus an unmarked GPT-2 decoder. Official scores via DeepMind `detector_mean`.

| Run | Source mean | Source wmean | Rewrite mean | Rewrite wmean | Tokens | Unmasked n-grams | Queries | Replacements |
|---|---|---|---|---|---|---|---|---|
| 1 (seed 0) | 0.6109 | 0.6286 | 0.5498 | 0.5556 | 320 | 315 | 120 | 35 |
| 2 (seed 1) | 0.6226 | 0.6408 | 0.5535 | 0.5607 | 320 | 316 | 120 | 34 |

Both runs: source mean > 0.53; rewrite mean and weighted mean closer to 0.50 than source; fit flags keys/hash_iv/g-values = false.

Per-run files: `run1/`, `run2/` (`source.txt`, `rewrite.txt`, `results.json`, `results.md`).
