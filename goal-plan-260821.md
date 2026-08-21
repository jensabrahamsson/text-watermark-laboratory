# Plan: Claude resample 2026-08-21

## Goal kind
research

## Acceptance criteria
1. The same 40 `PROMPTS` strings are collected into `experiments/claude-sample-2026-08-21` (reuse that empty folder via `--new-dir`) or, if that path is left empty, into `experiments/claude-sample-2026-08-21b`. Do not edit `PROMPTS`. Use `claude-mark-YYYY-MM-DD` only if Anthropic has announced marking.
2. Pair the new corpus against `experiments/claude-premark-2026-08` and the previous sample (`claude-sample-2026-08-19b` or `claude-mark-2026-08-19`). Run last-1 and last-4 leave-one-out only when `n_pairs >= 2`. Persist those win counts.
3. Append one dated English LOGBOOK block. Do not rewrite the existing `## 2026-08-21 resample` heading or any older entry.
4. `used_keys` stays false. The run is not a Claude detector and not a watermark claim. Last-1 ahead of last-4 is a style/model shift; last-4 ahead of last-1 is the public-mixin window order; same-day chance is draw noise.
5. `python -m pytest tests/test_resample.py tests/test_iterate.py tests/test_indicator.py -q` still passes.

## Verification plan
1. gating: From the lab venv, `python -m pytest tests/test_resample.py tests/test_iterate.py tests/test_indicator.py -q` → `{SCRATCH}/pytest.txt`. All tests pass. `PROMPTS` first and last strings in `scripts/collect_claude_premark.py` are unchanged.
2. gating: If at least two long texts were collected, `python -m text_watermark_tools resample --skip-collect --new-dir <that corpus>` writes last-1 and last-4 for pre-mark and previous sample with `used_keys=False` → `{SCRATCH}/resample-skip-collect.txt`.
3. evidence: `{SCRATCH}/logbook-check.txt` records: collection count (0 is allowed on usage-limit / missing login); whether `## 2026-08-15` and the original `## 2026-08-21 resample` still exist unchanged; new append only at the end; no rewrite of older LOGBOOK text.
4. evidence: A live claude.ai scrape is attempted with Chrome already logged in. If login, quota, or osascript times out, capture that to `{SCRATCH}/collect-live.txt` and keep the schedule. Do not wait for the next Wed/Fri/Sun 04:00 launchd slot to declare this goal done.

## Non-goals
- Training or shipping a Claude watermark detector
- Changing existing `PROMPTS` strings
- Treating last-1 style shift as a watermark, or last-4 as Anthropic’s detector
- Editing the `synthid-text` checkout except `pip install -e … --no-deps` from the lab venv
- Reimplementing `detector_mean`; inverting keys or the SHA-256 IV; downloading DIPPER
- A 7-day Grok interval loop (host launchd already owns Wed/Fri/Sun 04:00)
- Rewriting historical LOGBOOK text
- Secrets on argv or in git (`*-KEY.conf`, `.env`, `.browser-profile/`)

## Assumed scope
Work only in `/Users/jens/kod/text-watermark-tools`. Reuse `python -m text_watermark_tools resample` (collect via `scripts/collect_claude_premark.py --no-seed --assumed-watermark rumored`, pair, leave-one-out, append-only logbook). Public `score` is the wrong instance for Claude. English in new notes. Collection needs the Mac awake and Chrome logged in at claude.ai.

The 2026-08-21 04:00 launchd fire already logged `n_collected=0` and created an empty `experiments/claude-sample-2026-08-21` with no `manifest.jsonl`. Retry with `--new-dir experiments/claude-sample-2026-08-21` so a second empty `21b` is not allocated. Skip last-1/last-4 when fewer than two pairs exist. `collect_into` uses `check=False`, so a failed scrape can still append a zero-text row — do not rewrite that row; append a later note.

## Risks / Contradictions
- `/goal` does not take a markdown path. Name `goal-plan-260821.md` in the objective string. The harness plan is always `<session>/goal/plan.md`. Run `/goal` from the lab cwd, not the DeepMind `synthid-text` checkout.
- `new_sample_dir` would next create `claude-sample-2026-08-21b` because `claude-sample-2026-08-21` already exists. Reuse `--new-dir` unless a second same-day sample is intended.
- osascript times out after 30s on Chrome open; launchd stderr may not say whether the Mac was asleep or Chrome lacked Accessibility.
