# Key-free transfer

transfer n_methods=4 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-31-pair-distilgpt2-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 7/12 | 0.615 | 24/48 | 37/48 | 0.08546 | 0.3257 |
| hashtoklen | 9/12 | 0.571 | 10/48 | 43/48 | 0.04098 | 0.2180 |
| hashtoklenbackoff | 4/12 | 0.470 | 17/48 | 26/48 | 0.7936 | -0.1853 |
| postokhits | 9/12 | 0.591 | 10/48 | 42/48 | 0.01749 | 0.6199 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 10/48 | 12/48 | 24/14 | 11/25 | 0.686 |
| hashtoklen | 37/48 | 40/48 | 10/1 | 5/3 | 0.667 |
| hashtoklenbackoff | 12/48 | 5/48 | 17/19 | 22/21 | 0.436 |
| postokhits | 35/48 | 33/48 | 10/3 | 6/9 | 0.625 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashtok | in-sample-youden | 0.3098 | 14/48 | 38/48 | 0.292 | 0.792 |
| hashtoklen | in-sample-youden | 0.3881 | 10/48 | 43/48 | 0.208 | 0.896 |
| hashtoklenbackoff | in-sample-youden | 0.0000 | 17/48 | 26/48 | 0.354 | 0.542 |
| postokhits | in-sample-youden | 0.6987 | 10/48 | 43/48 | 0.208 | 0.896 |
| hashtok | nested-youden | 0.9174 | 11/48 | 41/48 | 0.229 | 0.854 |
| hashtok | nested-fpr10 | 0.8561 | 12/48 | 40/48 | 0.250 | 0.833 |
| hashtoklen | nested-youden | 0.1962 | 10/48 | 43/48 | 0.208 | 0.896 |
| hashtoklen | nested-fpr10 | 0.0000 | 10/48 | 43/48 | 0.208 | 0.896 |
| hashtoklenbackoff | nested-youden | 1.1025 | 9/48 | 37/48 | 0.188 | 0.771 |
| hashtoklenbackoff | nested-fpr10 | 1.0909 | 9/48 | 37/48 | 0.188 | 0.771 |
| postokhits | nested-youden | 0.5925 | 10/48 | 43/48 | 0.208 | 0.896 |
| postokhits | nested-fpr10 | 0.0000 | 10/48 | 42/48 | 0.208 | 0.875 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashtok auc=0.615 mean_pos=0.1248 mean_neg=-0.2009 diff=0.3257 pos>0=24/48 neg<=0=37/48 perm_p=0.08546 binom_p=0.5573 youden_t=0.0000 youden_sens=0.500 youden_spec=0.771 J=0.271
hashtok zeros=10/48 vs 12/48 decided_tp=24 fn=14 fp=11 tn=25 precision=0.686 decided_acc=0.662
hashtok prompts_marked_above=7/12 instance=key-free-hashtok used_keys=False
hashtoklen auc=0.571 mean_pos=0.2893 mean_neg=0.0713 diff=0.2180 pos>0=10/48 neg<=0=43/48 perm_p=0.04098 binom_p=1 youden_t=1.1062 youden_sens=0.188 youden_spec=0.958 J=0.146
hashtoklen zeros=37/48 vs 40/48 decided_tp=10 fn=1 fp=5 tn=3 precision=0.667 decided_acc=0.684
hashtoklen prompts_marked_above=9/12 instance=key-free-hashtoklen used_keys=False
hashtoklenbackoff auc=0.470 mean_pos=0.0215 mean_neg=0.2068 diff=-0.1853 pos>0=17/48 neg<=0=26/48 perm_p=0.7936 binom_p=0.9853 youden_t=-0.0178 youden_sens=0.646 youden_spec=0.438 J=0.083
hashtoklenbackoff zeros=12/48 vs 5/48 decided_tp=17 fn=19 fp=22 tn=21 precision=0.436 decided_acc=0.481
hashtoklenbackoff prompts_marked_above=4/12 instance=key-free-hashtoklenbackoff used_keys=False
postokhits auc=0.591 mean_pos=0.3369 mean_neg=-0.2830 diff=0.6199 pos>0=10/48 neg<=0=42/48 perm_p=0.01749 binom_p=1 youden_t=1.0589 youden_sens=0.208 youden_spec=0.938 J=0.146
postokhits zeros=35/48 vs 33/48 decided_tp=10 fn=3 fp=6 tn=9 precision=0.625 decided_acc=0.679
postokhits prompts_marked_above=9/12 instance=key-free-postokhits used_keys=False
