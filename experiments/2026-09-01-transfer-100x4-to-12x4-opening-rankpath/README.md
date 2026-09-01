# Isolated transfer: 100 families → original 12×4 lock C

GPT-2 100×4 rankpath tables, `--methods rankpath --fit-prefix 4 --pos-bucket 1`,
scored on `experiments/2026-08-17-pair-12x4`. Not `--rankpath` (no extra
count methods). `used_keys=false`. Overlap dropped 0.

Prompt ranking **10/12**. Nested Youden (primary) **24/48 vs 41/48**.
File AUC **0.770**. Isolated t=0 **24/48 vs 40/48**. Does not beat
recounted hard **25/48**. Lock B on this split was **11/12** / nested
**36/48**; rankpath is more domain-specific (H-iso-C).

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-12x4-opening-rankpath
```
