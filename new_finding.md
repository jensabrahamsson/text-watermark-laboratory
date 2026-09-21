# Longer hash history collapses key-free body ranking to chance

This note records one empirical enlargement of the key-free hole. It is
not a new `probe --methods` name, not leftover targeting, not key
recovery, and not a replacement of isolated hard last-4 **25/48**.
`used_keys=false` on every command below.

Headlines stay **9/12**, **25/48**, and **36/36**. Confirmatory lock A
interpolate last-4 on public `ngram_len=5` ($\Hw=4$) stays **99/100**.
PROTOCOL-next-longctx already opened $\Hw=12$ interpolate as **76/100**
and called that attenuation, not collapse. The missing grain is the
**file body**.

## The hole, stated

On the same GPT-2 public-key twins, leave-one-family-out interpolate
last-4 **ranks the second half of the file 93/100 when the mixin hash
history is $\Hw=4$, and 50/100 (AUC 0.501) when it is $\Hw=12$**.

Full-file $\Hw=12$ interpolate **76/100** is therefore not a weaker copy
of the same full-file reader. Tokens $[64{:}128)$ are chance. Tokens
$[0{:}4)$ still rank (**86/100** interpolate, **96/100** tokhits). Shared
4-gram `hits` can look even stronger on the whole file (**91/100**)
because that scorer ignores unseen body 4-grams and is then almost the
opening window (**95/100** at $[0{:}4)$, **53/100** at $[64{:}128)$).

An unmarked 2-versus-2 placebo on the public $\Hw=4$ 100-family pile is
chance (interpolate **57/100**, opening windows **49–51/100**). The
opening rank is not a table-construction artifact. It is the same
one-liner occupancy already decoded by `atoms` (`'The' → ' house'`,
`'The' → ' doctor'`). Isolated leftover files without those openings
remain the isolated-file hole. After $\Hw=12$, that hole is the bulk of
an ordinary 128-token string, not only a leftover slice.

This does **not** refute Christ et al. (2024) or Zhang et al. (2024).
It does not say prompt-group ranking on public $\Hw=4$ is noise. It says
key-free count-table detection of this mixin, away from reused openings,
does not survive a longer hash window on the same prompts.

## What was already on disk (no new pair)

| Corpus | Path |
|---|---|
| Public $\Hw=4$ 100×4 twins | `experiments/2026-09-01-pair-100x4/` |
| Public $\Hw=12$ 100×4 twins | `experiments/2026-09-03-pair-100x4-ngram13/` |
| $\Hw=12$ interpolate atoms | `experiments/2026-09-03-atoms-100x4-ngram13/results.md` |
| Public $\Hw=4$ interpolate atoms | `experiments/2026-09-03-atoms-100x4-public-loo/results.md` |
| $\Hw=12$ full-file interpolate | `experiments/2026-09-03-probe-100x4-ngram13-hard-last4/` (**76/100**) |
| Public $\Hw=4$ absolute windows through 32:64 | `experiments/2026-09-01-probe-100x4-hard-windows-absolute/` (32:64 interpolate **85/100**) |

Committed atoms already showed the mean token $\Delta$ dying after the
opening under $\Hw=12$:

| window | $\Hw=12$ marked $\Delta$ | $\Hw=4$ marked $\Delta$ |
|---|---|---|
| 0:4 | +2.712 | +1.756 |
| 4:16 | +0.619 | +1.604 |
| 16:32 | −0.009 | +0.455 |
| 32:64 | +0.017 | +0.256 |
| 64:128 | +0.008 | +0.174 |

Mean $\Delta$ is not prompt ranking. The commands below convert those
windows into the same strict `>` prompt-win count used everywhere else.

## Command 1 — $\Hw=12$ windows (the body collapse)

Do not overwrite `experiments/2026-09-03-probe-100x4-ngram13-hard-last4/`.
Write to a new directory. Flags match that freeze (`--context-len 4`,
`--skip-hashpool`, default `--pos-bucket 16`, no `--include-first`).
`unigram`, `hits`, and `tokhits` are existing method names.

```bash
source .venv/bin/activate
python -m text_watermark_tools probe experiments/2026-09-03-pair-100x4-ngram13 \
  --methods unigram,hits,tokhits,interpolate,hard --context-len 4 --skip-hashpool \
  --windows 0:4,4:16,16:32,32:64,64:128 \
  --out-dir /tmp/probe-ngram13-windows
```

Check `used_keys=false` in the printed header. Full-file interpolate must
still be **76/100** (same reader as the freeze). Then read the window
table in `/tmp/probe-ngram13-windows/results.md`.

Expected window prompt wins (strict `>`, 100 families):

| window | unigram | hits | tokhits | interpolate | hard |
|---|---|---|---|---|---|
| 0:4 | 90/100 | 95/100 | **96/100** | **86/100** | 82/100 |
| 4:16 | 76/100 | 39/100 | 33/100 | 75/100 | 47/100 |
| 16:32 | 70/100 | 49/100 | 48/100 | 57/100 | 57/100 |
| 32:64 | 62/100 | 61/100 | 57/100 | 57/100 | 55/100 |
| 64:128 | 59/100 | 53/100 | 63/100 | **50/100** | 59/100 |

Expected full-file prompt wins on the same run:

| method | prompt wins | file AUC | marked `lr>0` | unmarked `lr≤0` |
|---|---|---|---|---|
| unigram | 79/100 | 0.654 | 238/400 | 250/400 |
| hits | **91/100** | 0.843 | 332/400 | 255/400 |
| tokhits | **91/100** | 0.838 | 332/400 | 258/400 |
| interpolate | **76/100** | 0.666 | 267/400 | 222/400 |
| hard | 66/100 | 0.579 | 215/400 | 221/400 |

Holdout first lines that pin the collapse and the opening residual:

```text
# /tmp/probe-ngram13-windows/window-64-128/interpolate/holdout.md
prompts_marked_above=50 ... auc=0.501 perm_p=0.1949 ... prompt_sign_p=0.2004
pos>0=184/400 neg<=0=212/400

# /tmp/probe-ngram13-windows/window-0-4/tokhits/holdout.md
prompts_marked_above=96 ... auc=0.901
pos>0=313/400 neg<=0=308/400
```

Do **not** sell full-file hits **91/100** or tokhits **96/100** at $[0{:}4)$
as replacing **25/48**. Those ranks are the opening window. Interpolate
$[64{:}128)$ is **50/100**, AUC **0.501**, isolated **184/400 vs 212/400**
(balanced accuracy 396/800).

## Command 2 — public $\Hw=4$ tail (the contrast)

The opened absolute H2 dump stops at 32:64 (**85/100**). This command
adds the matching second-half window on the same public 100×4 pile.

```bash
python -m text_watermark_tools probe experiments/2026-09-01-pair-100x4 \
  --methods interpolate --context-len 4 --skip-hashpool \
  --windows 64:128 \
  --out-dir /tmp/probe-public100-w64-128
```

Expected: window 64:128 interpolate **93/100**, AUC **0.726**,
`pos>0=259/400`, `neg<=0=258/400`, `prompt_sign_p=0.0004998`,
`used_keys=false`. Full-file interpolate on that printout remains
**99/100** (the tables are the lock A reader; the new information is the
window row).

```text
# /tmp/probe-public100-w64-128/window-64-128/interpolate/holdout.md
prompts_marked_above=93 ... auc=0.726 perm_p=0.0004998 ... prompt_sign_p=0.0004998
pos>0=259/400 neg<=0=258/400 mean_pos=0.1741 mean_neg=-0.1076
```

That mean gap is the atoms 64:128 row for public $\Hw=4$ (+0.174 vs
−0.108). Under $\Hw=12$ the same window is +0.008 vs −0.013 and ranks
**50/100**.

## Command 3 — unmarked 2-versus-2 placebo

Same public 100 families, no mixin on either side. Draws 1–2 of
`*-unmarked-gen*.txt` are copied to `*-marked*.txt` names so `load_twins`
can read them. Draws 3–4 stay unmarked. This is not a `pair()` run.

```bash
python - <<'PY'
from pathlib import Path
src = Path("experiments/2026-09-01-pair-100x4")
dst = Path("/tmp/placebo-100x4-unmarked-2v2")
dst.mkdir(parents=True, exist_ok=True)
for prompt in sorted(src.glob("*-prompt.txt")):
    stem = prompt.name[: -len("-prompt.txt")]
    files = [src / f"{stem}-unmarked-gen.txt"] + [
        src / f"{stem}-unmarked-gen-{i}.txt" for i in (2, 3, 4)
    ]
    if not all(p.is_file() for p in files):
        raise SystemExit(f"missing unmarked draws for {stem}")
    (dst / f"{stem}-prompt.txt").write_text(prompt.read_text())
    (dst / f"{stem}-marked.txt").write_text(files[0].read_text())
    (dst / f"{stem}-marked-2.txt").write_text(files[1].read_text())
    (dst / f"{stem}-unmarked-gen.txt").write_text(files[2].read_text())
    (dst / f"{stem}-unmarked-gen-2.txt").write_text(files[3].read_text())
print("wrote", dst)
PY

python -m text_watermark_tools probe /tmp/placebo-100x4-unmarked-2v2 \
  --methods unigram,hits,tokhits,interpolate,hard --context-len 4 --skip-hashpool \
  --windows 0:4,16:32,64:128 \
  --out-dir /tmp/probe-placebo-100x4-unmarked-2v2
```

Expected full-file prompt wins (200 files per side, 2 draws):

| method | prompt wins | file AUC |
|---|---|---|
| unigram | 40/100 | 0.446 |
| hits | 46/100 | 0.482 |
| tokhits | 44/100 | 0.489 |
| interpolate | 57/100 | 0.542 |
| hard | 44/100 | 0.448 |

Opening 0:4 is **49/100** unigram, **51/100** hits, **50/100** tokhits,
**49/100** interpolate. If those opening ranks were a generic 100-family
split effect, they would appear here. They do not.

## How to read the three commands together

1. Public $\Hw=4$, tokens $[64{:}128)$: interpolate ranks **93/100**.
   Key-free last-4 still sees a body footprint when hash history is short.
2. Same prompts, mixin `ngram_len=13` ($\Hw=12$), tokens $[64{:}128)$:
   interpolate ranks **50/100**, AUC **0.501**. The body footprint is gone.
3. $\Hw=12$ tokens $[0{:}4)$ still rank (tokhits **96/100**). Full-file
   interpolate **76/100** is that opening plus Witten–Bell backoff through
   a chance-like tail. Full-file hits **91/100** is the opening with the
   tail dropped.
4. Unmarked-versus-unmarked does not reproduce the opening rank.

So the possibility of key-free detection **without detector keys but with
matched twins** is narrower than “76/100 attenuation.” It remains a
population ranking of **reused openings** under a longer hash window, and
it is chance on the rest of the string. Isolated-file detection of a
held-out 128-token file that does not copy those openings is not a
separate later failure; it is the same coverage bound, now applying to
in-family tails as well.

## What this is not

- Not a replacement of **25/48**, **9/12**, **36/36**, or lock A **99/100**.
- Not a claim that $\Hw=12$ official keyed detection failed (it is
  **400/400** above 0.55 on these twins).
- Not leftover targeting of the original 12.
- Not a new scorer.
- Not cryptographic undetectability of Christ et al. (2024). The
  construction here is still public-deepmind-30 tournament sampling.
- Not a proof about production Gemini. The public mixin’s short $\Hw=4$
  body rank (**93/100** at 64:128) is real on this pile; tripling $\Hw$
  removes it.

## Why this enlarges the hole rather than restating leftover

Leftover protocols already showed occupancy-free isolated sign at chance
on files whose openings were absent from train. Those were a slice of the
original 12. PROTOCOL-next-longctx then reported $\Hw=12$ interpolate
**76/100** as attenuation of the *full-file* prompt grain.

The enlargement is the window split of that 76/100: the residual is the
opening; the in-family tail is **50/100**. Public $\Hw=4$ on the same
token slice is **93/100**. Key-free finished-string detection of this
mixin, once contexts stop colliding, has nothing left to read in the
body even when the auditor still holds matched marked/unmarked twins
from 99 other families.
