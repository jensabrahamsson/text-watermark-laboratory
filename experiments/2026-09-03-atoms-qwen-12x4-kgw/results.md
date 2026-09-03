# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=35 seen=84 unseen=12108

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.0695 | 0.2205 | 62 | 226 |
| 4:16 | 0.0339 | -0.0322 | 2 | 1150 |
| 16:32 | 0.0689 | -0.0601 | 6 | 1530 |
| 32:64 | 0.0856 | -0.1363 | 6 | 3066 |
| 64:128 | 0.1482 | -0.1456 | 8 | 6136 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=5 meanΔ=1.628 'It' → '’s'
- n=5 meanΔ=1.150 'It' ' was' → ' a'
- n=2 meanΔ=1.154 'A' → ' few'
- n=1 meanΔ=3.676 'But' → ' it'
- n=1 meanΔ=4.338 'I' → ' had'
- n=1 meanΔ=4.219 'I' ' had' → ' to'
- n=1 meanΔ=0.208 'It' → ' was'
- n=1 meanΔ=4.114 'There' → '’s'

### 4:16
- n=1 meanΔ=0.792 ' didn' '’t' ' know' ' how' → ' to'

### 16:32
- n=1 meanΔ=0.791 ' didn' '’t' ' know' ' how' → ' to'
- n=1 meanΔ=0.910 ' stuck' ' out' ' of' ' the' → ' window'

### 32:64
- n=1 meanΔ=6.840 ' this' ' kind' ' of' ' thing' → ' before'

### 64:128
- n=2 meanΔ=0.427 ' the' ' other' ' side' ' of' → ' the'
- n=1 meanΔ=1.480 ' stuck' ' out' ' of' ' the' → ' window'
- n=1 meanΔ=6.685 ' this' ' kind' ' of' ' thing' → ' before'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
