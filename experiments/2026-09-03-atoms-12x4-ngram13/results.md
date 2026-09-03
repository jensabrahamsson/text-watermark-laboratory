# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=20 seen=160 unseen=12026

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.7144 | 0.0091 | 71 | 217 |
| 4:16 | 0.0472 | -0.2151 | 10 | 1142 |
| 16:32 | -0.0487 | -0.0809 | 17 | 1519 |
| 32:64 | -0.0640 | -0.0231 | 16 | 3056 |
| 64:128 | -0.0910 | -0.0637 | 46 | 6092 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=15 meanΔ=2.306 'The' → ' bus'
- n=8 meanΔ=2.088 'The' ' bus' → ' drivers'
- n=6 meanΔ=5.079 'The' → ' house'
- n=3 meanΔ=5.771 'The' ' bus' ' drivers' → ' are'
- n=3 meanΔ=6.999 'The' ' bus' ' drivers' → ' stopped'
- n=2 meanΔ=3.397 'The' → ' other'
- n=2 meanΔ=3.544 'The' → ' paper'
- n=1 meanΔ=1.707 'The' ' other' → ' day'

### 4:16
- n=2 meanΔ=7.601 ' bus' ' drivers' ' are' ' now' → ' back'
- n=2 meanΔ=5.895 ' drivers' ' are' ' now' ' back' → ' on'
- n=2 meanΔ=2.665 'The' ' bus' ' drivers' ' are' → ' now'
- n=2 meanΔ=6.669 'The' ' bus' ' drivers' ' stopped' → ' over'
- n=1 meanΔ=9.930 ':' '\n' '\n' '"' → 'My'

### 16:32
- n=1 meanΔ=0.065 ' I' ' left' '.' '\n' → '\n'
- n=1 meanΔ=1.106 ' left' '.' '\n' '\n' → 'I'
- n=1 meanΔ=6.412 ' roof' ' are' ' the' ' same' → ' as'

### 32:64
- n=1 meanΔ=6.355 ' roof' ' are' ' the' ' same' → ' as'
- n=1 meanΔ=0.974 ',' ' and' ' I' ' am' → ' not'
- n=1 meanΔ=7.129 '.' '\n' '\n' 'The' → ' bus'
- n=1 meanΔ=1.924 '.' ' I' ' knew' ' she' → ' was'

### 64:128
- n=2 meanΔ=6.213 '.' '\n' '\n' 'The' → ' other'
- n=2 meanΔ=1.937 '.' ' I' ' don' "'t" → ' know'
- n=1 meanΔ=0.065 ' I' ' left' '.' '\n' → '\n'
- n=1 meanΔ=0.937 ' left' '.' '\n' '\n' → 'I'
- n=1 meanΔ=1.170 ',' ' and' ' I' ' am' → ' not'
- n=1 meanΔ=1.910 '.' ' I' ' knew' ' she' → ' was'
- n=1 meanΔ=9.155 ':' '\n' '\n' '"' → 'My'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
