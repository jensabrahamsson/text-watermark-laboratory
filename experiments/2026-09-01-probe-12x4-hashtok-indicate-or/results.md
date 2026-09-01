# In-domain hashtok × indicate complementarity

Sources: `experiments/2026-08-17-indicate-holdout-12x4` and
`experiments/2026-09-01-probe-12x4-hashtok`. `used_keys=false`.

OR at t=0 is either `lr>0`. Coverage is primary if `lr!=0` else
fallback. Nested 2D Youden and LDA/logit/max/mean are leave-one-stem
thresholds on already-held-out LOO scores. Mixed AUC is not a detector.

| Rule | marked>0 | unmarked≤0 | combined |
|---|---|---|---|
| indicate | 29/48 | 23/48 | 52/96 |
| hashtok | 33/48 | 22/48 | 55/96 |
| hashpool | 35/48 | 29/48 | 64/96 |
| hits | 28/48 | 30/48 | 58/96 |
| postokhits | 24/48 | 45/48 | 69/96 |
| indicate OR hashtok | **39/48** | **12/48** | **51/96** |
| indicate OR hashpool | 41/48 | 17/48 | 58/96 |
| hits OR hashtok | 37/48 | 13/48 | 50/96 |
| postokhits OR hashtok | 35/48 | 21/48 | 56/96 |
| indicate AND hashtok | 23/48 | 33/48 | 56/96 |
| nested 2D Youden OR | 37/48 | 18/48 | 55/96 |
| nested 2D Youden AND | 26/48 | 28/48 | 54/96 |
| LDA stack t=0 | 28/48 | 27/48 | 55/96 |
| LDA nested-by-stem | 21/48 | 37/48 | 58/96 |
| logit nested-by-stem | 21/48 | 38/48 | 59/96 |
| max nested-by-stem | 21/48 | 39/48 | 60/96 |
| mean nested-by-stem | 19/48 | 36/48 | 55/96 |
| hits then hashtok | 29/48 | 25/48 | 54/96 |
| postokhits then hashtok | 35/48 | 22/48 | 57/96 |
| postokhits then hashpool | 36/48 | 29/48 | 65/96 |

Do not sell 41/48, 39/48, 37/48, 36/48, or 35/48. Combined OR is worse
than indicate. Coverage is worse than postokhits standalone. Honest
nested fusion returns to ~21 true positives.

Letter d2 stays negative on indicate and hashtok.
