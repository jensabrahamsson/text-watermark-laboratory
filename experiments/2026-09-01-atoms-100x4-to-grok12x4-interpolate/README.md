# Interpolate atoms: 100 one-liners → Grok-register 12×4

Decode of the frozen lock A tables
(`../2026-09-01-transfer-100x4-to-grok12x4-hard-last4/tables-counts/`).
Not a new `probe --methods` name. `used_keys=false`. Full-file marked
`lr>0` is **27/48**, matching the xreg t=0 readout.

Almost all interpolate mass is Witten–Bell backoff on **unseen** next
tokens, not observed last-4 copies:

| Window | Mean marked Δ | Mean unmarked Δ | seen | unseen |
|---|---|---|---|---|
| 0:4 | −0.017 | −0.397 | 81 | 207 |
| 4:16 | −0.096 | 0.003 | 16 | 1136 |
| 16:32 | 0.040 | −0.002 | 28 | 1508 |
| 32:64 | 0.085 | −0.114 | 87 | 2985 |
| 64:128 | 0.056 | −0.086 | 214 | 5924 |

Observed-token atoms that do fire: opening `'The' → ' car'` (n=19), and
in the tail GPT-2 paragraph/dialogue templates (`'\\n\\n' '"' 'I'`,
`'I' ' turned' ' my' → ' head'`). Those are shared continuation
4-grams, not a denser isolated-file detector. Occupancy-free postokhits
on the same files remains **0/48**. Do not sell tail **9/12** or
`The car`. Does not replace **25/48**.
