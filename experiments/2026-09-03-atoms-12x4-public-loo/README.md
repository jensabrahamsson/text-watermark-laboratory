# Interpolate occupancy: original-12 public `ngram_len=5` leave-one-out

Leave-one-family-out interpolate atoms on
`../2026-08-17-pair-12x4/`. Comparison baseline for H-long-occ, not a
matched-seed pair with the Hw=12 twins. Not a new `probe --methods`
name. `used_keys=false`. Marked `lr>0` **24/48**.

Exact next-token overlap is **269** seen versus **11912** unseen.
Window $[0{:}4)$ is 84 seen / 204 unseen. Opening `'The' → ' ferry'`
is n=8. Hw=12 original-12 has fewer seen events in every window
(`../2026-09-03-atoms-12x4-ngram13/`, **160** seen). Occupancy is
not a detector. Does not replace **25/48**.
