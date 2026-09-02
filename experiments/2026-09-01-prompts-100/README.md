# 100 confirmatory one-line prompts

New English scene lines, disjoint as strings from
`../2026-08-17-prompts-36/`. Same register as seeds 13–36. Input to
`pair` only. Committed **before** generation, as required by
[../../research/PROTOCOL-next.md](../../research/PROTOCOL-next.md).

Do not run `pair` until this directory is on the remote SHA named in
the logbook. Generator, draws, and analysis flags are frozen there.

```bash
python -m text_watermark_tools pair experiments/2026-09-01-prompts-100 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-09-01-pair-100x4
```
