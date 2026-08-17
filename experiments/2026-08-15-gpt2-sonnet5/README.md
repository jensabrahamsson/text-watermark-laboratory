# 2026-08-15 — GPT-2 mark vs Sonnet 5

Tokenizer and keys: GPT-2 + `DEFAULT_WATERMARKING_CONFIG`. Temp 1.0 (mixin max), top-k 40, ~420 new tokens.

The prompt was a travel essay. GPT-2 wrote a half-mad hotel/job listicle. Irrelevant to the mark.

## Files

| File | What |
|---|---|
| `t_high_temp.txt` | T, watermarked GPT-2 |
| `t_high_temp_errors.txt` | same T + deliberate grammar errors |
| `t_prime_sonnet5.txt` | Sonnet 5, **full rewrite** |
| `t_prime_sonnet5_proofread.txt` | Sonnet 5, **proofread only** |

`*.meta.json` is raw scores from the run (mean computed in numpy, same formula as `detector_mean`).

## Results

| Text | Tokens | Unmasked n-grams | Mean | Weighted mean |
|---|---|---|---|---|
| T | 418 | 411 | 0.617 | 0.638 |
| T + errors | 410 | 405 | 0.577 | 0.593 |
| Sonnet 5 proofread | 416 | 409 | **0.605** | **0.625** |
| Sonnet 5 rewrite | 391 | 385 | **0.502** | **0.502** |
| Rewrite + wrong key | 391 | 385 | 0.504 | 0.503 |

Proofread vs T+errors: ~56 word changes, 5-gram overlap ~0.60. The score **rose** because Claude put back ordinary English ≈ the original marked tokens.

## Interpretation

- We measured **our** mark, not “is this AI”.
- Both T′ are Claude. Only the proofread lights up.
- A human who only fixed the same errors could also have gotten ~0.60.
- Sonnet 5’s own mark is not visible here (wrong key, and the model is before the 2 Aug cutoff).
