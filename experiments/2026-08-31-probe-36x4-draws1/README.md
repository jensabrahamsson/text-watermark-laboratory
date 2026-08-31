# Draw-count ablation: 36 topics × 1 draw × 128 tokens

Same files as `../2026-08-31-pair-36x4/`, clipped with `--max-draws 1`.
Length-matched to the 12×4 corpus. Not the historical 256-token 36×1 run.

| Method | Prompt wins | File AUC | Nested-by-stem marked / unmarked |
|---|---|---|---|
| hits | **30/36** | 0.845 | 29/36 vs 31/36 |
| freqhits | 29/36 | 0.828 | 27/36 vs 26/36 |
| hitmass | **32/36** | **0.855** | 26/36 vs 33/36 |
| hashpool | 23/36 | 0.753 | 23/36 vs 31/36 |

Hits ranking matches the old 256-token 36×1 result (30/36). Hashpool needs
the extra tokens or extra draws.

See [../2026-08-31-probe-36x4/](../2026-08-31-probe-36x4/) for the 2-draw and
4-draw rows.
