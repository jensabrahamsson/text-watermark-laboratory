# Transfer: original 12×4 → 24 new 36×4 stems

Train on `experiments/2026-08-17-pair-12x4`. Score stems 13–36 in
`experiments/2026-08-31-pair-36x4` (`--overlap drop-from-test`). Each test
stem has four 128-token draws (96 marked files, 96 unmarked). `used_keys=false`.

Compare with the 1-draw 256-token reverse split
[../2026-08-31-transfer-12x4-to-36/](../2026-08-31-transfer-12x4-to-36/)
(hits **24/24**, AUC **0.986**, nested freqhits **23/24** vs **23/24**).

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| **hits** | **24/24** | 0.924 | 90/96 | 59/96 |
| freqhits | **24/24** | 0.896 | 89/96 | 69/96 |
| **hitmass** | **24/24** | **0.936** | 90/96 | 59/96 |
| hashpool | **24/24** | 0.888 | 85/96 | 48/96 |
| **logit** | **24/24** | 0.931 | 89/96 | 71/96 |

Prompt-mean ranking is perfect on these 24 new topics. Isolated sign at 0 is
not: hits marks 90/96 but only 59/96 unmarked files stay ≤ 0.

Nested thresholds from leave-one-prompt-out on the 12 training stems only:

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hits Youden | 0.008 | 90/96 | 63/96 | 0.94 | 0.66 |
| **hits FPR10** | 0.505 | **83/96** | **85/96** | **0.87** | **0.89** |
| freqhits Youden / FPR10 | 0.522 | 86/96 | 79/96 | 0.90 | 0.82 |
| hashpool Youden | 0.026 | 76/96 | 90/96 | 0.79 | 0.94 |
| logit Youden | 0.794 | 75/96 | 95/96 | 0.78 | 0.99 |

The nested hits 10% FPR gate on 96 new-topic files is the strongest
*balanced* out-of-family isolated-file result in this laboratory so far.
It is still GPT-2, 128 tokens, and laboratory prompts — not a universal
detector.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --test-dir experiments/2026-08-31-pair-36x4 \
  --overlap drop-from-test \
  --methods hits,freqhits,hitmass,hashpool,logit \
  --out-dir experiments/2026-08-31-transfer-12x4-to-36x4
```
