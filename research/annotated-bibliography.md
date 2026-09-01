# Annotated bibliography

Each entry is a full bibliographic record plus a **critical annotation**:
what the source claims, how this laboratory uses it, and what it must not
be sold as. Citation style is author–year; keys match
[references.bib](references.bib). Convention: [CITING.md](CITING.md).
Narrative: [related-work.md](related-work.md).

This is not a review of every sampling watermark. It is the set of sources
the notes actually rely on or must distinguish themselves from. Headlines
in this repository stay **10/12**, **29/48**, and **36/36**.

---

## Official keyed detection

**Dathathri, S., See, A., Ghaisas, S., Huang, P.-S., McAdam, R., Welbl, J., Bachani, V., Kaskasoli, A., Stanforth, R., Matejovicova, T., Hayes, J., Vyas, N., Al Merey, M., Brown-Cohen, J., Bunel, R., Balle, B., Cemgil, T., Ahmed, Z., Stacpoole, K., Shumailov, I., Baetu, C., Gowal, S., Hassabis, D., & Kohli, P. (2024).** Scalable watermarking for identifying large language model outputs. *Nature, 634*(8035), 818–823. https://doi.org/10.1038/s41586-024-08025-4

Annotation: Archival description of SynthID-Text: tournament sampling, g-values, mean / weighted-mean / Bayesian detectors, and a production Gemini experiment. This repository’s `score` path is the public reference implementation of that scheme (`public-deepmind-30`). Do not reimplement `detector_mean`. The paper is keyed detection. It is not a key-free isolated-file classifier and does not replace **29/48**.

**Google DeepMind. (2024).** SynthID-Text reference implementation [Computer software]. https://github.com/google-deepmind/synthid-text

Annotation: The code this lab installs with `pip install -e … --no-deps`. Trust the implementation of `get_gvals` (12 LCG mixes, then `(hash >> 30) % 2`), not the docstring. Do not edit the checkout except for that install.

---

## Earlier sampling watermarks

**Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., & Goldstein, T. (2023).** A watermark for large language models. In *Proceedings of the 40th International Conference on Machine Learning* (PMLR 202, pp. 17061–17084). https://proceedings.mlr.press/v202/kirchenbauer23a.html

Annotation: KGW: a keyed green-list bias on next-token sampling and a z-test detector. SynthID-Text is a tournament variant of this family, not a hidden-character tag. This lab does not implement KGW and does not treat KGW detectors as oracles for `public-deepmind-30`.

**Aaronson, S., & Kirchner, H. (2023).** Watermarking of large language models [Talk slides]. https://www.scottaaronson.com/talks/watermark.ppt

Annotation: Unpublished Gumbel / exponential-minimum scheme, cited from Dathathri et al. (2024). Distortion-free in the exponential-minimum sense. Not a peer-reviewed article; keep the “talk” label. Kuditipudi et al. (2024) give a related distortion-free construction with an archival TMLR record.

**Kuditipudi, R., Thickstun, J., Hashimoto, T., & Liang, P. (2024).** Robust distortion-free watermarks for language models. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=FpaCL1MO2C

Annotation: Inverse-transform and exponential-minimum sampling with a keyed random sequence; detection by alignment. Distortion-free up to a generation budget. This lab’s public mixin is tournament sampling, not this scheme.

**Christ, M., Gunn, S., & Zamir, O. (2024).** Undetectable watermarks for language models. In *Proceedings of Thirty Seventh Conference on Learning Theory* (PMLR 247, pp. 1125–1139). https://proceedings.mlr.press/v247/christ24a.html

Annotation: Cryptographic undetectability: without the key, watermarked output is computationally indistinguishable from the original model, even under adaptive queries. That is a different object from this lab’s empirical count-table indicator, which *expects* a distributional footprint. Do not cite Christ et al. as evidence that key-free indication is impossible on SynthID-Text; their theorem is about a different construction.

---

## Stealing, spoofing, and removal (not implemented here)

**Jovanović, N., Staab, R., & Vechev, M. (2024).** Watermark stealing in large language models. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235, pp. 22570–22593). https://proceedings.mlr.press/v235/jovanovic24a.html

Annotation: Automated API stealing that enables spoofing and scrubbing of KGW-family schemes. Archival arXiv id is **2402.19361**, not 2311.04378. This laboratory does not steal keys, train a spoof generator, or implement their attack. Invertibility of `hash_iv` from a static string is a different (and rejected) question; see [invertibility.md](invertibility.md).

**Zhang, H., Edelman, B. L., Francati, D., Venturi, D., Ateniese, G., & Barak, B. (2024).** Watermarks in the sand: Impossibility of strong watermarking for language models. In *Proceedings of the 41st International Conference on Machine Learning* (PMLR 235, pp. 58851–58880). https://proceedings.mlr.press/v235/zhang24o.html

Annotation: Impossibility of *strong* watermarking given a quality oracle and a mixing perturbation oracle. arXiv **2311.04378**. Earlier notes in this repo wrongly used that id for Jovanović et al. (2024). Zhang et al. do not recover keys from one string, and they do not supply this lab’s isolated-file indicator.

**Wu, Q., & Chandrasekaran, V. (2024).** Bypassing LLM watermarks with color-aware substitutions. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 8549–8581). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.acl-long.464

Annotation: Color-aware substitution (SCTS) against KGW green lists. Concurrent with Jovanović et al. (2024) on stealing-to-scrub. Requires prompting the watermarked model for colour. Not implemented here.

**Pang, Q., Hu, S., Zheng, W., & Smith, V. (2024).** No free lunch in LLM watermarking: Trade-offs in watermarking design choices. In *Advances in Neural Information Processing Systems 37*. https://arxiv.org/abs/2402.16187

Annotation: Robustness vs spoofing, multi-key vs removal, public detection APIs as oracles. NeurIPS 2024. This lab’s `contrast` path is instance-specificity of a *key-free* reader, not their detection-API attacks.

**Omidi, R., Dong, Y., & Wang, B. (2026).** On Google’s SynthID-Text LLM watermarking system: Theoretical analysis and empirical validation [Preprint]. arXiv. https://arxiv.org/abs/2603.03410

Annotation: First theoretical analysis of SynthID-Text’s **keyed** scores: mean-score TPR is unimodal in tournament layers; the Bayesian score is nondecreasing then saturates; Bernoulli(0.5) is optimal for detection. Also studies a layer-inflation **removal** attack on the mean score. This laboratory does **not** implement that attack. Their object is official g-value detection with keys. It is not `indicate` and it does not replace **29/48**.

**Han, X., Li, Q., Ni, J., & Zulkernine, M. (2025).** Robustness assessment and enhancement of text watermarking for Google’s SynthID [Preprint]. arXiv. https://arxiv.org/abs/2508.20228

Annotation: Meaning-preserving stress (paraphrase, copy-paste, back-translation) of SynthID-Text, plus a proposed hybrid (SynGuard). Current workflow does not download DIPPER and does not run SynGuard. Recorded so the robustness gap is cited, not invented.

---

## Key-free / third-party detection

**Gloaguen, T., Jovanović, N., Staab, R., & Vechev, M. (2025).** Black-box detection of language model watermarks. In *The Thirteenth International Conference on Learning Representations*. https://arxiv.org/abs/2405.20777

Annotation: Statistical tests for the *presence of a watermarking scheme as a generator property*, using limited black-box queries. ICLR 2025. This is **not** scoring a finished isolated string against count tables. Earlier README text wrongly attributed arXiv:2405.20777 to Sabanayagam, Hörl, and Dobriban; that authorship is incorrect.

**SRI Lab, ETH Zurich. (2024).** Probing Google DeepMind’s SynthID-Text watermark [Blog post]. https://www.sri.inf.ethz.ch/blog/probingsynthid

Annotation: Applies Gloaguen et al. (2025) to a local SynthID-Text deployment. Secondary web source. Cite the ICLR paper for the method; cite the blog only for the SynthID-specific write-up.

**Wang, Z., Ren, Y., Cao, Y., Fang, F., Li, X., & Guo, L. (2026).** Rethinking LLM watermark detection in black-box settings: A non-intrusive third-party framework. In *Findings of the Association for Computational Linguistics: ACL 2026* (pp. 19773–19790). Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.findings-acl.990

Annotation: TTP-Detect: third-party, key-agnostic verification from observable outputs and paired watermarked/unwatermarked references. Same *audit problem* as this lab, a different method (proxy model + relative hypothesis tests). This repository is a small checked-in instance of finished-string count-table indication on the public mixin, not TTP-Detect.

**Duan, H., Xiang, L., & Zhang, X. (2025).** PVMark: Enabling public verifiability for LLM watermarking schemes [Preprint]. arXiv. https://arxiv.org/abs/2510.26274

Annotation: Zero-knowledge proof that keyed detection ran faithfully, without disclosing the key. The detector **still uses the key**. That is not `indicate` / `blind`. Official `detector_mean` still requires instance keys (Google DeepMind, 2024, issue 22).

---

## Paraphrase

**Krishna, K., Song, Y., Karpinska, M., Wieting, J., & Iyyer, M. (2023).** Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense. In *Advances in Neural Information Processing Systems 36* (pp. 27469–27500). https://doi.org/10.52202/075280-1195

Annotation: DIPPER (11B T5-XXL) as a paraphrase attack on detectors, including watermarks. This lab’s current workflow **does not download DIPPER**; see [dipper-local.md](dipper-local.md). Cite Krishna et al. when discussing paraphrase robustness as a known threat, not as a measurement this repo has run.

---

## Policy and software (not peer-reviewed)

**Anthropic. (2026a).** Claude text watermark [Company announcement]. https://www.anthropic.com/news/claude-text-watermark

**Anthropic. (2026b).** How Claude marks AI-generated content [Help Center article]. https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content

Annotation: Primary sources for Anthropic’s announced mark (“a version of” SynthID-Text). Production keys and detector are not public. Claude remains a **future external test** for key-free indication. `score` on `public-deepmind-30` cannot read that instance. Accessed 2026-09-01.

**Google DeepMind. (2024).** Publicly verifiable detection (Issue 22) [GitHub issue]. https://github.com/google-deepmind/synthid-text/issues/22

Annotation: Feature request for publicly verifiable detection. Confirms that the public reference detector is still keyed.
