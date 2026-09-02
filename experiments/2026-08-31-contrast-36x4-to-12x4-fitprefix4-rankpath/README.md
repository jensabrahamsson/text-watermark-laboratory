# Key-free instance contrast (opening rank-path)

`--fit-prefix 4 --pos-bucket 1`. Isolated generated-only. `used_keys=false`.

**rankpath (tokbackoff).** Control vs unmarked is chance (AUC **0.498**,
perm p=0.42). Public vs control **9/12**, AUC **0.694**, close to public
vs unmarked **10/12**, AUC **0.683**. Isolated control `lr>0` is
**17/48**, not the poshits **0/48**. Ranking says other-instance does
not look marked; the isolated sign still spends false positives.

**rankuni.** Control looks marked: **30/48** `lr>0`, AUC **0.613**.
Public vs control is chance (**5/12**, AUC **0.502**). The rank unigram
is a tournament-sampling detector, not an instance detector.

Not key recovery. Not a universal detector. Write-up:
[../../research/key-free-rankpath.md](../../research/key-free-rankpath.md),
[../../research/key-free-contrast.md](../../research/key-free-contrast.md).

See [results.md](results.md).
