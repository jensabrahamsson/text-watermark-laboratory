# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=252 seen=28824 unseen=61305

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.6524 | -4.2739 | 2048 | 352 |
| 4:16 | 0.5618 | -3.3568 | 4012 | 5588 |
| 16:32 | 0.5335 | -3.3230 | 4987 | 7813 |
| 32:64 | 0.3123 | -3.3011 | 9627 | 15973 |
| 64:128 | 0.3452 | -3.7625 | 8150 | 31579 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=116 meanΔ=0.044 '\n\n' → '\n\n'
- n=116 meanΔ=0.021 '\n\n' '\n\n' → '\n\n'
- n=116 meanΔ=0.014 '\n\n' '\n\n' '\n\n' → '\n\n'
- n=84 meanΔ=1.952 '\n\n' '\n' → '"'
- n=80 meanΔ=1.779 '\n' → '"'
- n=56 meanΔ=1.909 '\n' '\n' → '"'
- n=36 meanΔ=1.853 '\n\n' '\n' '"' → 'This'
- n=32 meanΔ=1.472 '\n\n' '\n' '"' → 'It'

### 4:16
- n=1392 meanΔ=0.010 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=88 meanΔ=4.877 '\n' '"' 'This' ' is' → ' not'
- n=84 meanΔ=1.502 '"' 'This' ' is' ' not' → ' a'
- n=72 meanΔ=3.346 ' is' ' not' ' a' ' joke' → '.'
- n=68 meanΔ=14.098 'This' ' is' ' not' ' a' → ' joke'
- n=48 meanΔ=4.382 ' not' ' a' ' joke' '.' → ' This'
- n=40 meanΔ=12.255 '\n' '"' 'It' "'s" → ' difficult'
- n=40 meanΔ=4.595 '"' 'It' "'s" ' difficult' → ' to'

### 16:32
- n=1856 meanΔ=0.010 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=92 meanΔ=3.345 ' is' ' not' ' a' ' joke' → '.'
- n=84 meanΔ=1.625 '.' ' This' ' is' ' not' → ' a'
- n=80 meanΔ=0.627 ' she' ' said' '.' '\n' → '"'
- n=72 meanΔ=14.090 ' This' ' is' ' not' ' a' → ' joke'
- n=72 meanΔ=4.564 ' joke' '.' ' This' ' is' → ' not'
- n=72 meanΔ=3.310 ' you' ' know' ',' ' you' → ' know'
- n=72 meanΔ=0.748 ',"' ' she' ' said' '.' → '\n'

### 32:64
- n=3712 meanΔ=0.010 '\n\n' '\n\n' '\n\n' '\n\n' → '\n\n'
- n=224 meanΔ=3.346 ' is' ' not' ' a' ' joke' → '.'
- n=176 meanΔ=4.544 ',' ' you' ' know' ',' → ' you'
- n=168 meanΔ=1.223 ' know' ',' ' you' ' know' → ','
- n=168 meanΔ=3.163 ' you' ' know' ',' ' you' → ' know'
- n=144 meanΔ=4.382 ' not' ' a' ' joke' '.' → ' This'
- n=140 meanΔ=1.625 '.' ' This' ' is' ' not' → ' a'
- n=124 meanΔ=1.257 ' a' ' joke' '.' ' This' → ' is'

### 64:128
- n=408 meanΔ=3.345 ' is' ' not' ' a' ' joke' → '.'
- n=344 meanΔ=1.223 ' know' ',' ' you' ' know' → ','
- n=344 meanΔ=3.176 ' you' ' know' ',' ' you' → ' know'
- n=336 meanΔ=4.544 ',' ' you' ' know' ',' → ' you'
- n=308 meanΔ=1.625 '.' ' This' ' is' ' not' → ' a'
- n=264 meanΔ=4.564 ' joke' '.' ' This' ' is' → ' not'
- n=260 meanΔ=14.090 ' This' ' is' ' not' ' a' → ' joke'
- n=260 meanΔ=1.256 ' a' ' joke' '.' ' This' → ' is'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
