# 36×4 leave-one-out postokhits, matched 4-token opening

`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`. Same twins as
[`../2026-08-31-probe-36x4-fitprefix4-pos1/`](../2026-08-31-probe-36x4-fitprefix4-pos1/).
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

In-domain poshits **131/144** marked `lr>0` is mostly observed next
tokens, not The-Laplace. `postokhits` keeps **122/144**. Only 9 of 131
true positives were occupancy. The 12 unmarked false positives stay.
Prompt ranking stays 34/36. Not a universal detector. Do not replace
10/12, 29/48, or 36/36.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | zeros M/U | decided tp/fn | decided fp |
|---|---|---|---|---|---|---|---|
| poshits | 34/36 | 0.935 | **131/144** | **132/144** | 8/89 | 131/5 | 12 |
| postokhits | 34/36 | 0.912 | **122/144** | **132/144** | 19/105 | 122/3 | 12 |

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits \
  --out-dir experiments/2026-08-31-probe-36x4-fitprefix4-postokhits
```
