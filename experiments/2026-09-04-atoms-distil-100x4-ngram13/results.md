# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=325 seen=11182 unseen=85493

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.9294 | -0.2683 | 2036 | 364 |
| 4:16 | 1.5879 | -0.0589 | 3161 | 6439 |
| 16:32 | 0.2490 | -0.0301 | 1575 | 11225 |
| 32:64 | 0.0972 | -0.0055 | 2906 | 22694 |
| 64:128 | 0.0647 | -0.0473 | 1504 | 44771 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=238 meanΔ=1.670 '\n\n' → '\n'
- n=223 meanΔ=0.973 '\n\n' '\n' → '\n'
- n=223 meanΔ=4.811 '\n\n' '\n' '\n' → 'It'
- n=103 meanΔ=0.082 '\n' → 'The'
- n=15 meanΔ=0.320 'The' → ' man'
- n=14 meanΔ=1.449 '\n' 'The' → ' water'
- n=13 meanΔ=5.858 '\n' 'The' ' water' → ' had'
- n=13 meanΔ=3.980 'The' ' man' → ' with'

### 4:16
- n=215 meanΔ=5.195 '\n\n' '\n' '\n' 'It' → ' looked'
- n=212 meanΔ=0.296 '\n' '\n' 'It' ' looked' → ' like'
- n=209 meanΔ=3.278 '\n' 'It' ' looked' ' like' → ' a'
- n=149 meanΔ=3.212 'It' ' looked' ' like' ' a' → ' long'
- n=86 meanΔ=4.652 ' a' ' long' ' time' ' ago' → ','
- n=85 meanΔ=1.749 ' like' ' a' ' long' ' time' → ' ago'
- n=85 meanΔ=1.613 ' looked' ' like' ' a' ' long' → ' time'
- n=62 meanΔ=3.334 ' long' ' time' ' ago' ',' → ' but'

### 16:32
- n=16 meanΔ=1.945 '�' '�' '�' '�' → '�'
- n=6 meanΔ=11.460 '-' 'eyed' ' woman' ',' → ' holding'
- n=5 meanΔ=1.788 ' in' ' a' ' time' ' when' → ' the'
- n=4 meanΔ=4.504 ' been' ' caught' ' in' ' the' → ' process'
- n=4 meanΔ=5.303 ' caught' ' in' ' the' ' process' → '.'
- n=4 meanΔ=0.677 ' in' ' the' ' process' '.' → '\n'
- n=4 meanΔ=1.179 ' process' '.' '\n' '\n' → 'The'
- n=4 meanΔ=3.040 ' the' ' process' '.' '\n' → '\n'

### 32:64
- n=32 meanΔ=1.945 '�' '�' '�' '�' → '�'
- n=5 meanΔ=3.428 '�' '�' '\n' '�' → '�'
- n=3 meanΔ=0.006 '.' '\n' 'It' ' wasn' → "'t"
- n=2 meanΔ=1.149 '\n' '\n' 'It' ' was' → ' a'
- n=2 meanΔ=0.082 '\n' '\n' 'One' ' of' → ' the'
- n=2 meanΔ=4.251 '\n' 'It' ' wasn' "'t" → ' until'
- n=2 meanΔ=4.331 '\n' 'The' ' victim' ' told' → ' police'
- n=2 meanΔ=0.336 '\n\n' '\n\n' '\n\n' '\n\n' → '\n'

### 64:128
- n=74 meanΔ=1.898 '�' '�' '�' '�' → '�'
- n=11 meanΔ=0.065 ',"' ' he' ' said' '.' → '\n'
- n=7 meanΔ=3.406 '\n' '�' '�' '�' → '�'
- n=7 meanΔ=0.958 '.' '\n' 'He' ' said' → ' the'
- n=7 meanΔ=3.542 '�' '�' '\n' '�' → '�'
- n=6 meanΔ=6.988 '.' '\n' '�' '�' → '�'
- n=5 meanΔ=0.593 '\n\n' '\n\n' '\n\n' '\n\n' → '\n'
- n=5 meanΔ=0.679 ' he' ' said' '.' '\n' → '"'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
