# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-24short-plus-long12 test=experiments/2026-08-17-pair-12x4 n_train=36 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.639 | 20/48 | 48/48 | 0.0004998 | 1.9616 |
| postokhits | 12/12 | 0.739 | 20/48 | 48/48 | 0.0004998 | 1.9152 |
| postokbackoff | 12/12 | 0.757 | 22/48 | 48/48 | 0.0004998 | 1.9590 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 9/48 | 33/48 | 20/19 | 0/15 | 1.000 |
| postokhits | 28/48 | 43/48 | 20/0 | 0/5 | 1.000 |
| postokbackoff | 26/48 | 43/48 | 22/0 | 0/5 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; it is not key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.3366 | 20/48 | 48/48 | 0.417 | 1.000 |
| postokhits | in-sample-youden | 0.3366 | 20/48 | 48/48 | 0.417 | 1.000 |
| postokbackoff | in-sample-youden | 0.0000 | 22/48 | 48/48 | 0.458 | 1.000 |
| poshits | nested-youden | 0.0000 | 20/48 | 48/48 | 0.417 | 1.000 |
| poshits | nested-fpr10 | 0.0179 | 20/48 | 48/48 | 0.417 | 1.000 |
| postokhits | nested-youden | 0.4250 | 20/48 | 48/48 | 0.417 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 20/48 | 48/48 | 0.417 | 1.000 |
| postokbackoff | nested-youden | 0.4250 | 22/48 | 48/48 | 0.458 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 22/48 | 48/48 | 0.458 | 1.000 |

poshits auc=0.639 mean_pos=1.5039 mean_neg=-0.4577 diff=1.9616 pos>0=20/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9033 youden_t=0.0000 youden_sens=0.417 youden_spec=1.000 J=0.417
poshits zeros=9/48 vs 33/48 decided_tp=20 fn=19 fp=0 tn=15 precision=1.000 decided_acc=0.648
poshits prompts_marked_above=8/12 instance=key-free-poshits used_keys=False
postokhits auc=0.739 mean_pos=1.5107 mean_neg=-0.4045 diff=1.9152 pos>0=20/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9033 youden_t=0.0000 youden_sens=0.417 youden_spec=1.000 J=0.417
postokhits zeros=28/48 vs 43/48 decided_tp=20 fn=0 fp=0 tn=5 precision=1.000 decided_acc=1.000
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
postokbackoff auc=0.757 mean_pos=1.5546 mean_neg=-0.4045 diff=1.9590 pos>0=22/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.7646 youden_t=0.0000 youden_sens=0.458 youden_spec=1.000 J=0.458
postokbackoff zeros=26/48 vs 43/48 decided_tp=22 fn=0 fp=0 tn=5 precision=1.000 decided_acc=1.000
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
