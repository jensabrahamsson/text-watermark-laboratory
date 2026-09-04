# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-09-03-pair-100x4-ngram13 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=['0:4', '4:16', '16:32', '32:64', '64:128'] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. ranking_without_isolated_tp counts prompt wins with no marked file lr>0 — those stems rank because unmarked is more negative, not because any isolated file signs. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 76/100 | 0.666 | 267/400 | 222/400 | 0.0004998 | 0.1560 |
| hard | 66/100 | 0.579 | 215/400 | 221/400 | 0.0004998 | 0.0271 |
| hits | 91/100 | 0.843 | 332/400 | 255/400 | 0.0004998 | 0.5448 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 76/100 | 0/76 | 18 |
| hard | 66/100 | 2/66 (071, 090) | 26 |
| hits | 91/100 | 3/91 (026, 054, 071) | 8 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/400 | 0/400 | 267/133 | 178/222 | 0.600 |
| hard | 0/400 | 0/400 | 215/185 | 179/221 | 0.546 |
| hits | 0/400 | 1/400 | 332/68 | 145/254 | 0.696 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| interpolate | 250/400 | 209/400 | -0.0080 | 0.625 | 0.522 |
| hard | 169/400 | 276/400 | 0.0277 | 0.422 | 0.690 |
| hits | 274/400 | 348/400 | 0.2053 | 0.685 | 0.870 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 0:4 | interpolate | 86/100 | 0.823 | 254/400 | 366/400 |
| 0:4 | hard | 82/100 | 0.763 | 250/400 | 338/400 |
| 0:4 | hits | 95/100 | 0.875 | 300/400 | 360/400 |
| 4:16 | interpolate | 75/100 | 0.645 | 144/400 | 346/400 |
| 4:16 | hard | 47/100 | 0.476 | 44/400 | 373/400 |
| 4:16 | hits | 39/100 | 0.498 | 23/400 | 381/400 |
| 16:32 | interpolate | 57/100 | 0.529 | 182/400 | 235/400 |
| 16:32 | hard | 57/100 | 0.510 | 173/400 | 260/400 |
| 16:32 | hits | 49/100 | 0.494 | 224/400 | 146/400 |
| 32:64 | interpolate | 57/100 | 0.520 | 85/400 | 344/400 |
| 32:64 | hard | 55/100 | 0.526 | 155/400 | 220/400 |
| 32:64 | hits | 61/100 | 0.528 | 92/400 | 341/400 |
| 64:128 | interpolate | 50/100 | 0.501 | 63/400 | 362/400 |
| 64:128 | hard | 59/100 | 0.527 | 175/400 | 249/400 |
| 64:128 | hits | 53/100 | 0.516 | 90/400 | 329/400 |

interpolate auc=0.666 mean_pos=0.1298 mean_neg=-0.0262 diff=0.1560 pos>0=267/400 neg<=0=222/400 perm_p=0.0004998 (file-level, descriptive) binom_p=9.572e-12 (file-level, descriptive) youden_t=-0.0299 youden_sens=0.725 youden_spec=0.520 J=0.245
interpolate prompts_marked_above=76/100 ranking_without_isolated_tp=0/76 ranking_losses_with_isolated_tp=18 instance=key-free-interpolate used_keys=False
hard auc=0.579 mean_pos=0.0127 mean_neg=-0.0144 diff=0.0271 pos>0=215/400 neg<=0=221/400 perm_p=0.0004998 (file-level, descriptive) binom_p=0.07348 (file-level, descriptive) youden_t=0.0267 youden_sens=0.438 youden_spec=0.693 J=0.130
hard prompts_marked_above=66/100 ranking_without_isolated_tp=2/66 ranking_losses_with_isolated_tp=26 instance=key-free-counts used_keys=False
hits auc=0.843 mean_pos=0.4851 mean_neg=-0.0598 diff=0.5448 pos>0=332/400 neg<=0=255/400 perm_p=0.0004998 (file-level, descriptive) binom_p=4.044e-43 (file-level, descriptive) youden_t=0.2054 youden_sens=0.685 youden_spec=0.875 J=0.560
hits prompts_marked_above=91/100 ranking_without_isolated_tp=3/91 ranking_losses_with_isolated_tp=8 instance=key-free-hits used_keys=False
