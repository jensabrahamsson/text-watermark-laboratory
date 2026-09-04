# Report Revision Plan — 2026-09-05

## Review baseline

This review covers all 28 pages of
`report/Abrahamsson-2026-09-04-paired-reference-key-free-indication.pdf`, built
from the latest `origin/main` at commit `ed222a19`.

The scientific core is strong. The main remaining issues are overfull lines, an
unreadable artifact appendix, several undersized figure elements, and a narrative
that has become more defensive and expansive than the central result requires.

## 1. Lock the scientific message

Preserve the following hierarchy in `paper/main.tex`:

- We have built an indicator for watermark presence without the detector keys.
- The primary group-ranking result is 9/12, or 10/12 with the descriptive 0.02
  comparison margin.
- The isolated hard-sign sensitivity is 25/48; the complete balanced matrix is
  47/96.
- The 36/36 and 99/100 results are confirmatory group-level results, not evidence
  for universal isolated-file detection.
- Later generator, construction, and window results remain boundary and
  mechanistic tests. They do not replace the 25/48 endpoint.

Do not recompute experiments or alter historical result dumps as part of this
revision.

## 2. Tighten the narrative

- Reduce the plain-English summary to one compact paragraph without internal
  editorial commentary or a long list of forward references.
- Keep the core results in the abstract, but move the 20/20 occupancy-bound result
  and similarly secondary details into the results section.
- Replace repeated variants of "does not replace 25/48" with one explicit scope
  convention near the first isolated-file result, supplemented only where a later
  result would otherwise be easy to misread.
- Rename Section 9 to a title such as "Preregistered Boundary Tests."
- Retain the synthesis of longer context, other generators, and other watermark
  constructions in the main text. Move exhaustive matrices and the rankpath
  cemetery into the appendix or the machine-readable artifact manifest.
- Keep the distinction between group ranking and isolated classification explicit
  in prose, captions, and table headings.

## 3. Repair the concrete layout defects

- Convert the current mixed "Algorithm 1" / "Figure 1" object into a genuine
  algorithm caption type and update its references.
- Add `\FloatBarrier` at suitable section boundaries so tables and figures remain
  close to their first discussion and do not interrupt the following section.
- Replace `\sloppy` and `sloppypar` with structured tables or lists and local
  `\RaggedRight` formatting.
- Eliminate every overfull line, especially those on the current pages 17–18 and
  22–25.
- Move the overlapping annotation in the page-20 histogram into its caption.
- Enlarge the smallest labels in the method figures and verify print readability.
- Shorten figure and table captions, moving methodological explanations into the
  body text.
- Preserve redundant shape, line, and text cues so figures remain interpretable in
  grayscale.
- Refine the central results table without changing values or sample units: make
  group-ranking and isolated-file columns visually distinct and move lengthy
  qualifications into nearby prose.

## 4. Rebuild the artifact appendix

The current multi-page, fully justified path prose is the report's most serious
typographic problem.

- Replace it with a compact table containing experiment, lock or freeze, headline
  metric, and shortened commit or artifact hash.
- Keep `paper/artifacts.json` as the complete machine-readable registry.
- Include only headline artifacts in the PDF and point readers to the manifest for
  the exhaustive list.
- Use line-breaking code blocks for reproduction commands.
- Use semantic links in prose instead of raw repository paths.
- Render any unavoidable visible paths in ragged-right, breakable code formatting,
  never as justified prose.

## 5. Normalize the bibliography

In `paper/references.bib`:

- Verify titles, years, DOIs, URLs, and access dates against primary sources.
- Move argumentative or report-specific commentary out of bibliography entries and
  into the body text or footnotes.
- Standardize capitalization and web-reference metadata.
- Preserve the author–year citation style and ragged-right bibliography layout.
- Do not invent or infer missing papers or bibliographic facts.

## 6. Make the PDF build reproducible

- Add a documented Tectonic target to `paper/Makefile`, because Tectonic is the
  engine currently available and used by the successful build.
- Retain a documented pdfLaTeX/BibTeX route if both build paths are intended to be
  supported.
- Add a QA target that fails on undefined references, missing citations, and
  overfull boxes.
- Document the exact publication step that writes the dated PDF under `report/`.
- Treat the artifact manifest as the source of truth instead of duplicating its
  complete contents manually in LaTeX.
- Keep generated build logs out of the evidence chain unless they are regenerated
  and checked as part of the documented build.

## 7. Final acceptance checks

The revision is complete only when all of the following hold:

- The report tests pass in the documented environment.
- The PDF build has no undefined references or citations.
- The build has zero `Overfull \hbox` warnings and no visibly stretched paragraphs.
- Every page has been rendered and visually inspected.
- No text, path, figure, or table crosses the page margins.
- Figures remain readable at normal print size and in grayscale.
- Cross-references, hyperlinks, and PDF bookmarks work.
- All fonts are embedded.
- Title, author, language, and other PDF metadata are correct.
- Text extraction has a sensible reading order.
- No experimental output, frozen result, or historical dump has changed.
- `git diff --check` passes.

The current paper-test baseline is 32 passing tests and one environment-dependent
failure because `synthid_text` is not installed. Resolve that by documenting and
using the required editable `--no-deps` installation; do not weaken or fake the
test.

## Suggested implementation sequence

1. Refine the scientific narrative and scope language.
2. Rework floats, figures, tables, paths, and the artifact appendix.
3. Normalize bibliography metadata and prose references.
4. Add the reproducible build and layout-quality gates.
5. Rebuild, run tests, render every page, and complete visual QA.

Suggested commit messages:

- `Refine the report narrative and scope claims`
- `Rework report layout and artifact appendix`
- `Add reproducible PDF build and layout checks`
