# New-topic prefix-length curve (24×4 GPT-2 → original 12×4)

Same overlap as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/):
train on the 24 new 36-prompt stems × 4 draws, test on the original
12×4. `--prefix-lens` clips each completion before scoring.

`--skip-nested` skipped the expensive train-LOO Youden. Nested-by-stem
Youden below is computed on the frozen prefix LRs
(`nested_threshold_by_stem` in `stats.py`). That is not the same
protocol as the published train-LOO nested Youden (**26/48** vs **44/48**
on full files). Frozen count/hashpool tables are not copied here; they
are the same 24-stem fit as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/).

## Hits last-4 (new topics)

| Prefix tokens | Prompts marked > unmarked | Isolated marked `lr > 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|
| 16 | **11/12** | 40/48 | **0.752** | 25/48 vs 29/48 |
| 32 | 11/12 | 40/48 | 0.738 | 25/48 vs 28/48 |
| 64 | 11/12 | 41/48 | 0.775 | 30/48 vs 27/48 |
| 96 | **12/12** | 41/48 | 0.808 | 29/48 vs 42/48 |
| 128 | **12/12** | 42/48 | **0.793** | 27/48 vs 40/48 |

New-topic **ranking** appears in the first 16 tokens (11/12, AUC 0.752).
A nested-by-stem isolated-file gate on those short prefixes is weak
(25/48 vs 29/48 at 16 tokens). Full length recovers the published
ranking (12/12, AUC 0.793, isolated 42/48). AUC is not strictly
monotonic (96 tokens 0.808 vs 128 tokens 0.793 on this split).

This is still GPT-2 laboratory English. It is not a Qwen detector and
not a universal isolated-file yes/no.
