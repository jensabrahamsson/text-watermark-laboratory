# Scientific Paper: Key-Free Watermark Indication via Empirical Contrast

This directory contains the self-contained \LaTeX{} manuscript for the scientific report:

> **Key-Free Watermark Indication via Empirical Contrast: Population-Level Distinguishability and the Isolated-Text Boundary on SynthID-Text**
>
> **Author:** [jensabrahamsson](https://github.com/jensabrahamsson)  
> **Date:** September 2026

---

## Files

- [`main.tex`](main.tex): The primary \LaTeX{} manuscript, structured in standard academic journal/conference format.
- [`references.bib`](references.bib): Canonical Bib\TeX{} bibliography containing all citations (Dathathri et al., Kirchenbauer et al., Christ et al., Zhang et al., Jovanovi{\'c} et al., Kuditipudi et al., Wang et al., etc.).
- [`Makefile`](Makefile): Automated build script for `pdflatex` / `latexmk`.

---

## How to Compile

### 1. Locally with TeX Live or MacTeX
Run:
```bash
make
```
or manually:
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### 2. On Overleaf
1. Compress the directory into a zip file:
   ```bash
   zip -r paper.zip paper/main.tex paper/references.bib
   ```
2. Upload `paper.zip` as a New Project on [Overleaf](https://www.overleaf.com).
3. Select `main.tex` as the root document and compile.

---

## Key Content & Scientific Claims Documented

1. **The Central Discovery (Two-Grain Distinction):**
   - **Population Grain (Prompt-Group Ranking):** Proves that an empirical log-likelihood ratio test statistic on matched marked/unmarked generations reliably distinguishes watermark presence across prompt groups: **9/12** on original 12-LOO stems (10/12 with 0.02 margin), **36/36** on 36 topic families ($\mathrm{AUC} = 0.930$), and **99/100** on 100 new GPT-2 families (Lock A). Cross-generator transfer achieves **88/100** on DistilGPT-2 and **95/100** on Qwen2-1.5B.
   - **Isolated Grain (Single-Document Classification):** In contrast, evaluating an isolated text against zero yields only **25/48** (52.1\%, 95\% Clopper--Pearson interval $[0.372, 0.667]$ overlapping chance).

2. **Why a Fixed Key Leaves a Trace:**
   - Formal mathematical derivation of the **Two-Grain Concentration Theorem**: Central limit drift yields exponential concentration for prompt-group means ($\mathrm{Var} \sim \mathcal{O}(1/M)$), while single-text evaluations are dominated by sequence variance ($\mathrm{SNR} \ll 1$).
   - Proof that isolated recall is strictly bounded by opening context support. Leftover files with no opening atom overlap perform at chance (**10/20 vs 11/20**).

3. **Methodological Rigor & Corrections:**
   - Truncated-context overcount correction: documents the shift from pre-fix 10/12, 29/48 to recount 9/12, 25/48.
   - Disproves Laplace occupancy bias: demonstrates that observed-token backoff (`postokhits`) eliminates spurious detections.
   - Key-free argmax-snap watermark scrubbing: drops official keyed detector scores from 0.62 to chance (0.50) without knowledge of keys.

4. **Cryptographic Impossibility Reconciliation:**
   - Fully reconciles results with Christ et al. (2024) and Zhang et al. (2024), explaining why population contrast does not violate single-sample indistinguishability bounds.
