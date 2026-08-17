# 2026-08-17 — Qwen-plus iterate (our key)

Marked GPT-2 twin `01-harbour-marked.txt` (mean 0.623) → one paraphrase with **qwen-plus** (DashScope) → mean **0.509**. Stop: `at_chance=True` after 1 of 3 passes.

Not a remover. Not Claude. Only whether *public-deepmind-30* went dark.

```bash
python -m text_watermark_tools iterate experiments/2026-08-17-pair/01-harbour-marked.txt \
  --backend qwen --out-dir experiments/2026-08-17-iterate-qwen
```
