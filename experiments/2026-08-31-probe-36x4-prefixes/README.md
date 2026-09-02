# In-domain prefix-length curve on 36×4 GPT-2 twins

Same 36-prompt × 4-draw GPT-2 pairs as
[`../2026-08-31-probe-36x4-draws/`](../2026-08-31-probe-36x4/)
(`experiments/2026-08-31-probe-36x4/`).
`--prefix-lens 16,32,64,96,128` scores a token prefix of each completion
(character prefix for `--surface`) and writes `prefix-{N}/{method}/`.

The 128-token prefix is a sanity check: it must match the published
full-file 36×4 last-4 result. It does (hits **36/36**, isolated 134/144,
AUC **0.934**, nested-by-stem **119/144** vs **134/144**).

## Hits last-4 (in-domain)

| Prefix tokens | Prompts marked > unmarked | Isolated marked `lr > 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|
| 16 | **34/36** | 129/144 | **0.916** | 118/144 vs 127/144 |
| 32 | 35/36 | 131/144 | 0.917 | 119/144 vs 129/144 |
| 64 | **36/36** | 130/144 | 0.919 | 125/144 vs 130/144 |
| 96 | 36/36 | 132/144 | 0.924 | 121/144 vs 129/144 |
| 128 | **36/36** | 134/144 | **0.934** | 119/144 vs 134/144 |

The watermark footprint is **front-loaded**. Sixteen tokens already rank
34/36 prompts correctly in-domain (AUC 0.916). Isolated-file overlap at a
universal `t = 0` remains (129/144 at 16 tokens, 134/144 at 128). The
nested-by-stem gate stays close to `t = 0` and does not create a
universal isolated-file detector.

Prefixes are cumulative: the 64-token score includes the first 16.
Disjoint windows (`probe --windows 0:16,16:32,32:64,64:128`) ask whether
later tokens carry an independent mark. They mostly do not: see
[`../2026-08-31-probe-36x4-windows/`](../2026-08-31-probe-36x4-windows/).

Official `score` on the same first draws is 36/36 at full length. That is
the keyed reference, not the key-free claim.

See [research/key-free-probe.md](../../research/key-free-probe.md).
