# Interpolate atoms

Interpolate last-4 atoms from frozen count tables. unseen_next means the observed next token is absent from both marked and unmarked buckets (Witten–Bell backoff). Not keys, not a new probe method, not a universal detector.

used_keys=False n_rows=96 marked_lr>0=27

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | -0.0165 | -0.3967 | 81 | 207 |
| 4:16 | -0.0962 | 0.0032 | 16 | 1136 |
| 16:32 | 0.0403 | -0.0016 | 28 | 1508 |
| 32:64 | 0.0845 | -0.1144 | 87 | 2985 |
| 64:128 | 0.0557 | -0.0859 | 214 | 5924 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=19 meanΔ=2.720 'The' → ' car'
- n=2 meanΔ=2.881 'The' → ' school'
- n=1 meanΔ=2.063 'The' → ' door'
- n=1 meanΔ=3.435 'The' → ' street'
- n=1 meanΔ=3.019 'There' ' was' → ' one'

### 4:16
- n=1 meanΔ=5.964 '\n' '\n' 'For' ' the' → ' past'
- n=1 meanΔ=6.172 '\n' '\n' 'In' ' the' → ' same'
- n=1 meanΔ=10.336 '\n' 'For' ' the' ' past' → ' six'
- n=1 meanΔ=0.252 ' It' ' was' ' the' ' first' → ' time'
- n=1 meanΔ=1.953 ' is' ' the' ' first' ' time' → ' I'
- n=1 meanΔ=0.135 '.' ' It' ' was' ' the' → ' first'
- n=1 meanΔ=9.470 'For' ' the' ' past' ' six' → ' months'

### 16:32
- n=1 meanΔ=2.132 '\n' '\n' '"' 'I' → ' am'
- n=1 meanΔ=0.094 '\n' '\n' 'I' ' turned' → ' my'
- n=1 meanΔ=6.736 '\n' 'I' ' turned' ' my' → ' head'
- n=1 meanΔ=1.869 ' "' 'I' "'m" ' sorry' → ','
- n=1 meanΔ=10.108 ' He' ' had' ' a' ' big' → ' smile'
- n=1 meanΔ=7.175 ' been' ' on' ' the' ' road' → ' for'
- n=1 meanΔ=11.542 ' city' ' of' ' S' 'alf' → 'ord'
- n=1 meanΔ=3.861 ' had' ' been' ' on' ' the' → ' road'

### 32:64
- n=2 meanΔ=2.132 '\n' '\n' '"' 'I' → ' am'
- n=2 meanΔ=0.094 '\n' '\n' 'I' ' turned' → ' my'
- n=2 meanΔ=1.063 '.' '\n' '\n' '"' → 'I'
- n=2 meanΔ=1.348 '.' '\n' '\n' 'I' → ' turned'
- n=2 meanΔ=1.592 '.' '\n' '\n' 'When' → ' the'
- n=1 meanΔ=2.577 '\n' '\n' 'I' ' had' → ' not'
- n=1 meanΔ=6.420 '\n' '\n' 'The' ' sun' → ' had'
- n=1 meanΔ=6.736 '\n' 'I' ' turned' ' my' → ' head'

### 64:128
- n=5 meanΔ=1.063 '.' '\n' '\n' '"' → 'I'
- n=4 meanΔ=6.736 '\n' 'I' ' turned' ' my' → ' head'
- n=3 meanΔ=2.132 '\n' '\n' '"' 'I' → ' am'
- n=3 meanΔ=2.004 '\n' '\n' '"' 'I' → ' was'
- n=3 meanΔ=0.094 '\n' '\n' 'I' ' turned' → ' my'
- n=3 meanΔ=1.348 '.' '\n' '\n' 'I' → ' turned'
- n=2 meanΔ=3.656 ' he' ' was' ' going' ' to' → ' the'
- n=2 meanΔ=0.649 '.' '\n' '\n' 'I' → ' had'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
