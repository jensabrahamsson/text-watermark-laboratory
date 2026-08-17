# 2026-08-15 — known-mark v2 (close the residual)

Key-free surrogate: every source token from mixin `generate()` is an observation. Rewrite uses one unmarked-GPT-2 forward pass and the top alternative at each preferred position. Official scores via DeepMind `detector_mean`. No keys / `hash_iv` / g-values in the fit.

| Run | Source mean | Source wmean | Rewrite mean | Rewrite wmean | Unmasked n-grams | Replacements |
|---|---|---|---|---|---|---|
| v1 residual seed 0 | 0.6109 | 0.6286 | 0.5498 | 0.5556 | 315 | 35 |
| v1 residual seed 1 | 0.6226 | 0.6408 | 0.5535 | 0.5607 | 316 | 34 |
| **v2 seed 0** | 0.6116 | 0.6292 | **0.5012** | **0.5028** | 252 | 252 |
| **v2 seed 1** | 0.6226 | 0.6393 | **0.4983** | **0.4981** | 252 | 252 |

Cap was rewrite Mean **and** Weighted Mean ≤ 0.53 with source Mean > 0.53 and n-grams ≥ 200. Both v2 launches meet it. Fit flags keys/hash_iv/g-values = false.

v1 left ~0.05 residual because only ~35 tokens flipped (40 queried positions, rewritten contexts hid later matches, marked-sample alternatives stayed biased).
