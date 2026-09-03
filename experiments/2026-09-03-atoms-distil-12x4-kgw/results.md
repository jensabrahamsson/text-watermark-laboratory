# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=42 seen=130 unseen=11972

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.4560 | -0.6797 | 63 | 225 |
| 4:16 | 0.2846 | -0.4713 | 5 | 1147 |
| 16:32 | 0.2280 | -0.2115 | 7 | 1529 |
| 32:64 | 0.2325 | -0.2101 | 21 | 3051 |
| 64:128 | 0.2750 | -0.2077 | 34 | 6020 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=4 meanΔ=2.045 'I' → ' was'
- n=3 meanΔ=6.335 'They' → ' were'
- n=2 meanΔ=4.306 'I' → ' started'
- n=2 meanΔ=3.348 'I' → ' went'
- n=2 meanΔ=7.243 'It' → ' turns'
- n=2 meanΔ=3.142 'It' ' turns' → ' out'
- n=1 meanΔ=3.851 'And' → ' I'
- n=1 meanΔ=0.139 'I' → ' can'

### 4:16
- n=1 meanΔ=0.665 ' I' ' did' ' not' ' want' → ' to'
- n=1 meanΔ=9.806 '.' ' I' ' did' ' not' → ' want'

### 16:32
- n=1 meanΔ=1.810 ',' ' I' ' wouldn' "'t" → ' have'
- n=1 meanΔ=7.489 '.' ' He' ' said' ' he' → ' could'
- n=1 meanΔ=2.184 '.' ' I' ' am' ' not' → ' a'
- n=1 meanΔ=3.594 '.' ' I' ' wanted' ' to' → ' make'
- n=1 meanΔ=1.518 '.' ' The' ' rest' ' of' → ' the'

### 32:64
- n=2 meanΔ=3.350 ',' ' and' ' it' ' is' → ' not'
- n=2 meanΔ=1.479 '.' ' The' ' rest' ' of' → ' the'
- n=1 meanΔ=0.665 ' I' ' did' ' not' ' want' → ' to'
- n=1 meanΔ=8.789 ' I' ' want' ' to' ' make' → ' money'
- n=1 meanΔ=1.266 ' make' ' money' '.' '\n' → 'I'
- n=1 meanΔ=1.816 ' to' ' make' ' money' '.' → '\n'
- n=1 meanΔ=1.479 ' want' ' to' ' make' ' money' → '.'
- n=1 meanΔ=1.782 ',' ' I' ' wouldn' "'t" → ' have'

### 64:128
- n=4 meanΔ=0.604 ' I' ' did' ' not' ' want' → ' to'
- n=2 meanΔ=2.222 '.' ' I' ' am' ' not' → ' a'
- n=2 meanΔ=8.691 '.' ' I' ' did' ' not' → ' want'
- n=1 meanΔ=8.503 ' I' ' want' ' to' ' make' → ' money'
- n=1 meanΔ=1.374 ' make' ' money' '.' '\n' → 'I'
- n=1 meanΔ=1.813 ' to' ' make' ' money' '.' → '\n'
- n=1 meanΔ=1.469 ' want' ' to' ' make' ' money' → '.'
- n=1 meanΔ=3.234 ',' ' and' ' it' ' is' → ' not'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
