# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-distil-12x4-aaronson context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 7/12 | 0.637 | 8/48 | 48/48 | 0.001999 | 0.2083 |
| interpolate | 7/12 | 0.618 | 0/48 | 48/48 | 0.03048 | 0.2768 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 7/12 | 5/7 (01-harbour, 02-night-bus, 03-library, 05-kitchen, 12-ferry-queue) | 0 |
| interpolate | 7/12 | 7/7 | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 8/40 | 0/48 | 1.000 |
| interpolate | 0/48 | 0/48 | 0/48 | 0/48 | nan |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 20/48 | 44/48 | -0.5594 | 0.417 | 0.917 |
| interpolate | 20/48 | 45/48 | -1.8997 | 0.417 | 0.938 |

hard auc=0.637 mean_pos=-0.6404 mean_neg=-0.8486 diff=0.2083 pos>0=8/48 neg<=0=48/48 perm_p=0.001999 (file-level, descriptive) binom_p=1 (file-level, descriptive) youden_t=-0.5591 youden_sens=0.417 youden_spec=0.938 J=0.354
hard prompts_marked_above=7/12 ranking_without_isolated_tp=5/7 ranking_losses_with_isolated_tp=0 instance=key-free-counts used_keys=False
interpolate auc=0.618 mean_pos=-2.1821 mean_neg=-2.4589 diff=0.2768 pos>0=0/48 neg<=0=48/48 perm_p=0.03048 (file-level, descriptive) binom_p=1 (file-level, descriptive) youden_t=-1.9107 youden_sens=0.500 youden_spec=0.958 J=0.458
interpolate prompts_marked_above=7/12 ranking_without_isolated_tp=7/7 ranking_losses_with_isolated_tp=0 instance=key-free-interpolate used_keys=False
