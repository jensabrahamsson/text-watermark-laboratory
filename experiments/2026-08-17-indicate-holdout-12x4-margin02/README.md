# Soft bar: indicate rotate, margin=0.02

Same LRs as [`../2026-08-17-indicate-holdout-12x4/`](../2026-08-17-indicate-holdout-12x4/).
Hit if `marked_lr + 0.02 >= unmarked_lr`. One-file sign if `lr > -0.02`.

`used_keys=false`. This is a lower bar, not a stronger model.

```bash
python -m text_watermark_tools indicate holdout experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4 --margin 0.02 \
  --out-dir experiments/2026-08-17-indicate-holdout-12x4-margin02
```

(The files here were retuned from the strict hold-out JSON. The LRs did not change.)

## Result

| Grain | Strict (0) | margin 0.015 | **margin 0.02** |
|---|---|---|---|
| Prompts (mean of 4) | 10/12 | 11/12 | **11/12** |
| Sample pairs | 30/48 | 31/48 | **31/48** |
| Marked file above the bar | 29/48 (`lr>0`) | 37/48 | **39/48** (`lr>−0.02`) |
| Unmarked file at or below the bar | 23/48 | 25/48 | **26/48** (`lr≤0.02`) |

Station flips (gap 0.010). Office still misses (gap **0.066**).

0.02 vs 0.015: two more marked files clear the sign bar. No new prompt, no new pair.
**12/12** would need margin ≈ 0.066 and would count office — that miss is not close.
The same office gap already blocked `blind --margin 0.015`.
