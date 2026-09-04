# Scientific report: paired-reference key-free indication

LaTeX manuscript for a focused empirical technical report:

> **Paired-Reference, Key-Free Indication of a Public SynthID-Text Instance**
>
> **Author:** [Jens Abrahamsson](https://github.com/jensabrahamsson), MSc
> **Date:** 4 September 2026

This is a workshop-style empirical report, not a claim that the
laboratory invented key-free detection or refuted Christ et al. (2024)
or Zhang et al. (2024). The intended venue is a technical report. Group
ranking under a strong paired oracle is the positive result; the
prespecified isolated-file threshold is not. A plain-English lead sits
above the dense abstract. The public \texttt{get\_gvals} docstring
(``lowest three bits'') does not match the installed
\texttt{(hash >> 30) \% 2}; the report trusts the code. Hub revisions
were not recorded at generation; published scores read committed
strings. The laboratory's current \texttt{gpt2} cache is
\texttt{607a30d783dfa663caf39e06633721c8d4cfcd7e}.

## Files

- [`main.tex`](main.tex): article (abstract through bibliography).
- [`references.bib`](references.bib): BibTeX (author–year keys).
- [`Makefile`](Makefile): `pdflatex` / `latexmk` build.
- [`compile.log`](compile.log): last successful local `tectonic` build
  (28 A4 pages, git `8ea1d0c`). Prior compile `9d6677c`. Older compile `a50bc3f`. Compile `4c31077`. Compact SHA `ce5f168`. Open SHA `aea3d76`.
  Ingress SHA `7eea455`. Current PDF is
  [`../report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf`](../report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf)
  (overwrite in place; do not add a SHA snapshot per compile). Previous compact:
  [`../report/Abrahamsson-2026-09-04-paired-reference-key-free-indication-ce5f168.pdf`](../report/Abrahamsson-2026-09-04-paired-reference-key-free-indication-ce5f168.pdf).

Numbers are taken from this repository (`research/`, `experiments/`).
If a figure is not in those dumps, it is not in the paper.

## How to compile

```bash
make
```

or

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If `pdflatex` is missing, `make` fails; leave the TeX sources in git
anyway. Overleaf: upload `main.tex` and `references.bib`.

## Claims the manuscript actually makes

1. **Paired auditor (strong oracle).** Matched marked/unmarked twins.
   Key-free, not reference-free, not web-text detection. Public
   reference keys exist and are withheld at scoring time.

2. **Two grains.** Prompt-group ranking can work; isolated 128-token
   decisions at $\tau=0$ do not.
   - Ranking: exploratory hits **36/36** (AUC **0.930**); prospectively
     specified lock A leave-one-family-out **99/100** (mean $D_p=0.520$);
     corrected original hard last-4 **9/12**. Distil lock B **88/100**
     (1 tie), Qwen lock B **95/100**, native tables.
   - Isolated original 12, hard $\tau=0$: TP 25, FN 23, TN 22, FP 26;
     sensitivity 25/48, specificity 22/48, precision **25/51**
     $[0.348,0.634]$; balanced accuracy **47/96** ($48.96\%$). File AUC
     **0.590**. Prompt-clustered sign-flip of balanced accuracy is
     chance ($p=0.703$).
   - A ranking win can be “unmarked more negative” (garden: 0 isolated TPs).

3. **Leftover / perturbation.** Leftover last-4 **10/20 vs 11/20**;
   official leftover **20/20**. Argmax snap **0.622 → 0.499** is a
   mechanistic perturbation, not a fluent attack. Distil official
   first-draw **70/100** is a keyed control with a different unit from
   four-draw lock B (six ties; same 70 families also have marked mean
   $>0.55$ on this sample).

4. **Math.** Empirical LR uses $\hat P$, not $P_w$. Equality in
   expectation over random keys does not imply equality for one fixed
   instance. Concentration is conditional on fitted tables
   ($O(1/M)$ for group means). No Hoeffding/SNR theorem.

5. **Margin 0.02.** Descriptive sensitivity analysis only
   ($\bar\Lambda_m+0.02>\bar\Lambda_u$). Not a valid $1/2$ null test.

6. **Next lock.** Longer-context two-grain replication is frozen in
   `research/PROTOCOL-next-longctx.md` (SHA `b70986d`) before
   generation: public keys, `ngram_len=13` ($\Hw=12$), original 12
   prompts, seed 20260903. Original-12 $\Hw=12$: official first-draw
   **12/12**; interpolate and hard **6/12**; isolated hard **52/96**.
   Absolute-history 12-LOO mask-*k* remasure (same SHA) leaves hard
   prefix **5/12** and tails **9/12** unchanged versus the reindexed
   dump. Longer-history 100-family readout (not Distil/Qwen Phase B):
   interpolate **76/100** (below lock A **99/100**); isolated
   **489/800**. Figure hw12 is the paired-difference
   histogram (mean 0.156 vs lock A 0.520). Original-12 interpolate
   occupancy is **160** seen versus public $\Hw=4$ **269** seen
   (opening $[0{:}4)$ is 71 versus 84);
   100-family occupancy is **5878** versus **10158** (opening 1287 versus 1633)
   (leave-one-family-out atoms; not a detector). Isolated original-12 remains
   **47/96**; **6/12** and **76/100** are group rankings on $\Hw=12$
   twins. Body-window remasure (SHA `8283d1f`): interpolate $[64{:}128)$
   **50/100** versus public $\Hw=4$ **93/100**; opening **86/100**.
   That is not **25/48**. Qwen2-1.5B $\Hw=12$ on the 100 one-liners
   (SHA `636765c`): interpolate **76/100** (isolated **474/800**);
   hard **74/100**; official **91/100**; occupancy **3535** seen versus
   **98064** unseen (opening **1092** versus **1308**). That is not **25/48**.
   Qwen2-1.5B Aaronson on the 100 one-liners
   (SHA `a761a7d`): interpolate **100/100** (isolated **616/800**);
   hard **97/100**; official $z>3$ **99/100**; occupancy **8750** seen
   versus **92842** unseen (opening **1470** versus **930**). That is not **25/48**.

Pre-fix **10/12** / **29/48** stay historical. Isolated-file research is
not finished. Nested Youden is post hoc, not nested CV. Lock A
**99/100** is leave-one-family-out of a frozen algorithm, not a frozen
fitted detector. A Kirchenbauer green-list mixin is frozen in
`research/PROTOCOL-next-kgw.md` (SHA `8371406`; `--mixin kgw`, seed
20260904). Original-12 interpolate last-4 is **12/12** (isolated
**85/96**); occupancy **114** seen. 100-family interpolate is
**100/100** (isolated **747/800**); occupancy **4557** seen. That is
not **25/48**. Qwen2-1.5B Kirchenbauer on the 100 one-liners is named
in `research/PROTOCOL-next-kgw-qwen-100.md` (SHA `ed9fb20`) before
generation. Official first-draw $z>3$ is **90/100**. Interpolate last-4
is **96/100** (isolated **620/800**); hard is **63/100**. That lock is
not **25/48**. Distil / gpt2-medium unmarked-LM
opening rankpath 12-LOO is named in
`research/PROTOCOL-isolated-rankpath-lm.md` (SHA `d8e6f7f`). Distil-LM
isolated **32/48 vs 31/48**; medium-LM **31/48 vs 32/48**. Do not sell
**32/48** or **31/48**. gpt2-medium native opening rankpath is ranking
**6/12**, isolated **22/48 vs 30/48** (`PROTOCOL-isolated-rankpath-m12.md`,
SHA `2577771`). Do not sell **22/48**. GPT-2-small LM on gpt2-medium 12
is ranking **8/12**, isolated **20/48 vs 32/48** (`PROTOCOL-isolated-rankpath-g2m.md`,
SHA `336a1fd`). Do not sell **20/48**. Distil LM on gpt2-medium 12 is
ranking **11/12**, isolated **30/48 vs 31/48** (`PROTOCOL-isolated-rankpath-d2m.md`,
SHA `b3fd331`). Do not sell **30/48**. GPT-2-small LM on Distil 12 is
ranking **6/12**, isolated **24/48 vs 27/48** (`PROTOCOL-isolated-rankpath-g2d.md`,
SHA `d62c732`). Do not sell **24/48**. gpt2-medium LM on Distil 12 is
ranking **9/12**, isolated **30/48 vs 33/48** (`PROTOCOL-isolated-rankpath-m2d.md`,
SHA `571d4f1`). Do not sell **30/48**. Opening rankpath on generated
tokens `[4:16)` is ranking **7/12**, isolated **20/48 vs 22/48**
(`PROTOCOL-isolated-rankpath-body.md`, SHA `dbc61c5`). Do not sell
**20/48**. Distil-LM rankpath on generated tokens `[4:16)` is ranking
**6/12**, isolated **24/48 vs 23/48** (`PROTOCOL-isolated-rankpath-dbody.md`,
SHA `68b0514`). Do not sell **24/48**. gpt2-medium-LM rankpath on generated
tokens `[4:16)` is ranking **9/12**, isolated **27/48 vs 28/48**
(`PROTOCOL-isolated-rankpath-mbody.md`, SHA `3ea80e4`). Do not sell
**27/48**. Distil native rankpath on generated tokens `[4:16)` is ranking
**9/12**, isolated **25/48 vs 30/48** (`PROTOCOL-isolated-rankpath-d12body.md`,
SHA `468a66b`). Equality with **25/48** is not a win. Do not sell
**25/48**. gpt2-medium native rankpath on generated tokens `[4:16)` is ranking
**6/12**, isolated **20/48 vs 30/48** (`PROTOCOL-isolated-rankpath-m12body.md`,
SHA `37a2c43`). Do not sell **20/48**. GPT-2-small LM rankpath on Distil
generated tokens `[4:16)` is ranking **4/12**, isolated **26/48 vs 21/48**
(`PROTOCOL-isolated-rankpath-g2dbody.md`, SHA `08b89ee`). Do not sell
**26/48**. Distil LM rankpath on gpt2-medium generated tokens `[4:16)` is
ranking **11/12**, isolated **25/48 vs 33/48** (`PROTOCOL-isolated-rankpath-d2mbody.md`,
SHA `1b4c541`). Equality with **25/48** is not a win. GPT-2-small LM
rankpath on gpt2-medium generated tokens `[4:16)` is ranking **8/12**,
isolated **28/48 vs 30/48** (`PROTOCOL-isolated-rankpath-g2mbody.md`,
SHA `e677a6c`). Do not sell **28/48**. gpt2-medium LM rankpath on Distil
generated tokens `[4:16)` is ranking **9/12**, isolated **32/48 vs 25/48**
(`PROTOCOL-isolated-rankpath-m2dbody.md`, SHA `a550cb6`). Do not sell
**32/48**. GPT-2 rankpath on generated tokens `[16:32)` is ranking **7/12**,
isolated **23/48 vs 26/48** (`PROTOCOL-isolated-rankpath-mid.md`, SHA
`14afbd5`). Do not sell **23/48**. That lock is not **25/48**. GitHub tree pin: `1582a09` (100-family start `8f09aa6`).
A 2026-09-03 Claude resample vs pre-mark last-4 is **35/40** (not a
vendor detector; not **25/48**).
