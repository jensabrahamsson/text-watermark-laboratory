# 100 one-liners → original 12×4, lock A interpolate windows (absolute history)

Frozen command from [../../research/PROTOCOL-isolated-windows-absolute.md](../../research/PROTOCOL-isolated-windows-absolute.md).
`used_keys=false`. Duplicate `tables-counts/` not stored; see
`../2026-09-01-transfer-100x4-to-12x4-hard-last4/`.
Do **not** overwrite
`../2026-09-01-transfer-100x4-to-12x4-hard-windows/`.

Full-file ranking **8/12**. Absolute window **0:4** ranks **9/12**
(AUC 0.636), equal to reindexed **9/12**; **16:32** ranks **6/12**
(AUC 0.576). Front-loaded transfer still holds on the original 12.
Absolute 64:128 **fell** 8→6 versus reindexed.

Isolated t=0 on 0:4 is **25/48 vs 31/48** — the same *count* as the
headline isolated grain on a different transfer window, not a
calibrated detector. Does not replace **25/48**.
