# Opening-overlap including neighborhood paraphrases

Same protocol as [`../2026-08-31-openings-short-medium-tails/`](../2026-08-31-openings-short-medium-tails/)
plus [`../2026-08-31-pair-family12x4/`](../2026-08-31-pair-family12x4/).

| upto | postokhits | postokbackoff | postokbackoff2 |
|---|---|---|---|
| 24 short + medium + tails | **30/48** | **36/48** | **13/48** |
| +12 neighborhood scenes | **38/48** | **42/48** | **15/48** |

Precision **1.000** among decided. Exact 4-token copy stays **19/48**.
The +6 postokbackoff files are ferry `was so/over/waiting` via last-1,
not a copied 4-gram. `Closing is the`, `Now in the second`, `While
working on the`, and `The printer worked` remain zeros under last-k.
Do not sell 42/48 as beating 39/48. Not a universal detector.
