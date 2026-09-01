# 36 Grok-register scene prompts

New English multi-paragraph scene seeds, first person, everyday
settings, ~220–330 words. Input to `pair` only. Committed **before**
generation, as required by
[../../research/PROTOCOL-isolated-scale.md](../../research/PROTOCOL-isolated-scale.md).

Not copies of `../2026-09-01-prompts-grok12/` or the original 12. Not
one-liners. Not the medium `../2026-08-31-prompts-long12/` discovery
set. Not Claude. Do not mix grok12 into this train after seeing LRs.

Do not run `pair` until this directory is on the remote SHA named in
the logbook. Generator, draws, and analysis flags are frozen in that
protocol.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-grok36 \
  --n-samples 4 --max-new-tokens 128 --seed 20260905 \
  --out-dir experiments/2026-09-01-pair-grok36x4
```
