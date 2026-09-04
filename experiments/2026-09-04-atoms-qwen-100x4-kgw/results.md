# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=346 seen=4858 unseen=96740

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.6206 | -0.2890 | 1319 | 1081 |
| 4:16 | 0.2955 | -0.1847 | 902 | 8698 |
| 16:32 | 0.3981 | -0.2595 | 561 | 12239 |
| 32:64 | 0.3345 | -0.1700 | 743 | 24857 |
| 64:128 | 0.2552 | -0.1681 | 1333 | 49865 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=25 meanΔ=0.884 'A' '.' → ' �'
- n=23 meanΔ=0.921 'It' ' was' → ' a'
- n=13 meanΔ=0.229 'There' → ' was'
- n=12 meanΔ=1.429 'It' → ' wasn'
- n=12 meanΔ=0.658 'There' ' was' → ' a'
- n=11 meanΔ=0.455 'It' ' wasn' → '’t'
- n=9 meanΔ=1.564 'It' ' was' → ' an'
- n=6 meanΔ=3.662 'A' '.' → ' s'

### 4:16
- n=24 meanΔ=0.433 '\n' 'B' '.' ' �' → '�'
- n=18 meanΔ=0.706 ' �' '�' '确' '\n' → 'B'
- n=18 meanΔ=0.706 ' �' '�' '误' '\n' → '答案'
- n=18 meanΔ=0.024 '确' '\n' 'B' '.' → ' �'
- n=9 meanΔ=0.159 '�' '误' '\n' '答案' → ':'
- n=7 meanΔ=0.157 '误' '\n' '答案' ':\n\n' → 'A'
- n=5 meanΔ=0.020 'B' '.' ' �' '�' → '误'
- n=5 meanΔ=0.125 '�' '误' '\n' '答案' → ':\n\n'

### 16:32
- n=4 meanΔ=4.907 '答案' ':' ' A' '\n\n' → '《'
- n=4 meanΔ=5.039 '答案' ':\n\n' 'A' '\n\n' → '对'
- n=3 meanΔ=0.001 '\n' '答案' ':' ' B' → '\n\n'
- n=3 meanΔ=0.694 ',' ' but' ' there' ' was' → ' an'
- n=2 meanΔ=14.337 '\n' 'S' '.' ' in' → 'ce'
- n=2 meanΔ=2.166 '\n\n' '1' '9' '8' → '2'
- n=2 meanΔ=9.863 '\n\n' '《' '中共中央' '关于' → '党的'
- n=2 meanΔ=0.405 '\n\n' '《' '中国' '共产党' → '纪律'

### 32:64
- n=7 meanΔ=1.076 '\n' 'B' '.' ' �' → '�'
- n=5 meanΔ=0.720 ' �' '�' '确' '\n' → 'B'
- n=5 meanΔ=0.720 ' �' '�' '误' '\n' → '答案'
- n=5 meanΔ=0.023 '确' '\n' 'B' '.' → ' �'
- n=4 meanΔ=5.885 '。\n' 'A' '.' ' �' → '�'
- n=3 meanΔ=3.046 '.\n' 'That' "'s" ' why' → ' we'
- n=3 meanΔ=0.022 'B' '.' ' �' '�' → '误'
- n=3 meanΔ=0.448 '____' '。\n' 'A' '.' → ' �'

### 64:128
- n=11 meanΔ=3.165 '\n' 'B' '.' ' �' → '�'
- n=7 meanΔ=0.000 '\n' '答案' ':' ' B' → '\n\n'
- n=5 meanΔ=0.739 ' �' '�' '确' '\n' → 'B'
- n=5 meanΔ=0.739 ' �' '�' '误' '\n' → '答案'
- n=5 meanΔ=0.026 '确' '\n' 'B' '.' → ' �'
- n=4 meanΔ=0.088 '\n' '答案' ':' ' C' → '\n\n'
- n=4 meanΔ=0.030 ' on' ' the' ' other' ' side' → ' of'
- n=4 meanΔ=3.452 '.\n' 'It' ' wasn' "'t" → ' until'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
