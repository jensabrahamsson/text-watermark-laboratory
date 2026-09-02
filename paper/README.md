# Scientific report: key-free watermark indication

LaTeX manuscript for a focused empirical report:

> **Key-Free Watermark Indication via Empirical Contrast:**
> Prompt-Group Ranking and the Isolated-Text Boundary
> on a Public SynthID-Text Instance
>
> **Author:** [Jens Abrahamsson](https://github.com/jensabrahamsson)
> **Date:** September 2026

This is a workshop-style empirical report of a checked-in notebook, not
a claim that the laboratory invented key-free detection or refuted
Christ et al.\ (2024) or Zhang et al.\ (2024).

## Files

- [`main.tex`](main.tex): article (abstract through bibliography).
- [`references.bib`](references.bib): BibTeX (author–year keys).
- [`Makefile`](Makefile): `pdflatex` / `latexmk` build.
- [`compile.log`](compile.log): last local build attempt (no MacTeX on this host).

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
   Key-free, not reference-free, not web-text detection.

2. **Two grains.** Prompt-group ranking can work; isolated 128-token
   sign at `t=0` is chance-like.
   - Ranking: **9/12** (hard last-4 12-LOO; **10/12** with margin 0.02),
     **36/36** in-domain hits (AUC **0.930**), lock A **99/100**,
     Distil lock B **88/100** (1 tie), Qwen lock B **95/100**.
   - Isolated: **25/48**, Clopper–Pearson **[0.372, 0.667]** includes ½.
   - A ranking win can be “unmarked more negative” (garden: 0 isolated TPs).

3. **Leftover / scrub.** Leftover last-4 **10/20 vs 11/20**; official
   leftover **20/20**. Argmax snap **0.622 → 0.499**. Distil official
   **70/100** is watermark strength, not only the indicator.

4. **Math.** Empirical LR uses $\hat P$, not $P_w$. Concentration is a
   sketch ($O(1/M)$ for group means). No Hoeffding/SNR theorem.

Pre-fix **10/12** / **29/48** stay historical. Isolated-file research is
not finished.
