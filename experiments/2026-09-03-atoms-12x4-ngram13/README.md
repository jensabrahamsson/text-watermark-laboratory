# Interpolate occupancy: original-12 `ngram_len=13` leave-one-out

Leave-one-family-out interpolate atoms on
`../2026-09-03-pair-12x4-ngram13/`. Same rotate as the Hw=12 probe.
Not a new `probe --methods` name. `used_keys=false`. File LRs match
`../2026-09-03-probe-12x4-ngram13-hard-last4/interpolate/holdout.json`
(marked `lr>0` **20/48**).

Exact next-token overlap is **160** seen versus **12026** unseen
(Witten–Bell backoff). Window $[0{:}4)$ is 71 seen / 217 unseen.
Tails are almost all backoff. Opening `'The' → ' bus'` is n=15, not
a denser isolated-file detector. Public Hw=4 comparison:
`../2026-09-03-atoms-12x4-public-loo/` (**269** seen). Does not
replace **25/48**.
