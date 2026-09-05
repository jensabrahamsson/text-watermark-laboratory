# Makefile for the technical report.
# Default: Tectonic (XeTeX), which is the engine used for the dated PDF.
# Optional: pdfLaTeX/BibTeX via `make pdflatex` when those binaries exist.

TECTONIC = tectonic
PDFLATEX = pdflatex
BIBTEX = bibtex
REPORT = ../report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf

all: tectonic

# --keep-logs writes main.log (engine Overfull / undefined-ref lines).
# compile.log is Tectonic stdout/stderr. -X compile does not write tectonic.log.
tectonic: main.tex references.bib
	$(TECTONIC) -X compile --keep-logs main.tex > compile.log 2>&1 || (cat compile.log; exit 1)
	@perl -i -pe 's/[ \t]+$$//' compile.log

pdflatex: main.tex references.bib
	$(PDFLATEX) main.tex
	$(BIBTEX) main
	$(PDFLATEX) main.tex
	$(PDFLATEX) main.tex

# Fail on undefined references/citations and Overfull \hbox.
qa: tectonic
	@test -s compile.log
	@test -s main.log
	@if grep -E 'undefined (references|citations)|There were undefined references|Citation .* undefined' main.log compile.log; then \
		echo "QA fail: undefined references/citations in main.log"; exit 1; \
	fi; \
	if grep -F 'Overfull \hbox' main.log compile.log; then \
		echo "QA fail: Overfull \\hbox in main.log"; exit 1; \
	fi; \
	echo "QA ok: main.log compile.log"

publish: qa
	cp -f main.pdf $(REPORT)
	@echo "wrote $(REPORT)"

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz

distclean: clean
	rm -f main.pdf

.PHONY: all tectonic pdflatex qa publish clean distclean
