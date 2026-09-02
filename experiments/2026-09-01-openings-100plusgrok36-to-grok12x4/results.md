# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-100x4 | 100 | 69 | postokhits | 5/48 | 0/48 | 5 | 0 | 0 | nan |
| 2026-09-01-pair-grok36x4 | 136 | 146 | postokhits | 40/48 | 21/48 | 27 | 0 | 1 | 0.973 |

Zeros on the full combined train:

### postokhits (8 marked zeros)
- `102-car-boot` draw 4: The street was a
- `105-charity-shop` draw 2: ***

In
- `105-charity-shop` draw 3: Photograph by Chris
- `105-charity-shop` draw 4: ***

For
- `107-campsite` draw 3: By then I realized
- `108-registry-office` draw 1: After I'd finished
- `108-registry-office` draw 4: There was one place
- `109-scrapyard` draw 1: ***

Three

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
