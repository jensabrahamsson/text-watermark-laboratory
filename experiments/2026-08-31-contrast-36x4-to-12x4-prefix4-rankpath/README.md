# Key-free instance contrast (unbucketed prefix-4 rank-path)

`--fit-prefix 5 --pos-bucket 0`. Four choice-matrix rows (generated
tokens 1–4). `used_keys=false`.

**rankpath.** Public vs unmarked **11/12**, AUC **0.759**, isolated
**25/48 vs 43/48** (5 unmarked FPs). Control vs unmarked is chance
(AUC **0.511**, perm p=0.27) with isolated **6/48** `lr>0` — the same
false-positive rate as unmarked. Public vs control **9/12**, AUC
**0.752**. This is the cleaner instance check: other-instance does not
rank above unmarked.

**rankuni.** Control **22/48** `lr>0`, AUC 0.557. Still leakier.

Not poshits **0/48**. Not key recovery. Write-up:
[../../research/key-free-rankpath.md](../../research/key-free-rankpath.md),
[../../research/key-free-contrast.md](../../research/key-free-contrast.md).

See [results.md](results.md).
