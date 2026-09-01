# Interpolate atoms

Interpolate last-4 atoms from frozen count tables. unseen_next means the observed next token is absent from both marked and unmarked buckets (Witten–Bell backoff). Not keys, not a new probe method, not a universal detector.

used_keys=False n_rows=96 marked_lr>0=29

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.4955 | -0.3373 | 69 | 219 |
| 4:16 | 0.1555 | -0.1929 | 35 | 1117 |
| 16:32 | 0.0538 | 0.0753 | 35 | 1501 |
| 32:64 | 0.1458 | -0.0634 | 54 | 3018 |
| 64:128 | 0.0465 | -0.0609 | 137 | 5996 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=4 meanΔ=9.275 'Cl' → 'osing'
- n=4 meanΔ=5.757 'Cl' 'osing' → ' is'
- n=4 meanΔ=1.264 'Cl' 'osing' ' is' → ' the'
- n=4 meanΔ=6.059 'The' → ' dog'
- n=4 meanΔ=8.373 'The' ' dog' → ' gave'
- n=4 meanΔ=2.657 'The' ' dog' ' gave' → ' me'
- n=3 meanΔ=6.683 'The' → ' bus'
- n=2 meanΔ=2.596 'The' → ' car'

### 4:16
- n=4 meanΔ=11.951 ' dog' ' gave' ' me' ' a' → ' warm'
- n=4 meanΔ=12.447 ' is' ' the' ' same' ' as' → ' closing'
- n=4 meanΔ=2.453 'Cl' 'osing' ' is' ' the' → ' same'
- n=4 meanΔ=0.658 'The' ' dog' ' gave' ' me' → ' a'
- n=4 meanΔ=0.110 'osing' ' is' ' the' ' same' → ' as'
- n=1 meanΔ=11.733 '\n' '\n' '"' 'I' → ' haven'
- n=1 meanΔ=5.792 '\n' '"' 'I' ' haven' → "'t"
- n=1 meanΔ=0.017 ' said' '.' '\n' '\n' → 'The'

### 16:32
- n=2 meanΔ=2.917 '\n' '\n' 'I' ' turned' → ' my'
- n=2 meanΔ=10.390 '\n' 'I' ' turned' ' my' → ' head'
- n=2 meanΔ=10.306 '.' '\n' '\n' 'I' → ' turned'
- n=2 meanΔ=5.801 '.' ' I' ' was' ' standing' → ' at'
- n=2 meanΔ=10.344 'I' ' turned' ' my' ' head' → ' toward'
- n=1 meanΔ=0.353 '\n' '\n' '"' 'I' → ' am'
- n=1 meanΔ=5.371 '\n' '\n' 'The' ' door' → ' of'
- n=1 meanΔ=4.638 '\n' '"' 'I' ' am' → ' the'

### 32:64
- n=1 meanΔ=2.917 '\n' '\n' 'I' ' turned' → ' my'
- n=1 meanΔ=5.371 '\n' '\n' 'The' ' door' → ' of'
- n=1 meanΔ=2.497 '\n' 'The' ' door' ' of' → ' the'
- n=1 meanΔ=1.321 ' I' ' don' "'t" ' like' → ' the'
- n=1 meanΔ=3.774 ' I' ' had' ' never' ' imagined' → ' the'
- n=1 meanΔ=1.093 ' a' ' wheelchair' ',' ' as' → ' if'
- n=1 meanΔ=3.374 ' did' ' not' ' stop' '.' → ' It'
- n=1 meanΔ=4.956 ' don' "'t" ' like' ' the' → ' way'

### 64:128
- n=8 meanΔ=1.775 '.' '\n' '\n' '"' → 'I'
- n=3 meanΔ=0.353 '\n' '\n' '"' 'I' → ' am'
- n=3 meanΔ=10.390 '\n' 'I' ' turned' ' my' → ' head'
- n=2 meanΔ=2.917 '\n' '\n' 'I' ' turned' → ' my'
- n=2 meanΔ=0.146 ',"' ' I' ' said' '.' → ' "'
- n=2 meanΔ=10.306 '.' '\n' '\n' 'I' → ' turned'
- n=2 meanΔ=2.720 '."' '\n' '\n' '"' → 'I'
- n=2 meanΔ=4.449 'I' ' turned' ' my' ' head' → ' and'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
