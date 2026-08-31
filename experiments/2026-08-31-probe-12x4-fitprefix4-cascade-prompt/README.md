# Prompt-conditioned opening geometry (in-domain 12×4)

Same twins and 4-token clip as the isolated probe, with
`--prompt-context`. Isolated `indicate score` of a lone file cannot do
this.

Prompt-conditioned pivot-lda is **worse than chance** (7/12, AUC
0.468). The first tournament decision is given a held-out prompt.
postokbackoff with prompt last-k is 42/48 marked with 11 unmarked FPs;
that is not an isolated-file reader. Not a universal detector.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
