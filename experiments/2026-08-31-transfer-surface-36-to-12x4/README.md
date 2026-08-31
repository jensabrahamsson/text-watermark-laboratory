# Surface and logit, 24 new topics → 12×4 files

Same split as `../2026-08-31-transfer-nested-36-to-12x4/`. Adds UTF-8
`surface` and nested-calibrated `logit`. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hits | 8/12 | 0.769 | **39/48** | 28/48 |
| hitmass | **10/12** | **0.771** | 39/48 | 28/48 |
| hashpool | **11/12** | 0.766 | 34/48 | 30/48 |
| surface | 9/12 | 0.648 | 36/48 | 19/48 |
| logit | 8/12 | 0.760 | 22/48 | 39/48 |

Nested Youden (train stems only, frozen on test):

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| **hashpool** | **0.005** | **33/48** | **34/48** | **0.69** | **0.71** |
| surface | 0.022 | 15/48 | 40/48 | 0.31 | 0.83 |
| logit | 0.128 | 22/48 | 40/48 | 0.46 | 0.83 |

Byte pooling transfers out of family (9/12, AUC 0.648) but does not beat
nested token hashpool as an isolated-file rule. Logit at the nested point
matches hits nested, not hashpool nested.
