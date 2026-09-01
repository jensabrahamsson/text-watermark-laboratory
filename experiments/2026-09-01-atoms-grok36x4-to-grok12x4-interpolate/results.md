# Interpolate atoms

Interpolate last-4 atoms from frozen count tables. unseen_next means the observed next token is absent from both marked and unmarked buckets (Witten–Bell backoff). Not keys, not a new probe method, not a universal detector.

used_keys=False n_rows=96 marked_lr>0=39

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 2.5180 | -0.1811 | 119 | 169 |
| 4:16 | 0.5596 | -0.0266 | 87 | 1065 |
| 16:32 | 0.2935 | -0.1794 | 45 | 1491 |
| 32:64 | 0.0798 | -0.0879 | 100 | 2972 |
| 64:128 | 0.1354 | -0.0386 | 183 | 5955 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=19 meanΔ=2.596 'The' → ' car'
- n=6 meanΔ=6.493 'The' → ' coach'
- n=4 meanΔ=6.683 'The' → ' bus'
- n=4 meanΔ=6.772 'The' ' bus' → ' came'
- n=4 meanΔ=1.708 'The' ' bus' ' came' → ' to'
- n=4 meanΔ=10.905 'The' ' car' → 'park'
- n=4 meanΔ=4.017 'The' ' car' 'park' → ' was'
- n=3 meanΔ=0.566 '***' → '\n'

### 4:16
- n=4 meanΔ=4.801 ' car' 'park' ' was' ' empty' → ' and'
- n=4 meanΔ=5.739 'The' ' bus' ' came' ' to' → ' stop'
- n=4 meanΔ=5.369 'The' ' car' 'park' ' was' → ' empty'
- n=4 meanΔ=2.188 'park' ' was' ' empty' ' and' → ' I'
- n=3 meanΔ=2.690 ' and' ' I' ' left' '.' → ' It'
- n=3 meanΔ=13.079 ' and' ' the' ' car' ' is' → ' slow'
- n=3 meanΔ=7.425 ' bus' ' came' ' to' ' stop' → ' after'
- n=3 meanΔ=5.887 ' came' ' to' ' stop' ' after' → ' about'

### 16:32
- n=1 meanΔ=0.353 '\n' '\n' '"' 'I' → ' am'
- n=1 meanΔ=2.917 '\n' '\n' 'I' ' turned' → ' my'
- n=1 meanΔ=2.132 '\n' '"' 'I' ' am' → ' a'
- n=1 meanΔ=10.390 '\n' 'I' ' turned' ' my' → ' head'
- n=1 meanΔ=5.652 ' "' 'I' "'m" ' sorry' → ','
- n=1 meanΔ=5.581 ' I' ' got' ' out' ' and' → ' went'
- n=1 meanΔ=3.940 ' I' ' told' ' him' ' that' → ' I'
- n=1 meanΔ=1.820 ' I' ' went' ' back' ' to' → ' the'

### 32:64
- n=2 meanΔ=0.353 '\n' '\n' '"' 'I' → ' am'
- n=2 meanΔ=2.917 '\n' '\n' 'I' ' turned' → ' my'
- n=2 meanΔ=3.660 ' He' ' had' ' been' ' in' → ' a'
- n=2 meanΔ=1.775 '.' '\n' '\n' '"' → 'I'
- n=2 meanΔ=10.306 '.' '\n' '\n' 'I' → ' turned'
- n=2 meanΔ=1.994 '.' ' He' ' had' ' been' → ' in'
- n=1 meanΔ=1.430 '\n' '\n' 'I' ' had' → ' not'
- n=1 meanΔ=8.876 '\n' '\n' 'My' ' last' → ' thought'

### 64:128
- n=5 meanΔ=1.775 '.' '\n' '\n' '"' → 'I'
- n=4 meanΔ=10.390 '\n' 'I' ' turned' ' my' → ' head'
- n=3 meanΔ=0.353 '\n' '\n' '"' 'I' → ' am'
- n=3 meanΔ=2.917 '\n' '\n' 'I' ' turned' → ' my'
- n=3 meanΔ=5.518 ' I' ' did' ' not' ' know' → ' where'
- n=3 meanΔ=3.558 ' did' ' not' ' know' ' where' → ' to'
- n=3 meanΔ=10.306 '.' '\n' '\n' 'I' → ' turned'
- n=3 meanΔ=1.830 '.' ' I' ' did' ' not' → ' know'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
