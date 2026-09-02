# 100 one-liners → Grok-register 12×4, lock A interpolate windows (absolute history)

Frozen command from [../../research/PROTOCOL-isolated-windows-absolute.md](../../research/PROTOCOL-isolated-windows-absolute.md).
Fit is full-file last-4 (same tables as the xreg lock A run). Each window
scores that slice with **absolute** `score_span`. `used_keys=false`.
Duplicate `tables-counts/` not stored; see
`../2026-09-01-transfer-100x4-to-grok12x4-hard-last4/`.
Do **not** overwrite
`../2026-09-01-transfer-100x4-to-grok12x4-hard-windows/`.

Full-file ranking **11/12** is still not front-loaded on this split.
Absolute 0:4 equals reindexed **7/12**. Absolute 32:64 **rose** to
**10/12** versus reindexed **9/12**. Absolute 16:32 fell 8→7.
Absolute 64:128 stayed **9/12**.

| Window | Absolute prompt | Absolute AUC | t=0 marked | unmarked ≤0 | Reindexed prompt |
|---|---|---|---|---|---|
| 0:4 | 7/12 | 0.619 | 23/48 | 31/48 | 7/12 |
| 4:16 | 4/12 | 0.461 | 20/48 | 24/48 | 4/12 |
| 16:32 | 7/12 | 0.503 | 23/48 | 23/48 | 8/12 |
| 32:64 | **10/12** | 0.658 | 27/48 | 29/48 | 9/12 |
| 64:128 | **9/12** | 0.624 | 27/48 | 32/48 | 9/12 |

Occupancy-free openings on these files are **0/48**. Window 0:4 t=0
**23/48** is not observed-token TPs. Isolated t=0 stays chance-like
in every slice. Do not sell tail **10/12**. Does not replace **25/48**.
