# Opening-overlap bound

Isolated-file observed-token recall equals opening-atom overlap with train. Exact 4-token copy is a lower bound. Not keys, not hash_iv, not g-values, not a universal detector.

fit_prefix=4 pos_bucket=1 include_first=False used_keys=False

| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-01-pair-100x4 | 100 | 69 | postokhits | 5/48 | 0/48 | 5 | 0 | 0 | nan |

Zeros on the full combined train:

### postokhits (43 marked zeros)
- `101-service-station` draw 1: The carpark was
- `101-service-station` draw 2: The carpark was
- `101-service-station` draw 3: The carpark was
- `101-service-station` draw 4: The carpark was
- `102-car-boot` draw 1: The car boot was
- `102-car-boot` draw 2: The car boot was
- `102-car-boot` draw 3: The car boot was
- `102-car-boot` draw 4: The street was a
- `103-bowling-alley` draw 1: The night went off
- `103-bowling-alley` draw 2: The car sped through
- `103-bowling-alley` draw 3: The coach drove with
- `103-bowling-alley` draw 4: The coach drove home
- `104-hospital-corridor` draw 1: The bus came to
- `104-hospital-corridor` draw 2: The bus came to
- `104-hospital-corridor` draw 3: The bus came to
- `104-hospital-corridor` draw 4: The bus came to
- `105-charity-shop` draw 1: The car took over
- `105-charity-shop` draw 2: ***

In
- `105-charity-shop` draw 3: Photograph by Chris
- `105-charity-shop` draw 4: ***

For
- `106-boxing-gym` draw 1: The coach made it
- `106-boxing-gym` draw 2: The coach had given
- `106-boxing-gym` draw 3: The coach made it
- `106-boxing-gym` draw 4: The coach made it
- `107-campsite` draw 3: By then I realized
- `108-registry-office` draw 1: After I'd finished
- `108-registry-office` draw 4: There was one place
- `109-scrapyard` draw 1: ***

Three
- `109-scrapyard` draw 2: The car kept moving
- `109-scrapyard` draw 3: The car turned back
- `109-scrapyard` draw 4: The window to the
- `110-chip-shop` draw 1: The car is slow
- `110-chip-shop` draw 2: The night was quiet
- `110-chip-shop` draw 3: The door to the
- `110-chip-shop` draw 4: The car and the
- `111-fire-station` draw 1: The car is slow
- `111-fire-station` draw 2: The school is about
- `111-fire-station` draw 3: The car is slow
- `111-fire-station` draw 4: The school is about
- `112-taxi-rank` draw 1: The car turned back
- `112-taxi-rank` draw 2: The car went outside
- `112-taxi-rank` draw 3: The car took over
- `112-taxi-rank` draw 4: The car was silent

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
