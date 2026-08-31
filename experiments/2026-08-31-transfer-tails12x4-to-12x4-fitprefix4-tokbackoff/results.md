# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-tails12x4 test=experiments/2026-08-17-pair-12x4 n_train=12 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.495 | 10/48 | 48/48 | 0.01899 | 0.4494 |
| postokhits | 12/12 | 0.604 | 10/48 | 48/48 | 0.001999 | 0.6200 |
| postokbackoff | 12/12 | 0.740 | 23/48 | 48/48 | 0.0004998 | 0.9136 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 22/48 | 41/48 | 10/16 | 0/7 | 1.000 |
| postokhits | 38/48 | 48/48 | 10/0 | 0/0 | 1.000 |
| postokbackoff | 25/48 | 48/48 | 23/0 | 0/0 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; it is not key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokhits | in-sample-youden | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokbackoff | in-sample-youden | 0.0000 | 23/48 | 48/48 | 0.479 | 1.000 |
| poshits | nested-youden | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |
| poshits | nested-fpr10 | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokhits | nested-youden | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokbackoff | nested-youden | 0.0000 | 23/48 | 48/48 | 0.479 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 23/48 | 48/48 | 0.479 | 1.000 |

poshits auc=0.495 mean_pos=0.3167 mean_neg=-0.1327 diff=0.4494 pos>0=10/48 neg<=0=48/48 perm_p=0.01899 binom_p=1 youden_t=0.0000 youden_sens=0.208 youden_spec=1.000 J=0.208
poshits zeros=22/48 vs 41/48 decided_tp=10 fn=16 fp=0 tn=7 precision=1.000 decided_acc=0.515
poshits prompts_marked_above=8/12 instance=key-free-poshits used_keys=False
postokhits auc=0.604 mean_pos=0.6200 mean_neg=0.0000 diff=0.6200 pos>0=10/48 neg<=0=48/48 perm_p=0.001999 binom_p=1 youden_t=0.0000 youden_sens=0.208 youden_spec=1.000 J=0.208
postokhits zeros=38/48 vs 48/48 decided_tp=10 fn=0 fp=0 tn=0 precision=1.000 decided_acc=1.000
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
postokbackoff auc=0.740 mean_pos=0.9136 mean_neg=0.0000 diff=0.9136 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
postokbackoff zeros=25/48 vs 48/48 decided_tp=23 fn=0 fp=0 tn=0 precision=1.000 decided_acc=1.000
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
