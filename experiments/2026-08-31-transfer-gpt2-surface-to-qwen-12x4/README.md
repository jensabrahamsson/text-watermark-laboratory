# GPT-2 12×4 surface → new Qwen 12×4 (keep overlapping stems)

Same-topic tokenizer-free transfer: train a byte-4gram surface table on
the original GPT-2 12×4 pairs and score the new Qwen 12×4 sample.
`--overlap keep`.

## Result

Surface **7/12** prompts (AUC **0.525**), isolated marked `lr > 0` only
**5/48**, unmarked `lr ≤ 0` **48/48**. Chance ranking with a conservative
sign. A character table does not rescue GPT-2→Qwen on this new sample.

The earlier same-topic GPT-2 hits → original Qwen 12×1 ranking (11/12,
AUC 0.740, isolated 1/12) did **not** replicate here and was
sample-specific. See
[`../2026-08-31-transfer-gpt2-to-qwen/`](../2026-08-31-transfer-gpt2-to-qwen/).
