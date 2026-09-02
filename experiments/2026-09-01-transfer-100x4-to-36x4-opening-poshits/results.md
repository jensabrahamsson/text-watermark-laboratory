# Key-free transfer

transfer n_methods=1 train=experiments/2026-09-01-pair-100x4 test=experiments/2026-08-31-pair-36x4 n_train=100 n_test=36 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 35/36 | 0.955 | 134/144 | 127/144 | 0.0004998 | 3.0526 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 7/144 | 75/144 | 134/3 | 17/52 | 0.887 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.2568 | 114/144 | 142/144 | 0.792 | 0.986 |
| poshits | nested-youden | 0.1474 | 134/144 | 129/144 | 0.931 | 0.896 |
| poshits | nested-fpr10 | 0.1441 | 134/144 | 129/144 | 0.931 | 0.896 |

poshits auc=0.955 mean_pos=2.4139 mean_neg=-0.6388 diff=3.0526 pos>0=134/144 neg<=0=127/144 perm_p=0.0004998 binom_p=3.714e-29 youden_t=0.1137 youden_sens=0.931 youden_spec=0.896 J=0.826
poshits zeros=7/144 vs 75/144 decided_tp=134 fn=3 fp=17 tn=52 precision=0.887 decided_acc=0.903
poshits prompts_marked_above=35/36 instance=key-free-poshits used_keys=False
