# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=0 cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 10/12 | 0.818 | 38/48 | 40/48 | 0.0004998 | 2.0821 |
| rankpath | 9/12 | 0.674 | 30/48 | 35/48 | 0.002999 | 0.2367 |
| rankuni | 9/12 | 0.563 | 28/48 | 25/48 | 0.1014 | 0.0141 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 0/48 | 12/48 | 38/10 | 8/28 | 0.826 |
| rankpath | 0/48 | 0/48 | 30/18 | 13/35 | 0.698 |
| rankuni | 0/48 | 0/48 | 28/20 | 23/25 | 0.549 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 38/48 | 40/48 | 0.792 | 0.833 |
| rankpath | in-sample-youden | 0.0450 | 30/48 | 37/48 | 0.625 | 0.771 |
| rankuni | in-sample-youden | -0.0115 | 32/48 | 22/48 | 0.667 | 0.458 |
| postokbackoff | nested-youden | 0.5705 | 38/48 | 44/48 | 0.792 | 0.917 |
| postokbackoff | nested-fpr10 | 0.4478 | 38/48 | 42/48 | 0.792 | 0.875 |
| rankpath | nested-youden | 0.2291 | 21/48 | 40/48 | 0.438 | 0.833 |
| rankpath | nested-fpr10 | 0.3100 | 14/48 | 44/48 | 0.292 | 0.917 |
| rankuni | nested-youden | -0.0223 | 35/48 | 20/48 | 0.729 | 0.417 |
| rankuni | nested-fpr10 | 0.0696 | 6/48 | 42/48 | 0.125 | 0.875 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

postokbackoff auc=0.818 mean_pos=1.4993 mean_neg=-0.5828 diff=2.0821 pos>0=38/48 neg<=0=40/48 perm_p=0.0004998 binom_p=3.085e-05 youden_t=0.5517 youden_sens=0.792 youden_spec=0.917 J=0.708
postokbackoff zeros=0/48 vs 12/48 decided_tp=38 fn=10 fp=8 tn=28 precision=0.826 decided_acc=0.786
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
rankpath auc=0.674 mean_pos=0.0632 mean_neg=-0.1735 diff=0.2367 pos>0=30/48 neg<=0=35/48 perm_p=0.002999 binom_p=0.0557 youden_t=0.0246 youden_sens=0.625 youden_spec=0.771 J=0.396
rankpath zeros=0/48 vs 0/48 decided_tp=30 fn=18 fp=13 tn=35 precision=0.698 decided_acc=0.677
rankpath prompts_marked_above=9/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.563 mean_pos=0.0128 mean_neg=-0.0013 diff=0.0141 pos>0=28/48 neg<=0=25/48 perm_p=0.1014 binom_p=0.1562 youden_t=0.0060 youden_sens=0.583 youden_spec=0.583 J=0.167
rankuni zeros=0/48 vs 0/48 decided_tp=28 fn=20 fp=23 tn=25 precision=0.549 decided_acc=0.552
rankuni prompts_marked_above=9/12 instance=key-free-rankuni used_keys=False
