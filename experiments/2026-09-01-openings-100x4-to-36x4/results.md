# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-100x4 | 100 | 69 | postokhits | 117/144 | 103/144 | 29 | 0 | 5 | 0.958 |

Zeros on the full combined train:

### postokhits (27 marked zeros)
- `01-harbour` draw 1: After arriving home,
- `01-harbour` draw 2: The ferry was in
- `01-harbour` draw 3: The ferry was over
- `01-harbour` draw 4: The ferry was quiet
- `02-night-bus` draw 1: The bus stop has
- `02-night-bus` draw 2: The bus rides with
- `02-night-bus` draw 3: The bus moves on
- `02-night-bus` draw 4: The bus moves on
- `03-library` draw 1: Closing is the
- `03-library` draw 2: Closing is my
- `03-library` draw 3: Closing is my
- `03-library` draw 4: Closing is the
- `04-market` draw 1: The dog gave me
- `04-market` draw 2: The dog gave me
- `04-market` draw 3: The dog gave me
- `04-market` draw 4: The dog gave me
- `06-station` draw 1: The car sped at
- `08-letter` draw 4: After I'd posted
- `10-office` draw 2: The printer worked.
- `11-garden` draw 2: Now back to the
- `11-garden` draw 4: The car that was
- `12-ferry-queue` draw 1: The ferry was in
- `12-ferry-queue` draw 2: The ferry was so
- `12-ferry-queue` draw 3: The ferry was so
- `12-ferry-queue` draw 4: The ferry was so
- `35` draw 1: The plan was to
- `35` draw 2: The plan was to

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
