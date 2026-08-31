# Same-topic GPT-2 tables → Qwen2-1.5B twins

Train on `../2026-08-17-pair-12x4/` (GPT-2, four draws). Score
`../2026-08-17-pair-qwen/` (Qwen2-1.5B, one draw). Overlap **keep**: the
twelve stems match. Token methods retokenize Qwen text with GPT-2 BPE.
`surface` reads UTF-8 bytes. `used_keys=false`.

This is matched-prompt, different-generator transfer. It is not an
out-of-family test.

| Method | Prompt wins | File AUC | Marked `> 0` | perm p (mean) |
|---|---|---|---|---|
| **hits** | **11/12** | **0.740** | 1/12 | 0.39 |
| hitmass | **11/12** | 0.747 | 1/12 | 0.39 |
| hashpool | 7/12 | 0.521 | 4/12 | 0.34 |
| surface | 8/12 | 0.646 | 2/12 | 0.14 |
| logit | 9/12 | 0.708 | 0/12 | 0.38 |

Paired ranking of the same prompt can transfer through a *probe* tokenizer
(GPT-2 BPE of Qwen text): hits **11/12**. Isolated sign at 0 does not: the
LR scale shifts negative, so almost every Qwen file looks unmarked at
threshold 0. Token hashpool does not transfer (AUC 0.521). The mean-gap
permutation on n=12 files is noisy; quote **11/12 paired wins**, not a
single-file detector.

Different topics as well as a different generator is chance: see
`../2026-08-31-transfer-36-to-qwen/`.
