# In-domain tokhybrid copies hashtok; poshashtok is a specificity knob

Leave-one-prompt-out on `experiments/2026-08-17-pair-12x4`. Full
128-token files, last-4. `tokhybrid` is occupancy-free hybrid: exact
tokhits when the n-gram and next token were seen, else hashtok.
`poshashtok` is occupancy-free hashing with `i // 16` prepended (the
pospool analog). That namespace is not a watermark key. Occupancy
`hybrid` is the Laplace control. Still no keys.

```bash
python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods tokhybrid,poshashtok,hashtok,hybrid \
  --out-dir experiments/2026-09-01-probe-12x4-tokhybrid-poshashtok
```

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested-by-stem |
|---|---|---|---|---|---|
| **poshashtok** | 11/12 | 0.621 | **28/48** | 25/48 | **14/48 vs 38/48** |
| hashtok | 9/12 | 0.664 | **33/48** | **22/48** | 22/48 vs 30/48 |
| hybrid | 11/12 | 0.725 | **35/48** | 28/48 | 24/48 vs 41/48 |
| **tokhybrid** | **11/12** | 0.683 | **33/48** | **22/48** | **23/48 vs 35/48** |

`tokhybrid` copies hashtok's isolated t=0 gate (**33/48 vs 22/48**,
same 33 true positives). Token-level tokhits does not flip any file
sign versus hashed collisions alone. Prompt ranking rises to **11/12**
(hashtok 9/12); station remains the prompt miss. Nested-by-stem
**23/48 vs 35/48** is still worse spec than hits **22/48 vs 39/48**.

Occupancy `hybrid` extras versus tokhybrid are the same four files as
hashpool versus hashtok (night-bus d3, library d2, market d1,
ferry-queue d4). Letter d2 stays negative on all four readers.
`poshashtok` is a specificity knob (nested **14/48 vs 38/48**), not a
denser isolated-file reader. Do **not** sell 33/48, 35/48, 28/48, or
tokhybrid 11/12 as replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
