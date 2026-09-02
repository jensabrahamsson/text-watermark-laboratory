# Occupancy leftover-20 bound

Official prefix scores use detector keys (positive control). Leftover interpolate atoms do not. Neither replaces 25/48.

official_used_keys=True leftover=20 covered=28

| prefix | leftover marked mean | >0.55 | covered marked mean | >0.55 | unmarked mean | >0.55 |
|---|---|---|---|---|---|---|
| 5 | 0.6533 | 18/20 | 0.6202 | 27/28 | 0.4813 | 14/48 |
| 16 | 0.6272 | 20/20 | 0.6252 | 28/28 | 0.4955 | 3/48 |
| 128 | 0.6242 | 20/20 | 0.6198 | 28/28 | 0.5000 | 0/48 |

atoms_used_keys=False n_rows=40 leftover marked lr>0=13

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.0791 | -0.2125 | 21 | 99 |
| 4:16 | 0.2657 | -0.0842 | 15 | 465 |
| 16:32 | 0.0277 | 0.1194 | 7 | 633 |
| 32:64 | 0.2374 | -0.0800 | 31 | 1249 |
| 64:128 | 0.0434 | -0.1112 | 52 | 2502 |

Official leftover detection uses keys. Leftover atoms are not a leftover-file detector. Does not replace 25/48.
