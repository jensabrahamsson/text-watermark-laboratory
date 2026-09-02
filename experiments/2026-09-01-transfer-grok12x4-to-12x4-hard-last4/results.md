# Key-free transfer

transfer n_methods=1 train=experiments/2026-09-01-pair-grok12x4 test=experiments/2026-08-17-pair-12x4 n_train=12 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 5/12 | 0.586 | 23/48 | 30/48 | 0.06247 | 0.0587 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| interpolate | 5/12 | 0/5 | 6 (02-night-bus, 07-rain, 09-workshop, 10-office, 11-garden, 12-ferry-queue) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/48 | 0/48 | 23/25 | 18/30 | 0.561 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| interpolate | in-sample-youden | 0.0000 | 23/48 | 30/48 | 0.479 | 0.625 |
| interpolate | nested-youden | 0.1088 | 16/48 | 41/48 | 0.333 | 0.854 |
| interpolate | nested-fpr10 | 0.1382 | 14/48 | 43/48 | 0.292 | 0.896 |

interpolate auc=0.586 mean_pos=0.0268 mean_neg=-0.0319 diff=0.0587 pos>0=23/48 neg<=0=30/48 perm_p=0.06247 binom_p=0.6673 youden_t=0.1459 youden_sens=0.292 youden_spec=0.938 J=0.229
interpolate zeros=0/48 vs 0/48 decided_tp=23 fn=25 fp=18 tn=30 precision=0.561 decided_acc=0.552
interpolate prompts_marked_above=5/12 ranking_without_isolated_tp=0/5 ranking_losses_with_isolated_tp=6 instance=key-free-interpolate used_keys=False
