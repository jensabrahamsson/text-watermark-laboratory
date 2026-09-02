# New-topic disjoint windows (24×4 GPT-2 → original 12×4)

Same overlap as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/).
`--windows` scores half-open token slices independently.
`--skip-nested` skipped train-LOO Youden. Nested-by-stem below is on
the frozen window LRs. Frozen tables are the same 24-stem fit as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/).

Window `0:16` matches the 16-token prefix run (hits 11/12, AUC 0.752).

## Hits last-4 (new topics)

| Window tokens | Prompts marked > unmarked | Isolated marked `lr > 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|
| 0:16 | **11/12** | 40/48 | **0.752** | 25/48 vs 29/48 |
| 16:32 | 8/12 | 27/48 | 0.512 | 8/48 vs 42/48 |
| 32:64 | 8/12 | 27/48 | 0.666 | 41/48 vs 21/48 |
| 64:128 | 10/12 | 24/48 | 0.650 | 24/48 vs 24/48 |
| full 128 (published) | **12/12** | 42/48 | **0.793** | train-LOO Youden 26/48 vs 44/48 |

Out of family, the transferable hits signal is almost entirely in the
first 16 tokens. The next 16 tokens are chance (AUC 0.512). Later windows
are weak and do not recover the full-file 12/12 ranking by themselves.

Still GPT-2 laboratory English. Not a Qwen detector.
