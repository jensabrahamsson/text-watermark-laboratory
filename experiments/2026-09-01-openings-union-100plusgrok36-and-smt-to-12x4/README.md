# Opening-coverage union: leftover-20 ∪ short+medium+tails → original 12×4

Protocol: [research/PROTOCOL-isolated-leftover-union.md](../../research/PROTOCOL-isolated-leftover-union.md).
Frozen SHA **`e5a5f6b`**. Named **`3d8c78d`**.

Set-union of **published** occupancy-free opening zeros. Not mixed
tables, not a new `probe --methods` name, not `detector_mean`.
`used_keys=false`.

| Train | Covered | Source |
|---|---|---|
| 100 one-liners + grok36 | **28/48** | `../2026-09-01-openings-100plusgrok36-to-12x4/` |
| short+medium+tails | **30/48** | `../2026-08-31-openings-short-medium-tails/` |
| Intersection | **28/48** | mixed ⊂ SMT |
| Set-union | **30/48** | this dump (equals SMT) |
| Leftover (both zero) | **18/48** | harbour, library, station-4, letter 2–3, office 1/3/4, ferry-queue |

SMT-only covers are garden-1 and garden-4. Mixed 100+grok36 added no
unique occupancy-free openings over already-published SMT coverage.

Leftover 12-LOO hard last-4 is **10/18 vs 10/18**. Mixed occupancy-free
leftover sign is **0/18 vs 18/18** by construction. Occupancy-free
leftover-18 is closed for more unrelated GPT-2 scenes
([PROTOCOL-isolated-occupancy-closed.md](../../research/PROTOCOL-isolated-occupancy-closed.md)).
Do not sell union **30/48** or leftover **10/18** as replacing **25/48**.
