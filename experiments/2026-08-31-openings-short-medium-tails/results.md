# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-08-31-pair-36x4 | 24 | 25 | postokhits | 16/48 | 13/48 | 3 | 0 | 0 | 1.000 |
| 2026-08-31-pair-36x4 | 24 | 25 | postokbackoff | 16/48 | 13/48 | 3 | 0 | 0 | 1.000 |
| 2026-08-31-pair-36x4 | 24 | 25 | postokbackoff2 | 13/48 | 13/48 | 0 | 0 | 0 | 1.000 |
| 2026-08-31-pair-long12x4 | 36 | 39 | postokhits | 20/48 | 14/48 | 7 | 0 | 0 | 1.000 |
| 2026-08-31-pair-long12x4 | 36 | 39 | postokbackoff | 22/48 | 14/48 | 9 | 2 | 0 | 1.000 |
| 2026-08-31-pair-long12x4 | 36 | 39 | postokbackoff2 | 13/48 | 14/48 | 0 | 0 | 0 | 1.000 |
| 2026-08-31-pair-tails12x4 | 48 | 63 | postokhits | 30/48 | 19/48 | 17 | 0 | 0 | 1.000 |
| 2026-08-31-pair-tails12x4 | 48 | 63 | postokbackoff | 36/48 | 19/48 | 23 | 6 | 0 | 1.000 |
| 2026-08-31-pair-tails12x4 | 48 | 63 | postokbackoff2 | 13/48 | 19/48 | 0 | 0 | 0 | 1.000 |

Zeros on the full combined train:

### postokhits (18 marked zeros)
- `01-harbour` draw 1: The ferry was so
- `01-harbour` draw 2: The ferry was over
- `01-harbour` draw 3: The ferry was in
- `01-harbour` draw 4: The ferry was in
- `03-library` draw 1: Closing is the
- `03-library` draw 2: Closing is the
- `03-library` draw 3: Closing is the
- `03-library` draw 4: Closing is the
- `06-station` draw 4: The conductor turned and
- `08-letter` draw 2: Now in the second
- `08-letter` draw 3: While working on the
- `10-office` draw 1: The printer worked.
- `10-office` draw 3: The printer worked.
- `10-office` draw 4: The printer worked better
- `12-ferry-queue` draw 1: The ferry was so
- `12-ferry-queue` draw 2: The ferry was so
- `12-ferry-queue` draw 3: The ferry was so
- `12-ferry-queue` draw 4: The ferry was waiting

### postokbackoff (12 marked zeros)
- `01-harbour` draw 1: The ferry was so
- `01-harbour` draw 2: The ferry was over
- `06-station` draw 4: The conductor turned and
- `08-letter` draw 2: Now in the second
- `08-letter` draw 3: While working on the
- `10-office` draw 1: The printer worked.
- `10-office` draw 3: The printer worked.
- `10-office` draw 4: The printer worked better
- `12-ferry-queue` draw 1: The ferry was so
- `12-ferry-queue` draw 2: The ferry was so
- `12-ferry-queue` draw 3: The ferry was so
- `12-ferry-queue` draw 4: The ferry was waiting

### postokbackoff2 (35 marked zeros)
- `01-harbour` draw 1: The ferry was so
- `01-harbour` draw 2: The ferry was over
- `01-harbour` draw 3: The ferry was in
- `01-harbour` draw 4: The ferry was in
- `02-night-bus` draw 1: The bus is a
- `02-night-bus` draw 2: The bus is all
- `02-night-bus` draw 3: After two and a
- `02-night-bus` draw 4: The bus is all
- `03-library` draw 1: Closing is the
- `03-library` draw 2: Closing is the
- `03-library` draw 3: Closing is the
- `03-library` draw 4: Closing is the
- `04-market` draw 1: The dog gave me
- `04-market` draw 2: The dog gave me
- `04-market` draw 3: The dog gave me
- `04-market` draw 4: The dog gave me
- `05-kitchen` draw 4: "Who is on
- `06-station` draw 4: The conductor turned and
- `07-rain` draw 1: "Whoop!"
- `07-rain` draw 2: "My sister's
- `08-letter` draw 1: The second version is
- `08-letter` draw 2: Now in the second
- `08-letter` draw 3: While working on the
- `08-letter` draw 4: The second version is
- `10-office` draw 1: The printer worked.
- `10-office` draw 3: The printer worked.
- `10-office` draw 4: The printer worked better
- `11-garden` draw 1: Now a little after
- `11-garden` draw 2: The car is really
- `11-garden` draw 3: The car is really
- `11-garden` draw 4: Now a little after
- `12-ferry-queue` draw 1: The ferry was so
- `12-ferry-queue` draw 2: The ferry was so
- `12-ferry-queue` draw 3: The ferry was so
- `12-ferry-queue` draw 4: The ferry was waiting

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
