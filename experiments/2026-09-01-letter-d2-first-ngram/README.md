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
abstains. Letter d3's rescue is last-1 `',' → ' my'`.

JSON: `results.json` (official means use keys; ranks do not),
`backoff-trace.json` (`used_keys=false`), `fifth-rank-bins.json`.
In-domain prefix-5 rankpath:
[../2026-09-01-probe-12x4-fitprefix5-rankpath/](../2026-09-01-probe-12x4-fitprefix5-rankpath/).

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
