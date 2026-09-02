# Citation convention

Prose in this repository uses **author–year** (Harvard), the same family as
Nature and most CS technical reports. The canonical machine-readable list is
[references.bib](references.bib). Critical annotations — what each source
claims, and what it is *not* for this lab — are in
[annotated-bibliography.md](annotated-bibliography.md). Narrative placement
is [related-work.md](related-work.md).

This is the citation layer for a future research report. It is **not** the
dissertation itself. Do not invent papers. Prefer the archival venue
(journal or proceedings) over arXiv when both exist. Label preprints and
web pages as such. In-text forms:

| Authors | Narrative | Parenthetical |
|---|---|---|
| One | Aaronson (2023) | (Aaronson, 2023) |
| Two | Wu and Chandrasekaran (2024) | (Wu & Chandrasekaran, 2024) |
| Three or more | Dathathri et al. (2024) | (Dathathri et al., 2024) |

BibTeX keys match `author+year+keyword` (for example `dathathri2024synthid`).
A later LaTeX report can compile the same `.bib` with `biblatex` (style
`authoryear`) or `natbib`. Do not switch to numeric IEEE in the markdown
notes unless the whole corpus is converted at once.

When a claim in the notes depends on a paper, cite it. Lab measurements
(10/12, 29/48, 36/36) are this repository's data, not a paper.
