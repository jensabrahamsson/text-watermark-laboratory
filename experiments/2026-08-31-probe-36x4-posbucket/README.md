# Position-bucketed last-4 on 36×4 GPT-2 twins

Same 36-prompt × 4-draw GPT-2 pairs as
[`../2026-08-31-probe-36x4/`](../2026-08-31-probe-36x4/).
`--methods hits,poshits,pospool --pos-bucket 16`. Hits is the published
unbucketed last-4 reader. `poshits` namespaces each last-4 context by
`i // 16`. `used_keys=false`.

## Leave-one-of-36-out

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|---|
| hits | **36/36** | **134/144** | 76/144 | **0.934** | **119/144 vs 134/144** |
| poshits | 34/36 | **134/144** | **97/144** | 0.925 | 119/144 vs 129/144 |
| pospool | 35/36 | 127/144 | 110/144 | 0.903 | 107/144 vs 128/144 |

In-domain, poshits keeps the same t=0 recall as hits (**134/144**) and
lifts unmarked `≤ 0` from 76/144 to **97/144**. Prompt-grain ranking
drops two stems (34/36 vs 36/36). Nested-by-stem Youden stays close to
the hits gate (119 vs 129 rather than 119 vs 134). This is not a
universal isolated-file detector: unmarked files still overlap at t=0.

Do not replace the published 36/36 hits ranking with 34/36 poshits.

See [research/key-free-probe.md](../../research/key-free-probe.md).
