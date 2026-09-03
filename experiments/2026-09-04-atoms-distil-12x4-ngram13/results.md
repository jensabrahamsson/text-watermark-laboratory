# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=21 seen=175 unseen=11994

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.3642 | -0.2118 | 111 | 177 |
| 4:16 | 0.2335 | -0.0872 | 33 | 1119 |
| 16:32 | 0.0314 | -0.0755 | 4 | 1532 |
| 32:64 | -0.0899 | -0.0453 | 12 | 3060 |
| 64:128 | -0.0400 | -0.0637 | 15 | 6106 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=9 meanΔ=0.823 'The' → ' man'
- n=9 meanΔ=3.370 'The' ' man' → ' with'
- n=8 meanΔ=0.126 '\n' → 'The'
- n=8 meanΔ=2.810 'The' ' man' ' with' → ' the'
- n=4 meanΔ=1.856 '\n\n' '\n' → '\n'
- n=4 meanΔ=1.567 'I' → ' would'
- n=4 meanΔ=6.047 'The' → ' bus'
- n=3 meanΔ=2.714 'I' → ' didn'

### 4:16
- n=7 meanΔ=10.844 'The' ' man' ' with' ' the' → ' keys'
- n=5 meanΔ=3.204 ' man' ' with' ' the' ' keys' → ' of'
- n=5 meanΔ=11.019 ' the' ' keys' ' of' ' the' → ' van'
- n=5 meanΔ=1.410 ' with' ' the' ' keys' ' of' → ' the'
- n=3 meanΔ=3.599 ' didn' "'t" ' know' ' what' → ' I'
- n=3 meanΔ=3.260 "'t" ' know' ' what' ' I' → ' was'
- n=3 meanΔ=2.266 'I' ' didn' "'t" ' know' → ' what'

### 16:32
- n=2 meanΔ=2.587 ' of' ' the' ' house' '.' → ' I'

### 32:64
- n=1 meanΔ=1.405 ' I' ' didn' "'t" ' have' → ' a'
- n=1 meanΔ=1.867 ' The' ' only' ' time' ' I' → ' had'
- n=1 meanΔ=1.646 '.' ' The' ' only' ' time' → ' I'

### 64:128
- n=1 meanΔ=2.070 ' I' ' didn' "'t" ' have' → ' a'
- n=1 meanΔ=3.313 ' The' ' only' ' time' ' I' → ' had'
- n=1 meanΔ=1.764 '.' ' The' ' only' ' time' → ' I'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
