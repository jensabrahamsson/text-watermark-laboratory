# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-03-pair-distil-100x4-kgw context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 82/100 | 0.666 | 180/400 | 322/400 | 0.0004998 | 0.1380 |
| interpolate | 100/100 | 0.915 | 346/400 | 337/400 | 0.0004998 | 0.5874 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 82/100 | 13/82 | 9 |
| interpolate | 100/100 | 0/100 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/400 | 0/400 | 180/220 | 78/322 | 0.698 |
| interpolate | 0/400 | 0/400 | 346/54 | 63/337 | 0.846 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 247/400 | 267/400 | -0.0939 | 0.618 | 0.667 |
| interpolate | 365/400 | 319/400 | -0.1151 | 0.912 | 0.797 |

hard auc=0.666 mean_pos=0.0355 mean_neg=-0.1025 diff=0.1380 pos>0=180/400 neg<=0=322/400 perm_p=0.0004998 (file-level, descriptive) binom_p=0.9799 (file-level, descriptive) youden_t=-0.0940 youden_sens=0.623 youden_spec=0.670 J=0.292
hard prompts_marked_above=82/100 ranking_without_isolated_tp=13/82 ranking_losses_with_isolated_tp=9 instance=key-free-counts used_keys=False
interpolate auc=0.915 mean_pos=0.1509 mean_neg=-0.4365 diff=0.5874 pos>0=346/400 neg<=0=337/400 perm_p=0.0004998 (file-level, descriptive) binom_p=1.517e-53 (file-level, descriptive) youden_t=-0.1137 youden_sens=0.917 youden_spec=0.810 J=0.728
interpolate prompts_marked_above=100/100 ranking_without_isolated_tp=0/100 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
