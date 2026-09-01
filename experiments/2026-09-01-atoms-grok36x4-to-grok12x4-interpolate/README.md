# Interpolate atoms: 36 Grok-length → grok12×4

Decode of the frozen lock A tables
(`../2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4/tables-counts/`).
Not a new `probe --methods` name. `used_keys=false`. Full-file marked
`lr>0` is **39/48**, matching interpolate t=0 and occupancy-free
postokhits **39/48**. Nested interpolate Youden is **36/48 vs 39/48**.
Opening coverage is **39/48** (exact 21/48; 3 unmarked FP).

Window 0:4 is the occupancy-free channel: marked mean Δ +2.518 vs
unmarked −0.181, with 119 seen vs 169 unseen. Observed-token atoms:
`'The' → ' car'` (n=19), `'The' → ' coach'` (n=6), `'The' → ' bus'`
(n=4), `'The' ' car' 'park' → ' was'` (n=4). Those are shared
Grok-register openings, equal to the opening-overlap bound, not a
universal detector.

The tail is still Witten–Bell backoff (64:128: 183 seen vs 5955
unseen). Dialogue templates (`'.' '\\n\\n' '"' → 'I'`,
`'I' ' turned' ' my' → ' head'`) fire there as they did on the
100-one-liner train. Interpolate nested **36/48** is slightly *below*
occupancy-free **39/48** because that tail noise is not a cleaner
sign. Do not sell `'The' → ' car'`, occupancy-free **39/48**, or
nested **36/48**. Does not replace **25/48**.
