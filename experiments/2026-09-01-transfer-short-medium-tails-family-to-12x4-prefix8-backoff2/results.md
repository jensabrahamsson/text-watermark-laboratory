# Key-free transfer

transfer n_methods=1 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff2 | 12/12 | 0.674 | 18/48 | 46/48 | 0.0004998 | 1.1794 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff2 | 30/48 | 46/48 | 18/0 | 2/0 | 0.900 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff2 | in-sample-youden | 0.5083 | 18/48 | 46/48 | 0.375 | 0.958 |
| postokbackoff2 | nested-youden | 0.0077 | 18/48 | 46/48 | 0.375 | 0.958 |
| postokbackoff2 | nested-fpr10 | 0.0000 | 18/48 | 46/48 | 0.375 | 0.958 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

postokbackoff2 auc=0.674 mean_pos=1.2193 mean_neg=0.0398 diff=1.1794 pos>0=18/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.9703 youden_t=0.9563 youden_sens=0.375 youden_spec=1.000 J=0.375
postokbackoff2 zeros=30/48 vs 46/48 decided_tp=18 fn=0 fp=2 tn=0 precision=0.900 decided_acc=0.900
postokbackoff2 prompts_marked_above=12/12 instance=key-free-postokbackoff2 used_keys=False
