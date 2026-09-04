# 100-LOO interpolate / hard / hits windows on ngram_len=13 twins

Protocol: [research/PROTOCOL-next-longctx-windows.md](../../research/PROTOCOL-next-longctx-windows.md)
(freeze SHA `8283d1f`). `used_keys=false`. Do not overwrite
`../2026-09-03-probe-100x4-ngram13-hard-last4/` (full-file interpolate
**76/100**). Full-file interpolate here is still **76/100**.

| Window | interpolate | hard | hits |
|---|---|---|---|
| 0:4 | **86/100**, AUC **0.823**, 327/400 | 82/100, 0.763 | **95/100**, 0.875 |
| 4:16 | 75/100, 0.645 | 47/100, 0.476 | 39/100, 0.498 |
| 16:32 | 57/100, 0.529 | 57/100, 0.510 | 49/100, 0.494 |
| 32:64 | 57/100, 0.520 | 55/100, 0.526 | 61/100, 0.528 |
| 64:128 | **50/100**, AUC **0.501**, 184/400 | 59/100, 0.527 | 53/100, 0.516 |
| full file | **76/100**, 0.666, 267/400 | 66/100, 0.579 | **91/100**, 0.843 |

Tail interpolate **50/100** is chance (file-level binom $p\approx 0.95$;
perm $p\approx 0.19$). Hits full-file **91/100** sits with the opening
**95/100**, not the tail **53/100**. Public $\Hw=4$ on the same slice is
`../2026-09-04-probe-100x4-public-w64-128/` (**93/100**). Do not sell
**50/100**, **86/100**, or **91/100** as replacing **25/48**.
