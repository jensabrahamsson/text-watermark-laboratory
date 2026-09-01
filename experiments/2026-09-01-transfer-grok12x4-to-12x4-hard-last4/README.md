# Grok-register 12×4 → original 12×4, lock A interpolate last-4

Frozen command from
[../../research/PROTOCOL-isolated-register.md](../../research/PROTOCOL-isolated-register.md).
Train: `../2026-09-01-pair-grok12x4/`. Test: `../2026-08-17-pair-12x4/`.
No test prompt entered the fit. `used_keys=false`.

Prompt ranking **5/12**. Nested Youden (train-LOO threshold)
**16/48 vs 41/48**. t=0 **23/48 vs 30/48**. Does not beat recounted
hard **25/48**. Does not beat one-liner lock A nested **23/48**.
H-reg-A fails: Grok-length train did not lift isolated nested Youden.

Harbour and library now rank (they were one-liner lock A losses).
Night-bus and ferry-queue still lose. Medium stems 07–12 mostly lose.
Register match is not a universal isolated detector.
