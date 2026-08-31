# Matched 16-token fit on 36×4 GPT-2 twins

`--fit-prefix 16` clips every draw to the first 16 tokens **before fit
and score**. That is not `--prefix-lens 16`, which fits on the full 128
tokens and then scores a prefix. The earlier prefix curve is
[`../2026-08-31-probe-36x4-prefixes/`](../2026-08-31-probe-36x4-prefixes/).
Same 36×4 GPT-2 pairs as
[`../2026-08-31-probe-36x4/`](../2026-08-31-probe-36x4/).
`used_keys=false`. Surface texts are left full; this clip is on token
ids.

## Hits last-4 (matched 16-token window)

| Protocol | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden |
|---|---|---|---|---|---|
| Full 128-token hits (published) | **36/36** | 134/144 | 76/144 | **0.934** | 119/144 vs 134/144 |
| Fit full, score prefix 16 | **34/36** | 129/144 | 93/144 | 0.916 | 118/144 vs 127/144 |
| **Fit and score first 16** | **34/36** | 132/144 | **112/144** | **0.929** | **121/144 vs 136/144** |
| Matched 16-token hashpool | 34/36 | 129/144 | 92/144 | 0.917 | 117/144 vs 137/144 |

Matching the train window to the front-loaded 4-gram footprint raises
t=0 specificity (112/144 unmarked `≤ 0` vs 76/144 on the full reader and
93/144 on fit-full/score-prefix) without collapsing in-domain ranking
(34/36, AUC 0.929 vs 36/36 / 0.934). Isolated overlap at a universal
t=0 remains.

See [research/key-free-probe.md](../../research/key-free-probe.md).
