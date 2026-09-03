# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=376 seen=4557 unseen=96991

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.5400 | -0.4935 | 1044 | 1356 |
| 4:16 | 0.3811 | -0.2905 | 254 | 9346 |
| 16:32 | 0.4280 | -0.3038 | 505 | 12295 |
| 32:64 | 0.4248 | -0.3276 | 988 | 24612 |
| 64:128 | 0.4143 | -0.3307 | 1766 | 49382 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=14 meanΔ=0.905 'They' → ' were'
- n=13 meanΔ=0.264 'He' → ' was'
- n=9 meanΔ=1.310 'He' → ' had'
- n=7 meanΔ=2.286 '"' → 'Do'
- n=7 meanΔ=2.205 'The' → ' next'
- n=6 meanΔ=1.014 '"' → 'Oh'
- n=6 meanΔ=0.238 '"' → 'We'
- n=6 meanΔ=1.350 'And' → ' so'

### 4:16
- n=2 meanΔ=1.688 ' front' ' of' ' the' ' building' → ','
- n=2 meanΔ=4.812 ' got' ' up' ' from' ' his' → ' chair'
- n=2 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=2 meanΔ=2.817 ' o' "'" 'clock' ',' → ' the'
- n=2 meanΔ=2.664 ' of' ' the' ' building' ',' → ' and'
- n=2 meanΔ=2.722 ' the' ' building' ',' ' and' → ' we'
- n=2 meanΔ=5.083 ' the' ' front' ' of' ' the' → ' building'
- n=2 meanΔ=2.304 ' turned' ' his' ' attention' ' to' → ' the'

### 16:32
- n=3 meanΔ=2.120 ' and' ' said' ',' ' "' → 'I'
- n=3 meanΔ=3.623 '.' '\n' '\n' 'I' → ' can'
- n=2 meanΔ=0.012 '\n' '\n' 'He' ' didn' → "'t"
- n=2 meanΔ=5.688 '\n' '\n' 'He' ' had' → ' gone'
- n=2 meanΔ=10.809 '\n' '\n' 'He' ' then' → ' returned'
- n=2 meanΔ=2.828 ' He' ' was' ' dressed' ' in' → ' a'
- n=2 meanΔ=2.107 ' on' ' my' ' own' ',' → ' and'
- n=2 meanΔ=1.595 ' there' '.' ' I' ' did' → ' not'

### 32:64
- n=10 meanΔ=0.623 '.' '\n' '\n' 'They' → ' were'
- n=9 meanΔ=0.220 '.' '\n' '\n' 'He' → ' was'
- n=5 meanΔ=0.371 '.' ' I' ' did' ' not' → ' want'
- n=3 meanΔ=0.104 '\n' '\n' 'He' ' added' → ':'
- n=3 meanΔ=0.940 '.' '\n' '\n' 'He' → ' told'
- n=3 meanΔ=11.459 '.' '\n' '\n' 'It' → ' happened'
- n=3 meanΔ=4.740 '.' ' The' ' first' ' day' → ' was'
- n=3 meanΔ=0.337 'He' ' added' ':' ' "' → 'I'

### 64:128
- n=8 meanΔ=0.213 '.' '\n' '\n' 'He' → ' was'
- n=6 meanΔ=0.494 '.' '\n' '\n' 'They' → ' were'
- n=5 meanΔ=0.361 '\n' '\n' 'He' ' said' → ' he'
- n=5 meanΔ=1.065 '.' '\n' '\n' '"' → 'We'
- n=4 meanΔ=2.121 ' and' ' said' ',' ' "' → 'I'
- n=4 meanΔ=0.000 ' he' ' said' '.' '\n' → '\n'
- n=4 meanΔ=2.307 ',' ' and' ' it' ' is' → ' not'
- n=4 meanΔ=6.183 '.' '\n' '\n' 'And' → ' they'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
