# Makefile for the technical report.
# Default: Tectonic (XeTeX), which is the engine used for the dated PDF.
# Optional: pdfLaTeX/BibTeX via `make pdflatex` when those binaries exist.

TECTONIC = tectonic
PDFLATEX = pdflatex
BIBTEX = bibtex
REPORT = ../report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf

all: tectonic

tectonic: main.tex references.bib
	$(TECTONIC) -X compile main.tex

pdflatex: main.tex references.bib
	$(PDFLATEX) main.tex
	$(BIBTEX) main
	$(PDFLATEX) main.tex
	$(PDFLATEX) main.tex

# Fail on undefined references/citations and Overfull \hbox.
qa: tectonic
	@test -s tectonic.log || test -s main.log
	@log=$$(ls -t tectonic.log main.log 2>/dev/null | head -1); \
	if grep -E 'undefined (references|citations)|There were undefined references|Citation .* undefined' "$$log"; then \
		echo "QA fail: undefined references/citations in $$log"; exit 1; \
	fi; \
	if grep -F 'Overfull \hbox' "$$log"; then \
		echo "QA fail: Overfull \\hbox in $$log"; exit 1; \
	fi; \
	echo "QA ok: $$log"

publish: qa
	cp -f main.pdf $(REPORT)
	@echo "wrote $(REPORT)"

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz

distclean: clean
	rm -f main.pdf

.PHONY: all tectonic pdflatex qa publish clean distclean
