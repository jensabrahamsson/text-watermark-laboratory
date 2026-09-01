# Headline 12-LOO mask-*k* windows

Frozen in [PROTOCOL-isolated-mask.md](../../research/PROTOCOL-isolated-mask.md)
(`004397c`). Existing `--windows` on hard last-4 and interpolate.
Not a new `probe --methods` name. `used_keys=false`.

Full-file hard remains **9/12**, isolated **25/48**.

| Window | Hard prompt | Hard `lr>0` | Interpolate prompt |
|---|---|---|---|
| 0:2 | **10/12** | 27/48 vs 31/48 | **9/12** |
| 0:4 | **5/12** | 29/48 vs 26/48 | **9/12** |
| 0:8 | **6/12** | 33/48 vs 25/48 | **8/12** |
| 4:128 | **9/12** | 27/48 vs 22/48 | **5/12** |
| 8:128 | **9/12** | 29/48 vs 23/48 | **3/12** |

Hard prompt ranking survives masking the first 4 and 8 generated tokens.
Prefix 0:4 hard is chance. Interpolate is front-loaded; hard is not.
Do not sell prefix **10/12** or tail **9/12** as replacing **25/48**.
