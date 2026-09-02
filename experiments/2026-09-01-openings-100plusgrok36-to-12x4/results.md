# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-100x4 | 100 | 69 | postokhits | 18/48 | 14/48 | 5 | 0 | 0 | 1.000 |
| 2026-09-01-pair-grok36x4 | 136 | 146 | postokhits | 28/48 | 22/48 | 13 | 0 | 1 | 0.963 |

Zeros on the full combined train:

### postokhits (20 marked zeros)
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
- `11-garden` draw 1: Now a little after
- `11-garden` draw 4: Now a little after
- `12-ferry-queue` draw 1: The ferry was so
- `12-ferry-queue` draw 2: The ferry was so
- `12-ferry-queue` draw 3: The ferry was so
- `12-ferry-queue` draw 4: The ferry was waiting

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
