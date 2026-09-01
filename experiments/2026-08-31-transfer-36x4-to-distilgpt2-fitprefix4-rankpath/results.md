# Key-free transfer

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-31-pair-distilgpt2-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 9/12 | 0.636 | 21/48 | 34/48 | 0.01749 | 0.4524 |
| rankuni | 5/12 | 0.475 | 18/48 | 28/48 | 0.6452 | -0.0211 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 1/48 | 0/48 | 21/26 | 14/34 | 0.600 |
| rankuni | 0/48 | 0/48 | 18/30 | 20/28 | 0.474 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| rankpath | in-sample-youden | 0.0817 | 21/48 | 34/48 | 0.438 | 0.708 |
| rankuni | in-sample-youden | 0.0000 | 18/48 | 28/48 | 0.375 | 0.583 |
| rankpath | nested-youden | -0.3833 | 24/48 | 30/48 | 0.500 | 0.625 |
| rankpath | nested-fpr10 | 0.7979 | 11/48 | 45/48 | 0.229 | 0.938 |
| rankuni | nested-youden | -0.0493 | 18/48 | 26/48 | 0.375 | 0.542 |
| rankuni | nested-fpr10 | 0.2765 | 4/48 | 45/48 | 0.083 | 0.938 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

rankpath auc=0.636 mean_pos=-0.2720 mean_neg=-0.7244 diff=0.4524 pos>0=21/48 neg<=0=34/48 perm_p=0.01749 binom_p=0.8438 youden_t=0.3293 youden_sens=0.396 youden_spec=0.833 J=0.229
rankpath zeros=1/48 vs 0/48 decided_tp=21 fn=26 fp=14 tn=34 precision=0.600 decided_acc=0.579
rankpath prompts_marked_above=9/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.475 mean_pos=-0.1521 mean_neg=-0.1310 diff=-0.0211 pos>0=18/48 neg<=0=28/48 perm_p=0.6452 binom_p=0.9703 youden_t=0.0642 youden_sens=0.292 youden_spec=0.792 J=0.083
rankuni zeros=0/48 vs 0/48 decided_tp=18 fn=30 fp=20 tn=28 precision=0.474 decided_acc=0.479
rankuni prompts_marked_above=5/12 instance=key-free-rankuni used_keys=False
