# Letter d2 first official 5-gram vs isolated rankpath

Letter d2 (`08-letter-marked-2.txt`) is the unique leftover that
in-domain opening rankpath also misses. Official `public-deepmind-30`
mean on the isolated first 5-gram is **0.733** (22/30 g-values = 1).
That path uses detector keys. **Not a key-free reader.**

The 5-gram is `Now in the second I` (ids
`[3844, 287, 262, 1218, 314]`). Isolated `--fit-prefix 4` rankpath
never scores generated token 4: three rank symbols are tokens 1–3.
Official `detector_mean` on a 5-token prefix scores exactly that
missing tournament.

Unmarked GPT-2 ranks of generated token 4 (`I`):

| Context | Rank in top-40 | Symbol |
|---|---|---|
| Isolated (`Now in the second` → `I`) | **41** (miss) | 0 |
| Prompt-conditioned (generation geometry) | **11** | 4 |

The last official n-gram of `prompt + generated[:5]` equals the
isolated 5-gram (`g_last_equal`). Isolated rankpath is looking at the
right tokens and the wrong language-model context. Generation-time
rank 11 is not the near-tie bin (ranks 2–3) the alphabet was built
for.

Letter d3's first 5-gram is also an isolated top-k miss (rank 41,
official 0.767). Prefix-4 already signs it from tokens 1–3. Ferry-queue
d4 is the other official-5-gram invisibility mode: mean **0.700** on
the **argmax** token (rank 1 isolated and prompt). Among 45 marked
files with official prefix-5 >0.55, isolated token-4 rank is 10 argmax
and 8 miss. Unmarked isolated miss is 7/48 vs marked 9/48.

60-stem prefix-8 `postokbackoff` letter d2 `lr=-0.606` is last-1
`' in' → ' the'` (2 vs 8), not the 5-gram. The 5-gram is unseen at
last-4/3/2; `' second'` never continues with `' I'`. `postokbackoff2`
abstains. Letter d3's rescue is last-1 `',' → ' my'`. All four extra
prefix-8 TPs are last-1; **20 of 38** TPs are last-1 only.
`postokbackoff2` is **18/48 vs 46/48**.

JSON: `results.json` (official means use keys; ranks do not),
`backoff-trace.json` (`used_keys=false`), `fifth-rank-bins.json`,
`prefix8-backoff-orders.json`, `hashtok-trace.json` (`used_keys=false`),
`hashtokbackoff-trace.json` (`used_keys=false`).
60-stem prefix-5 hashpool signs letter d2 at lr=0.372 with **0/8**
hashes seeing `I`; hashtok abstains. Hashed backoff still does not
read that 5-gram: last-4/3/2 hashes never saw `I`; last-1 saw it
unmarked only (c_m=0, c_u=2, δ=−1.10). hashtokbackoff lr=0.096
(`n_used=3`); hashtokbackoff2 lr=0.694 is tokens 1–2 (`Now`→` in` at
order 3, `Now in`→` the` at order 4), not token 4. The i=1 "order 3"
hit is a one-token prefix hashed into the order-3 table, not a 3-gram.
Exact-length `hashtoklen` still abstains (`n_used=0`). Exact backoff2
lr=0.797 is legal last-2 `'Now in' → ' the'` (i=2, order 2), not token
4; including last-1 of `I` makes hashtoklenbackoff −0.152.
`hashtoklen-trace.json` (`used_keys=false`, `exact_len=true`).
Harbour d2 official 5-gram `The ferry was over ,` is the unique
hashtoklen extra versus exact `postokhits`: last-4 of that comma is
unmarked-like as an exact 4-gram (lr=−2.65) and marked-like in one
colliding hash (1/8 hashes, bucket 178, c_m=11, c_u=0, lr=+0.618).
Not Laplace occupancy. Letter d2 still abstains. JSON:
`harbour-d2-hashtoklen-trace.json`.
Occupancy-free drop-one skip-grams (`hashskip`) **see** letter d2's
`I` on two tagged last-4 holes, both unmarked-only (c_m=0, c_u=1,
lr=−0.847). Coarsening is not a leftover rescue. Nested Youden on
that reader is **16/48 vs 41/48**. JSON:
`letter-d2-hashskip-trace.json`.
In-domain prefix-5 rankpath:
[../2026-09-01-probe-12x4-fitprefix5-rankpath/](../2026-09-01-probe-12x4-fitprefix5-rankpath/).
Hashed occupancy write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
