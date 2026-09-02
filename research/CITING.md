# Citation convention

Prose in this repository uses **author–year** (Harvard), the same family as
Nature and most CS technical reports. The canonical machine-readable list is
[references.bib](references.bib). Critical annotations — what each source
claims, and what it is *not* for this lab — are in
[annotated-bibliography.md](annotated-bibliography.md). Narrative placement
is [related-work.md](related-work.md).

This is the citation layer for a future research report. The report
author line is **Jens Abrahamsson, Master of Science**. It is **not**
the dissertation itself. Do not write `thesis/`. Do not invent papers. Prefer the archival venue
(journal or proceedings) over arXiv when both exist. Label preprints and
web pages as such. The locked abstract (shop window: what is new first) is
[abstract.md](abstract.md). In-text forms:

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
(**9/12**, **25/48**, **36/36**, lock A **99/100**) are this repository's
data, not a paper. Pre-fix **10/12** / **29/48** stay in historical JSON.

## Measurements, indications, theorems

Do not mix these sentence types. Mixing them is not a result.

| Kind | What it is | What this laboratory may write |
|---|---|---|
| Theorem | A proof about a stated construction or oracle | Cite Christ et al. (2024) and Zhang et al. (2024) for *their* claims. This laboratory **did not refute** those theorems. |
| Measurement | A protocol, a grain, a count, raw JSON | “Under protocol P on instance I and generator G, statistic T was *k*/*n*.” |
| Indication | A measurement that is consistent with a hypothesis and does not prove a theorem | Observation + scope + hypothesis + explicit non-claim. |
| Slogan | Informal collapse of a theorem onto a different object | Not a result. Do not write it as one. |

Scientific form for an indication:

1. **Observation.** Protocol, instance, generator, grain, *k*/*n*, `used_keys`.
2. **Scope.** What was held out; what was not measured (production Gemini, isolated file, other schemes).
3. **Hypothesis.** One sentence the observation is consistent with.
4. **Non-claim.** What the observation does *not* establish.

Example that is allowed: under the frozen lock A protocol on `public-deepmind-30` GPT-2 twins, prompt-group interpolate ranking was **99/100**. That is consistent with a learnable next-token footprint of this tournament instance without detector keys. It does not refute Christ et al. (2024) (different construction). It does not refute Zhang et al. (2024) (different oracles; this lab did not run a quality-preserving mixing attack). It does not establish isolated-file detection (**25/48**).

Forbidden:

- “We disproved Christ et al. (2024)” or “we disproved Zhang et al. (2024).”
- “**99/100** is a distinguisher of the kind their theorem forbids for *their* scheme.” This laboratory did not instantiate that scheme.
- “Key-free detection is possible” as an unscoped theorem.
- “Key-free detection fails” as a collapse of isolated **25/48** onto prompt-group **99/100**.
- Treating a frontier-model sketch as a proof.

Allowed clustered descriptions of **already-opened** scores, when they
change a claim and are labelled as such:

- Clopper–Pearson intervals on prompt-win or isolated-sign counts
  (Clopper & Pearson, 1934). Isolated **25/48** is **[0.372, 0.667]**
  and includes ½. Hard last-4 **9/12** includes ½; margin-0.02
  **10/12** does not. That is why both 9/12 and 10/12 are reported.
- Exact McNemar / binomial on discordant **prompt-family** signs
  (McNemar, 1947), directed at the frozen ranking endpoint. Absolute
  H2 0:4 versus 16:32 is **86 / 13 / 1 / 0**; one-sided p ≈ 0.00092.
- `permutation_prompt_sign_p`: sign-flip on prompt-mean(marked −
  unmarked). Prompt family is the unit.

These are not a second freeze, not a new `probe --methods` name, and
not a theorem. Leave-one-prompt-out tables share training mass, so
families are weakly dependent. Independent binomial intervals on two
**paired** windows are not a test of those windows. Anytime-valid /
e-value machinery does not apply after a one-shot freeze-and-open.
If the p-value does not change a claim beyond the frozen count, omit
it. Do not paste a language-model derivation as a proof that
tournament sampling is distinguishable in the sense of Christ et al.
(2024).

A complexity-theoretic proof that tournament sampling is key-free distinguishable, in the sense of Christ et al. (2024), would be a different paper. This notebook does not contain that proof. Placement of the theorems relative to the measurements: [related-work.md](related-work.md).

## Manuscript position

The measurements here are a **strong empirical notebook**, interesting
to the field. They are **not field-defining** and **not a finished
conference paper**. Position the contribution as a cheap count-table
LR with an exact auditor (key-free, not reference-free) and two grains
(population ranking vs isolated **25/48**). The honest next artifact is
a workshop, artifact, or focused empirical report, not `thesis/` and
not a slogan. Lock: [threat-model.md](threat-model.md).
