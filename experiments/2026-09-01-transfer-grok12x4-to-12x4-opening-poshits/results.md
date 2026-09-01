# Key-free transfer

transfer n_methods=1 train=experiments/2026-09-01-pair-grok12x4 test=experiments/2026-08-17-pair-12x4 n_train=12 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 7/12 | 0.432 | 6/48 | 47/48 | 0.2699 | 0.0626 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| poshits | 7/12 | 5/7 (03-library, 05-kitchen, 06-station, 07-rain, 09-workshop) | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 24/48 | 40/48 | 6/18 | 1/7 | 0.857 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.0000 | 6/48 | 47/48 | 0.125 | 0.979 |
| poshits | nested-youden | 0.0000 | 6/48 | 47/48 | 0.125 | 0.979 |
| poshits | nested-fpr10 | 0.0000 | 6/48 | 47/48 | 0.125 | 0.979 |

poshits auc=0.432 mean_pos=0.0369 mean_neg=-0.0257 diff=0.0626 pos>0=6/48 neg<=0=47/48 perm_p=0.2699 binom_p=1 youden_t=0.0000 youden_sens=0.125 youden_spec=0.979 J=0.104
poshits zeros=24/48 vs 40/48 decided_tp=6 fn=18 fp=1 tn=7 precision=0.857 decided_acc=0.406
poshits prompts_marked_above=7/12 ranking_without_isolated_tp=5/7 ranking_losses_with_isolated_tp=0 instance=key-free-poshits used_keys=False
