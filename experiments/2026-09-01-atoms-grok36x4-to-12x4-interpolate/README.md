# Interpolate atoms: 36 Grok-length → original 12×4

Decode of the frozen lock A tables
(`../2026-09-01-transfer-grok36x4-to-12x4-hard-last4/tables-counts/`).
Not a new `probe --methods` name. `used_keys=false`. Full-file marked
`lr>0` is **29/48**, matching interpolate t=0. Nested Youden on those
same files is **26/48 vs 33/48**. Occupancy-free postokhits stays
**10/48**, equal to opening coverage **10/48**.

Almost all interpolate mass is Witten–Bell backoff on **unseen** next
tokens. Window 0:4 has 69 seen vs 219 unseen; tail 64:128 is 137 seen
vs 5996 unseen. Marked 0:4 Δ is +0.496 because unmarked Δ is more
negative (−0.337) and because a few unbucketed body copies fire, not
because occupancy-free openings jumped from 10 to 29.

Observed-token atoms that do fire in 0:4: library `'Cl' → 'osing'`
(n=4; `Closing is the…`), `'The' → ' dog'` (n=4), `'The' → ' bus'`
(n=3), `'The' → ' car'` (n=2). Library is a postokhits **zero**:
opening-bucketed occupancy-free never sees `Closing`. Interpolate
tables are unbucketed full-file last-4, so a 4-gram from a grok36
**body** can still score a test opening. That gap (29 vs 10) is not a
denser isolated-file detector. Tail hits are GPT-2 paragraph/dialogue
templates (`'.' '\\n\\n' '"' → 'I'`, `'I' ' turned' ' my' → ' head'`).

Do not sell nested **26/48**, t=0 **29/48**, `Closing`, or `The dog`.
Does not replace **25/48**.
