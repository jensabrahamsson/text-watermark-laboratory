# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=24 seen=269 unseen=11912

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.0967 | -0.2204 | 84 | 204 |
| 4:16 | 0.2303 | -0.0601 | 32 | 1120 |
| 16:32 | -0.0118 | -0.0613 | 33 | 1503 |
| 32:64 | -0.0383 | 0.0106 | 26 | 3046 |
| 64:128 | -0.0651 | 0.0132 | 94 | 6039 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=9 meanΔ=1.748 '"' → 'This'
- n=9 meanΔ=2.217 '"' 'This' → ' is'
- n=8 meanΔ=6.401 'The' → ' ferry'
- n=8 meanΔ=4.778 'The' ' ferry' → ' was'
- n=5 meanΔ=2.761 '"' 'This' ' is' → ' the'
- n=4 meanΔ=7.208 '"' → 'Oh'
- n=4 meanΔ=3.467 '"' 'Oh' → ','
- n=4 meanΔ=5.010 '"' 'Oh' ',' → ' my'

### 4:16
- n=4 meanΔ=10.861 '"' 'Oh' ',' ' my' → ' God'
- n=4 meanΔ=6.205 'Oh' ',' ' my' ' God' → ',"'
- n=3 meanΔ=3.572 ' God' ',"' ' I' ' muttered' → ','
- n=3 meanΔ=4.248 ' I' ' muttered' ',' ' and' → ' then'
- n=3 meanΔ=11.106 ' my' ' God' ',"' ' I' → ' muttered'
- n=3 meanΔ=2.009 ',' ' my' ' God' ',"' → ' I'
- n=3 meanΔ=2.147 ',"' ' I' ' muttered' ',' → ' and'
- n=2 meanΔ=1.374 ' muttered' ',' ' and' ' then' → ' the'

### 16:32
- n=2 meanΔ=7.842 '\n' '\n' 'I' ' turned' → ' my'
- n=2 meanΔ=4.234 '\n' 'I' ' turned' ' my' → ' head'
- n=2 meanΔ=1.115 '.' '\n' '\n' 'I' → ' turned'
- n=2 meanΔ=10.101 '."' '\n' '\n' 'He' → ' turned'
- n=1 meanΔ=4.868 '\n' '\n' '"' 'I' → ' was'
- n=1 meanΔ=1.223 '\n' '\n' 'He' ' turned' → ' to'
- n=1 meanΔ=5.128 '\n' '\n' 'The' ' door' → ' of'
- n=1 meanΔ=7.395 '\n' '"' 'I' ' was' → ' working'

### 32:64
- n=1 meanΔ=7.842 '\n' '\n' 'I' ' turned' → ' my'
- n=1 meanΔ=5.245 '\n' '\n' 'The' ' door' → ' of'
- n=1 meanΔ=1.377 '\n' 'The' ' door' ' of' → ' the'
- n=1 meanΔ=4.356 ' it' '.' '\n' '\n' → 'He'
- n=1 meanΔ=10.858 ' was' ' working' ' on' ' a' → ' project'
- n=1 meanΔ=1.625 '"' 'I' ' was' ' working' → ' on'
- n=1 meanΔ=6.272 ',"' ' I' ' said' '.' → ' "'
- n=1 meanΔ=1.693 '.' '\n' '\n' '"' → 'I'

### 64:128
- n=8 meanΔ=1.723 '.' '\n' '\n' '"' → 'I'
- n=6 meanΔ=4.753 '\n' '\n' '"' 'I' → ' was'
- n=3 meanΔ=3.789 '\n' '"' 'I' ' was' → ' pretty'
- n=3 meanΔ=4.266 '\n' 'I' ' turned' ' my' → ' head'
- n=2 meanΔ=6.815 '\n' '\n' 'I' ' turned' → ' my'
- n=2 meanΔ=10.877 ' I' ' just' ' didn' "'t" → ' care'
- n=2 meanΔ=9.176 ' I' ' said' '.' ' "' → 'Who'
- n=2 meanΔ=2.230 ' for' ' me' '.' ' I' → ' was'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
