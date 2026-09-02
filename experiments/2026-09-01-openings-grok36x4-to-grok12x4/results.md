# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-grok36x4 | 36 | 77 | postokhits | 39/48 | 21/48 | 26 | 0 | 3 | 0.929 |

Zeros on the full combined train:

### postokhits (9 marked zeros)
- `102-car-boot` draw 4: The street was a
- `105-charity-shop` draw 2: ***

In
- `105-charity-shop` draw 3: Photograph by Chris
- `105-charity-shop` draw 4: ***

For
- `107-campsite` draw 2: The sun was rising
- `107-campsite` draw 3: By then I realized
- `108-registry-office` draw 1: After I'd finished
- `108-registry-office` draw 4: There was one place
- `109-scrapyard` draw 1: ***

Three

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
