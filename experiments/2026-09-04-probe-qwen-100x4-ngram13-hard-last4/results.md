# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-qwen-100x4-ngram13 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 74/100 | 0.599 | 361/400 | 115/400 | 0.0004998 | 0.1809 |
| interpolate | 76/100 | 0.647 | 273/400 | 201/400 | 0.0004998 | 0.2995 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 74/100 | 2/74 (058, 064) | 25 |
| interpolate | 76/100 | 1/76 (064) | 23 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 361/39 | 285/115 | 0.559 |
| interpolate | 0/400 | 0/400 | 273/127 | 199/201 | 0.578 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 358/400 | 110/400 | -0.0006 | 0.895 | 0.275 |
| interpolate | 214/400 | 262/400 | 0.1183 | 0.535 | 0.655 |

hard auc=0.599 mean_pos=0.0925 mean_neg=-0.0883 diff=0.1809 pos>0=361/400 neg<=0=115/400 perm_p=0.0004998 (file-level, descriptive) binom_p=9.472e-67 (file-level, descriptive) youden_t=0.0000 youden_sens=0.902 youden_spec=0.287 J=0.190
hard prompts_marked_above=74/100 ranking_without_isolated_tp=2/74 ranking_losses_with_isolated_tp=25 instance=key-free-counts used_keys=False
interpolate auc=0.647 mean_pos=0.1059 mean_neg=-0.1936 diff=0.2995 pos>0=273/400 neg<=0=201/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.135e-13 (file-level, descriptive) youden_t=0.1200 youden_sens=0.535 youden_spec=0.680 J=0.215
interpolate prompts_marked_above=76/100 ranking_without_isolated_tp=1/76 ranking_losses_with_isolated_tp=23 instance=key-free-interpolate used_keys=False
