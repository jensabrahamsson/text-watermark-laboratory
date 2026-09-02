# New-topic matched 16-token fit with 4-token position buckets

Same overlap as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/).
`--fit-prefix 16 --pos-bucket 4 --skip-nested`. Hits reproduces
[`../2026-08-31-transfer-36x4-to-12x4-fitprefix16/`](../2026-08-31-transfer-36x4-to-12x4-fitprefix16/).
Unbucketed count tables are not copied. Frozen `tables-poshits/` is the
16-token bucket-4 reader. `used_keys=false`.

Nested-by-stem Youden below is on the frozen test LRs, not train-LOO.
In-sample Youden is conservative (16/48 vs 45/48 at t=0.731).

## Hits last-4 (new topics)

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden |
|---|---|---|---|---|---|
| Full 128-token hits | **12/12** | **42/48** | 24/48 | 0.793 | 27/48 vs 40/48 |
| Matched 16-token hits | **11/12** | 39/48 | 31/48 | 0.818 | 39/48 vs 36/48 |
| **Matched 16-token poshits, bucket 4** | **11/12** | 39/48 | **33/48** | **0.820** | **39/48 vs 38/48** |

The finer opening buckets add a small OOD lift on top of the matched
16-token fit: file AUC 0.820 vs 0.818, unmarked ≤0 33/48 vs 31/48,
nested-by-stem 39/48 vs 38/48. Prompt grain stays 11/12. This is still
not a universal isolated-file detector.

See [research/key-free-probe.md](../../research/key-free-probe.md).
