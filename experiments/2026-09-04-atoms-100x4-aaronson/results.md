# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=208 seen=25167 unseen=76418

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.7414 | -5.4921 | 1977 | 423 |
| 4:16 | 1.2541 | -3.5979 | 2769 | 6831 |
| 16:32 | 0.9123 | -3.6477 | 3212 | 9588 |
| 32:64 | 0.6055 | -3.6522 | 5899 | 19701 |
| 64:128 | 0.6066 | -3.6415 | 11310 | 39875 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=392 meanΔ=1.120 '\n' → '"'
- n=228 meanΔ=2.874 '\n' '"' → 'This'
- n=228 meanΔ=0.998 '\n' '"' 'This' → ' is'
- n=56 meanΔ=1.024 '\n' '"' 'It' → "'s"
- n=48 meanΔ=2.085 '\n' '"' → 'She'
- n=20 meanΔ=8.196 '\n' '"' 'She' → ' started'
- n=16 meanΔ=11.062 '\n' '"' → 'God'
- n=16 meanΔ=2.549 '\n' '"' → 'Wait'

### 4:16
- n=136 meanΔ=2.080 ' a' ' joke' '.' ' This' → ' is'
- n=136 meanΔ=4.887 ' is' ' not' ' a' ' joke' → '.'
- n=136 meanΔ=4.423 ' not' ' a' ' joke' '.' → ' This'
- n=128 meanΔ=6.292 '\n' '"' 'This' ' is' → ' not'
- n=96 meanΔ=2.515 '"' 'This' ' is' ' not' → ' a'
- n=84 meanΔ=13.832 '"' 'This' ' is' ' like' → ' having'
- n=80 meanΔ=7.643 'This' ' is' ' like' ' having' → ' your'
- n=68 meanΔ=7.292 ' This' ' is' ' not' ' a' → ' joke'

### 16:32
- n=196 meanΔ=4.891 ' is' ' not' ' a' ' joke' → '.'
- n=196 meanΔ=4.698 ' joke' '.' ' This' ' is' → ' not'
- n=196 meanΔ=2.800 '.' ' This' ' is' ' not' → ' a'
- n=192 meanΔ=7.231 ' This' ' is' ' not' ' a' → ' joke'
- n=128 meanΔ=2.080 ' a' ' joke' '.' ' This' → ' is'
- n=128 meanΔ=4.422 ' not' ' a' ' joke' '.' → ' This'
- n=76 meanΔ=0.852 '\n' '\n' '"' 'This' → ' is'
- n=68 meanΔ=1.091 ' said' '.' '\n' '\n' → '"'

### 32:64
- n=272 meanΔ=4.887 ' is' ' not' ' a' ' joke' → '.'
- n=256 meanΔ=0.850 '\n' '\n' '"' 'This' → ' is'
- n=224 meanΔ=7.226 ' This' ' is' ' not' ' a' → ' joke'
- n=224 meanΔ=2.803 '.' ' This' ' is' ' not' → ' a'
- n=220 meanΔ=2.079 ' a' ' joke' '.' ' This' → ' is'
- n=220 meanΔ=4.696 ' joke' '.' ' This' ' is' → ' not'
- n=220 meanΔ=4.419 ' not' ' a' ' joke' '.' → ' This'
- n=216 meanΔ=2.816 '.' '\n' '\n' '"' → 'This'

### 64:128
- n=640 meanΔ=0.845 '\n' '\n' '"' 'This' → ' is'
- n=592 meanΔ=6.302 '\n' '"' 'This' ' is' → ' not'
- n=580 meanΔ=2.817 '.' '\n' '\n' '"' → 'This'
- n=536 meanΔ=4.889 ' is' ' not' ' a' ' joke' → '.'
- n=464 meanΔ=2.512 '"' 'This' ' is' ' not' → ' a'
- n=408 meanΔ=1.280 ' joke' '.' '\n' '\n' → '"'
- n=404 meanΔ=0.012 ' a' ' joke' '.' '\n' → '\n'
- n=404 meanΔ=0.079 ' not' ' a' ' joke' '.' → '\n'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
