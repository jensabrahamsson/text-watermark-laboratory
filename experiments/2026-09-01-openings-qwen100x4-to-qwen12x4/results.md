# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-qwen-100x4 | 100 | 157 | postokhits | 37/48 | 12/48 | 33 | 0 | 0 | 1.000 |

Zeros on the full combined train:

### postokhits (11 marked zeros)
- `01-harbour` draw 1: **Chapter 5
- `01-harbour` draw 2: **THE STAG
- `01-harbour` draw 3: **THE STAG
- `01-harbour` draw 4: **Chapter 5
- `02-night-bus` draw 1: What are the main
- `02-night-bus` draw 3: What are the main
- `02-night-bus` draw 4: What are the main
- `06-station` draw 1: He nodded, then
- `06-station` draw 3: He got off,
- `08-letter` draw 1: The truth will not
- `08-letter` draw 2: The truth is,

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
