# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=96 marked_lr>0=44 seen=114 unseen=12071

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 0.1516 | -0.2423 | 40 | 248 |
| 4:16 | 0.2274 | -0.1909 | 4 | 1148 |
| 16:32 | 0.2874 | -0.2368 | 6 | 1530 |
| 32:64 | 0.2501 | -0.1545 | 19 | 3053 |
| 64:128 | 0.2929 | -0.1438 | 45 | 6092 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=4 meanΔ=1.897 'I' → ' walked'
- n=3 meanΔ=0.994 'I' → ' was'
- n=2 meanΔ=0.405 'He' → ' had'
- n=2 meanΔ=5.189 'I' → ' drive'
- n=1 meanΔ=3.825 'I' → ' can'
- n=1 meanΔ=3.502 'I' → ' made'
- n=1 meanΔ=7.738 'It' → ' takes'

### 4:16
- n=1 meanΔ=1.248 ',' ' and' ' said' ',' → ' "'

### 32:64
- n=2 meanΔ=0.625 ' I' ' thought' ' it' ' must' → ' have'
- n=2 meanΔ=4.811 ' it' "'s" ' always' ' the' → ' same'
- n=2 meanΔ=3.325 ' thought' ' it' ' must' ' have' → ' been'
- n=2 meanΔ=2.893 '.' ' The' ' next' ' morning' → ' I'
- n=1 meanΔ=2.463 ' it' ' must' ' have' ' been' → ' a'
- n=1 meanΔ=5.024 ' know' ' what' ' to' ' do' → '.'
- n=1 meanΔ=5.873 ' must' ' have' ' been' ' a' → ' good'
- n=1 meanΔ=2.928 ' what' ' to' ' do' '.' → ' He'

### 64:128
- n=2 meanΔ=3.453 ' I' ' am' ' sorry' ' for' → ' what'
- n=2 meanΔ=5.698 '.' ' I' ' am' ' sorry' → ' for'
- n=1 meanΔ=2.613 ' it' ' must' ' have' ' been' → ' a'
- n=1 meanΔ=4.868 ' it' "'s" ' always' ' the' → ' same'
- n=1 meanΔ=5.008 ' know' ' what' ' to' ' do' → '.'
- n=1 meanΔ=5.226 ' must' ' have' ' been' ' a' → ' good'
- n=1 meanΔ=2.929 ' what' ' to' ' do' '.' → ' He'
- n=1 meanΔ=0.590 ',' ' and' ' said' ',' → ' "'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
