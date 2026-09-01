# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtoklen | 12/12 | 0.701 | 21/48 | 45/48 | 0.0004998 | 0.7758 |
| hashskip | 8/12 | 0.663 | 25/48 | 35/48 | 0.001999 | 0.5957 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtoklen | 27/48 | 44/48 | 21/0 | 3/1 | 0.875 |
| hashskip | 21/48 | 27/48 | 25/2 | 13/8 | 0.658 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashtoklen | in-sample-youden | 0.3881 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashskip | in-sample-youden | 0.0000 | 25/48 | 35/48 | 0.521 | 0.729 |
| hashtoklen | nested-youden | 0.1962 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashtoklen | nested-fpr10 | 0.0000 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashskip | nested-youden | 0.8665 | 16/48 | 41/48 | 0.333 | 0.854 |
| hashskip | nested-fpr10 | 0.6641 | 17/48 | 39/48 | 0.354 | 0.812 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashtoklen auc=0.701 mean_pos=0.8070 mean_neg=0.0312 diff=0.7758 pos>0=21/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.8438 youden_t=0.0000 youden_sens=0.438 youden_spec=0.938 J=0.375
hashtoklen zeros=27/48 vs 44/48 decided_tp=21 fn=0 fp=3 tn=1 precision=0.875 decided_acc=0.880
hashtoklen prompts_marked_above=12/12 instance=key-free-hashtoklen used_keys=False
hashskip auc=0.663 mean_pos=0.6946 mean_neg=0.0989 diff=0.5957 pos>0=25/48 neg<=0=35/48 perm_p=0.001999 binom_p=0.4427 youden_t=0.0084 youden_sens=0.521 youden_spec=0.750 J=0.271
hashskip zeros=21/48 vs 27/48 decided_tp=25 fn=2 fp=13 tn=8 precision=0.658 decided_acc=0.688
hashskip prompts_marked_above=8/12 instance=key-free-hashskip used_keys=False
