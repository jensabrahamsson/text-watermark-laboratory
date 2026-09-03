# Promising ideas for making key-free watermark detection more possible (2026-09-03)

This note is an exhaustive working inventory of **ideas that make key-free detection of a sampling watermark more possible**, not a new `probe --methods` name, not leftover targeting of the original 12, not key recovery, and not a replacement of isolated hard last-4 **25/48**.

Author–year citations follow [research/CITING.md](research/CITING.md). Lab counts are this repository’s data, not a paper. Pre-fix **10/12** / **29/48** stay in historical JSON. Headlines stay **9/12**, **25/48**, and **36/36**. Confirmatory lock A interpolate last-4 on public `ngram_len=5` ($\Hw=4$) stays **99/100**. `used_keys=false` on every key-free command below.

The request that produced this file asked for three holds to be exhausted, several times, with all scientific references and all laboratory information that bears on them:

1. **Make the opening the product.** Occupancy-free tokhits had precision 1 when it answered.
2. **Stop scoring last-4 against $\Hw=12$.** Match table order to the hash window, or run the TTP-Detect proxy this laboratory never reimplemented.
3. **Detection as API queries to the generator**, several draws of the same prompt, not a webpage. That grain is already **99/100**. It is a different hole than a file on the web.

Calendar protocol: work toward these holds through **5 September 2026 10:00 CEST**. `/goal` time budgets of the form `30m` / `2h` are not supported; the calendar cutoff is a research protocol, not a token budget. This file is the deliverable.

Scientific form for every indication in this note (CITING.md): observation, scope, hypothesis, non-claim. This laboratory **did not refute** Christ et al. (2024) or Zhang et al. (2024). Do not sell later counts as replacing **25/48**.

---

## 0. What “more possible” means here

Key-free detection in this repository is **not one number**. [research/narrative.md](research/narrative.md) and [research/threat-model.md](research/threat-model.md) lock two grains:

```
matched marked/unmarked twins
        │
        ├─ prompt-group ranking (mean LR per stem)
        │    12-LOO hard last-4 **9/12** (margin 0.02 → 10/12)
        │    36×4 hits **36/36**
        │    100×4 lock A **99/100**
        │
        └─ isolated file (one LR against 0)
             12-LOO hard last-4 **25/48 vs 22/48**
             leftover occupancy-free zeros **10/20 vs 11/20** (chance)
             occupancy-covered **15/28** of those 25 TPs
```

“More possible” does **not** mean “raise isolated **25/48** by inventing another hashed scorer on the old 12×4 twins.” [research/PROTOCOL-next.md](research/PROTOCOL-next.md) forbids new `probe --methods` names on those twins except bug-fix remeasures. The three holds are product and protocol moves:

| Hold | Product | What it refuses to pretend |
|---|---|---|
| 1. Opening as product | A **selective classifier** that answers only when an observed next-token atom is in the tables. Precision 1.000 on decided files of the published OOD tokhits gate. Zeros are abstentions. | A universal isolated-file detector of a stranger’s webpage. |
| 2. Match order to $\Hw$, or TTP-Detect | Score last-$k$ with $k \approx \Hw$, drop Witten–Bell on unseen body 4-grams of a 12-token hash, **or** compare against Wang et al. (2026) on a **new** frozen corpus. | That full-file interpolate **76/100** under $\Hw=12$ is a weaker copy of lock A **99/100**. |
| 3. API / multi-draw | Query the generator, same prompt, several draws. Lock A **99/100** is already this grain. Align with Gloaguen et al. (2025). | That **99/100** is detection of one finished file found on the web. |

The auditor is key-free and **not reference-free** (threat-model.md). Matched twins, or black-box queries that can toggle or resample a generator, are in-scope. “One stranger’s file, no corpus, no keys” is the isolated-file hole. Mixing those sentences is how a strong notebook becomes a slogan.

---

## 1. Hold 1 — make the opening the product

### 1.1 Observation (laboratory)

Occupancy-free `postokhits` / `tokhits` skip a context unless the **observed next token** appeared on either side of the training tables (`n_m[token] + n_u[token] < 1`). Laplace occupancy of empty cells cannot vote. Zeros are abstentions, not sign errors. Primary write-up: [research/key-free-tokhits.md](research/key-free-tokhits.md). Helper: `openings` CLI; `lr == 0` iff `n_used == 0`. Isolated recall equals train atom overlap.

Published OOD gate (24 short 36×4 stems → original 12×4, `--fit-prefix 4 --pos-bucket 1`, skip generated token 0):

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,hits,tokhits \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits
```

| Reader | Prompt wins | marked `lr>0` | decided tp/fp | precision |
|---|---|---|---|---|
| poshits (occupancy Laplace) | **12/12** | **39/48** | 39 / 7 | 0.848 |
| postokhits (occupancy-free) | **12/12** | **16/48** | **16 / 0** | **1.000** |

JSON: `experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/results.md`. Decided accuracy of postokhits on that gate is **1.000** (16 TP, 0 FN among decided marked files; 0 FP, 4 TN among decided unmarked). Thirty-two marked files and forty-four unmarked files are zeros.

The nine marked zeros on that gate are openings with **no** overlapping context at indices 1–3: `After two and a` (night-bus d3), `Closing is the` (all four library draws), `Now in the second` / `While working on the` (letter), `Now a little after` (garden). Library is a prompt echo of “Closing time is announced twice”, not a generic temporal class.

Twenty-three of the thirty-nine poshits TPs were **anti-occupancy** on shared `'The'`: train occupancy 8 marked vs 52 unmarked, so every novel continuation after `'The'` got δ ≈ +0.330. That family also produced **all 7** unmarked FPs (The weather / passengers / cat / …). Occupancy-free drops those TPs **and** those FPs. The remaining TPs are observed-token atoms (`'"' → 'This'`, `'This' → ' is'`, `'Oh'`, `'Who'`, `'My'`).

More train, same precision 1.000, more coverage:

| Train | postokhits `lr>0` | decided precision |
|---|---|---|
| 24 short one-liners | **16/48** | **1.000** |
| 12 medium scenes | **19/48** | **1.000** |
| short + medium | **20/48** | **1.000** |
| tail-matched | **30/48** | **1.000** |
| short+medium+tails (postokbackoff) | **36/48** | **1.000** |
| neighbourhood paraphrases + SMT (covered) | **42/48** covered; isolated `lr>0` **34/48** | **1.000** on decided observed-token |

tokbackoff / postokbackoff shrink last-$k$ until an observed next token hits. They do not fall to the unigram. Harbour’s extra files are last-1 `' was' → ' in'`. After / Closing / Now / While still have **no** observed next token at any shorter order. Coverage is a train-atom problem, not a missing scorer name.

Control-shuffled-30 (different instance, same tournament family): postokhits **0/48** control `lr>0`. Public vs control still **12/12**. Official lamp on those 48 control files: public **0.501**, matching control keys **0.624**. The occupancy-free opening reader is **instance-specific without keys**. Write-up: [research/key-free-contrast.md](research/key-free-contrast.md).

In-domain 12-LOO hard last-4 **25/48** splits leftover vs covered ([research/PROTOCOL-isolated-split.md](research/PROTOCOL-isolated-split.md)): leftover **10/20 vs 11/20** (chance), covered **15/28**. The 25 TPs are not a leftover-file detector. Occupancy-covered openings carry 15 of 25. Leftover last-4 is chance. Do not sell 10/20 or 15/28 as replacing **25/48**.

Opening-overlap bound (`openings` CLI): isolated occupancy-free recall **equals** train atom coverage. 100 one-liners → original 12: covered **18/48**. 100 ∪ grok36: disjoint union **28/48**. Distil ∪ SMT: **33/48**. Leftover after those unions is closed for more unrelated GPT-2 scenes. Isolated observed-token recall does not grow by adding another hashed method; it grows by putting the missing opening in train.

### 1.2 Hypothesis

On this mixin, the **high-precision key-free channel** is not “classify every 128-token file.” It is: **if and only if the test opening copies an observed (context, next) atom from marked/unmarked reference twins, emit a signed LR; otherwise abstain.**

That is already how `postokhits` behaves. The product move is to **stop reporting zeros as false negatives** in the shop window, and to ship the opening atom table as the detector, with an explicit reject option.

### 1.3 Adjacent literature (not watermark papers, same decision problem)

The occupancy-free zero is Chow’s reject option, not a failed detector.

- **Chow (1957, 1970).** Optimum recognition with a reject option. Chow (1970), *IEEE Transactions on Information Theory, 16*(1), 41–46, doi:10.1109/TIT.1970.1054406. Reject when the maximum posterior is below a threshold. The error–reject curve is the object. Occupancy-free `n_used=0` is a **hard abstention** (no posterior to threshold); Chow’s rule is the continuous analogue once a posterior exists.
- **Bartlett and Wegkamp (2008).** Classification with a reject option using a hinge loss. *Journal of Machine Learning Research, 9*, 1823–1840. Convex surrogate for cost-sensitive abstention. The laboratory cost of a false mark on a human file is the reject-cost problem; precision 1.000 on decided files is the empirical extreme of setting that cost high.
- **Geifman and El-Yaniv (2017).** Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30*. User sets a risk $r^*$; the selector $g$ abstains until empirical risk is below $r^*$ with high probability. Map: $g=1$ iff `n_used>0` (and, optionally, $|\Lambda| \ge t$). Coverage is $P(g=1)$; selective risk on that OOD gate was **0** among decided files.
- **Heng and Soh (2026).** Know when to abstain: optimal selective classification with likelihood ratios. ICLR 2026; arXiv:2505.15008. Neyman–Pearson lemma: the optimal selector score is a monotone transform of a likelihood ratio $p_c(x)/p_w(x)$. This laboratory **already scores a likelihood ratio** $\Lambda = \log P_m - \log P_u$ on next tokens. The missing piece is to treat **whether to emit $\Lambda$** as a second NP test (select vs abstain), not to invent a new $\Lambda$. Their $\Delta$-KNN / $\Delta$-MDS selectors are the same geometry TTP-Detect uses as a **detector** (kNN, Mahalanobis); here they would be used as a **gating** function on top of tokhits.
- **Neyman and Pearson (1933).** On the problem of the most efficient tests of statistical hypotheses. *Philosophical Transactions of the Royal Society A, 231*, 289–337. The lemma Heng and Soh invoke. For a fixed Type I rate (false marks among decided files), the most powerful test is an LR threshold. Precision 1.000 at $\tau=0$ among decided files of the OOD tokhits gate is an empirical NP corner: Type I among decided = 0, power = coverage.
- **Clopper and Pearson (1934); McNemar (1947).** Already in [research/references.bib](research/references.bib). Isolated **25/48** Clopper–Pearson **[0.372, 0.667]** includes ½. A selective classifier with 16/16 decided TPs and 0 FP does **not** inherit that interval; it has a different $n$ (decided files) and a coverage parameter. Report **both**.

Watermark papers that already treat “when not to score”:

- **Huang, Zhu, Zhu, Lee, Jiao, and Jordan (2023).** Towards optimal statistical watermarking. arXiv:2312.07930. Hypothesis-testing view of **keyed** watermarking; UMP tests; token-budget $\Theta(h^{-1}\log(1/h))$ in entropy $h$. Adjacent because it says detection is an LR test with a sample-size (coverage) constraint. It does **not** give this lab a key-free isolated-file theorem. Cite as a preprint unless an archival venue is confirmed.
- **Dathathri et al. (2024).** SynthID-Text **masks repeated context hashes** so they do not add repeated evidence. The official detector already abstains on repeated contexts. Occupancy-free tokhits abstains on **unseen** contexts. Same family of idea (do not invent evidence), opposite side of the table.

### 1.4 Product sketch (not implemented in this PR)

Name it honestly: **Opening Indicator**, not “watermark detector.”

Inputs the auditor has (threat-model.md):

- Frozen occupancy-free tables from marked/unmarked twins (or a published atom list).
- A test string.
- A tokenizer matched to the generator (GPT-2 BPE for these tables).

Decision:

1. Take the first $F$ generated tokens (frozen $F=4$ on lock B; product may ship $F=4$ only).
2. For each position $i=1..F-1$ (skip token 0 unless `--include-first` is a named ablation; it **hurts** the 4-token OOD gate, 9/12 vs 12/12).
3. If the exact (bucketed) context and next token were seen, add Laplace log-ratio; else skip.
4. If `n_used=0`, output **ABSTAIN** (not “unmarked”).
5. If `n_used>0` and $\Lambda>0$, output **MARKED** with the atom list that fired.
6. If `n_used>0` and $\Lambda\le 0$, output **NOT THIS INSTANCE** (still not “human”).

Calibration that is already on disk and must stay in the shop window:

- Control-shuffled-30: **0/48** `lr>0`. Instance-specific.
- Unmarked 2-versus-2 placebo on public 100×4: opening 0:4 interpolate **49/100**, tokhits **50/100** (`/tmp/probe-placebo-100x4-unmarked-2v2` if re-run). Opening rank is not a split artifact.
- Coverage bound: recall cannot exceed train-atom overlap. Publish the atom book, not a mysterious score.

`--include-first` postokhits on combined train was **43/48** marked with **10** unmarked FP (first-token unigram). Do not put token 0 into the product without a new freeze. Unbucketed tokbackoff on that train was **36/48** marked, **3** FP (precision 0.923). Position bucket 1 is the precision lock.

### 1.5 Second pass over hold 1 (same hold, different angle)

**Authorship / stylometry, not watermarks.** A closed-set authorship problem with a reject option is: “is this *this writer*, or abstain?” Occupancy-free tokhits is closed-set **instance** indication with abstention. Pang et al. (2024) discuss public detection APIs as oracles; this product is the opposite of a public keyed API: it is a **published atom book** for one instance. Forging the opening (`The bus`, `Closing is the`) is a coverage attack, not key recovery. Jovanović et al. (2024) steal keyed mappings from API samples; an opening-atom product is stealable by **copying openings**, which `openings` already measures. That is honesty, not a reason to hide the product.

**Steganalysis.** Classical steganalysis often abstains when the cover is too short. The opening product is honest about length: four tokens, not 128. Selling a 128-token interpolate score that is almost the opening (Hw=12 100-family hits **91/100** full-file vs **95/100** at 0:4) is the dishonest version of the same product.

**Library science / fingerprinting.** An ISBN is not a hash of the whole book. An opening atom is a fingerprint of **how this instance starts a family of prompts**. The original-12 leftover files do not share those ISBNs. Treat leftover as **out of catalogue**, not as detector failure.

### 1.6 Third pass over hold 1 (what would kill the product)

- **Generator change.** DistilGPT2 12×4 official **12/12**, in-domain hits **9/12**, native opening rankpath **8/12** (chance). GPT-2 36×4 hits → Distil **5/12**. Distil occupancy-free leftover-18 coverage **3/18**. Qwen native opening rankpath **8/12**. The opening product is **tokenizer- and generator-specific**. Ship one book per generator, or do not ship.
- **Register change.** Grok-length train → original 12 lock A nested **16/48 vs 41/48**; occupancy-free **5/48 = coverage**. Reverse 100 one-liners → grok12 occupancy-free **0/48**. One-liner atom books do not cover Grok-length leftover openings. The product’s catalogue must match seed length, or it abstains (correct).
- **Paraphrase of the opening.** Krishna et al. (2023) DIPPER; this lab does not download DIPPER ([research/dipper-local.md](research/dipper-local.md)). Neighbourhood paraphrases of the 12 scenes had official **12/12** and **no** Closing/Now/While/The ferry openings; SMT+paraphrase coverage of original 12 was **42/48** with last-2+ **15/48**. A paraphrased opening is an abstention, not a miss to be “fixed” with hashpool.
- **Christ et al. (2024).** Cryptographic undetectability for a **different construction**. An opening-atom distinguisher on `public-deepmind-30` GPT-2 twins is not a distinguisher against their scheme. Do not write that this product refutes them.
- **Zhang et al. (2024).** Quality oracle + mixing perturbation. This product does not claim robustness to mixing. Official leftover-18 **18/18** at prefix-128 uses **keys**. Do not cite Zhang et al. as “key-free cannot work.”

### 1.7 Exact next measurements (existing methods only)

Do **not** add a method name. Use `postokhits`, `openings`, `atoms`, `contrast`.

- Publish a **coverage–precision curve** on the already-frozen OOD JSON: decided precision vs `n_used` threshold (already 1.000 at `n_used>0` on that gate). Clopper–Pearson on decided TP/(TP+FP) with $n=$ decided marked+unmarked.
- Frozen lock B is already opening poshits **100/100** (in-family). The product claim is OOD **precision given coverage**, not 100/100.
- Do not leftover-target After/Closing/Now/While with new scenes. PROTOCOL-isolated-occupancy-closed already closed that for unrelated GPT-2 scenes.

---

## 2. Hold 2 — stop scoring last-4 against $\Hw=12$; match the hash window or run TTP-Detect

### 2.1 The mismatch, stated

Public SynthID-Text reference: `ngram_len=5`, watermark hash history $\Hw=4$ ([research/how-synthid-works.md](research/how-synthid-works.md); Dathathri et al., 2024; Google DeepMind, 2024). Count-table last-4 is then the **same length** as the keyed hash window. Lock A **99/100** and 12-LOO **9/12** live in that match.

PROTOCOL-next-longctx froze `ngram_len=13` ($\Hw=12$) and **kept `--context-len 4`**. That was an honest replication of the published reader, not a claim that last-4 is the MLE for a 12-token hash. Opened Phase A: interpolate and hard **6/12**, isolated **22/48 vs 30/48**. Phase B: interpolate **76/100** (below lock A **99/100**). Body collapse (100 families, same interpolate last-4 reader as the **76/100** freeze): tokens $[64{:}128)$ interpolate **50/100**, AUC **0.501**, while public $\Hw=4$ on the same slice is **93/100**. Mean marked $\Delta$ after 16: is ≈ 0 under $\Hw=12$ (atoms dumps). Official keyed on those twins is still **400/400**.

CLI already documents the distinction:

```text
--context-len   Last-k tokens as context (fit knob, not watermark ngram_len)
```

(`src/text_watermark_tools/cli.py`, help on `--context-len`).

**Scoring last-4 against $\Hw=12$ asks a 4-gram table to explain a 12-token keyed hash.** Unseen 4-grams then take Witten–Bell mass (Witten & Bell, 1991; Chen & Goodman, 1999). `interpolate` on the body is mostly `unseen_next`. `hits` that **skip** unseen 4-grams recover the opening and drop the tail: Hw=12 100×4 full-file hits **91/100** ≈ 0:4 hits **95/100**, tail 64:128 hits **53/100**.

Kirchenbauer et al. (2023) default in this lab (`PROTOCOL-next-kgw.md`): `seeding_scheme=lefthash`, **`context_width=1`**. That hash window is **shorter** than last-4. Opened interpolate last-4 on the original 12: **12/12**, file AUC **0.947**, isolated **44/48 vs 41/48**. Occupancy atoms: marked $\Delta$ stays positive in **every** window, including 64:128 (+0.293 vs −0.144). The body is readable when the hash window is short.

Zhao et al. (2024) Unigram-Watermark goes further: a **fixed** green/red split (hash window length 0). TTP-Detect reports Unigram F1 ≈ 1.0 on their tables (Wang et al., 2026, Table 1). Shorter (or null) context is the regime where finished-string key-free geometry is strongest. Longer $\Hw$ is the regime where only openings collide.

### 2.2 New diagnostic on existing twins (2026-09-03, this note)

No new method names. `hits`, `tokhits`, `interpolate`, `hard` already exist. Do not overwrite frozen experiment directories. Commands below write to `/tmp`. `used_keys=false`.

#### 2.2.1 $\Hw=12$ original-12: last-4 vs last-12

Frozen last-4 interpolate on `experiments/2026-09-03-pair-12x4-ngram13` is **6/12** (AUC 0.541). Occupancy-free last-4 on the same twins:

```bash
source .venv/bin/activate
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hits,tokhits,interpolate --context-len 4 --skip-hashpool \
  --windows 0:4,16:32,64:128 \
  --out-dir /tmp/probe-ngram13-12x4-ctx4-hits
```

| method | prompt wins | file AUC | marked `lr>0` | unmarked `lr≤0` | decided precision |
|---|---|---|---|---|---|
| interpolate last-4 (freeze) | **6/12** | 0.541 | 20/48 | 31/48 | 0.541 |
| hits last-4 | **9/12** | 0.662 | 25/48 | 31/48 | 0.595 |
| tokhits last-4 | **9/12** | 0.712 | 25/48 | 34/48 | 0.641 |

Window 0:4 tokhits is already **10/12**, AUC **0.803**. Window 16:32 hits **3/12**; tokhits **1/12**. The last-4 occupancy-free gain is the opening, not a recovered body.

Match table order to $\Hw=12$:

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods unigram,hits,tokhits,interpolate,hard --context-len 12 --skip-hashpool \
  --windows 0:12,16:32,64:128 \
  --out-dir /tmp/probe-ngram13-12x4-ctx12
```

| method | prompt wins | file AUC | marked `lr>0` | unmarked `lr≤0` | decided tp/fp | precision |
|---|---|---|---|---|---|---|
| interpolate last-12 | **6/12** | 0.539 | 20/48 | 31/48 | 20/17 | 0.541 |
| hard last-12 | 7/12 | 0.553 | 24/48 | 32/48 | 24/16 | 0.600 |
| hits last-12 | **10/12** | 0.686 | 25/48 | 33/48 | 25/15 | 0.625 |
| tokhits last-12 | **10/12** | **0.803** | 25/48 | **42/48** | **25/6** | **0.806** |

Kitchen ranks with **0** isolated TPs under last-12 hits/tokhits (ranking_without_isolated_tp 1/10). Window 0:12 tokhits **10/12**, AUC 0.803. Window **16:32 and 64:128 hits/tokhits: 0/12**, AUC 0.500 — **no last-12 occupancy in the body**. Interpolate 64:128 is **7/12**, AUC 0.477 (backoff noise).

**Hypothesis.** Under $\Hw=12$, matching $k=\Hw$ and **skipping unseen n-grams** recovers prompt ranking **10/12** versus interpolate last-4 **6/12** on the same 12 families, and that residual **is still the opening** (0:12). Witten–Bell interpolate does not get the match for free: last-12 interpolate stays **6/12**. Do **not** sell last-12 tokhits **10/12** or isolated **25/48** as replacing published **25/48** (different twins, different reader, kitchen has 0 TPs). Do not add a method name. This is a fit-knob diagnostic the freeze already allowed (`--context-len`).

#### 2.2.2 Kirchenbauer `context_width=1`: last-1 **reads the body**

Frozen last-4 interpolate on KGW 12×4 is already **12/12**, AUC 0.947. Match last-1 to `context_width=1`:

```bash
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hits,tokhits,interpolate --context-len 1 --skip-hashpool \
  --windows 0:4,16:32,64:128 \
  --out-dir /tmp/probe-kgw-12x4-ctx1
```

| method | prompt wins | file AUC | marked `lr>0` | unmarked `lr≤0` |
|---|---|---|---|---|
| hits last-1 | **12/12** | **0.975** | **46/48** | 40/48 |
| tokhits last-1 | **12/12** | 0.970 | 46/48 | 39/48 |
| interpolate last-1 | **12/12** | 0.951 | 44/48 | 41/48 |

Windows (hits last-1):

| window | prompt wins | file AUC |
|---|---|---|
| 0:4 | **8/12** | 0.558 |
| 16:32 | **12/12** | 0.823 |
| 64:128 | **12/12** | **0.932** |

This is the **inverse** of SynthID H2 (opening stronger than mid-file). On default Kirchenbauer lefthash $h=1$, the **body** outranks the opening. Token $[64{:}128)$ hits last-1: `prompts_marked_above=12`, AUC **0.932**, `pos>0=45/48`, `prompt_sign_p=0.0004998`, `used_keys=false`.

**Hypothesis.** Key-free finished-string detection of a **short-window** green-list mixin is a **body** problem, not an opening problem. Key-free detection of **long-window** tournament sampling is an **opening** problem. Matching $k$ to $\Hw$ is how you find out which product you are in. Do **not** sell KGW last-1 **46/48** or tail **12/12** as replacing **25/48**. Different mixin (Kirchenbauer et al., 2023, not Dathathri et al., 2024). Official control is the matching $z$-test, not `detector_mean`.

KGW 100-family corpus is named in PROTOCOL-next-kgw.md; if opened later, the prediction from this diagnostic is: last-1 (or last-4) interpolate/hits stay strong in the tail, unlike Hw=12 SynthID **50/100**.

### 2.3 TTP-Detect — the proxy this lab never reimplemented

Wang, Ren, Cao, Fang, Li, and Guo (2026). Rethinking LLM watermark detection in black-box settings: a non-intrusive third-party framework. In *Findings of the Association for Computational Linguistics: ACL 2026*, pp. 19773–19790. doi:10.18653/v1/2026.findings-acl.990. arXiv:2603.14968.

Closest published **finished-string paired-reference** analog of `indicate` ([research/related-work.md](research/related-work.md), [research/annotated-bibliography.md](research/annotated-bibliography.md)). Same audit problem. Different method. This repository **does not reimplement TTP-Detect on the old 12×4 files** (PROTOCOL-next.md; related-work.md “Later benchmark, not a method race”).

#### Method (from the paper, so a later comparison can be faithful)

**Threat model.** User $U$, provider $S$, auditor $D$. $S$ exposes a generation API with a **binary watermark control flag**. $D$ does not get keys, scheme, or internals. $D$ may query $S$ to build references.

**Hypothesis test.** For query text $t_q$:

$$\mathcal{H}_0: t_q \sim P_o, \qquad \mathcal{H}_1: t_q \sim P_{wm}$$

$P_o$, $P_{wm}$ are $S$’s unmarked and marked output distributions. Not “human vs machine.” Local reference anchors.

**References.** Query $S$ for $N$ paired completions: $\mathcal{T}_o$, $\mathcal{T}_{wm}$. Paper uses $N=16$ as a practical trade-off; $N=0$ is reference-free proxy classification and is **weaker**, especially on SynthID and Unbiased (their Figure 4; +5–10% F1 from $N=8$ and $N=16$ vs $N=0$ on distribution-preserving schemes).

**Proxy.** Instruction-tune a proxy $\mathcal{M}_{proxy}$ to predict watermark labels from completions (Gu et al., 2024, learnability). At detection time, take $\ell_2$-normalized last-token hidden state $z(t)$.

**Four relative modules** (ensemble via logistic regression, FPR-calibrated threshold $\tau$):

1. **Local consistency (kNN).** Kernel-weighted fraction of $k$ nearest reference neighbours that are watermarked. $A_{Loc}$.
2. **Mahalanobis.** After PCA, $\Delta_{Mah} = \delta^2_{\hat\Sigma_o}(z,\mu_o) - \delta^2_{\hat\Sigma_{wm}}(z,\mu_{wm})$. Sigmoid → $A_{Mah}$.
3. **Energy distance.** Non-parametric global geometry when Gaussians fail. $A_{Ene}$.
4. **Adaptive rank (NLL).** Token-wise NLL under a scoring LM: global cross-entropy $E_{GE}$ and local volatility $E_{LV}$. Direction $\rho_f$ is **estimated from references**, not assumed. Conformity ranks vs $\mathcal{T}_{wm}$ and $\mathcal{T}_o$. This module is the largest SynthID ablation drop in their Figure 3(b).

**SynthID numbers in their Table 1** (MarkLLM hyperparameters, `ngram_len=5`; **not** this lab’s GPT-2 12×4):

| Setting | TPR | TNR | F1 | AUC |
|---|---|---|---|---|
| Llama-3.1-8B, C4 | 0.865 | 0.930 | 0.894 | 0.938 |
| OPT-6.7B, C4 | 0.910 | 0.905 | 0.908 | 0.957 |
| Llama-3.1-8B, OpenGen | 0.875 | 0.785 | 0.838 | 0.896 |
| OPT-6.7B, OpenGen | 0.860 | 0.855 | 0.858 | 0.924 |

They note SynthID and Unbiased (Hu et al., 2024) are **harder** than KGW/Unigram because they are closer to distribution-preserving. Unigram TTP F1 is ~1.0. That pattern **matches** this lab: short-window KGW last-1 body **12/12** vs long-window SynthID body **50/100**.

**Gu et al. (2024).** On the learnability of watermarks for language models. ICLR 2024. arXiv:2312.04469. Watermark distillation: a student can learn to **emit** KGW / Aaronson / Kuditipudi marks. TTP-Detect uses the converse: if marks are learnable, a proxy can **amplify** them in representation space. This lab’s count tables are a **non-neural** proxy of the same idea. A later comparison asks: how much of TTP-Detect’s SynthID F1 does last-4 interpolate / opening tokhits recover on **identical twins**?

**Liu et al. (2024).** An unforgeable publicly verifiable watermark for large language models (UPV). ICLR 2024. arXiv:2307.16230. Two networks, shared embeddings; detection without the generation key. TTP-Detect uses UPV as a **baseline**, not as this lab’s method. UPV still couples a trained detector to an injection network. Count-table LR does not.

**Fairoze, Garg, Jha, Mahloujifar, Mahmoody, and Wang (2025).** Publicly-detectable watermarking for language models. *IACR Communications in Cryptology, 1*(4). doi:10.62056/ahmpdkp10. Cryptographic signature in the text via rejection sampling; detection uses a **public key**, not a secret watermark key. Distortion-free without the public key. Different object: they **change the scheme** so verification is public. TTP-Detect and this lab try to verify **existing private-key schemes** without that redesign. Do not collapse Fairoze et al. into `indicate`.

**Duan, Xiang, and Zhang (2025).** PVMark. arXiv:2510.26274. ZK that **keyed** detection ran. Still uses the key internally. Not key-free indication.

**Hu et al. (2024).** Unbiased watermark for large language models. ICLR 2024. Distribution-preserving reweighting; TTP-Detect’s hard case alongside SynthID. Gloaguen et al. (2025) also target this family (cache-augmented / unbiased). Adjacent because “unbiased ⇒ undetectable by users” is the claim Gloaguen empirically puncture with **API queries** (hold 3), while TTP-Detect punctures it with **paired references + proxy** (hold 2).

### 2.4 How to compare TTP-Detect without contaminating the old 12×4

related-work.md: *given identical paired reference twins and a held-out finished-string corpus, how much of TTP-Detect’s third-party discrimination does an embarrassingly simple count/opening LR recover?*

Protocol sketch (not run in this PR; do not peek a fourth scorer into PROTOCOL-next):

1. **New** frozen corpus, or the already-opened 100×4 public twins with a **held-out slice** named before fitting the proxy.
2. Provider API = local `pair` with mixin on/off (this lab already has $P_o$, $P_{wm}$).
3. Implement TTP-Detect from Wang et al. (2026) / their code if released; do **not** edit `synthid-text`.
4. Same test strings, two auditors: (A) leave-one-family-out interpolate last-4 and opening postokhits; (B) TTP-Detect ensemble.
5. Report prompt-grain ranking and isolated $\tau$ **and** TTP’s FPR-calibrated $\tau$. Coverage / abstention of tokhits vs TTP’s always-answer.
6. Expected directional result from this lab’s diagnostics: on public $\Hw=4$, simple LR should take a **large share** of prompt-grain discrimination (lock A **99/100**). On $\Hw=12$ bodies, TTP’s adaptive-rank / proxy may still see NLL structure after count tables go to chance (**50/100**). That gap is the measurement. If TTP also dies on Hw=12 tails, the hole is in the **signal**, not in count tables.

Do not run this on `experiments/2026-08-17-pair-12x4` as a fishing trip.

### 2.5 Second pass over hold 2 (smoothing, hashing, Gloaguen’s $H$)

**Witten–Bell (Witten & Bell, 1991; surveyed in Chen & Goodman, 1999).** Interpolate last-4 on Hw=12 is a language-model smoother, not a watermark detector. Unseen mass dominates (atoms: Hw=12 100×4 window 64:128 marked $\Delta$ +0.008). **Idea:** ship `hits`/`tokhits` as the default when $k$ is large, and treat interpolate as an Hw-matched smoother only when occupancy is high (public $\Hw=4$).

**Gloaguen et al. (2025), Red-Green test, appendix on SynthID.** They model SynthID-Text as LeftHash $h=3$ + larger context + tournament + caching. Their test needs the hashing window $H$ **matched**, not overestimated: overestimate triggers repeated-context caching and **zero** information. SRI Lab (2024) blog: for SynthID, estimate $h$ correctly; $K=1$ cache means you must not over-bound $H$. **This is the same knob as `--context-len` vs `ngram_len`.** Gloaguen match $H$ for **API** tests (hold 3). This hold matches $k$ for **tables**. Both are “stop using the wrong window.”

**Kirchenbauer et al. (2023) LeftHash $h=1$ vs SelfHash $h=3$.** Gloaguen instantiate both. This lab’s KGW freeze is $h=1$. SelfHash $h=3$ would be a named mixin freeze, not a new method on old twins. Prediction: $h=3$ sits between $h=1$ body-readable and $\Hw=12$ opening-only.

**Omidi, Dong, and Wang (2026).** Keyed SynthID analysis; TPR of mean score unimodal in tournament layers. Not `indicate`. Adjacent: layer count (this lab: 12 LCG mixes then `(hash >> 30) % 2`) is another “window” besides $\Hw$. Do not reimplement `detector_mean`. Do not run their layer-inflation attack.

**Hash pooling** (`hashpool`, `hashtok`) collides contexts so held-out prompts still score. It is a stealing-style regulariser (Jovanović et al., 2024, family), **not** reconstruction of SynthID’s hash. Opening hashtok 12-LOO was **24/48 vs 47/48**, below **25/48**. Do not sell hashed signs as replacing **25/48**. Under Hw=12, hashing last-4 cannot create last-12 occupancy. Match $k$ first, hash second.

### 2.6 Third pass over hold 2 (what matching $k$ cannot do)

- It cannot detect a leftover original-12 file whose opening is absent from train. Last-12 tokhits on Hw=12 still has **23/48** marked zeros.
- It cannot make interpolate last-12 beat last-4 on Hw=12 (both **6/12** here). The win is **occupancy-free**, not Witten–Bell at the right order.
- It cannot be sold as a bug-fix of PROTOCOL-next-longctx. That freeze **intentionally** reused last-4. This diagnostic is a later idea, recorded here, not a rewrite of the freeze flags.
- Production Gemini / Claude: not measured. Anthropic (2026a, 2026b) remains a future external test.

---

## 3. Hold 3 — detection as API queries, several draws, same prompt (already 99/100)

### 3.1 Observation (laboratory)

Lock A (PROTOCOL-next.md): leave-one-family-out interpolate last-4 on 100 new GPT-2 families, public keys, $\Hw=4$. Prompt-group ranking **99/100** (stem 088 misses). File AUC **0.898**. Official first-draw keyed **100/100**. Isolated 352/400 vs 290/400 is **secondary** and must not replace **25/48**.

That measurement is: **for each prompt family, four marked draws vs four unmarked draws, mean LR compared.** It is not a webpage. It is an **API-shaped** experiment: you may resample the same prompt. [research/threat-model.md](research/threat-model.md): the auditor can run the same prompts through marked and unmarked generators.

Placebo (unmarked 2-vs-2 on the same 100 families): interpolate **57/100**. Opening windows **49–51/100**. Multi-draw ranking is not automatic from having 100 stems.

H2: window 0:4 **99/100** vs 16:32 **89/100** reindexed, **87/100** absolute; McNemar **86/13/1/0**. Even the API grain is opening-heavy on public $\Hw=4$, but the **tail still ranks** (64:128 interpolate **93/100** on public 100×4). Under $\Hw=12$ the tail is **50/100**. The API product on public DeepMind-30 GPT-2 is real; the API product on long-hash tournament **without openings** is not shown.

Distil lock B **88/100** (1 tie); Qwen lock B **95/100**. Same grain, other generators. Rankpath (lock C) drops more (H3). The API product is more generator-robust for **poshits** than for rankpath, and still not **25/48**.

### 3.2 Gloaguen et al. (2025) — the published API product

Gloaguen, Jovanović, Staab, and Vechev (2025). Black-box detection of language model watermarks. *ICLR 2025*. arXiv:2405.20777. Code: https://github.com/eth-sri/watermark-detection.

**Question:** is *this generator* watermarked? Limited black-box queries. Prompt only; text out; no logits. Not scoring a finished isolated string.

**Three families of tests:**

1. **Red-Green (Kirchenbauer-style, and SynthID as a variant).** Steer the model into choosing from a small set $\Sigma$ after a prefix $t_1$ and a repeated-token context $t_2$ of length $\ge H$. Estimate logits from $K$ samples per $(t_1,t_2)$. Flag green/red shifts that depend on $t_2$ but not $t_1$. Permutation test on $S_x$. On SynthID / Gemma-7B they report median $p=0.000$ across 100 runs (appendix F.4). **Must estimate $H$, not overestimate** (cache).
2. **Fixed-sampling (Kuditipudi et al., 2024 ITS/EXP).** Rarefaction / uniqueness of outputs to a high-diversity prompt. Distortion-free in expectation vs seed; practical implementations lack diversity.
3. **Cache-augmented / unbiased (Hu et al., 2024; Wu et al.).** Tests aimed at schemes that cache or reweight to preserve the distribution.

SRI Lab (2024), *Probing Google DeepMind’s SynthID-Text watermark*: Red-Green test on a **local** SynthID-Text deployment passes ($p\approx 0$); Gemini 1.5 API showed no reliable watermark (matches “watermark in app/web, not API” claims). **Web deployments are the wrong query surface** for thousands of similar prompts. That sentence is hold 3 in one line: **the hole that is already 99/100 is the API; the hole that is 25/48 is the webpage.**

Gloaguen also ran tests on GPT-4, Claude 3, Gemini 1.0 Pro and did not find strong evidence at that time. This lab must not call paid APIs unless Jens explicitly asks (AGENTS.md). Local Hugging Face generators only for any replication here.

**Alignment with lock A.** Gloaguen: many queries, constructed prompts, estimate of $p(x\mid t_1,t_2)$. Lock A: natural prompts, four draws, count-table LR, leave-one-family-out. Same **access class** (repeatable generation), different **statistic**. Lock A does not need their fruit-list template. Their test does not need matched unmarked twins if they compare across $t_2$ on a single (putatively marked) API. This lab’s twins are stronger (explicit $P_o$). A product could **offer both**: (i) twin-table ranking if the auditor can toggle the mixin; (ii) Gloaguen Red-Green if the auditor has only one API but many queries.

**Cost.** Gloaguen include a query-cost appendix. Lock A uses 800 generations per 100 families × 2 (marked/unmarked) at 128 tokens — cheap on GPT-2, not cheap on a paid frontier API. The opening product (hold 1) needs tables built once, then **zero** queries at test time. These are different SKUs.

### 3.3 Second pass over hold 3 (statistical watermarking as sample size)

Huang et al. (2023, arXiv:2312.07930): number of i.i.d. tokens for small Type I/II scales as $\Theta(h^{-1}\log(1/h))$ in entropy $h$, better than $h^{-2}$. **Several draws of the same prompt** are how this lab buys sample size without a longer hash window. Four draws × 100 families is a population. One file × 128 tokens under $\Hw=12$ is a body with no colliding 12-grams.

Kuditipudi et al. (2024): distortion-free watermarks with alignment detection; Gloaguen’s fixed-sampling test is the black-box attack on the “undetectable to users” slogan. Aaronson and Kirchner (2023): Gumbel / exponential-minimum; a named future mixin freeze in PROTOCOL-next-kgw.md, not this file.

Pang et al. (2024): no free lunch; public detection APIs as oracles. An API product that answers “is the generator marked?” **is** a public oracle for the **scheme**, which Jovanović et al. (2024) and Wu and Chandrasekaran (2024) can feed. That is an ethics/threat note, not a reason to deny the measurement. Gloaguen discuss implications in their appendix A.

### 3.4 Third pass over hold 3 (product sketch)

**SKU A — Generator test (already empirically 99/100 on public GPT-2 twins).**

- Input: API or local mixin with on/off, or two endpoints.
- Protocol: $P$ prompts, $n=4$ draws, max tokens 128, leave-one-family-out interpolate last-4 with $k=\Hw$ when known (hold 2), else last-4 for public DeepMind-30.
- Output: $D_p$ sign count, permutation $p$ on prompt means, `used_keys=false`.
- Do not report isolated 352/400 as the headline.

**SKU B — Gloaguen Red-Green on a single marked API.**

- Input: one generator, many queries, estimate $H$.
- Output: $p$-value for scheme presence, optional $\hat h$, $\hat\delta$.
- SynthID: match $H$ to `ngram_len-1`; do not overestimate (cache).
- Do not run on paid Claude/Qwen-plus.

**SKU C — Webpage / isolated file.**

- This is **not** 99/100. Headline **25/48**. Opening product (hold 1) if the auditor accepts abstention. TTP-Detect (hold 2) if the auditor has paired references and a proxy budget. Do not put SKU A’s number on SKU C’s box.

### 3.5 What 99/100 is consistent with, and what it is not

Allowed (CITING.md example): under frozen lock A on `public-deepmind-30` GPT-2 twins, prompt-group interpolate ranking was **99/100**. Consistent with a learnable next-token footprint of this tournament instance without detector keys.

Not: a distinguisher of the kind Christ et al. (2024) forbid for *their* scheme. Not Zhang et al. (2024). Not isolated-file detection. Not production Gemini. Not “key-free detection is possible” as an unscoped theorem.

---

## 4. Exhaustion loops: extra promising ideas (holds 1–3 again, plus neighbours)

Each item is an idea that survived a second look. None is a new `probe --methods` name on 12×4 / 36×4.

### 4.1 Combine hold 1 and hold 2 (already seen in §2.2)

On Hw=12 12-family twins, last-12 tokhits **10/12** ranking, decided precision **0.806**, **23/48** marked abstentions, body coverage **0**. The opening product **plus** matched $k$ is the honest Hw=12 SKU. Interpolate last-4 **6/12** is the dishonest SKU (Witten–Bell on the wrong window).

### 4.2 Combine hold 1 and hold 3

Build opening tables from **API draws** (SKU A), ship the atom book for **offline** SKU C with abstention. Coverage of original-12 from 100 one-liners is **18/48**. The API is how you grow the catalogue; the webpage is how you spend it. Leftover-18 is closed for unrelated scenes: more one-liners do not cover `Closing is the`. Grow the catalogue with **register-matched** tails, or accept abstention.

### 4.3 Combine hold 2 and hold 3

Gloaguen estimate $H$ from queries; this lab’s `--context-len` should be set to that $\hat H$. A joint pipeline: (1) Red-Green / cache tests → $\hat H$, scheme family; (2) if short-window KGW-like, use last-1 / last-4 **body** tables; (3) if SynthID-like long $H$, use opening tokhits only.

### 4.4 Unigram / fixed split as the “easy” limit

Zhao et al. (2024) Unigram-Watermark; TTP Unigram F1 ≈ 1.0; this lab’s KGW $h=1$ last-1 tail **12/12**. If a provider ships a **fixed** green list, key-free body detection is the central product, not a footnote. If they ship $\Hw=12$ tournament, it is not.

### 4.5 Adaptive-rank / NLL without a full TTP reimplementation

TTP’s module 4 is token NLL mean and volatility, direction-adaptive. This lab already has `pivot` (unmarked-LM choice geometry, entropy pooling, argmax snap) and `rankpath` (five-symbol rank tables). Opening rankpath 12-LOO **11/12**, isolated **41/48**, but OOD 24-short **10/12 / 28/48**, control **6/48**, leftover rankpath **12/20 vs 14/20**. Rankpath is **not** the high-precision product (hold 1). It may still be the right **cheap proxy** for TTP adaptive-rank on a new corpus. Compare rankpath vs TTP $A_{Ada}$ on the same twins before training a neural proxy. Do not add rankpath to the old 12×4 freeze.

### 4.6 Mahalanobis / energy on count-table features

Instead of hidden states, take the vector of per-position tokhits contributions (sparse, mostly zeros). Two-sample geometry on that vector is TTP modules 2–3 without instruction tuning. If it fails, the proxy network was doing the work. If it works, count tables already contain the geometry. Existing `learn` hashlog/tokmlp/charcnn on 4-token 24→12 did **not** beat poshits AUC 0.873 (tokmlp 0.714, hashlog 0.606). Learned scorers → Distil/Qwen were chance. Do not expect a cheap MLP to replace TTP’s proxy on OOD; do expect a diagnostic.

### 4.7 Snap-rate / argmax (removal, not detection)

`scrub` / snap-rate: official mean on 48 marked files **0.622 → 0.499**. Detection-adjacent: if a provider’s API allows temperature 0, Gloaguen-style tests change. Not a key-free file detector. Keep it in the inventory as an API **attack** surface, not a SKU C product.

### 4.8 Instance contrast as a product filter

`contrast` public vs control-shuffled-30: poshits/postokhits **0/48** control `lr>0`. A shipped opening book should **fail** on a second key. That is a unit test for “this instance,” not tournament-in-general. Second-key in-domain lock A (PROTOCOL-isolated-xkey.md) interpolate last-4 **7/12**, isolated **30/48 vs 25/48**; H-xkey-iso fails as a raw count; do not sell **30/48**.

### 4.9 Official keyed leftover bound (honesty, not a key-free win)

Leftover-20 official **20/20** at prefix-128 (keys). Leftover-15 official **15/15** at prefix-5 (keys). Key-free leftover last-4 is chance. The keys still see leftover files. A product that pretends leftover is unmarked is lying; a product that **abstains** on leftover is aligned with tokhits.

### 4.10 Two-sample tests from statistics (MMD, energy)

TTP’s energy score is already a two-sample energy distance (related to Cramér / energy statistics; Gretton et al.’s MMD is the RKHS cousin). Running MMD on $z(t)$ is a module they could have added. Running MMD on **token-id histograms of openings** is a hold-1 two-sample test across draws of the same prompt (hold 3). Cheap. Not a new probe method if implemented as a notebook on existing JSON.

### 4.11 Selective generation (Heng & Soh’s outlook)

They suggest LLMs abstain when uncertain. The **watermark auditor** can abstain; the **generator** that refuses to emit unseen openings is a different paper. Out of scope except as a citation bridge.

### 4.12 Public verifiability vs key-free indication

Google DeepMind issue 22: publicly verifiable detection still not in `detector_mean`. Duan et al. (2025) ZK-wrap keys. Fairoze et al. (2025) redesign the scheme. Liu et al. (2024) UPV. Wang et al. (2026) TTP. This lab: count tables. Five answers to “third party without the secret.” They are not interchangeable. A promising **policy** idea: an auditor SKU A (99/100) plus published opening book (hold 1) is available **now** on the public mixin without waiting for ZK circuits.

### 4.13 Claude / Anthropic (future, not now)

Anthropic (2026a, 2026b): a version of SynthID-Text; production keys not public. `score` cannot read it. Do not train a classifier on the pre-mark corpus alone. Paired before/after is the experiment. Hold 3 (API) may be blocked if the mark is app/web only (SRI on Gemini). Hold 1 (openings) needs twins. Hold 2 (TTP) needs a watermark flag. Record so the gap is cited, not invented. LOGBOOK after every resample.

### 4.14 Paraphrase robustness (known threat, not measured here)

Krishna et al. (2023) DIPPER; Han et al. (2025) SynGuard preprint; TTP-Detect reports Dipper ablations (adaptive rank not uniformly best under Dipper). This lab’s neighbourhood paraphrases: official **12/12**, openings change. Opening product **fails open** (abstain) under paraphrase; that is acceptable if advertised. Body product on KGW last-1 may be more paraphrase-brittle (Zhao et al. argue Unigram is more edit-robust **for keyed $z$**; key-free last-1 tables are a different object).

### 4.15 Mixer width / last-$k$ occupancy-free already closed on 12×4

PROTOCOL-next.md: occupancy-free last-$k$ at frozen mixer is the last order axis on that corpus; in-domain last-1 is chance; last-3 prompt **11/12** has t=0 **24/48**. Do not reopen hashed mixer search. Hold 2’s `--context-len 12` is **not** that search: it is matching a **named** `ngram_len=13` corpus.

### 4.16 Kirchenbauer 100×4 (named, prediction)

PROTOCOL-next-kgw names 100 families. Prediction from §2.2.2: tail windows remain above chance; opening 0:4 may be **weaker** than the tail (8/12 vs 12/12 on the 12-family last-1 diagnostic). If that holds, the **body product** is real for green-list $h=1$ and must not be confused with SynthID Hw=12.

### 4.17 Aaronson–Kirchner Gumbel mixin (named third freeze, not this file)

Distortion-free in the exponential-minimum sense. Gloaguen fixed-sampling tests are the API analogue. Count-table last-4 may fail like Hw=12 or succeed like Kuditipudi diversity failure. Do not guess; freeze first.

### 4.18 Surface UTF-8 hashpool

12-LOO **10/12**, AUC **0.602**. Cross-generator hope; in-domain weak. Not the precision-1 product. Keep as a negative.

### 4.19 Prompt-context geometry

Opening pivot-lda with prompt context: **7/12**, AUC 0.468. Worse than chance. Isolated-file protocol must **not** condition on the prompt if the product is a webpage. API product **may** condition on the prompt (Gloaguen does). Another SKU distinction.

### 4.20 Nested Youden vs $\tau=0$

100×4 lock A nested-by-stem **322/400 vs 338/400** is in-family and not **25/48**. Occupancy lock B **392/400 vs 382/400** with 198/400 unmarked `n_used=0`. Nested thresholds on already-OOF scores are not a product. $\tau=0$ plus abstention is.

---

## 5. Map of SKUs (so the three holds cannot be collapsed)

| SKU | Access | Statistic | Best evidence in this lab | Adjacent paper | Isolated **25/48**? |
|---|---|---|---|---|---|
| Opening book with abstention | Finished string + tables | occupancy-free LR; ABSTAIN if `n_used=0` | postokhits decided precision **1.000** (16/48 coverage on OOD 24→12) | Chow (1970); Geifman & El-Yaniv (2017); Heng & Soh (2026) | No. Coverage-bound recall. |
| Hw-matched occupancy-free tables | Finished string + tables; $k \approx \Hw$ | hits/tokhits at $k$ | Hw=12 last-12 tokhits **10/12** vs interpolate last-4 **6/12**; body still 0/12 | Gloaguen $H$ matching; Witten & Bell (1991) | No. |
| Short-window body tables | Finished string + tables | last-1 / last-4 on $h=1$ KGW | KGW last-1 64:128 hits **12/12**, AUC 0.932 | Kirchenbauer et al. (2023); Zhao et al. (2024) | No. Different mixin. |
| TTP-Detect | Paired refs + proxy + query text | kNN + Mahalanobis + energy + adaptive NLL | **Not run here.** Paper SynthID F1 ~0.84–0.91 | Wang et al. (2026); Gu et al. (2024) | Unknown on our twins. |
| Generator / multi-draw | Repeatable API or mixin toggle | prompt-mean LR or Gloaguen tests | lock A **99/100**; Gloaguen SynthID $p\approx 0$ local | Gloaguen et al. (2025); SRI Lab (2024) | No. Different grain. |
| Official keyed `score` | Keys | `detector_mean` | **12/12**, **100/100**, Hw=12 **400/400**, leftover **20/20** | Dathathri et al. (2024) | Not key-free. |

---

## 6. Exact reproduction commands for the 2026-09-03 diagnostics

Environment: `source .venv/bin/activate`, `used_keys=false`. Do not overwrite `experiments/2026-09-03-probe-12x4-ngram13-hard-last4/` or `experiments/2026-09-03-probe-12x4-kgw-hard-last4/`.

```bash
# A. Hw=12, match k=12, occupancy-free vs interpolate
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods unigram,hits,tokhits,interpolate,hard --context-len 12 --skip-hashpool \
  --windows 0:12,16:32,64:128 \
  --out-dir /tmp/probe-ngram13-12x4-ctx12

# B. Hw=12, last-4 occupancy-free (same twins as the 6/12 freeze)
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-ngram13 \
  --methods hits,tokhits,interpolate --context-len 4 --skip-hashpool \
  --windows 0:4,16:32,64:128 \
  --out-dir /tmp/probe-ngram13-12x4-ctx4-hits

# C. KGW context_width=1, match k=1, body windows
python -m text_watermark_tools probe experiments/2026-09-03-pair-12x4-kgw \
  --methods hits,tokhits,interpolate --context-len 1 --skip-hashpool \
  --windows 0:4,16:32,64:128 \
  --out-dir /tmp/probe-kgw-12x4-ctx1
```

Expected headlines (strict `>` prompt wins, 12 families):

- A tokhits **10/12**, AUC 0.803; interpolate **6/12**; windows 16:32 and 64:128 hits/tokhits **0/12**.
- B tokhits **9/12**, AUC 0.712; interpolate **6/12**; window 0:4 tokhits **10/12**.
- C hits **12/12**, AUC 0.975; window 64:128 hits **12/12**, AUC 0.932; window 0:4 hits **8/12**.

100-family Hw=12 body collapse (leave-one-family-out interpolate last-4, same flags as the **76/100** freeze, windows not overwritten into that dump): public $\Hw=4$ tokens $[64{:}128)$ interpolate **93/100**, AUC **0.726**; $\Hw=12$ the same slice **50/100**, AUC **0.501**, `prompt_sign_p=0.2004`. Full-file $\Hw=12$ interpolate remains **76/100**. Opening residual: 0:4 interpolate **86/100**, tokhits **96/100**. Do not overwrite `experiments/2026-09-03-probe-100x4-ngram13-hard-last4/`. Unmarked 2-versus-2 placebo on public 100×4: interpolate **57/100**; opening 0:4 **49–51/100**. Those 100-family window commands are recorded in the LOGBOOK / companion body-collapse note if merged; they are not a new method name.

---

## 7. Full bibliography (every work this note relies on or distinguishes)

Archival venue preferred. Preprints and blogs labelled. Keys match [research/references.bib](research/references.bib) when present; additional items below are cited in author–year for this note and must not be invented beyond the records fetched 2026-09-03.

### 7.1 Already in `research/references.bib`

- Dathathri et al. (2024). *Nature, 634*, 818–823. SynthID-Text. Keyed `score`.
- Google DeepMind (2024). synthid-text reference implementation. `(hash >> 30) % 2`.
- Kirchenbauer et al. (2023). ICML, PMLR 202. KGW. This lab’s `--mixin kgw` freeze.
- Aaronson and Kirchner (2023). Talk slides. Gumbel / exponential-minimum.
- Kuditipudi et al. (2024). TMLR. Distortion-free; Gloaguen fixed-sampling family.
- Christ et al. (2024). COLT, PMLR 247. Cryptographic undetectability. **Not refuted.**
- Zhang et al. (2024). ICML, PMLR 235. Strong watermarking impossibility. **Not refuted.**
- Jovanović et al. (2024). ICML. Watermark stealing. Not implemented here.
- Wu and Chandrasekaran (2024). ACL. Color-aware substitutions.
- Pang et al. (2024). NeurIPS. No free lunch; detection APIs as oracles.
- Gloaguen et al. (2025). ICLR. Black-box **generator** tests. Hold 3.
- SRI Lab, ETH Zurich (2024). Blog. SynthID local Red-Green test. Cite Gloaguen for method.
- Krishna et al. (2023). NeurIPS. DIPPER. Not downloaded here.
- Wang et al. (2026). ACL Findings. TTP-Detect. Hold 2.
- Omidi, Dong, and Wang (2026). arXiv:2603.03410. Keyed SynthID theory. Preprint.
- Duan, Xiang, and Zhang (2025). arXiv:2510.26274. PVMark ZK. Preprint.
- Han, Li, Ni, and Zulkernine (2025). arXiv:2508.20228. SynGuard / robustness. Preprint.
- Anthropic (2026a, 2026b). Claude watermark announcements. Future test.
- Google DeepMind (2024). GitHub issue 22. Publicly verifiable detection request.
- Clopper and Pearson (1934). *Biometrika*.
- McNemar (1947). *Psychometrika*.

### 7.2 Additional records used in this note (verified 2026-09-03)

- Chow, C. K. (1957). An optimum character recognition system using decision functions. *IRE Transactions on Electronic Computers, EC-6*(4), 247–254.
- Chow, C. K. (1970). On optimum recognition error and reject tradeoff. *IEEE Transactions on Information Theory, 16*(1), 41–46. doi:10.1109/TIT.1970.1054406.
- Neyman, J., & Pearson, E. S. (1933). On the problem of the most efficient tests of statistical hypotheses. *Philosophical Transactions of the Royal Society A, 231*, 289–337.
- Bartlett, P. L., & Wegkamp, M. H. (2008). Classification with a reject option using a hinge loss. *Journal of Machine Learning Research, 9*, 1823–1840.
- Geifman, Y., & El-Yaniv, R. (2017). Selective classification for deep neural networks. In *Advances in Neural Information Processing Systems 30*.
- Heng, A., & Soh, H. (2026). Know when to abstain: optimal selective classification with likelihood ratios. ICLR 2026. arXiv:2505.15008.
- Witten, I. H., & Bell, T. C. (1991). The zero-frequency problem: Estimating the probabilities of novel events in adaptive text compression. *IEEE Transactions on Information Theory, 37*(4), 1085–1094. doi:10.1109/18.87000. (Witten–Bell; interpolate’s unseen mass.)
- Chen, S. F., & Goodman, J. (1999). An empirical study of smoothing techniques for language modeling. *Computer Speech & Language, 13*(4), 359–394. (Survey placing Witten–Bell among interpolated smoothers.)
- Gu, C., Li, X. L., Liang, P., & Hashimoto, T. (2024). On the learnability of watermarks for language models. ICLR 2024. arXiv:2312.04469. OpenReview: https://openreview.net/forum?id=9k0krNzvlV.
- Zhao, X., Ananth, P., Li, L., & Wang, Y.-X. (2024). Provable robust watermarking for AI-generated text. ICLR 2024. Unigram-Watermark. arXiv:2306.17439.
- Liu, A., Pan, L., Hu, X., Li, S., Wen, L., King, I., & Yu, P. S. (2024). An unforgeable publicly verifiable watermark for large language models. ICLR 2024. UPV. arXiv:2307.16230.
- Hu, Z., Chen, L., Wu, X., Wu, Y., Zhang, H., & Huang, H. (2024). Unbiased watermark for large language models. ICLR 2024. arXiv:2310.10669.
- Fairoze, J., Garg, S., Jha, S., Mahloujifar, S., Mahmoody, M., & Wang, M. (2025). Publicly-detectable watermarking for language models. *IACR Communications in Cryptology, 1*(4). doi:10.62056/ahmpdkp10. arXiv:2310.18491.
- Huang, B., Zhu, H., Zhu, B., Lee, J. D., Jiao, J., & Jordan, M. I. (2023). Towards optimal statistical watermarking. arXiv:2312.07930. Preprint. (Author order as on v2 HTML; some indexes list Zhu, B. second.)
- Pan, L., Liu, A., He, Z., Gao, Z., Zhang, X., Nakagawa, Y., Wen, L., & King, I. (2024). MarkLLM: An open-source toolkit for LLM watermarking. (Cited by Wang et al., 2026, for hyperparameters; confirm venue before a paper bibliography. Used here only as “TTP-Detect’s MarkLLM configs,” not as an independent claim.)

If a later paper bibliography is compiled, add these to `references.bib` rather than leaving them only here. Do not add papers that were not checked.

### 7.3 Laboratory documents (not papers)

[research/CITING.md](research/CITING.md), [research/related-work.md](research/related-work.md), [research/annotated-bibliography.md](research/annotated-bibliography.md), [research/narrative.md](research/narrative.md), [research/threat-model.md](research/threat-model.md), [research/how-synthid-works.md](research/how-synthid-works.md), [research/key-free-tokhits.md](research/key-free-tokhits.md), [research/key-free-contrast.md](research/key-free-contrast.md), [research/key-free-twins.md](research/key-free-twins.md), [research/key-free-rankpath.md](research/key-free-rankpath.md), [research/key-free-probe.md](research/key-free-probe.md), [research/results-ledger.md](research/results-ledger.md), [research/PROTOCOL-next.md](research/PROTOCOL-next.md), [research/PROTOCOL-next-longctx.md](research/PROTOCOL-next-longctx.md), [research/PROTOCOL-next-kgw.md](research/PROTOCOL-next-kgw.md), [research/PROTOCOL-isolated.md](research/PROTOCOL-isolated.md), [research/PROTOCOL-isolated-split.md](research/PROTOCOL-isolated-split.md), [research/PROTOCOL-isolated-windows.md](research/PROTOCOL-isolated-windows.md), [research/PROTOCOL-h2-absolute.md](research/PROTOCOL-h2-absolute.md), [research/invertibility.md](research/invertibility.md), [research/LOGBOOK.md](research/LOGBOOK.md), AGENTS.md.

---

## 8. Non-claims (read before citing this file)

1. This file does **not** replace **9/12**, **25/48**, **36/36**, or lock A **99/100**.
2. Last-12 tokhits **10/12** on Hw=12 original-12 is **not** published 12-LOO hard last-4 **9/12** and **not** **25/48**. Kitchen has 0 isolated TPs. Body coverage is 0.
3. KGW last-1 **46/48** / tail **12/12** is **not** SynthID isolated detection and **not** **25/48**.
4. Decided precision **1.000** is **not** recall **16/48**, and **16/48** is **not** **25/48**.
5. TTP-Detect is **not** implemented here. Their SynthID F1 is **not** a number on our GPT-2 twins.
6. Gloaguen et al. (2025) is **not** lock A. Lock A is **not** a webpage detector.
7. Christ et al. (2024) and Zhang et al. (2024) are **not** refuted.
8. No new `probe --methods` name. `--context-len` is an existing fit knob.
9. Keys, `hash_iv`, and `detector_mean` are not used in the key-free commands.
10. Claude is not detected. Paid APIs were not called.

---

## 9. What to do next (priority if the calendar still has room)

1. **Ship the shop window as three SKUs** in narrative/threat-model prose (not this PR’s job unless asked): opening+abstain; generator multi-draw **99/100**; isolated **25/48** leftover chance.
2. **Hw-matched occupancy-free** as the default analysis companion whenever `ngram_len` ≠ 5: same methods, `--context-len ngram_len-1`, report hits/tokhits **and** interpolate. Already legal under PROTOCOL-next-longctx’s “no new method names.”
3. **TTP-Detect comparison** on a **new** frozen corpus (related-work.md), not a reslice of the original 12.
4. **Gloaguen Red-Green** on local GPT-2 public mixin with estimated $H=4$, as a hold-3 sibling to lock A, if CPU budget allows; do not call paid APIs.
5. **KGW 100×4** as named: test the prediction that the tail stays alive (body product).

Until those exist, the promising ideas that already have evidence are:

- Occupancy-free openings are a **precision-1 selective classifier**, not a failed 48-file detector.
- Last-4 interpolate on $\Hw=12$ is the **wrong window**; occupancy-free last-12 ranking **10/12** is still openings; KGW $h=1$ last-1 **reads 128-token bodies**.
- **99/100** is an **API / multi-draw** result, which is the setting Gloaguen et al. (2025) treat as the realistic black box, and which is not a file on the internet.
