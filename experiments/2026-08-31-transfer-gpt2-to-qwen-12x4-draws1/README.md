# GPT-2 tables on the first draw of the new Qwen 12×4 sample

`--max-draws 1 --overlap keep --skip-nested`. Probe-BPE (GPT-2 tokenizer).

hits **6/12** AUC **0.455**, isolated **1/12**. hashpool **7/12** AUC 0.507.

The original same-topic transfer (11/12) does not hold on a new Qwen draw
of the same prompts. See
[../2026-08-31-transfer-gpt2-to-qwen-12x4/](../2026-08-31-transfer-gpt2-to-qwen-12x4/).
