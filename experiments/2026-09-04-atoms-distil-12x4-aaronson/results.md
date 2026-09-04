# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=0 seen=196 unseen=11996

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.6798 | -3.0718 | 133 | 155 |
| 4:16 | -2.0234 | -2.6172 | 10 | 1142 |
| 16:32 | -2.2148 | -2.4533 | 20 | 1516 |
| 32:64 | -2.4062 | -2.4137 | 9 | 3063 |
| 64:128 | -2.2428 | -2.4590 | 24 | 6120 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=28 meanΔ=3.380 'I' → ' had'
- n=12 meanΔ=1.894 '\n' '\n' → '"'
- n=12 meanΔ=6.605 'I' ' had' → ' two'
- n=8 meanΔ=5.870 '\n' '\n' '"' → 'This'
- n=8 meanΔ=8.973 'I' ' had' ' two' → ' tickets'
- n=4 meanΔ=6.147 'I' ' had' → ' put'

### 4:16
- n=4 meanΔ=1.050 ' she' ' said' '.' '\n' → '"'
- n=4 meanΔ=0.054 ',"' ' she' ' said' '.' → '\n'

### 16:32
- n=8 meanΔ=6.958 '.' '\n' 'I' ' had' → ' two'
- n=4 meanΔ=1.054 ' she' ' said' '.' '\n' → '"'
- n=4 meanΔ=0.053 ',"' ' she' ' said' '.' → '\n'

### 32:64
- n=8 meanΔ=6.958 '.' '\n' 'I' ' had' → ' two'

### 64:128
- n=20 meanΔ=6.923 '.' '\n' 'I' ' had' → ' two'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
