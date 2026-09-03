# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=267 seen=5878 unseen=95624

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 2.7122 | -0.1131 | 1287 | 1113 |
| 4:16 | 0.6188 | -0.0256 | 840 | 8760 |
| 16:32 | -0.0090 | -0.0720 | 544 | 12256 |
| 32:64 | 0.0172 | -0.0214 | 1099 | 24501 |
| 64:128 | 0.0077 | -0.0133 | 2108 | 48994 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=38 meanΔ=2.635 'The' → ' house'
- n=28 meanΔ=6.734 'The' → ' doctor'
- n=25 meanΔ=2.552 'The' → ' smell'
- n=25 meanΔ=1.230 'The' → ' water'
- n=25 meanΔ=2.034 'The' ' smell' → ' of'
- n=24 meanΔ=8.922 'The' → ' audience'
- n=24 meanΔ=6.569 'The' ' audience' → ' went'
- n=21 meanΔ=1.448 'The' → ' fire'

### 4:16
- n=16 meanΔ=3.110 'The' ' audience' ' went' ' crazy' → '.'
- n=14 meanΔ=2.606 'The' ' water' ' had' ' a' → ' very'
- n=13 meanΔ=4.937 'The' ' doctor' ' examined' ' her' → ' for'
- n=10 meanΔ=3.769 ' It' ' didn' "'t" ' seem' → ' that'
- n=10 meanΔ=2.820 ' audience' ' went' ' crazy' '.' → ' It'
- n=10 meanΔ=0.003 ' crazy' '.' ' It' ' didn' → "'t"
- n=10 meanΔ=3.396 ' fire' ' department' ' was' ' called' → ' to'
- n=10 meanΔ=4.327 ' went' ' crazy' '.' ' It' → ' didn'

### 16:32
- n=5 meanΔ=0.098 '.' '\n' '\n' '"' → 'We'
- n=5 meanΔ=0.382 '.' '\n' '\n' 'He' → ' was'
- n=3 meanΔ=0.567 '\n' '\n' 'The' ' water' → ' was'
- n=3 meanΔ=7.077 ' to' ' the' ' hospital' ',' → ' where'
- n=3 meanΔ=2.801 ' wa' 'ver' ' for' ' long' → '.'
- n=3 meanΔ=8.609 "'t" ' wa' 'ver' ' for' → ' long'
- n=3 meanΔ=0.012 ',' '000' '.' '\n' → '\n'
- n=2 meanΔ=6.565 '\n' '\n' 'He' ' was' → ' released'

### 32:64
- n=7 meanΔ=0.053 '\n' '\n' '"' 'I' → "'m"
- n=5 meanΔ=4.693 '.' '\n' '\n' 'There' → ' were'
- n=4 meanΔ=0.697 '.' '\n' '\n' '"' → 'He'
- n=4 meanΔ=0.515 '.' '\n' '\n' 'It' → "'s"
- n=4 meanΔ=0.841 '.' '\n' '\n' 'When' → ' the'
- n=3 meanΔ=1.099 '\n' '\n' '"' 'Yes' → ',"'
- n=3 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=3 meanΔ=0.000 ' she' ' said' '.' '\n' → '\n'

### 64:128
- n=8 meanΔ=0.288 ',"' ' he' ' said' '.' → '\n'
- n=7 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=7 meanΔ=0.713 '.' '\n' '\n' '"' → 'He'
- n=6 meanΔ=0.044 '.' '\n' '\n' '"' → 'We'
- n=5 meanΔ=4.272 ' law' '-' 'crime' '-' → 'and'
- n=5 meanΔ=0.148 '-' 'crime' '-' 'and' → '-'
- n=5 meanΔ=0.529 '.' '\n' '\n' 'It' → "'s"
- n=4 meanΔ=0.099 '\n' '\n' '"' 'I' → "'m"

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
