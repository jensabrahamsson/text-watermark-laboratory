# Key-free transfer

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 10/12 | 0.683 | 28/48 | 33/48 | 0.001999 | 0.6346 |
| rankuni | 8/12 | 0.628 | 29/48 | 25/48 | 0.01899 | 0.1228 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 28/20 | 15/33 | 0.651 |
| rankuni | 0/48 | 0/48 | 29/19 | 23/25 | 0.558 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

rankpath auc=0.683 mean_pos=-0.0881 mean_neg=-0.7227 diff=0.6346 pos>0=28/48 neg<=0=33/48 perm_p=0.001999 binom_p=0.1562 youden_t=-0.8521 youden_sens=0.854 youden_spec=0.500 J=0.354
rankpath zeros=0/48 vs 0/48 decided_tp=28 fn=20 fp=15 tn=33 precision=0.651 decided_acc=0.635
rankpath prompts_marked_above=10/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.628 mean_pos=0.0907 mean_neg=-0.0321 diff=0.1228 pos>0=29/48 neg<=0=25/48 perm_p=0.01899 binom_p=0.09671 youden_t=0.0642 youden_sens=0.583 youden_spec=0.708 J=0.292
rankuni zeros=0/48 vs 0/48 decided_tp=29 fn=19 fp=23 tn=25 precision=0.558 decided_acc=0.562
rankuni prompts_marked_above=8/12 instance=key-free-rankuni used_keys=False
