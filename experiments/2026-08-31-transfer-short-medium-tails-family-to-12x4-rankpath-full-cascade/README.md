# Count opening + full-file rank-path cascade (60-stem → 12×4)

`--fit-prefix 4 --pos-bucket 1` postokbackoff with
`--rankpath-full --rankpath-pos-bucket 0 --cascade-fallback rankpath`.
`used_keys=false`.

Count channel: **42 covered / 34 `lr>0`**, precision 1.0 among decided.
Full-file rankpath fallback signs **4/6** leftover zeros and 17 of 42
uncovered unmarked files. Combined cascade **38/48**, precision 0.691.
Do not sell 38/48.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
