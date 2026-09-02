# Nested thresholds: 12×4 → 24 new 36-topic stems

Same split as `../2026-08-31-transfer-12x4-to-36/`. Nested Youden / 10% FPR
from leave-one-prompt-out on the twelve training families, frozen on stems
13–36. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hits | **24/24** | **0.986** | 24/24 | 14/24 |
| **freqhits** | **24/24** | 0.984 | 24/24 | 13/24 |
| hitmass | 23/24 | 0.977 | 24/24 | 14/24 |
| hashpool | 23/24 | 0.924 | 21/24 | 20/24 |

Nested operating points:

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hits Youden | 0.008 | 24/24 | 16/24 | 1.00 | 0.67 |
| hits FPR10 | 0.505 | 20/24 | 24/24 | 0.83 | 1.00 |
| **freqhits Youden / FPR10** | **0.522** | **23/24** | **23/24** | **0.96** | **0.96** |
| hitmass Youden | 0.009 | 21/24 | 23/24 | 0.88 | 0.96 |
| hashpool Youden | 0.026 | 12/24 | 24/24 | 0.50 | 1.00 |

Training on four draws per prompt gives shared 4-grams enough support that
a count ≥ 4 gate (`freqhits`) plus a nested threshold is an almost balanced
isolated-file rule on *new* topics. That is still GPT-2 mixin twins, not a
universal detector. Threshold 0 remains badly calibrated for hits (10
unmarked false positives).
