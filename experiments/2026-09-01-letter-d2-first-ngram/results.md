# Letter d2 first official 5-gram

Reference `public-deepmind-30` on the isolated first 5-gram uses keys.
Ranks are unmarked GPT-2, no keys.

| Check | Letter d2 |
|---|---|
| Opening 5 tokens | `Now in the second I` |
| Official isolated prefix-5 mean | **0.733** (22/30) |
| Isolated rank of token 4 | **41** (miss top-k) |
| Prompt-conditioned rank of token 4 | **11** |
| Isolated prefix-4 rankpath | −1.163 |
| Isolated prefix-5 rankpath | −1.208 |

Prefix-4 rankpath never sees the official 5-gram. Prefix-5 sees it as
symbol 0 (isolated miss) and still misses.

Among 45 marked files with official prefix-5 >0.55, isolated token-4
rank is **10 argmax** and **8 miss**. Unmarked isolated miss is 7/48.

60-stem prefix-8 postokbackoff letter d2 `lr=-0.606` (`n_used=2`) is
last-1 `' in' → ' the'`, not the 5-gram. The 5-gram is unseen.
`postokbackoff2` abstains.

Leftover isolated top-k misses at token 4: letter d2 and letter d3
only. Ferry-queue d4 is officially marked (0.700) on the argmax.
