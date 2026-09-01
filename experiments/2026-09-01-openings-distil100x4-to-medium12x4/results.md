# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-distil-100x4 | 100 | 207 | postokhits | 22/48 | 4/48 | 12 | 0 | 0 | 1.000 |

Zeros on the full combined train:

### postokhits (26 marked zeros)
- `01-harbour` draw 1: The ferry was leaving
- `01-harbour` draw 2: The ferry was leaving
- `01-harbour` draw 3: The ferry was leaving
- `01-harbour` draw 4: ***

Three
- `02-night-bus` draw 1: The bus is old
- `02-night-bus` draw 2: The bus's name
- `02-night-bus` draw 3: The bus is old
- `02-night-bus` draw 4: The bus is old
- `05-kitchen` draw 1: Danger, I
- `05-kitchen` draw 2: The cook came over
- `05-kitchen` draw 4: The cook, whose
- `06-station` draw 2: The car doors slid
- `06-station` draw 3: The car turned in
- `06-station` draw 4: The car turned into
- `08-letter` draw 1: The letter also claimed
- `08-letter` draw 2: Now a little bit
- `08-letter` draw 3: The letter also claimed
- `08-letter` draw 4: The letter also claimed
- `11-garden` draw 1: The plan is for
- `11-garden` draw 2: After about 2 and
- `11-garden` draw 3: The plan is for
- `11-garden` draw 4: Now a little back
- `12-ferry-queue` draw 1: The ferry was empty
- `12-ferry-queue` draw 2: The ferry was empty
- `12-ferry-queue` draw 3: The ferry was empty
- `12-ferry-queue` draw 4: The ferry was empty

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
