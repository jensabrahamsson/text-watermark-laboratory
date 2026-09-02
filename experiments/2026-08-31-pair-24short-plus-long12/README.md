# Combined train: 24 short one-liners + 12 medium scenes

Hardlinks only. Stems 13–36 from
[`../2026-08-31-pair-36x4/`](../2026-08-31-pair-36x4/) and stems 37–48 from
[`../2026-08-31-pair-long12x4/`](../2026-08-31-pair-long12x4/).
Not a new sample. Used as `--pair_dir` train for transfer onto 12×4.

Git keeps this README only. Rebuild:

```bash
mkdir -p experiments/2026-08-31-pair-24short-plus-long12
python - <<'PY'
from pathlib import Path
dst = Path("experiments/2026-08-31-pair-24short-plus-long12")
src36 = Path("experiments/2026-08-31-pair-36x4")
src12 = Path("experiments/2026-08-31-pair-long12x4")
for p in src36.glob("*.txt"):
    stem = p.name.split("-")[0]
    if stem.isdigit() and 13 <= int(stem) <= 36:
        target = dst / p.name
        if not target.exists():
            target.hardlink_to(p)
for p in src12.glob("*.txt"):
    target = dst / p.name
    if not target.exists():
        target.hardlink_to(p)
PY
```
