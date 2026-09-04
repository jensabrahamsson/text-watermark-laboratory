# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=12 seen=457 unseen=11735

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 2.1043 | -1.7927 | 127 | 161 |
| 4:16 | -0.3486 | -1.5594 | 12 | 1140 |
| 16:32 | -0.5896 | -1.8511 | 8 | 1528 |
| 32:64 | -0.3902 | -1.5835 | 13 | 3059 |
| 64:128 | 0.0374 | -1.5614 | 297 | 5847 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=24 meanΔ=1.437 'At' → ' last'
- n=20 meanΔ=2.353 'At' ' last' → ','
- n=20 meanΔ=3.721 'At' ' last' ',' → ' the'
- n=12 meanΔ=7.178 'At' → ' least'
- n=12 meanΔ=7.963 'At' ' least' → ' once'
- n=8 meanΔ=1.565 'At' ' least' ' once' → ','
- n=8 meanΔ=9.067 '[' → ' ]'
- n=8 meanΔ=5.861 '[' ' ]' → ' '

### 4:16
- n=8 meanΔ=5.419 'At' ' least' ' once' ',' → ' this'
- n=4 meanΔ=7.525 ' (' '1' '4' ')\n\n' → 'This'

### 16:32
- n=4 meanΔ=7.526 ' (' '1' '4' ')\n\n' → 'This'

### 32:64
- n=4 meanΔ=3.683 '.\n' 'At' ' last' ',' → ' the'
- n=4 meanΔ=1.904 '.\n' 'At' ' least' ' once' → ','
- n=4 meanΔ=5.416 'At' ' least' ' once' ',' → ' this'

### 64:128
- n=244 meanΔ=3.226 '0' '0' '0' '0' → '0'
- n=16 meanΔ=3.701 '.\n' 'At' ' last' ',' → ' the'
- n=12 meanΔ=10.260 ' I' ' would' ' pay' ' an' → ' extra'
- n=8 meanΔ=1.201 ' pay' ' an' ' extra' ' ' → '2'
- n=8 meanΔ=5.063 ' would' ' pay' ' an' ' extra' → ' '
- n=4 meanΔ=1.904 '.\n' 'At' ' least' ' once' → ','
- n=4 meanΔ=5.423 'At' ' least' ' once' ',' → ' this'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
