# Disjoint token windows on 36×4 GPT-2 twins

Prefixes are cumulative. These runs use `--windows 0:16,16:32,32:64,64:128`
so each slice is scored **without** earlier tokens. Same 36×4 GPT-2 pairs
and last-4 `hits` / `hashpool` as
[`../2026-08-31-probe-36x4/`](../2026-08-31-probe-36x4/).
`used_keys=false`.

Window `0:16` must match the published 16-token prefix. It does.

## Hits last-4 (in-domain)

| Window tokens | Prompts marked > unmarked | Isolated marked `lr > 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|
| 0:16 | **34/36** | 129/144 | **0.916** | 118/144 vs 127/144 |
| 16:32 | 22/36 | 74/144 | 0.549 | 32/144 vs 119/144 |
| 32:64 | 28/36 | 92/144 | 0.651 | 63/144 vs 118/144 |
| 64:128 | 29/36 | 108/144 | 0.723 | 94/144 vs 114/144 |
| full 128 (published) | **36/36** | 134/144 | **0.934** | 119/144 vs 134/144 |

The keyed mixin biases **every** position (`ngram_len=5`). The key-free
4-gram reader does not. Shared last-4 contexts that separate marked from
unmarked twins are **front-loaded**: the first 16 tokens already rank
34/36 (AUC 0.916). Tokens 16–32 are near chance (22/36, AUC 0.549). The
tail (64–128) still ranks above chance (29/36, AUC 0.723) but does not
match the opening.

This is a statement about the laboratory count-table indicator, not a
claim that later tokens are unmarked under official `score`.

See [research/key-free-probe.md](../../research/key-free-probe.md).
