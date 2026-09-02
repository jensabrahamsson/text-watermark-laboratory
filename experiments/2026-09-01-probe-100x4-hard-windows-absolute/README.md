# Absolute-history lock A interpolate windows

Protocol: [research/PROTOCOL-h2-absolute.md](../../research/PROTOCOL-h2-absolute.md).

Twins: `../2026-09-01-pair-100x4/`. Same flags as PROTOCOL-next H2.
New out-dir so the reindexed dump is not overwritten. `used_keys=false`.

| Window | Absolute prompt | Absolute AUC | Absolute t=0 | Reindexed prompt |
|---|---|---|---|---|
| 0:4 | **99/100** | **0.885** | 372/400 vs 272/400 | **99/100** |
| 16:32 | **87/100** | **0.695** | 267/400 vs 240/400 | **89/100** |

H2-abs holds (99 > 87). Absolute 16:32 did not rise versus reindexed
**89/100**. Do not sell **99/100** or **87/100** as replacing **25/48**.
Keep `../2026-09-01-probe-100x4-hard-windows/`.
