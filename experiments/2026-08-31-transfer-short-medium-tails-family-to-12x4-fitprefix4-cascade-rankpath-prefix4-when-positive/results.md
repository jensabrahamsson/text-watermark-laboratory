# Key-free cascade (positive-when, prefix-4 rankpath leftover)

Rebound from saved prefix-4 cascade rows. No new GPT-2 forwards.
`--cascade-when positive`: count LR only when `lr>0`; otherwise prefix-4 rankpath.
`used_keys=false`.

Cascade: count LR when lr>0, unmarked-LM rankpath when count is nonpositive (zeros and covered negatives). Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff fallback=rankpath cascade_when=positive pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 34/48 >0 34/34 unmarked<=0 0/1 precision=1.000
rankpath fallback marked 14/48 >0 6/14 unmarked<=0 40/48
combined marked>0 40/48 unmarked<=0 40/48
cascade rankpath_end=4 (opening prefix-N, not the full file)
rankpath uncovered FPR10 t=0.2591 marked>t 5/14 unmarked<=t 44/48
combined at fallback FPR10 marked>t 39/48 unmarked<=t 44/48. Count stays at 0; mixed AUC is still not a detector.
rankpath-fallback marked files:
- `01-harbour` draw 1: The ferry was so lr>0=0.1098
- `01-harbour` draw 2: The ferry was over lr>0=0.4027
- `01-harbour` draw 3: The ferry was in lr<=0=-0.3330
- `01-harbour` draw 4: The ferry was in lr<=0=-0.3330
- `06-station` draw 4: The conductor turned and lr<=0=-0.5998
- `08-letter` draw 2: Now in the second lr<=0=-0.9578
- `08-letter` draw 3: While working on the lr<=0=-0.4075
- `10-office` draw 1: The printer worked. lr<=0=-0.3458
- `10-office` draw 3: The printer worked. lr<=0=-0.3458
- `10-office` draw 4: The printer worked better lr>0=0.5175
- `12-ferry-queue` draw 1: The ferry was so lr>0=0.4027
- `12-ferry-queue` draw 2: The ferry was so lr>0=0.4027
- `12-ferry-queue` draw 3: The ferry was so lr>0=0.4027
- `12-ferry-queue` draw 4: The ferry was waiting lr<=0=-0.4523

