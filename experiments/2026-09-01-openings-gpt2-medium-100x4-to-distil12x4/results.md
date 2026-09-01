# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-gpt2-medium-100x4 | 100 | 64 | postokhits | 5/48 | 2/48 | 2 | 0 | 1 | 0.750 |

Zeros on the full combined train:

### postokhits (43 marked zeros)
- `01-harbour` draw 1: You can't take
- `01-harbour` draw 2: There was only one
- `01-harbour` draw 3: You can't really
- `01-harbour` draw 4: You can't really
- `02-night-bus` draw 1: You go to the
- `02-night-bus` draw 2: You can now buy
- `02-night-bus` draw 3: You can't tell
- `02-night-bus` draw 4: You can't tell
- `03-library` draw 1: You can now see
- `03-library` draw 2: You can now see
- `03-library` draw 3: You can now see
- `03-library` draw 4: You can't tell
- `04-market` draw 1: There was one place
- `04-market` draw 3: After about ten minutes
- `04-market` draw 4: The dog gave me
- `05-kitchen` draw 1: You can't tell
- `05-kitchen` draw 2: You can now play
- `05-kitchen` draw 3: You can't tell
- `05-kitchen` draw 4: You can't tell
- `06-station` draw 1: The train began again
- `06-station` draw 2: The train began,
- `06-station` draw 3: The train passed over
- `06-station` draw 4: A spokesman from the
- `07-rain` draw 2: You can't tell
- `08-letter` draw 1: The second version is
- `08-letter` draw 2: Now how do you
- `08-letter` draw 3: Now you must check
- `08-letter` draw 4: The second version is
- `09-workshop` draw 2: The hand didn't
- `09-workshop` draw 3: Now a little hard
- `09-workshop` draw 4: You can't tell
- `10-office` draw 1: I heard voices of
- `10-office` draw 2: I asked the first
- `10-office` draw 3: There would be some
- `10-office` draw 4: The meeting had just
- `11-garden` draw 1: 'We're going
- `11-garden` draw 2: Bicycle owners,
- `11-garden` draw 3: 'We're going
- `11-garden` draw 4: 'We're going
- `12-ferry-queue` draw 1: On this day,
- `12-ferry-queue` draw 2: When the ramp came
- `12-ferry-queue` draw 3: With the current state
- `12-ferry-queue` draw 4: But the rush of

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
