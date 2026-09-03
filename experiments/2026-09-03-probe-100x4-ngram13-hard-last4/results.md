# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-100x4-ngram13 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 66/100 | 0.579 | 215/400 | 221/400 | 0.0004998 | 0.0271 |
| interpolate | 76/100 | 0.666 | 267/400 | 222/400 | 0.0004998 | 0.1560 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 66/100 | 2/66 (071, 090) | 26 |
| interpolate | 76/100 | 0/76 | 18 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 215/185 | 179/221 | 0.546 |
| interpolate | 0/400 | 0/400 | 267/133 | 178/222 | 0.600 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 169/400 | 276/400 | 0.0277 | 0.422 | 0.690 |
| interpolate | 250/400 | 209/400 | -0.0080 | 0.625 | 0.522 |

hard auc=0.579 mean_pos=0.0127 mean_neg=-0.0144 diff=0.0271 pos>0=215/400 neg<=0=221/400 perm_p=0.0004998 (file-level, descriptive) binom_p=0.07348 (file-level, descriptive) youden_t=0.0267 youden_sens=0.438 youden_spec=0.693 J=0.130
hard prompts_marked_above=66/100 ranking_without_isolated_tp=2/66 ranking_losses_with_isolated_tp=26 instance=key-free-counts used_keys=False
interpolate auc=0.666 mean_pos=0.1298 mean_neg=-0.0262 diff=0.1560 pos>0=267/400 neg<=0=222/400 perm_p=0.0004998 (file-level, descriptive) binom_p=9.572e-12 (file-level, descriptive) youden_t=-0.0299 youden_sens=0.725 youden_spec=0.520 J=0.245
interpolate prompts_marked_above=76/100 ranking_without_isolated_tp=0/76 ranking_losses_with_isolated_tp=18 instance=key-free-interpolate used_keys=False
