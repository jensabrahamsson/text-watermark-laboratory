# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=273 seen=3535 unseen=98064

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 1.0596 | -0.4658 | 1092 | 1308 |
| 4:16 | 0.2286 | -0.1553 | 678 | 8922 |
| 16:32 | 0.1079 | -0.2061 | 279 | 12521 |
| 32:64 | 0.0382 | -0.2203 | 524 | 25076 |
| 64:128 | 0.0831 | -0.1657 | 962 | 50237 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=44 meanΔ=5.363 'The' → ' day'
- n=43 meanΔ=1.170 'The' → ' woman'
- n=36 meanΔ=5.533 'The' ' day' → ' was'
- n=20 meanΔ=5.839 'The' ' day' ' was' → ' long'
- n=20 meanΔ=3.266 'The' ' woman' → ','
- n=20 meanΔ=5.623 'The' ' woman' ',' → ' who'
- n=16 meanΔ=1.483 'The' → ' '
- n=16 meanΔ=0.672 'The' → ' author'

### 4:16
- n=19 meanΔ=4.052 'The' ' day' ' was' ' long' → ','
- n=8 meanΔ=2.650 ' author' ' thought' ' it' ' was' → ' a'
- n=8 meanΔ=6.897 ' day' ' was' ' long' ',' → ' hot'
- n=8 meanΔ=4.710 ' thought' ' it' ' was' ' a' → ' good'
- n=8 meanΔ=1.247 ' was' ' a' ' good' ' idea' → ' to'
- n=8 meanΔ=2.950 ' was' ' long' ',' ' hot' → ','
- n=8 meanΔ=2.791 'The' ' author' ' thought' ' it' → ' was'
- n=8 meanΔ=0.862 'The' ' woman' ',' ' who' → ' was'

### 16:32
- n=4 meanΔ=0.374 ' It' ' was' ' one' ' of' → ' those'
- n=2 meanΔ=0.210 ' It' ' was' ' the' ' first' → ' time'
- n=2 meanΔ=1.479 ' there' ' is' ' not' ' enough' → ' information'
- n=2 meanΔ=4.419 ' when' ' he' ' was' ' a' → ' child'
- n=2 meanΔ=1.090 ',' ' said' ':' ' "' → 'I'
- n=2 meanΔ=1.128 '.' ' It' ' was' ' the' → ' first'
- n=2 meanΔ=1.427 '.\n' 'At' ' first' ',' → ' the'
- n=1 meanΔ=0.345 ' ' '2' '0' '1' → '8'

### 32:64
- n=2 meanΔ=5.118 ' Let' "'s" ' give' ' stream' → ' of'
- n=2 meanΔ=2.929 ' for' ' the' ' night' '.' → ' The'
- n=2 meanΔ=6.823 ' give' ' stream' ' of' ' consciousness' → ' first'
- n=2 meanΔ=0.933 ' on' ' top' ' of' ' each' → ' other'
- n=2 meanΔ=0.000 ' set' ' up' ' an' ' equation' → ' based'
- n=2 meanΔ=0.687 ' the' ' sound' ' of' ' a' → ' car'
- n=2 meanΔ=3.597 ' two' ' years' ' ago' '.\n' → 'A'
- n=2 meanΔ=12.734 "'s" ' give' ' stream' ' of' → ' consciousness'

### 64:128
- n=3 meanΔ=1.724 ' ' '2' '0' '1' → '7'
- n=3 meanΔ=0.354 ' �' '�' '确' '\n' → '答案'
- n=3 meanΔ=0.354 ' �' '�' '误' '\n' → 'B'
- n=3 meanΔ=0.168 ',"' ' he' ' said' '.' → ' "'
- n=3 meanΔ=9.487 '其中' '的' '正确' '答案' → '。\n'
- n=3 meanΔ=7.065 '选出' '其中' '的' '正确' → '答案'
- n=3 meanΔ=9.163 '，请' '选出' '其中' '的' → '正确'
- n=3 meanΔ=0.470 '�' '确' '\n' '答案' → ':\n'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
