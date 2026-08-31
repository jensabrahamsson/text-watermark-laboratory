# Matched 16-token poshits bucket sweep (36×4)

Matched 16-token poshits bucket sweep. Bucket 16 is a no-op on a 16-token prefix. Not keys. Not a universal detector.

| bucket | prompt wins | file auc | marked>0 | unmarked<=0 | nested-by-stem |
|---|---|---|---|---|---|
| 1 | 34/36 | 0.938 | 132/144 | 132/144 | 124/144 vs 132/144 |
| 2 | 34/36 | 0.938 | 132/144 | 132/144 | 124/144 vs 132/144 |
| 4 | 34/36 | 0.937 | 133/144 | 114/144 | 122/144 vs 127/144 |
| 8 | 34/36 | 0.936 | 133/144 | 114/144 | 122/144 vs 127/144 |
