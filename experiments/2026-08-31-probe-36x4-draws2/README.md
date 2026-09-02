# Draw-count ablation: 36 topics × 2 draws × 128 tokens

`--max-draws 2` on `experiments/2026-08-31-pair-36x4`.

| Method | Prompt wins | File AUC | Nested-by-stem marked / unmarked |
|---|---|---|---|
| hits | 33/36 | 0.875 | 52/72 vs 64/72 |
| freqhits | 33/36 | 0.873 | 56/72 vs 64/72 |
| hitmass | **34/36** | **0.878** | 52/72 vs 69/72 |
| hashpool | 31/36 | 0.840 | 52/72 vs 67/72 |

Between the 1-draw 30/36 and the 4-draw 36/36. Extra draws help both ranking
and the nested isolated-file gate.

See [../2026-08-31-probe-36x4/](../2026-08-31-probe-36x4/).
