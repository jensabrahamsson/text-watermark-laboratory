# Isolated transfer: 100 families → 36×4 lock C

Same frozen rankpath tables/flags as the original-12 transfer, test
directory `experiments/2026-08-31-pair-36x4`. `used_keys=false`.

Prompt ranking **35/36**. Nested Youden **109/144 vs 117/144**. File AUC
**0.838**. Isolated t=0 **115/144 vs 112/144**. Same-register overlap, not
a universal detector. Does not replace **25/48**.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --methods rankpath --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-09-01-transfer-100x4-to-36x4-opening-rankpath
```
