# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-09-04-pair-distil-12x4-ngram13 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 6/12 | 0.485 | 16/48 | 26/48 | 0.7151 | -0.0099 |
| interpolate | 9/12 | 0.563 | 21/48 | 28/48 | 0.09595 | 0.0567 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| hard | 6/12 | 1/6 (05-kitchen) | 4 (01-harbour, 02-night-bus, 03-library, 10-office) |
| interpolate | 9/12 | 1/9 (05-kitchen) | 3 (01-harbour, 06-station, 07-rain) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 16/32 | 22/26 | 0.421 |
| interpolate | 0/48 | 0/48 | 21/27 | 20/28 | 0.512 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 33/48 | 17/48 | -0.0611 | 0.688 | 0.354 |
| interpolate | 39/48 | 13/48 | -0.1832 | 0.812 | 0.271 |

hard auc=0.485 mean_pos=-0.0180 mean_neg=-0.0082 diff=-0.0099 pos>0=16/48 neg<=0=26/48 perm_p=0.7151 (file-level, descriptive) binom_p=0.9934 (file-level, descriptive) youden_t=-0.0624 youden_sens=0.750 youden_spec=0.375 J=0.125
hard prompts_marked_above=6/12 ranking_without_isolated_tp=1/6 ranking_losses_with_isolated_tp=4 instance=key-free-counts used_keys=False
interpolate auc=0.563 mean_pos=-0.0070 mean_neg=-0.0638 diff=0.0567 pos>0=21/48 neg<=0=28/48 perm_p=0.09595 (file-level, descriptive) binom_p=0.8438 (file-level, descriptive) youden_t=-0.1876 youden_sens=0.854 youden_spec=0.312 J=0.167
interpolate prompts_marked_above=9/12 ranking_without_isolated_tp=1/9 ranking_losses_with_isolated_tp=3 instance=key-free-interpolate used_keys=False
