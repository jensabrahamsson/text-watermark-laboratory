# 2026-08-31 — key-free leave-one-out on 36×4 GPT-2 twins

Leave-one-prompt-out on `experiments/2026-08-31-pair-36x4` (36 stems × 4 draws
× 128 tokens). No keys, `hash_iv`, or g-values. `--max-draws 4`.

This is **in-domain**: the held-out prompt is a new topic, but the generator,
length, and the other 35 laboratory prompts are the same. Do not read 36/36
as a universal detector, and do not replace the published 12×4 hard last-4
**10/12** / **29/48** headlines with it.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| **hits** | **36/36** | **0.934** | **134/144** | 76/144 |
| freqhits | 35/36 | 0.916 | 131/144 | 81/144 |
| **hitmass** | **36/36** | **0.938** | 134/144 | 76/144 |
| **hashpool** | **36/36** | 0.909 | 128/144 | 96/144 |

Threshold 0 is still not a calibrated yes/no: hits sensitivity 134/144 with
unmarked specificity only 76/144.

Leave-one-stem Youden on the already-held-out LRs (threshold fitted on the
other 35 stems, then applied to this stem):

| Method | Nested-by-stem marked>t | Unmarked≤t | mean t | sens | spec |
|---|---|---|---|---|---|
| **hits** | **119/144** | **134/144** | 0.759 | 0.826 | 0.931 |
| freqhits | 122/144 | 130/144 | 0.722 | 0.847 | 0.903 |
| hitmass | 116/144 | 134/144 | 0.028 | 0.806 | 0.931 |
| hashpool | 111/144 | 128/144 | 0.027 | 0.771 | 0.889 |

That nested-by-stem hits gate is the honest in-domain isolated-file operating
point on this corpus. It is still the same generator and topic pool.

Draw-count ablation on the same files (`--max-draws`):

| Draws | hits wins | hits AUC | Nested-by-stem hits |
|---|---|---|---|
| 1 (128 tokens) | 30/36 | 0.845 | 29/36 vs 31/36 |
| 2 | 33/36 | 0.875 | 52/72 vs 64/72 |
| 4 | **36/36** | **0.934** | **119/144 vs 134/144** |

One 128-token draw matches the old 36-topic × 1 ranking (hits **30/36** on
the 256-token corpus too). Extra *draws*, not extra topics, are what lift
prompt-grain ranking to 36/36. Hashpool is weaker on the short 1-draw slice
(23/36) than on the historical 256-token 36×1 run (31/36).

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods hits,freqhits,hitmass,hashpool \
  --out-dir experiments/2026-08-31-probe-36x4
```
