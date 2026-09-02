# Deep Review of "Key-Free Watermark Indication via Empirical Contrast"

- **Review date:** 2026-09-03
- **Recommendation:** Major revision
- **Scope:** The review is deliberately limited to the report itself: the rendered 14-page PDF, `paper/main.tex`, and `paper/references.bib`. I did not inspect implementation code, experiment dumps, protocol notes, repository history, or external sources. Consequently, statements about reproducibility mean "reproducible from the report alone," and literature claims are assessed for framing and internal use rather than independently fact-checked.

## Executive assessment

The report contains a real and potentially useful empirical contribution: under a strong paired-reference audit setting, a key-free count-table score can rank marked prompt groups above matched unmarked prompt groups on the measured public SynthID-Text instance. The most persuasive evidence is not the original 9/12 result but the prospectively described 100-family result, provided that its training and evaluation topology is clarified. The report is also unusually candid about what the result is not. It repeatedly distinguishes key-free from reference-free, group ranking from isolated-file classification, one public key set from production systems, and empirical behavior from a cryptographic theorem. That restraint is a substantial strength.

The paper is not ready in its current form because several central quantities are interpreted or documented too loosely. The isolated-file headline uses marked recall (25/48) as if it were the primary classification statistic, although the same report gives 22/48 true negatives and a file AUC of 0.590. At the stated zero threshold, the complete confusion matrix implies 47/96 correct decisions, or 48.96% accuracy and balanced accuracy, while the AUC describes a different, threshold-free question. Those facts can coexist, but the paper does not yet explain the distinction cleanly enough. Likewise, the 0.02 comparison margin is not defined in the method, and a binomial interval around 10/12 cannot be compared to a 0.5 null without deriving the null success probability under the margin rule.

The second major weakness is reproducibility. The report does not say unambiguously which corpus fits each count table, whether the 100-family "confirmatory" result is a frozen-model test or leave-one-family-out refitting within the new 100 families, how Phase B tables are trained, how zero-used-token files are scored, or how the headline Witten-Bell interpolation is computed. These are not supplementary details: they determine what 99/100 and the isolated counts mean.

My recommendation is therefore **major revision, not rejection**. The report already has a defensible central result. The necessary changes would sharpen that result rather than weaken it: define the audit topology, use full classification metrics, demote or recalibrate the margin analysis, specify the primary reader mathematically, and separate prospectively locked evidence from exploratory ablations.

## The contribution as the report currently defines it

My reading of the report is as follows:

1. The auditor receives labeled marked and unmarked generations from the same prompt families and the same base generator/tokenizer, but it does not use detector keys, `hash_iv`, official g-values, or the official score at decision time.
2. The primary group-level task compares the mean empirical log-likelihood ratio of four marked draws with the mean over four unmarked draws for a held-out prompt family.
3. The isolated task applies a zero threshold to one file's empirical score, without showing its twin at test time.
4. The report's group-level evidence is 9/12 on the original hard reader, 36/36 for an in-domain hits reader, and 99/100 for confirmatory GPT-2 lock A. Native DistilGPT-2 and Qwen experiments give 88/100 and 95/100 for lock B.
5. The original hard reader gives 25/48 marked files above zero and 22/48 unmarked files at or below zero. The report treats this zero-threshold result as chance-like and explicitly declines to claim a general single-file detector.
6. Ablations argue that prompt-group ranking is not solely the pre-fix truncated-context bug, not equivalent to isolated opening-token coverage, and not evidence of key recovery. A key-free argmax perturbation reduces the official keyed mean on marked files from approximately 0.62 to 0.50, but changes most tokens and is not presented as a fluent attack.

That is a coherent research question. The paper should preserve this exact scope.

## Principal strengths

### 1. The two-grain distinction is the paper's strongest idea

The separation between prompt-group ranking and isolated-file classification is clear, important, and supported with a concrete stem-level example. Table 3 is especially effective: garden wins the group comparison with 0/4 marked files above zero, while station, office, and ferry-queue lose their group comparisons despite contributing five isolated true positives. This makes the non-equivalence of the two tasks visible rather than merely asserted.

The paper should build even more of its presentation around this table and the paired-difference geometry behind it.

### 2. The threat model is unusually candid

The report plainly states that the auditor requires marked and unmarked training twins, that this is a strong oracle, and that the method is neither reference-free nor fully blind. It also makes clear that the public DeepMind instance is not a Claude or Gemini detector. These qualifications are not buried in the final paragraph; they appear in the abstract, introduction, threat model, results, limitations, and conclusion.

### 3. Negative and inconvenient results are retained

The report does not hide the corrected 9/12 and 25/48 results, the pre-fix overcount, the chance-like leftover slice, weak transfer cases, the Distil keyed-control weakness, or the fact that multi-key replication has not begun. This is good scientific practice and gives the report credibility.

### 4. Several internal numerical checks are correct

I recomputed the following solely from values printed in the report:

| Check | Result |
|---|---:|
| Table 3 prompt wins | 9/12 |
| Table 3 isolated marked positives | 25/48 |
| Station + office + ferry-queue isolated positives | 5 |
| Table 6 covered + leftover marked positives | 15 + 10 = 25 |
| Table 6 covered + leftover unmarked true negatives | 11 + 11 = 22 |
| H3 Distil drops, lock B / lock C | 12 / 28 |
| H3 Qwen drops, lock B / lock C | 5 / 12 |
| H2 discordant-pair one-sided probability | 15/16384 = 0.0009155 |
| One-sided binomial tail for 25/48 | 0.4427167 |

The printed Clopper-Pearson intervals also match exact binomial inversion to the shown precision: 9/12 gives [0.428142, 0.945139], 10/12 gives [0.515862, 0.979137], and 25/48 gives [0.371870, 0.667134]. The numerical problem is therefore not arithmetic; it is which estimand and null model those intervals are being asked to support.

### 5. The rendered report is visually sound

All 14 pages render cleanly. Tables fit the text block, mathematical symbols are legible, fonts are embedded, page numbering is consistent, links are readable, and I found no clipping, overlap, missing glyphs, unresolved citations, or broken cross-references. The typography is already above the level of a typical internal lab note.

## Major issues requiring revision

### 1. The isolated-file conclusion is built around sensitivity, not classification performance

**Where:** Abstract; Sections 1.2, 3.3, 6.1, 6.2, 6.6, 6.7, and 8; Table 2.

The report calls 25/48 the isolated classification result. That number is only the number of marked files with score above zero, hence sensitivity at one threshold. The same table gives 22/48 unmarked files at or below zero, hence specificity. With balanced classes, the complete zero-threshold result is:

- true positives: 25;
- false negatives: 23;
- true negatives: 22;
- false positives: 26;
- sensitivity: 25/48 = 52.08%;
- specificity: 22/48 = 45.83%;
- accuracy and balanced accuracy: (25 + 22)/96 = **48.96%**.

The Clopper-Pearson interval [0.372, 0.667] is an interval for sensitivity alone. It is not an interval for classifier accuracy, balanced accuracy, or discrimination. A random classifier's sensitivity is not intrinsically 0.5; it depends on its positive prediction rate. The proper support for "the zero-threshold classifier is at chance" is the full confusion matrix and a paired or prompt-clustered analysis of accuracy or balanced accuracy.

The report also gives file AUC 0.590 with a descriptive permutation p-value of 0.040. AUC asks whether marked files tend to rank above unmarked files across all thresholds; it does not test whether threshold zero is calibrated. A weakly informative score can therefore have AUC above 0.5 while producing chance accuracy at a bad fixed threshold. The manuscript should say exactly that. Phrases such as "the same tables do not classify one 128-token file" currently overstate what the reported AUC permits. A defensible formulation is: **the prespecified zero threshold does not yield useful isolated-file decisions on this set; threshold-free file ranking is weak (AUC 0.590) and requires independent confirmation.**

The same problem recurs when transfer readers are said not to "beat 25/48." For example:

- 23/48 marked and 38/48 unmarked correct implies 61/96 = 63.54% balanced accuracy;
- 16/48 marked and 48/48 unmarked correct implies 64/96 = 66.67%;
- 24/48 marked and 41/48 unmarked correct implies 65/96 = 67.71%.

These do **not** automatically establish better detectors: some thresholds are selected post hoc, dependencies are not handled, and abstentions may be counted as negatives. But they do show that comparing marked recall alone with 25/48 is not a sufficient evaluation rule. A low-recall, high-specificity reader may be useful for a different operating point.

**Required revision:**

1. Make the 2x2 confusion matrix the primary zero-threshold isolated result.
2. Report sensitivity, specificity, balanced accuracy, precision, and AUC with prompt-clustered uncertainty.
3. Define the target operating criterion before comparing readers: balanced accuracy, recall at a fixed false-positive rate, AUC, or a selective-classification metric.
4. For abstaining readers, report coverage and conditional performance separately. Do not silently count `n_used = 0` as a confident negative.
5. Explain why the AUC permutation result and zero-threshold failure test different hypotheses.

### 2. The 0.02 comparison margin has no defined decision rule or valid chance baseline

**Where:** Abstract; Sections 1.2 and 6.1; Table 2.

Equation (1) defines a strict win, but the margin result is never defined mathematically. Because the count increases from 9/12 to 10/12, the apparent rule is a tolerance such as

\[
\Delta_p > -0.02,
\]

rather than a stricter superiority condition such as \(\Delta_p > +0.02\). If so, it is a non-inferiority or practical-equivalence rule, not the same Bernoulli trial as strict positive ranking.

Under a symmetric no-effect distribution, \(P(\Delta_p > -0.02)\) is generally greater than 0.5. Therefore the Clopper-Pearson interval [0.516, 0.979] excluding 0.5 does not establish above-chance performance under the margin rule. The null success probability must be induced by the score distribution and the exact margin rule, for example through a prompt-level sign-flip or label-permutation procedure. The choice of 0.02 also needs units, practical justification, and a statement of whether it was fixed before the original 12 scores were inspected.

For reference, the naive one-sided binomial tail is 0.072998 for strict 9/12 and 0.019287 for 10/12 under an assumed 0.5 success null. The latter calculation is not meaningful unless 0.5 is actually the correct null after applying the margin.

**Required revision:** Define the margin, justify it, and either derive its null distribution or demote it to a descriptive sensitivity analysis. Until then, remove the claim that the margin result excludes one-half from the abstract and headline table.

### 3. The training, validation, and test topology is too ambiguous for the headline 99/100 claim

**Where:** Sections 4.1, 4.3, 4.4, 6.4, 6.5, and 6.7; Tables 4 and 5.

The report says the analysis flags were frozen before generating 100 new GPT-2 families, but it does not state clearly where the fitted count tables came from. Two materially different designs are possible:

1. a fitted reader was frozen on an earlier corpus and then applied unchanged to the 100 families; or
2. the reader definition was frozen, but each of the 100 test families was scored by a table refitted on the other 99 new families.

The language "in-family," "leave-one-prompt-out," and "nested-by-stem" suggests the second interpretation. If that is correct, 99/100 is a prospective confirmation of an algorithm and evaluation protocol, not an evaluation of a frozen fitted detector. That is still valuable, but the distinction must be explicit in the abstract, methods, table caption, and conclusion.

Phase B is similarly unclear. The text calls Distil and Qwen results "native," but does not say whether each generator gets its own leave-one-family-out marked/unmarked tables or whether GPT-2 tables are transferred. H3 has a different meaning in those two cases: native refitting measures how the method behaves across generator distributions, while frozen GPT-2 transfer measures cross-generator portability.

**Required revision:** Add a protocol matrix with one row per headline result and the following columns:

| Result | Development status | Table-fitting corpus | Hyperparameter-selection corpus | Threshold-selection corpus | Evaluation corpus | Unit |
|---|---|---|---|---|---|---|
| Original 12 hard | exploratory/locked-after-correction | ... | ... | none, zero | ... | prompt/file |
| 36-topic hits | exploratory | ... | ... | ... | ... | prompt/file |
| GPT-2 lock A | prospective protocol / frozen model | ... | ... | ... | ... | prompt |
| Distil lock B/C | ... | ... | ... | ... | ... | prompt |
| Qwen lock B/C | ... | ... | ... | ... | ... | prompt |

Also include a simple fold diagram or pseudocode. The word "confirmatory" should be tied to an immutable dated protocol, commit, or appendix and should state exactly what was fixed before data generation.

### 4. The primary confirmatory reader is not specified mathematically

**Where:** Sections 4.2 and 4.4.

The paper provides a Lidstone formula and a short description of the `hard` reader, but the primary confirmatory lock A is Witten-Bell `interpolate`. No interpolation recurrence, backoff weights, support definition, or unseen-event convention is given. A reader cannot reconstruct the 99/100 analysis from the paper.

Several other method details are also missing or ambiguous:

- whether \(V\) in Equation (3) means the full tokenizer vocabulary, the union of observed next tokens, or another support;
- what happens if a context is seen in one table but unseen in the other;
- the log base and any clipping or finite-value rules;
- how a file is scored when \(n = |\mathcal I(x)| = 0\);
- whether an abstention receives score zero, no score, or a separate state;
- the exact position buckets and prefix inclusion rules;
- whether prompt tokens are available as context;
- the exact absolute-history and reindexed-window algorithms;
- the exact mapping for `rankpath`.

The current rankpath description is internally incomplete: "five-symbol ... rank (miss top-k, or rank 1-4 inside top-k)" literally accounts for a miss and ranks 1 through 4 but says nothing about candidates ranked 5 through 40. If "rank 1-4" means four bins rather than four literal ranks, list the bin boundaries.

**Required revision:** Give exact pseudocode for fitting and scoring `hard`, lock A `interpolate`, lock B `poshits`, and lock C `rankpath`. State all zero-count, zero-coverage, tie, and fallback conventions. Methods mentioned only in passing, such as hash pooling, should move to an appendix unless they support a reported result.

### 5. Core notation collides, and the context-length story is internally inconsistent

**Where:** Sections 3.1, 3.3, 4.2, 6.3, 7.3, and 7.4.

The paper reuses symbols in ways that make key claims hard to follow:

- \(k\) denotes the language model's top-k value (40), the count-table context length (4), and the mask-k ablation.
- \(t\) denotes token position in Equation (4) and apparently the decision threshold in phrases such as "at t=0."
- \(H\) denotes the watermark context, while "last-4" and `context_len=4` are used without a stable distinction between a four-token context and a four-token window.
- The vocabulary is introduced as \(\mathcal V\), while Equation (3) uses plain \(V\).
- The prose alternates between the mathematical score \(\Lambda\) and the implementation field `lr` without explicitly equating them.

There is also a concrete contradiction. Section 3.1 says `ngram_len=5` corresponds to context length \(H=4\). Section 6.3 says "Matching mixin `ngram_len = 5` (context length 5) does not beat last-4." Both cannot be the same definition. The manuscript must distinguish watermark hash history, next-token n-gram order, and count-table history length.

The opening-window description is likewise underspecified. Generated token 0 is skipped, the first \(H\) generated tokens cannot form a complete context, yet window 0:4 is a major result. It is unclear how many scored events 0:4 contains, which shorter suffixes are allowed, and whether prompt context is excluded.

**Required revision:** Reserve \(K\) for top-K sampling, \(h\) for count-table history, \(H_w\) for watermark history, \(\tau\) for decision threshold, and \(m\) for the number of masked positions. Define slices as half-open token-index intervals and state whether history preceding a slice remains visible. Correct the `ngram_len` contradiction.

### 6. The inference does not fully respect the paired and clustered design

**Where:** Sections 3.3, 5, 6.1, 6.3, 6.4, and 7.3.

The report correctly notes that prompt families are the independent ranking unit and that leave-one-prompt-out folds share training mass. It then nevertheless displays ordinary binomial intervals and uses language such as "excludes 1/2" without consistently marking those intervals as descriptive. Clopper-Pearson assumes independent Bernoulli trials with a common success probability. Shared fitted tables and deliberately selected prompt families weaken both assumptions.

The term "population grain" also suggests inference to a broader prompt population, but the prompt-sampling frame is not defined. If the 12, 36, and 100 prompts are fixed designed sets rather than random draws from a stated population, confidence intervals describe a hypothetical repeated sampling process that the paper must name.

Section 5's variance sketch needs refinement. It assumes the 2M marked and unmarked draws are independent. The experiment is repeatedly described as paired, but the report does not say whether paired generations share random seeds or sampling streams. More importantly, all held-out scores share estimated tables, so the simple O(1/M) statement is clean only conditionally on the fitted reader. Unconditionally, shared training-estimation uncertainty contributes another variance component.

A more faithful formulation is to define the within-pair contrast

\[
D_{p,j}=\Lambda(x^{(m)}_{p,j})-\Lambda(x^{(u)}_{p,j})
\]

and state conditions under which \(\operatorname{Var}(M^{-1}\sum_j D_{p,j}\mid\widehat P_m,\widehat P_u)=O(1/M)\). If marked and unmarked draws are not seed-paired, call the design prompt-matched rather than sample-paired.

**Required revision:**

1. Specify the randomization and pairing mechanism.
2. Use prompt-level paired differences as the primary group effect, with their magnitudes, not only win counts.
3. Give cluster-aware or prompt-level permutation/bootstrap uncertainty.
4. State the exact permutation scheme behind every reported p-value.
5. Add intervals for 36/36, 99/100, 88/100, and 95/100, with a dependence caveat. Under an ordinary independent-binomial model, their exact 95% intervals would be approximately [0.903, 1.000], [0.946, 1.000], [0.800, 0.936], and [0.887, 0.984], respectively; a valid final analysis should reflect the actual design rather than copy these mechanically.

### 7. "Nested Youden" is explicitly not fully nested and may leak outer-test information

**Where:** Sections 4.3, 6.4, and 6.7.

The paper commendably says that nested Youden-by-stem is a "threshold nest, not second-level nested cross-validation." That warning also means the resulting file counts should not be presented as unbiased held-out classifier performance.

As described, a threshold for target family p is selected from other families' already-held-out scores. If those other families' base scores were produced by models trained on all families except themselves, their fitted models included family p. In that common cross-validation topology, information from the outer test family can influence the data used to select its threshold. The report does not provide enough detail to determine whether this leakage occurs in every protocol, but the possibility is material.

**Required revision:** Draw the exact nesting topology. For an unbiased nested estimate, the outer fold must remove p before any model fitting or threshold selection; inner scores and thresholds must be produced only from the remaining families. Otherwise label the counts "post-hoc threshold analysis" and keep them out of detector-performance comparisons.

### 8. H3 and the keyed-control comparison support weaker claims than the prose makes

**Where:** Sections 1.1, 4.4, 6.5, and 8; Table 5.

H3 is declared to hold because raw prompt-win drops are larger for rankpath than poshits. The arithmetic is correct, but raw drops are not a formal interaction test. Lock B starts at 100/100 and lock C at 96/100 on GPT-2, creating different baselines and ceiling behavior. The same prompts are used across generators, so a paired per-prompt analysis of win/loss transitions is available in principle and would be more informative. Confidence intervals for the difference in drops are also needed.

The meaning of "generator-specific" depends on the unresolved training question. If each generator receives native refitting, the experiment measures variation in within-generator learnability. If GPT-2 tables are frozen and transferred, it measures portability. The paper currently blends these interpretations.

The keyed column presents a second problem. GPT-2's 100/100 and Distil's 70/100 appear to be first-draw file-level threshold counts, whereas lock B/C are four-draw prompt-group comparisons. Those rates have different decision units and different statistical power. Table 5 visually invites a direct comparison even though the report calls the official measure a positive control.

Calling Distil's 70/100 "watermark strength" is too categorical from the report alone. A lower keyed pass rate can reflect the interaction among watermark bias, generator distribution, repeated-context masking, score threshold, and sampling variability. "Lower official keyed positive-control pass rate" is the claim directly supported by the table.

**Required revision:** Separate keyed file-level controls from key-free group-level endpoints, define the 0.55 threshold and why it is used, show keyed score distributions rather than only pass counts, and replace raw-drop confirmation of H3 with a paired contrast. Explain Table 1's otherwise undefined `Prompt` column.

### 9. The report is not independently reproducible from its own methods section

**Where:** Sections 4, 6, and the final data-availability sentence.

The final GitHub URL is useful but not immutable, and the report itself omits essential run metadata:

- exact Hugging Face model identifiers and revisions;
- tokenizer identifiers and revisions;
- the SynthID-Text code revision and public configuration artifact;
- library versions;
- prompt lists and prompt-construction rules;
- seed allocation and whether marked/unmarked twins share seeds;
- sampling behavior around EOS and padding;
- Qwen chat-template or plain-text formatting;
- exact commands for each headline table;
- direct paths and checksums for frozen result files;
- the chronological boundary between exploratory and prospectively locked work.

Several repository-local labels are also unexplained to an outside reader: "Grok-length," `grok36`, stem 088, "The-Laplace," `Closing`, `The car`, "lamp," and "same BPE." The report should not require familiarity with the laboratory's internal vocabulary.

Because this is a public-key reference implementation, the threat model should explicitly say that the keys exist publicly in the reference code but are deliberately withheld from the key-free reader. Otherwise "without the vendor's keys" and "public instance" can sound contradictory.

**Required revision:** Add an artifact appendix with immutable version identifiers, a corpus manifest, exact commands, and a one-page protocol chronology. Define every internal label on first use.

## Secondary scientific and editorial issues

### The paper is too defensive in places

The repeated caveats are valuable, but phrases such as "A reviewer who writes...", "honest miss," "not sold as," "not uniquely cursed," "lamp," and "this notebook" make the paper sound like an internal rebuttal log. Replace them with neutral scientific language. For example:

- "not sold as replacing 25/48" -> "is not directly comparable to the prespecified hard-reader sensitivity";
- "honest miss" -> "negative zero-threshold result";
- "the original 12 are not uniquely cursed" -> "the failure is not confined to the original 12-family set";
- "official lamp" -> "official keyed score above the prespecified threshold".

The report can be candid without sounding adversarial.

### The main narrative is obscured by too many protocol fragments

Sections 6.6 through 7.7 contain many denominators, corpus unions, thresholds, and transfer directions in dense prose. The reader must remember which of 12, 20, 28, 36, 48, 100, 144, and 400 is active, as well as whether each number is prompt wins, true positives, true negatives, coverage, or keyed passes.

Keep the core paper centered on:

1. the threat model;
2. strict 12-LOO group versus file behavior;
3. the prospectively generated 100-family lock;
4. one cross-generator test;
5. one artifact/control table.

Move the remaining transfer and leftover catalog to an appendix with a standardized result table.

### The report needs one decisive figure

A figure would communicate the two-grain result better than another table. The most useful design would show, for each original stem, the four marked and four unmarked file scores, their group means, the zero threshold, and the resulting group-win sign. Garden, station, office, and ferry-queue would then make the paper's central point visually immediate.

A second optional panel could show the 100 prompt-level paired differences for lock A, including the single miss and effect magnitudes. Reporting only 99 signs hides whether most wins are large or barely above zero.

### Table semantics should be standardized

The notation `23/48 vs. 38/48` is not self-describing. Every table should state whether the order is TP/TN, marked-positive/unmarked-negative, sensitivity/specificity, or something else. Table 2 places a file AUC in a row whose grain column says `group`; the row mixes two units. Table 5 mixes first-draw keyed file decisions with four-draw prompt-group ranking. Table 6 uses the undefined shorthand `100 union grok36`.

Use separate columns for prompt wins, TP, TN, balanced accuracy, AUC, threshold, and coverage, leaving inapplicable cells blank.

### Statistical citations and method citations need attention

The sentence in Section 3.3 cites Clopper and Pearson after mentioning both file-level permutation and binomial p-values. That source supports exact binomial intervals, not the unspecified permutation procedure. The report should cite or define the permutation method separately. The primary Witten-Bell interpolation and Lidstone smoothing also deserve methodological citations or complete in-paper definitions.

### The related-work section is responsible but could be shorter

The distinctions from cryptographic undetectability, strong watermarking impossibility, key stealing, public verification, and third-party detection are valuable. They currently consume substantial space before the paper's own method is fully specified. A tighter comparison table could replace several paragraphs and make the closest task relationship - paired-reference third-party auditing - easier to see.

### The title can better expose the strong oracle

"Key-Free Watermark Indication" is accurate only after reading the subtitle and threat model. A more self-contained title would include "Paired-Reference" or "Matched Marked/Unmarked Samples," for example:

> Paired-Reference, Key-Free Indication of a Public SynthID-Text Instance

This would reduce the risk that readers initially interpret the work as standalone document detection.

## Section-by-section comments

### Abstract

The abstract is admirably specific but overloaded with metrics. It should state the evaluation topology of 99/100, replace the isolated sensitivity-only framing with the full zero-threshold result, and demote the 0.02 margin unless its null is fixed. The argmax result is secondary and can move out of the abstract if space is needed.

### Introduction

The research question is clear. The phrase "Prompt-group ranking without keys is real" should be tied to "on these measured corpora and one public instance" in the same sentence. The contribution list should distinguish exploratory, corrective, and confirmatory evidence.

### Related Work

The scope boundaries are thoughtful. The section should identify the precise novelty dimension in one sentence: inexpensive empirical count-table auditing under paired labeled references for a fixed public instance. Avoid spending more text on what the paper did not refute than on how its closest empirical comparator differs.

### Preliminaries and Threat Model

This is conceptually strong. It needs three additions: the fact that the reference keys are public but withheld by design, the marked/unmarked seed relationship, and an explanation of Table 1's `Prompt` scores. Clarify whether \(E[g]=1/2\) is over random keys, hash outputs, tokens, or the unmarked generation distribution for the fixed instance.

### Method

This section requires the largest expansion. It currently defines the simplest reader better than the primary confirmatory reader. Add exact algorithms, corpus-to-fold mappings, threshold handling, zero-coverage behavior, and model/runtime details. A reader should be able to reproduce Table 4 without inspecting code.

### Why a Fixed Key Can Leave a Trace

The intuition is good and appropriately labeled a sketch. Recast the variance statement conditionally on fitted tables and around within-pair differences. Also separate two mechanisms: repeated context overlap permits direct empirical memorization, while unigram or Witten-Bell backoff can propagate broader distributional shifts. The current paragraph blends them.

### Results

The stem table is excellent. The 100-family section needs effect magnitudes and uncertainty, not only win counts. The cross-generator section needs a formal paired comparison and a clear native-versus-transfer definition. The isolated section should lead with the full confusion matrix and distinguish fixed-threshold accuracy from AUC.

### Ablations, Artifacts, and Scrubbing

The overcount correction is important and belongs in the main text. The remaining material would be easier to audit as a protocol table or appendix. Argmax snap should be called a mechanistic perturbation unless textual quality and self-consistent regeneration are evaluated; changing 60-90 of 128 tokens with original rather than updated prefixes is far from a practical watermark-removal attack.

### Limitations

This section is strong but arrives after several claims that need the same qualification earlier. Add explicit limitations for the 0.02 margin, non-fully-nested Youden thresholds, fixed prompt sets, lack of a frozen fitted detector test, and the distinction between sensitivity and complete classifier performance.

### Conclusion

The conclusion should retain the strong positive group-level result. It should replace "the same tables do not classify" with a precise zero-threshold statement and acknowledge the weak threshold-free AUC. It should also say whether 99/100 is frozen-model evaluation or prospectively specified leave-one-family-out evaluation.

## Visual and production review

The PDF is clean and readable, with these smaller production issues:

1. The abstract is dense for a one-column first page. Removing secondary counts would improve entry into the paper.
2. Citation links in green and URLs in bright blue are readable on screen but may have weak grayscale and accessibility behavior. A darker or monochrome submission style would be safer.
3. The PDF is not tagged and does not expose title/author metadata in `pdfinfo`. Add `pdftitle`, `pdfauthor`, `pdfsubject`, and `pdfkeywords`, and consider a tagged-PDF workflow if the venue supports it.
4. The author's GitHub address on the title page is typeset as plain monospaced text rather than as a URL command.
5. The first Anthropic bibliography entry is split between pages 12 and 13, leaving a URL continuation at the top of page 13. Avoiding page breaks within bibliography entries would improve polish.
6. Pages 10 and 11 are numerically dense. A summary table and one figure would substantially improve scanability.

None of these is a blocking layout defect.

## Prioritized revision plan

### Priority 0 - required before scientific submission

1. Replace sensitivity-only isolated claims with the full confusion matrix and a declared primary metric.
2. Define or demote the 0.02 margin analysis and remove the unsupported comparison to a 0.5 null.
3. State the complete train/validation/test topology for every headline, especially 99/100 and Phase B.
4. Specify Witten-Bell interpolation, score-zero/abstention behavior, and rankpath exactly.
5. Resolve the context-length contradiction and notation collisions.
6. Reframe nested Youden results as post hoc unless fully nested evaluation is run.

### Priority 1 - needed for a strong empirical paper

1. Add prompt-level effect sizes and cluster-aware uncertainty.
2. Replace H3 raw-drop reasoning with a paired comparison.
3. Separate keyed file controls from key-free group endpoints.
4. Add immutable artifact identifiers, prompts, models, seeds, and commands.
5. Add a two-grain score figure and a standardized protocol/result table.

### Priority 2 - editorial polish

1. Shorten the defensive caveat language and remove internal-lab idioms.
2. Move most protocol variants to an appendix.
3. Add PDF metadata and improve accessibility/print link styling.
4. Prevent bibliography entries from splitting across pages where practical.

## Suggested core claim after revision

Assuming the apparent leave-one-family-out interpretation of the 100-family experiment is correct, the report's central claim could be stated as:

> With matched labeled marked/unmarked reference generations and no detector keys at scoring time, an empirical count-table auditor ranks marked prompt-group means above unmarked means in 9/12 exploratory original families and 99/100 prospectively generated same-register GPT-2 families under a predeclared leave-one-family-out protocol. On the original 96 individual files, the prespecified zero threshold yields 25/48 sensitivity, 22/48 specificity, and 47/96 balanced accuracy, while threshold-free file AUC is 0.590. These results establish group-level paired-reference indication for one public SynthID-Text instance, not a calibrated standalone detector or a universal key-free detector.

This wording preserves the positive result, states the negative result using the correct classification unit, and makes the strong oracle visible.

## Final recommendation

**Major revision.** The report's central scientific observation is worth preserving and publishing: prompt-group ranking can remain strong under a key-free but paired-reference audit even when a prespecified isolated-file threshold fails. The current manuscript already understands that conceptual distinction. Its main task now is to make the statistical estimands, fold topology, and primary reader as precise as the narrative caveats. Once those points are corrected, the work will be substantially more credible, easier to reproduce, and harder to misread as either a universal detector or a null result.
