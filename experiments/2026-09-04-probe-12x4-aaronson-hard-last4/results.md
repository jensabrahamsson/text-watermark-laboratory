# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-12x4-aaronson context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 12/12 | 0.976 | 24/48 | 48/48 | 0.0004998 | 1.0660 |
| interpolate | 11/12 | 0.955 | 8/48 | 48/48 | 0.0004998 | 1.7379 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 12/12 | 6/12 (01-harbour, 02-night-bus, 03-library, 06-station, 08-letter, 09-workshop) | 0 |
| interpolate | 11/12 | 9/11 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 24/24 | 0/48 | 1.000 |
| interpolate | 0/48 | 0/48 | 8/40 | 0/48 | 1.000 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 40/48 | 46/48 | -0.5902 | 0.833 | 0.958 |
| interpolate | 40/48 | 46/48 | -1.7547 | 0.833 | 0.958 |

hard auc=0.976 mean_pos=0.0139 mean_neg=-1.0522 diff=1.0660 pos>0=24/48 neg<=0=48/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.5573 (file-level, descriptive) youden_t=-0.5913 youden_sens=0.917 youden_spec=0.979 J=0.896
hard prompts_marked_above=12/12 ranking_without_isolated_tp=6/12 ranking_losses_with_isolated_tp=0 instance=key-free-counts used_keys=False
interpolate auc=0.955 mean_pos=-0.9014 mean_neg=-2.6393 diff=1.7379 pos>0=8/48 neg<=0=48/48 perm_p=0.0004998 (file-level, descriptive) binom_p=1 (file-level, descriptive) youden_t=-1.7354 youden_sens=0.917 youden_spec=0.979 J=0.896
interpolate prompts_marked_above=11/12 ranking_without_isolated_tp=9/11 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
