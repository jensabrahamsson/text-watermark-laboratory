# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=14 seen=65 unseen=12127

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | -0.0447 | 0.1588 | 41 | 247 |
| 4:16 | -0.2607 | 0.0623 | 2 | 1150 |
| 16:32 | -0.1508 | -0.1834 | 1 | 1535 |
| 32:64 | -0.0578 | 0.0403 | 5 | 3067 |
| 64:128 | -0.0956 | -0.0422 | 16 | 6128 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=12 meanΔ=2.022 'The' → ' day'
- n=7 meanΔ=6.577 'The' ' day' → ' before'
- n=4 meanΔ=4.220 'The' ' day' → ' was'

### 32:64
- n=1 meanΔ=10.836 ' and' ' emotions' ' that' ' are' → ' common'

### 64:128
- n=2 meanΔ=3.513 ' side' ' of' ' the' ' road' → '.'
- n=2 meanΔ=10.981 ' the' ' side' ' of' ' the' → ' road'
- n=1 meanΔ=10.868 ' and' ' emotions' ' that' ' are' → ' common'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
