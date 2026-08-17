# Frozen key-free indicator (GPT-2, last-4)

Tables fit on `../2026-08-17-pair-12x4/` (12 prompts × 4 samples). Token counts only.

```bash
python -m text_watermark_tools indicate score path/to/T.txt \
  --tables experiments/indicator-gpt2
```

Prints `lr=` on one file. Positive ⇒ more like this marked pile. Not `detector_mean`. Not Claude. Not Anthropic. ≈0 is not “human”.

These tables are fit on **all** 12 prompts. Honest single-text numbers are the rotate hold-out: [`../2026-08-17-indicate-holdout-12x4/`](../2026-08-17-indicate-holdout-12x4/) (10/12 at prompt grain; 29/48 marked files have `lr>0`).
