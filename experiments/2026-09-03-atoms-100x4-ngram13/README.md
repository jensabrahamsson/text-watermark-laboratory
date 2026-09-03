# Interpolate occupancy: 100-family `ngram_len=13` leave-one-out

Leave-one-family-out interpolate atoms on
`../2026-09-03-pair-100x4-ngram13/`. Same rotate as the Hw=12 100-family
probe. Not a new `probe --methods` name. `used_keys=false`. File LRs
match `../2026-09-03-probe-100x4-ngram13-hard-last4/interpolate/holdout.json`
(marked `lr>0` **267/400**).

Exact next-token overlap is **5878** seen versus **95624** unseen.
Window $[0{:}4)$ is 1287 seen / 1113 unseen (one-liner openings are
not mostly backoff). Public Hw=4 comparison:
`../2026-09-03-atoms-100x4-public-loo/` (**10158** seen). Every window
has fewer seen events under Hw=12. Occupancy is not a detector. Does
not replace **25/48**.
