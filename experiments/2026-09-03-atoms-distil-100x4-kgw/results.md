# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=346 seen=16170 unseen=71541

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.0638 | -0.5443 | 1800 | 600 |
| 4:16 | 0.1246 | -0.4780 | 2700 | 6900 |
| 16:32 | 0.1392 | -0.4246 | 3487 | 9313 |
| 32:64 | 0.1451 | -0.4269 | 7103 | 18497 |
| 64:128 | 0.2625 | -0.5024 | 1080 | 36231 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=172 meanΔ=0.036 '\n\n' → '\n\n'
- n=157 meanΔ=0.011 '\n\n' '\n\n' → '\n\n'
- n=152 meanΔ=0.008 '\n\n' '\n\n' '\n\n' → '\n\n'
- n=31 meanΔ=0.031 '\n\n' '\n' → '\n'
- n=16 meanΔ=0.374 '\n' → '\n'
- n=11 meanΔ=0.096 '�' → '�'
- n=10 meanΔ=2.478 '\n\n' '\n' → 'He'
- n=5 meanΔ=0.627 '\n\n' '\n' → 'At'

### 4:16
- n=1768 meanΔ=0.004 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=2 meanΔ=1.708 '\n\n' '\n' '\n' 'It' → ' was'
- n=2 meanΔ=0.364 '\n\n' '\n' '\n' '�' → '�'
- n=2 meanΔ=4.354 '\n\n' '\n\n' '\n' '\n' → 'He'
- n=2 meanΔ=1.041 '\n\n' '\n\n' '\n\n' '\n' → 'It'
- n=2 meanΔ=0.016 ',' ' and' ' it' ' didn' → "'t"
- n=2 meanΔ=1.170 ',' ' the' ' man' ' on' → ' the'
- n=2 meanΔ=1.327 'It' ' would' ' have' ' been' → ' a'

### 16:32
- n=2323 meanΔ=0.004 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=2 meanΔ=3.521 '\n\n' '\n\n' '\n' 'The' → ' city'
- n=2 meanΔ=2.489 ' 2' ' a' '.' 'm' → '.,'
- n=2 meanΔ=0.040 '.' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=2 meanΔ=1.150 '.' ' If' ' you' "'re" → ' not'
- n=1 meanΔ=4.469 '\n' '\n' 'He' ' was' → ' found'
- n=1 meanΔ=9.049 '\n\n' '\n' '\n' 'Follow' → ' @'
- n=1 meanΔ=1.717 '\n\n' '\n' '\n' 'It' → ' was'

### 32:64
- n=4669 meanΔ=0.004 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=3 meanΔ=1.138 ' and' ' said' ',' ' "' → 'I'
- n=2 meanΔ=7.294 '\n' 'And' ' there' ' was' → ' one'
- n=2 meanΔ=0.012 '\n' 'He' ' added' ':' → ' "'
- n=2 meanΔ=0.667 '\n' 'He' ' said' ':' → ' "'
- n=2 meanΔ=0.480 '\n\n' '\n\n' '\n\n' '\n' → 'I'
- n=2 meanΔ=8.125 ' He' ' looked' ' at' ' me' → ' with'
- n=2 meanΔ=1.898 ' and' ' it' "'s" ' the' → ' first'

### 64:128
- n=97 meanΔ=0.005 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=10 meanΔ=3.036 ',' ' and' ' I' ' said' → ','
- n=6 meanΔ=5.445 '.' ' I' ' mean' ',' → ' I'
- n=4 meanΔ=3.019 ' I' ' knew' ' he' ' was' → ' going'
- n=4 meanΔ=3.901 ' The' ' next' ' day' ',' → ' the'
- n=4 meanΔ=0.398 ',"' ' he' ' said' '.' → '\n'
- n=3 meanΔ=4.282 ' I' ' mean' ',' ' I' → '�'
- n=3 meanΔ=2.028 ',' ' and' ' he' ' said' → ','

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
