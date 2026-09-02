# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-grok36x4 | 36 | 77 | postokhits | 10/48 | 8/48 | 8 | 0 | 1 | 0.909 |

Zeros on the full combined train:

### postokhits (38 marked zeros)
- `01-harbour` draw 1: The ferry was so
- `01-harbour` draw 2: The ferry was over
- `01-harbour` draw 3: The ferry was in
- `01-harbour` draw 4: The ferry was in
- `03-library` draw 1: Closing is the
- `03-library` draw 2: Closing is the
- `03-library` draw 3: Closing is the
- `03-library` draw 4: Closing is the
- `05-kitchen` draw 1: "This is it
- `05-kitchen` draw 2: "This is it
- `05-kitchen` draw 3: "Oh, my
- `05-kitchen` draw 4: "Who is on
- `06-station` draw 1: "This is the
- `06-station` draw 2: "This is the
- `06-station` draw 3: "This is the
- `06-station` draw 4: The conductor turned and
- `07-rain` draw 1: "Whoop!"
- `07-rain` draw 2: "My sister's
- `07-rain` draw 3: "This is the
- `07-rain` draw 4: "Oh, my
- `08-letter` draw 1: The second version is
- `08-letter` draw 2: Now in the second
- `08-letter` draw 3: While working on the
- `08-letter` draw 4: The second version is
- `09-workshop` draw 1: "Oh, my
- `09-workshop` draw 2: "Oh, my
- `09-workshop` draw 3: "This is it
- `09-workshop` draw 4: "This is actually
- `10-office` draw 1: The printer worked.
- `10-office` draw 2: "This is the
- `10-office` draw 3: The printer worked.
- `10-office` draw 4: The printer worked better
- `11-garden` draw 1: Now a little after
- `11-garden` draw 4: Now a little after
- `12-ferry-queue` draw 1: The ferry was so
- `12-ferry-queue` draw 2: The ferry was so
- `12-ferry-queue` draw 3: The ferry was so
- `12-ferry-queue` draw 4: The ferry was waiting

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
