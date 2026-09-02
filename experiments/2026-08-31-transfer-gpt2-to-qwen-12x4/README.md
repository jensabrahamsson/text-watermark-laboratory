# Transfer: GPT-2 12×4 tables → new Qwen 12×4 sample

Train on `experiments/2026-08-17-pair-12x4`. Score
`experiments/2026-08-31-pair-qwen-12x4` with overlap **keep** (same 12
prompt stems). Qwen text is read with the **GPT-2 tokenizer** (probe BPE),
as in `../2026-08-31-transfer-gpt2-to-qwen/`. `used_keys=false`.

The published same-topic transfer on the *original* Qwen 12×1 corpus was
hits **11/12** (AUC **0.740**, isolated `lr>0` **1/12**). This new Qwen
sample of the same prompts does **not** reproduce that ranking.

| Method | Prompt wins | File AUC | Marked `> 0` |
|---|---|---|---|
| hits | 5/12 | 0.355 | 5/48 |
| hashpool | 8/12 | 0.568 | 17/48 |
| logit | 5/12 | 0.451 | 4/48 |

First-draw only (`--max-draws 1`): hits **6/12** AUC 0.455; isolated 1/12.
That matches the old isolated-sign failure and does **not** match the old
paired 11/12.

Same-topic GPT-2 hits through a probe tokenizer was sample-specific. Do
not sell 11/12 as a cross-generator detector. Nested gates on this split
collapse to ~4/48 recall.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --test-dir experiments/2026-08-31-pair-qwen-12x4 \
  --overlap keep --methods hits,hashpool,hitmass,logit \
  --out-dir experiments/2026-08-31-transfer-gpt2-to-qwen-12x4
```
