# Opening-coverage union: Distil 100×4 ∪ short+medium+tails → original 12×4

Protocol: [research/PROTOCOL-isolated-dsmt.md](../../research/PROTOCOL-isolated-dsmt.md).
Frozen SHA **`b1f0c7d`**. Named **`5cc418e`**.

Set-union of **published** occupancy-free opening zeros. Not mixed
tables, not a new `probe --methods` name, not `detector_mean`.
`used_keys=false`.

| Train | Covered | Source |
|---|---|---|
| Distil 100×4 → original 12 | **23/48** | `../2026-09-01-openings-distil100x4-to-12x4/` |
| short+medium+tails | **30/48** | `../2026-08-31-openings-short-medium-tails/` |
| Intersection | **20/48** | Distil ∩ SMT |
| Set-union | **33/48** | this dump |
| Leftover (both zero) | **15/48** | harbour, library, station-4, letter 2–3, ferry-queue |

Distil-only covers are office-1, office-3, and office-4. Those are the
leftover-18 Distil covers from xgen. SMT-only covers are night-bus,
letter 1/4, and garden.

Leftover 12-LOO hard last-4 is **9/15 vs 8/15**. Distil occupancy-free
leftover sign is **0/15** marked by construction. Do not sell union
**33/48** or leftover **9/15** as replacing **25/48**. Do not target
leftover-15 openings after peeking.
