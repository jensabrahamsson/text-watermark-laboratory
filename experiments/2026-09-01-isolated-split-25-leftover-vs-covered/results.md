# Isolated 25/48 split: leftover vs occupancy-covered

In-domain isolated TPs split on occupancy-free leftover membership. Not mixed tables, not a new probe method, not keys. Does not replace 25/48.

used_keys=False leftover=20 covered=28 primary_marked>0=25
leftover marked>0 10/20, unmarked≤0 11/20
covered marked>0 15/28, unmarked≤0 11/28

Secondary holdouts:

- 12loo-interpolate-last4: leftover 10/20 vs 11/20; covered 14/28 vs 13/28
- 12loo-opening-rankpath: leftover 16/20 vs 16/20; covered 25/28 vs 19/28

Leftover TPs are not leftover-file detection. Covered TPs are opening-atom overlap. Does not replace 25/48.
