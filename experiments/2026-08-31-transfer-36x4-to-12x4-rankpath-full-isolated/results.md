# Key-free transfer

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=True rankpath_pos_bucket=0
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 6/12 | 0.534 | 24/48 | 26/48 | 0.3623 | 0.0024 |
| rankuni | 9/12 | 0.597 | 41/48 | 17/48 | 0.05697 | 0.0011 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 24/24 | 22/26 | 0.522 |
| rankuni | 0/48 | 0/48 | 41/7 | 31/17 | 0.569 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| rankpath | in-sample-youden | 0.0067 | 23/48 | 31/48 | 0.479 | 0.646 |
| rankuni | in-sample-youden | -0.0008 | 44/48 | 11/48 | 0.917 | 0.229 |
| rankpath | nested-youden | 0.0077 | 22/48 | 33/48 | 0.458 | 0.688 |
| rankpath | nested-fpr10 | 0.0290 | 9/48 | 42/48 | 0.188 | 0.875 |
| rankuni | nested-youden | 0.0031 | 25/48 | 29/48 | 0.521 | 0.604 |
| rankuni | nested-fpr10 | 0.0029 | 26/48 | 29/48 | 0.542 | 0.604 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

| prefix tokens | method | prompt wins | file auc | marked>0 | unmarked<=0 |
|---|---|---|---|---|---|
| 4 | rankpath | 11/12 | 0.759 | 25/48 | 43/48 |
| 4 | rankuni | 10/12 | 0.653 | 31/48 | 27/48 |
| 16 | rankpath | 9/12 | 0.622 | 18/48 | 40/48 |
| 16 | rankuni | 7/12 | 0.558 | 25/48 | 30/48 |
| 32 | rankpath | 5/12 | 0.550 | 21/48 | 31/48 |
| 32 | rankuni | 8/12 | 0.589 | 32/48 | 23/48 |
| 64 | rankpath | 5/12 | 0.532 | 22/48 | 31/48 |
| 64 | rankuni | 10/12 | 0.649 | 41/48 | 16/48 |
| 128 | rankpath | 6/12 | 0.534 | 24/48 | 26/48 |
| 128 | rankuni | 9/12 | 0.597 | 41/48 | 17/48 |

| window tokens | method | prompt wins | file auc | marked>0 | unmarked<=0 |
|---|---|---|---|---|---|
| 0:16 | rankpath | 9/12 | 0.622 | 18/48 | 40/48 |
| 0:16 | rankuni | 7/12 | 0.558 | 25/48 | 30/48 |
| 16:32 | rankpath | 5/12 | 0.471 | 21/48 | 25/48 |
| 16:32 | rankuni | 9/12 | 0.562 | 25/48 | 26/48 |
| 32:64 | rankpath | 6/12 | 0.479 | 25/48 | 23/48 |
| 32:64 | rankuni | 4/12 | 0.461 | 25/48 | 19/48 |
| 64:128 | rankpath | 7/12 | 0.568 | 27/48 | 28/48 |
| 64:128 | rankuni | 5/12 | 0.492 | 30/48 | 21/48 |

rankpath auc=0.534 mean_pos=-0.0034 mean_neg=-0.0057 diff=0.0024 pos>0=24/48 neg<=0=26/48 perm_p=0.3623 binom_p=0.5573 youden_t=0.0137 youden_sens=0.417 youden_spec=0.771 J=0.188
rankpath zeros=0/48 vs 0/48 decided_tp=24 fn=24 fp=22 tn=26 precision=0.522 decided_acc=0.521
rankpath prompts_marked_above=6/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.597 mean_pos=0.0030 mean_neg=0.0019 diff=0.0011 pos>0=41/48 neg<=0=17/48 perm_p=0.05697 binom_p=3.12e-07 youden_t=0.0000 youden_sens=0.854 youden_spec=0.354 J=0.208
rankuni zeros=0/48 vs 0/48 decided_tp=41 fn=7 fp=31 tn=17 precision=0.569 decided_acc=0.604
rankuni prompts_marked_above=9/12 instance=key-free-rankuni used_keys=False
