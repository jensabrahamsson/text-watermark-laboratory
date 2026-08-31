# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 0.0004998 | 1.5101 |
| poshits | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 1.6315 |
| hashpool | 11/12 | 0.788 | 29/48 | 38/48 | 0.0004998 | 1.4550 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.820 mean_pos=1.2994 mean_neg=-0.2107 diff=1.5101 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0400 youden_sens=0.812 youden_spec=0.792 J=0.604
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
poshits auc=0.873 mean_pos=1.2933 mean_neg=-0.3382 diff=1.6315 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
hashpool auc=0.788 mean_pos=0.8847 mean_neg=-0.5702 diff=1.4550 pos>0=29/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.09671 youden_t=0.6512 youden_sens=0.521 youden_spec=1.000 J=0.521
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
