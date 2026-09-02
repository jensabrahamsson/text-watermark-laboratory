# 2026-08-31 — key-free leave-one-out on Qwen 12×4

Leave-one-prompt-out on `experiments/2026-08-31-pair-qwen-12x4` with the
**Qwen tokenizer**. `used_keys=false`. New sample; do not overwrite the
published original 12×1 hashpool **10/12** (AUC **0.750**).

Four draws do **not** close the Qwen gap the way they close the GPT-2 gap.

| Draws | hits wins | hits AUC | hashpool wins | hashpool AUC |
|---|---|---|---|---|
| 1 (this sample) | 7/12 | 0.500 | 8/12 | 0.674 |
| 4 | 8/12 | 0.602 | 7/12 | 0.638 |

4-draw isolated sign at 0: hits 24/48 (unmarked ≤0 19/48); hashpool 36/48
(unmarked ≤0 20/48). Nested-by-stem hits Youden is 14/48 vs 46/48
(specificity knob, not a detector).

Hits still lacks shared 4-grams on a large tokenizer. Extra draws raise
hits AUC from chance to 0.60 and the mean gap’s permutation p, but prompt
grain stays 8/12. Hashpool on this seed is weaker than the original 12×1
run (10/12). Treat that 10/12 as the published corpus, this as a
replication check that did not match.

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-qwen-12x4 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --methods hits,freqhits,hitmass,hashpool \
  --out-dir experiments/2026-08-31-probe-qwen-12x4
```
