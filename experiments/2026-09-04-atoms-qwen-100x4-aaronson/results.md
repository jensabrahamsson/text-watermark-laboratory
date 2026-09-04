# Interpolate atoms

Leave-one-family-out interpolate last-4 atoms. Each family is scored on tables fit on the other families (same rotate as probe). unseen_next is Witten–Bell backoff. Not keys, not a new probe method, not a universal detector.

used_keys=False mode=leave-one-family-out n_rows=800 marked_lr>0=216 seen=8750 unseen=92842

| window | mean marked Δ | mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | 2.5098 | -2.6129 | 1470 | 930 |
| 4:16 | 0.1640 | -2.0535 | 859 | 8741 |
| 16:32 | 0.4333 | -2.1771 | 825 | 11975 |
| 32:64 | 0.5493 | -2.0591 | 2075 | 23525 |
| 64:128 | 0.5846 | -1.9984 | 3521 | 47671 |

Top observed-token marked Δ>0 atoms by window:

### 0:4
- n=124 meanΔ=7.781 'At' → ' last'
- n=112 meanΔ=4.583 'At' ' last' → ','
- n=84 meanΔ=0.556 'At' → ' least'
- n=72 meanΔ=2.101 'At' ' last' ',' → ' the'
- n=48 meanΔ=2.169 'At' → ' the'
- n=36 meanΔ=9.332 'At' ' least' → ' once'
- n=28 meanΔ=1.846 'At' ' last' ',' → ' he'
- n=28 meanΔ=5.189 'At' ' the' → ' bottom'

### 4:16
- n=28 meanΔ=2.814 '0' '0' '0' '0' → '0'
- n=12 meanΔ=2.014 ' he' ' had' ' some' ' time' → ' to'
- n=12 meanΔ=3.164 ' least' ' he' ' had' ' some' → ' time'
- n=12 meanΔ=8.793 'At' ' least' ' he' ' had' → ' some'
- n=12 meanΔ=1.372 'At' ' least' ' once' ' when' → ' I'
- n=12 meanΔ=3.223 'At' ' the' ' bottom' ',' → ' the'
- n=12 meanΔ=7.294 'At' ' the' ' end' ' of' → ' its'
- n=8 meanΔ=4.804 '\n' 'B' '.' ' wrong' → '\n'

### 16:32
- n=152 meanΔ=2.843 '0' '0' '0' '0' → '0'
- n=20 meanΔ=11.896 ':\n' 'A' '\n\n' '我国' → '宪法'
- n=20 meanΔ=0.693 'A' '\n\n' '我国' '宪法' → '规定'
- n=20 meanΔ=8.068 '答案' ':\n' 'A' '\n\n' → '我国'
- n=16 meanΔ=9.446 '\n\n' '我国' '宪法' '规定' → '：'
- n=16 meanΔ=9.538 '中华人民' '共和国' '公民' '在' → '法律'
- n=16 meanΔ=11.609 '公民' '在' '法律' '面前' → '一律'
- n=16 meanΔ=12.787 '共和国' '公民' '在' '法律' → '面前'

### 32:64
- n=384 meanΔ=2.848 '0' '0' '0' '0' → '0'
- n=28 meanΔ=0.981 '一律' '平等' '。' '这' → '表明'
- n=24 meanΔ=1.783 '.\n' 'At' ' last' ',' → ' the'
- n=20 meanΔ=9.468 ' ' '任何' '组织' '或' → '个人'
- n=20 meanΔ=9.366 '.' ' ' '任何' '组织' → '或'
- n=20 meanΔ=10.101 'A' '.' ' ' '任何' → '组织'
- n=20 meanΔ=10.186 '任何' '组织' '或' '个人' → '都'
- n=20 meanΔ=12.302 '或' '个人' '都' '必须' → '尊重'

### 64:128
- n=788 meanΔ=2.848 '0' '0' '0' '0' → '0'
- n=48 meanΔ=1.793 '.\n' 'At' ' last' ',' → ' the'
- n=40 meanΔ=9.468 ' ' '任何' '组织' '或' → '个人'
- n=40 meanΔ=9.375 '.' ' ' '任何' '组织' → '或'
- n=36 meanΔ=6.359 '.' ' Most' ' of' ' them' → ' just'
- n=24 meanΔ=9.999 'C' '.' ' ' '任何' → '组织'
- n=24 meanΔ=10.863 '任何' '组织' '或' '个人' → '不得'
- n=20 meanΔ=2.954 ' All' ' she' ' needed' ' was' → ' a'

Not detector_mean. Not Claude. Not a new probe method. Does not replace 25/48.
