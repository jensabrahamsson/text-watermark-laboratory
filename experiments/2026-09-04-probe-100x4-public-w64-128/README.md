# Public Hw=4 interpolate on tokens [64:128)

Protocol: [research/PROTOCOL-next-longctx-windows.md](../../research/PROTOCOL-next-longctx-windows.md)
(freeze SHA `8283d1f`). Twins: `../2026-09-01-pair-100x4/`.
`used_keys=false`. Do not overwrite
`../2026-09-01-probe-100x4-hard-windows-absolute/` (absolute H2 through
32:64). Full-file interpolate here is still lock A **99/100**.

| Window | interpolate |
|---|---|
| 64:128 | **93/100**, AUC **0.726**, isolated **259/400**, unmarked $\le 0$ **258/400** |
| full file | **99/100**, 0.898, **352/400** |

Same slice under $\Hw=12$ is
`../2026-09-04-probe-100x4-ngram13-windows/` interpolate **50/100**,
AUC **0.501**. Do not sell **93/100** as replacing **25/48**.
