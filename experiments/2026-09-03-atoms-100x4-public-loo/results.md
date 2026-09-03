# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=352 seen=10158 unseen=91353

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.7556 | -0.5096 | 1633 | 767 |
| 4:16 | 1.6043 | -0.1128 | 2086 | 7514 |
| 16:32 | 0.4546 | -0.1231 | 1239 | 11561 |
| 32:64 | 0.2558 | -0.0990 | 1899 | 23701 |
| 64:128 | 0.1741 | -0.1078 | 3301 | 47810 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=235 meanΔ=2.579 '"' → 'This'
- n=223 meanΔ=0.448 '"' 'This' → ' is'
- n=101 meanΔ=0.424 '"' 'This' ' is' → ' the'
- n=69 meanΔ=4.929 '"' 'This' ' is' → ' just'
- n=66 meanΔ=0.818 '"' → 'I'
- n=39 meanΔ=2.620 '"' → 'Then'
- n=34 meanΔ=2.463 '"' → 'Who'
- n=21 meanΔ=0.552 '"' 'Who' → ' is'

### 4:16
- n=39 meanΔ=7.093 '"' 'This' ' is' ' the' → ' scene'
- n=39 meanΔ=7.903 'This' ' is' ' the' ' scene' → ' we'
- n=36 meanΔ=3.688 ' is' ' the' ' scene' ' we' → ' had'
- n=31 meanΔ=12.421 '"' 'This' ' is' ' just' → ' sad'
- n=31 meanΔ=5.472 'This' ' is' ' just' ' sad' → ',"'
- n=24 meanΔ=7.966 ' the' ' scene' ' we' ' had' → ' all'
- n=23 meanΔ=1.057 ' had' ' all' ' been' ' waiting' → ' for'
- n=23 meanΔ=6.844 ' scene' ' we' ' had' ' all' → ' been'

### 16:32
- n=48 meanΔ=1.028 ' said' '.' '\n' '\n' → 'The'
- n=25 meanΔ=1.064 '.' '\n' '\n' '"' → 'I'
- n=19 meanΔ=0.000 ' she' ' said' '.' '\n' → '\n'
- n=17 meanΔ=2.101 '\n' '\n' '"' 'I' → ' am'
- n=14 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=14 meanΔ=0.762 ',"' ' she' ' said' '.' → '\n'
- n=13 meanΔ=1.990 '\n' '\n' '"' 'I' → ' was'
- n=12 meanΔ=0.861 ',"' ' he' ' said' '.' → '\n'

### 32:64
- n=64 meanΔ=1.060 '.' '\n' '\n' '"' → 'I'
- n=41 meanΔ=1.992 '\n' '\n' '"' 'I' → ' was'
- n=22 meanΔ=2.107 '\n' '\n' '"' 'I' → ' am'
- n=19 meanΔ=8.530 '\n' '"' 'I' ' was' → ' pretty'
- n=15 meanΔ=1.022 ' said' '.' '\n' '\n' → 'The'
- n=12 meanΔ=0.932 '.' '\n' '\n' '"' → 'We'
- n=10 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=9 meanΔ=0.871 ',"' ' he' ' said' '.' → '\n'

### 64:128
- n=76 meanΔ=1.060 '.' '\n' '\n' '"' → 'I'
- n=50 meanΔ=1.989 '\n' '\n' '"' 'I' → ' was'
- n=38 meanΔ=1.023 ' said' '.' '\n' '\n' → 'The'
- n=30 meanΔ=0.934 '.' '\n' '\n' '"' → 'We'
- n=23 meanΔ=8.535 '\n' '"' 'I' ' was' → ' pretty'
- n=23 meanΔ=1.489 '."' '\n' '\n' '"' → 'I'
- n=19 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=16 meanΔ=0.867 ',"' ' he' ' said' '.' → '\n'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
