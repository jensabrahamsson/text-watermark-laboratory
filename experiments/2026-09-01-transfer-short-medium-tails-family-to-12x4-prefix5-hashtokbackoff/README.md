# 60-stem prefix-5 hashed backoff → 12×4

Same train as prefix-5 `hashtok`. Per-order hash tables (last-4/3/2/1),
occupancy-free. `used_keys=false`.

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashpool | 11/12 | 0.841 | **34/48** | 34/48 | 30/48 vs 43/48 | 0.708 |
| hashtok | 9/12 | 0.761 | **30/48** | 36/48 | 26/48 vs 42/48 | 0.714 |
| hashtokbackoff | 10/12 | 0.836 | **38/48** | 35/48 | **30/48 vs 40/48** | 0.745 |
| hashtokbackoff2 | 10/12 | 0.818 | **36/48** | 34/48 | **30/48 vs 42/48** | 0.720 |
| postokbackoff | 10/12 | 0.782 | 34/48 | 40/48 | 33/48 vs 42/48 | 0.810 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 15/48 vs 46/48 | 0.882 |

Letter d2 official 5-gram `Now in the second I`: last-4/3/2 hashes
never saw `I`. Last-1 saw it **unmarked only** (c_m=0, c_u=2,
δ=−1.10). hashtokbackoff2's letter d2 `lr=0.694` is tokens 1–2
(`Now`→` in` at order 3, n=1; `Now in`→` the` at order 4), not
token 4. Including last-1 dilutes that to 0.096.

Library ×4 and letter d3 are last-4 hashed observed-token extras
versus exact `hashtok`. Nested Youden stays **30/48**. Do not sell
38/48 or 36/48 as beating poshits **39/48** or replacing **29/48**.

JSON: `backoff-order-trace.json`. Write-up:
[../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
