# 100 one-liners → Grok-register 12×4, lock A interpolate windows

Frozen command from [../../research/PROTOCOL-isolated-windows.md](../../research/PROTOCOL-isolated-windows.md).
Fit is full-file last-4 (same tables as the xreg lock A run). Each window
scores only that slice. `used_keys=false`. Duplicate `tables-counts/`
not stored; see `../2026-09-01-transfer-100x4-to-grok12x4-hard-last4/`.

Full-file ranking **11/12** is not front-loaded on this split:

| Window | Prompt | File AUC | t=0 marked | unmarked ≤0 |
|---|---|---|---|---|
| 0:4 | 7/12 | 0.619 | 23/48 | 31/48 |
| 4:16 | 4/12 | 0.467 | 21/48 | 26/48 |
| 16:32 | 8/12 | 0.497 | 23/48 | 23/48 |
| 32:64 | **9/12** | 0.630 | 26/48 | 28/48 |
| 64:128 | **9/12** | 0.616 | 26/48 | 31/48 |

Occupancy-free openings on these files are **0/48**. Window 0:4 t=0
**23/48** is not observed-token TPs. Isolated t=0 stays chance-like
in every slice. Do not sell tail **9/12**. Does not replace **25/48**.
