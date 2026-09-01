# In-domain hashtok n=2 seed sweep: width win is not stable

Occupancy-free `hashtok`, 12×4 leave-one-out, last-4, full files.
`--n-hashes 2` at the library default mixer seed **20260831** was
**34/48 vs 31/48**, nested **28/48 vs 37/48**, AUC **0.764** — better
than default n=8 on that same gate. That seed is a random feature-hash
initializer, not SynthID `hash_iv`. This sweep asks whether the n=2
win is a width law or a lucky mixer.

`rotate_hashpool(..., seed=)` / `fit_hashpool_twins(..., seed=)`.
Default seed 20260831 reproduces the locked n=2 holdout.

| n_hashes | seed | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem | letter d2 |
|---|---|---|---|---|---|---|---|
| 2 | **20260831** | **11/12** | **0.764** | **34/48** | **31/48** | **28/48 vs 37/48** | −0.076 |
| 2 | 0 | 9/12 | 0.637 | 34/48 | 21/48 | 28/48 vs 30/48 | **+0.031** |
| 2 | 1 | **11/12** | 0.687 | 33/48 | 25/48 | 29/48 vs 36/48 | −0.114 |
| 2 | 7 | **11/12** | 0.695 | 30/48 | 28/48 | 27/48 vs 34/48 | −0.120 |
| 2 | 42 | 10/12 | 0.743 | 34/48 | 30/48 | **34/48 vs 25/48** | −0.106 |
| 2 | 12345 | 10/12 | 0.712 | 31/48 | 25/48 | 25/48 vs 37/48 | **+0.104** |
| 8 | 20260831 | 9/12 | 0.664 | 33/48 | 22/48 | 22/48 vs 30/48 | −0.027 |
| 8 | 0 | 9/12 | 0.658 | 33/48 | **32/48** | **32/48 vs 33/48** | −0.215 |
| 8 | 7 | **11/12** | 0.719 | 31/48 | 29/48 | **28/48 vs 37/48** | −0.056 |

n=2 t=0 unmarked spec ranges **21–31/48**. Nested spec ranges
**25–37/48**. Prompt ranking ranges **9–11/12**. Default seed 20260831
is among the *best* n=2 mixers here, not a typical one. Seed 0 copies
the 34 TPs and collapses spec to **21/48** (default n=8 territory).
Seed 42 nested **34/48 vs 25/48** is a recall knob, not a detector.
Letter d2 flips sign with seed (0 and 12345); that is not the official
5-gram.

n=8 is seed-sensitive too: seed 7 nested **28/48 vs 37/48** matches the
advertised n=2 default. The in-domain n=2 vs n=8 comparison at one seed
is confounded. 24→12 transfer already preferred n=8. Keep the CLI
defaults (`n_hashes=8`, seed `20260831`). Do **not** sell 34/48 as a
width law or as replacing **29/48**.

JSON: `results.json` and `n{2,8}-seed*/hashtok/holdout.json`.
Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
