# Original-12 Kirchenbauer twins

Frozen in [PROTOCOL-next-kgw.md](../../research/PROTOCOL-next-kgw.md)
(SHA `8371406`), named `09e40d4` before generation.

```bash
python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --n-samples 4 --max-new-tokens 128 --seed 20260904 --mixin kgw \
  --hub-revision 607a30d783dfa663caf39e06633721c8d4cfcd7e \
  --out-dir experiments/2026-09-03-pair-12x4-kgw
```

Official scores are Hugging Face `WatermarkDetector` z-scores, not
SynthID `detector_mean`. Hub revision was pinned. Do not sell a
Kirchenbauer count as replacing **25/48**.
