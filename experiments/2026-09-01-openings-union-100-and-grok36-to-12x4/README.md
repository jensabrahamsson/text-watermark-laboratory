# Opening-coverage union: 100 one-liners ∪ 36 Grok-length → original 12×4

Set-union of **published** occupancy-free opening zeros. Not mixed
tables, not a new `probe --methods` name, not `detector_mean`.
`used_keys=false`.

| Train | Covered | Source |
|---|---|---|
| 100 one-liners | **18/48** | `../2026-09-01-openings-100x4-to-12x4/` |
| 36 Grok-length | **10/48** | `../2026-09-01-openings-grok36x4-to-12x4/` |
| Intersection | **0/48** | complementary openings |
| Set-union | **28/48** | this dump |
| Leftover (both zero) | **20/48** | harbour, library, station-4, letter 2–3, office 1/3/4, garden 1/4, ferry-queue |

The 100-only covers are kitchen, station 1–3, rain, letter 1/4,
workshop, office-2. The grok36-only covers are night-bus, market,
garden 2–3.

Leftover interpolate/rankpath signs are from **already-opened**
holdouts, not mixed tables. Grok36 interpolate on the 20 leftover
files is **13/20** marked `lr>0` vs **14/20** unmarked `lr≤0`. That
slice includes library `Closing` unbucketed body copies. Do not sell
**28/48** or leftover **13/20** as replacing **25/48**. Mixed tables
are [PROTOCOL-isolated-pool.md](../../research/PROTOCOL-isolated-pool.md).
