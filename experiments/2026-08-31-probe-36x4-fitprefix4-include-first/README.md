# Matched 4-token include-first

36×4 leave-one-out. `--fit-prefix 4 --pos-bucket 1 --include-first`.
Scores generated token 0 as a first-token unigram (sentinel context,
not a watermark key). `used_keys=false`.

| Method | wins | AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| hits | **35/36** | 0.924 | 124/144 | 100/144 |
| poshits | **35/36** | 0.925 | 123/144 | 114/144 |
| first | 34/36 | 0.687 | 114/144 | 92/144 |

In-domain prompt grain ticks up 34→35. Isolated t=0 is worse than
skipping token 0 (poshits unmarked ≤0 114 vs 132). Averaging the
first-token unigram into hits is not free. See the OOD run.
