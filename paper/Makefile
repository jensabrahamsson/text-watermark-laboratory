# Makefile for compiling the scientific paper

PDFLATEX = pdflatex
BIBTEX = bibtex
LATEXMK = latexmk

all: main.pdf

main.pdf: main.tex references.bib
	@which $(LATEXMK) > /dev/null 2>&1 && $(LATEXMK) -pdf main.tex || ( \
		$(PDFLATEX) main.tex && \
		$(BIBTEX) main && \
		$(PDFLATEX) main.tex && \
		$(PDFLATEX) main.tex \
	)

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz

distclean: clean
	rm -f main.pdf

.PHONY: all clean distclean
