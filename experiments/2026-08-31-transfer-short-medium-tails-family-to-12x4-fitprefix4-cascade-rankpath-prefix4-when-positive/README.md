# 60-stem count + prefix-4 rankpath, `--cascade-when positive`

Rebound from
[`../2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/`](../2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/).
No new GPT-2 forwards. `used_keys=false`.

Coverage cascade keeps a negative count LR when `n_used>0`. Eight of
those covered files are harbour / ferry-queue openings whose last-1
`' was'` continuation looks unmarked (`The ferry was so/over/...`).
`--cascade-when positive` sends count-nonpositive files to prefix-4
rankpath instead.

| Rule | marked>0 | unmarked≤0 | precision |
|---|---|---|---|
| count `lr>0` only | **34/48** | **48/48** | **1.000** |
| coverage cascade (zeros only) | 35/48 | 43/48 | 0.875 |
| **positive-when cascade** | **40/48** | **40/48** | 0.833 |

Five of eight covered-negatives sign (`The ferry was so/over`) plus
one leftover zero (`The printer worked better`). Eight unmarked FPs,
all from rankpath. Combined accuracy **80/96** vs count **82/96**.
Do not sell 40/48 as beating poshits **39/48** or replacing **29/48**.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
