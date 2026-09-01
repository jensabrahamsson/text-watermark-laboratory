# Key-free transfer

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 11/12 | 0.759 | 25/48 | 43/48 | 0.0004998 | 0.6586 |
| rankuni | 10/12 | 0.653 | 31/48 | 27/48 | 0.004998 | 0.1338 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 25/23 | 5/43 | 0.833 |
| rankuni | 0/48 | 0/48 | 31/17 | 21/27 | 0.596 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

rankpath auc=0.759 mean_pos=-0.0622 mean_neg=-0.7208 diff=0.6586 pos>0=25/48 neg<=0=43/48 perm_p=0.0004998 binom_p=0.4427 youden_t=-0.1442 youden_sens=0.625 youden_spec=0.875 J=0.500
rankpath zeros=0/48 vs 0/48 decided_tp=25 fn=23 fp=5 tn=43 precision=0.833 decided_acc=0.708
rankpath prompts_marked_above=11/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.653 mean_pos=0.0668 mean_neg=-0.0669 diff=0.1338 pos>0=31/48 neg<=0=27/48 perm_p=0.004998 binom_p=0.02973 youden_t=0.0806 youden_sens=0.500 youden_spec=0.771 J=0.271
rankuni zeros=0/48 vs 0/48 decided_tp=31 fn=17 fp=21 tn=27 precision=0.596 decided_acc=0.604
rankuni prompts_marked_above=10/12 instance=key-free-rankuni used_keys=False
