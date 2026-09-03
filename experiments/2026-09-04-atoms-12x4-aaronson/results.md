# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=8 seen=573 unseen=11618

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.5701 | -4.1571 | 167 | 121 |
| 4:16 | -0.5484 | -2.5115 | 73 | 1079 |
| 16:32 | -0.8220 | -2.6385 | 68 | 1468 |
| 32:64 | -1.0087 | -2.6514 | 90 | 2982 |
| 64:128 | -1.0102 | -2.6283 | 175 | 5968 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=24 meanΔ=1.157 '\n' → '"'
- n=20 meanΔ=2.940 '\n' '"' → 'This'
- n=12 meanΔ=2.011 '\n' '"' 'This' → ' is'
- n=8 meanΔ=6.371 '\n' → 'They'
- n=8 meanΔ=1.885 '\n' 'I' → ' had'
- n=8 meanΔ=8.998 '\n' 'I' ' had' → ' two'

### 4:16
- n=8 meanΔ=2.291 '\n' '"' 'This' ' is' → ' like'
- n=8 meanΔ=1.981 ' you' "'re" ' going' ' to' → ' have'
- n=8 meanΔ=10.920 '"' 'This' ' is' ' like' → ' having'
- n=8 meanΔ=3.879 "'re" ' going' ' to' ' have' → ' to'
- n=8 meanΔ=7.055 'This' ' is' ' like' ' having' → ' your'
- n=4 meanΔ=4.433 ' going' ' to' ' have' ' to' → ' have'
- n=4 meanΔ=5.433 ' have' ' to' ' have' ' a' → ' little'
- n=4 meanΔ=2.479 ' said' '.' '\n' '\n' → '"'

### 16:32
- n=8 meanΔ=4.453 ' going' ' to' ' have' ' to' → ' have'
- n=8 meanΔ=5.612 ' have' ' to' ' have' ' a' → ' little'
- n=8 meanΔ=1.503 ' to' ' have' ' a' ' little' → ' bit'
- n=8 meanΔ=1.169 ' to' ' have' ' to' ' have' → ' a'
- n=4 meanΔ=2.472 ' said' '.' '\n' '\n' → '"'
- n=4 meanΔ=0.035 ' she' ' said' '.' '\n' → '\n'
- n=4 meanΔ=1.971 ' you' "'re" ' going' ' to' → ' have'
- n=4 meanΔ=3.912 "'re" ' going' ' to' ' have' → ' to'

### 32:64
- n=16 meanΔ=4.456 ',"' ' she' ' said' ' again' → ','
- n=16 meanΔ=1.341 '.' '\n' '\n' 'I' → ' had'
- n=12 meanΔ=3.890 "'re" ' going' ' to' ' have' → ' to'
- n=8 meanΔ=4.453 ' going' ' to' ' have' ' to' → ' have'
- n=8 meanΔ=5.612 ' have' ' to' ' have' ' a' → ' little'
- n=8 meanΔ=1.503 ' to' ' have' ' a' ' little' → ' bit'
- n=8 meanΔ=1.169 ' to' ' have' ' to' ' have' → ' a'
- n=8 meanΔ=1.971 ' you' "'re" ' going' ' to' → ' have'

### 64:128
- n=28 meanΔ=4.445 ',"' ' she' ' said' ' again' → ','
- n=24 meanΔ=5.552 ' have' ' to' ' have' ' a' → ' little'
- n=24 meanΔ=1.534 ' to' ' have' ' a' ' little' → ' bit'
- n=24 meanΔ=1.341 '.' '\n' '\n' 'I' → ' had'
- n=16 meanΔ=4.433 ' going' ' to' ' have' ' to' → ' have'
- n=16 meanΔ=1.176 ' to' ' have' ' to' ' have' → ' a'
- n=12 meanΔ=1.971 ' you' "'re" ' going' ' to' → ' have'
- n=12 meanΔ=3.912 "'re" ' going' ' to' ' have' → ' to'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
