# Interpolate occupancy: 100-family public `ngram_len=5` leave-one-out

Leave-one-family-out interpolate atoms on
`../2026-09-01-pair-100x4/`. Comparison baseline for Hw=12 100-family
occupancy, not a matched-seed pair. Not a new `probe --methods` name.
`used_keys=false`. File LRs match
`../2026-09-01-probe-100x4-hard-last4/interpolate/holdout.json`
(marked `lr>0` **352/400**; lock A ranking **99/100**).

Exact next-token overlap is **10158** seen versus **91353** unseen.
Window $[0{:}4)$ is 1633 seen / 767 unseen. Hw=12 100-family has fewer
seen events in every window (`../2026-09-03-atoms-100x4-ngram13/`,
**5878** seen). Occupancy is not a detector. Does not replace
**25/48**.
