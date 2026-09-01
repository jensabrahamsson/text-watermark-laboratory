# In-domain 25/48 split: leftover vs occupancy-covered

Decode of published JSON. Not a new `probe --methods` name.
Frozen in [PROTOCOL-isolated-split.md](../../research/PROTOCOL-isolated-split.md)
(`f09d0e2`). `used_keys=false`.

The headline isolated-file count is 12-LOO hard last-4 marked `lr>0`
**25/48**. Mixed occupancy-free pooling covers **28/48** original-12
openings and leaves **20** zeros. This dump crosses those two facts.

| Slice | Marked `lr>0` | Unmarked `lr≤0` |
|---|---|---|
| Leftover 20 | **10/20** | **11/20** |
| Occupancy-covered 28 | **15/28** | **11/28** |
| Full 48 | **25/48** | **22/48** |

Leftover last-4 is chance (9 leftover FPs). Covered TPs are openings
that 100+grok36 later copy. Ranking-loss TPs (station-4, office-4,
ferry-queue 1–3) are all leftover and are the published **5** TPs on
ranking losses. Letter leftover (`Now` / `While`) and garden leftover
are **0/2**. Leftover TPs and FNs share openings (`Closing is the`,
`The ferry was so` / `in`).

Do not sell leftover **10/20**, covered **15/28**, in-domain leftover
rankpath **16/20**, or mixed leftover rankpath **12/20** as replacing
**25/48**. Isolated-file detection is not finished.
