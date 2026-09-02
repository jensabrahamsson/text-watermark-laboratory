# Isolated 25/48 split: leftover vs occupancy-covered

In-domain isolated TPs split on occupancy-free leftover membership. Not mixed tables, not a new probe method, not keys. Does not replace 25/48.

used_keys=False leftover=20 covered=28 primary_marked>0=27
leftover marked>0 11/20, unmarked≤0 11/20
covered marked>0 16/28, unmarked≤0 11/28

Secondary holdouts:

- hard-8:128: leftover 12/20 vs 12/20; covered 17/28 vs 11/28
- hard-0:4: leftover 12/20 vs 9/20; covered 17/28 vs 17/28
- interpolate-4:128: leftover 7/20 vs 12/20; covered 13/28 vs 14/28

Leftover TPs are not leftover-file detection. Covered TPs are opening-atom overlap. Does not replace 25/48.
