# Grok-written seeds (17 Aug 2026)

Twelve short English texts, written here. Not GPT-2 mixin. Not Claude. They were not generated under DeepMind’s public mixin, so `score` on these files should sit around 0.50 against instance `public-deepmind-30`. That is a statement about *this* key set, not about how Grok is built.

They are **prompts**, not finished marked documents. SynthID-Text does not stamp an existing string. Run the same files through the mixin like this:

```bash
source .venv/bin/activate
python -m text_watermark_tools score experiments/2026-08-17-grok-prompts
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --out-dir experiments/2026-08-17-pair --max-new-tokens 128
```

`pair` writes `*-prompt.txt` (the same seed), `*-unmarked-gen.txt` (GPT-2 without mixin) and `*-marked.txt` (GPT-2 + mixin). Only the new tokens carry the mark.
