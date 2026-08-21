# Claude mark attempt (2026-08-19)

Same `PROMPTS` as [../claude-premark-2026-08/](../claude-premark-2026-08/), rerun on claude.ai after a rumor that Anthropic text marking is live.

**37 / 40 prompts.** ~112k characters. Usage limit stopped the run on the courtyard washing-line prompt. Still missing:

- neighbours sharing a washing line
- small ferry delayed by wind
- retired teacher letter

Not an announced retrofit. Manifest `assumed_watermark` is `rumored`. Do not
treat this pile as ground-truth marked. A leave-one-out **hypothesis** run
against the pre-mark twins is in
[`../2026-08-19-claude-rumor-twins/`](../2026-08-19-claude-rumor-twins/)
(last-1 28/37, last-4 24/37). That is a style-shift measurement, not a
Claude detector. Lab notes: [research/LOGBOOK.md](../../research/LOGBOOK.md).

Public `score` (`public-deepmind-30`) on three pairs sat at chance on both sides, as expected (wrong instance):

| Prompt | Premark mean | 2026-08-19 mean |
|---|---:|---:|
| harbour | 0.495 | 0.506 |
| library | 0.504 | 0.504 |
| chess club | 0.499 | 0.497 |

That is not evidence the rumor is true or false.

Protocol: [research/paired-corpus.md](../../research/paired-corpus.md).

```bash
source .venv/bin/activate
python scripts/collect_claude_premark.py --via applescript --n 0 --pause 25 \
  --out-dir experiments/claude-mark-2026-08-19 \
  --suffix sonnet5-mark \
  --assumed-watermark rumored \
  --no-seed
```
