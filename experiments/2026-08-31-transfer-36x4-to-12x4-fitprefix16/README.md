# New-topic matched 16-token fit (24×4 GPT-2 → original 12×4)

Same overlap as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/).
`--fit-prefix 16` clips train and test draws to the first 16 tokens
before fit and score. That is not `--prefix-lens 16` on a full-file
table ([`../2026-08-31-transfer-36x4-to-12x4-prefixes/`](../2026-08-31-transfer-36x4-to-12x4-prefixes/)).
`--skip-nested`. `used_keys=false`.

Frozen `tables-counts/` and `tables-hashpool/` here are **16-token**
fits, not copies of the 128-token transfer tables.

Nested-by-stem Youden below is on the frozen test LRs, not train-LOO.
In-sample Youden on the 16-token hits fit is conservative (16/48 vs
44/48 at t=0.677).

## Hits last-4 (new topics, matched 16 tokens)

| Protocol | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden |
|---|---|---|---|---|---|
| Full 128-token hits | **12/12** | **42/48** | 24/48 | 0.793 | 27/48 vs 40/48 |
| Fit full, score prefix 16 | **11/12** | 40/48 | 23/48 | 0.752 | 25/48 vs 29/48 |
| **Fit and score first 16** | **11/12** | 39/48 | **31/48** | **0.818** | **39/48 vs 36/48** |
| Matched 16-token hashpool | 9/12 | 27/48 | 26/48 | 0.636 | 20/48 vs 44/48 |

Matched 16-token OOD hits **beats full-file hits on file AUC** (0.818 vs
0.793) and on t=0 specificity (31/48 vs 24/48). Nested-by-stem on those
short LRs is nearly balanced (39/48 vs 36/48). Prompt grain drops one
stem (11/12 vs 12/12). Hashpool on the 16-token window does not transfer
(9/12, AUC 0.636).

See [research/key-free-probe.md](../../research/key-free-probe.md).
