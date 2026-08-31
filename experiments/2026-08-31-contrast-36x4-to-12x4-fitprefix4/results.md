# Key-free instance contrast

instance-contrast n_rows=9 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 control=experiments/2026-08-31-pair-12x4-controlkeys n_control=48 n_aligned=48 fit_prefix=4 used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| hits | control-vs-unmarked | 8/12 | 0.458 | 0/48 | 33/48 | 0.1649 | 0.2552 |
| hits | public-vs-control | 12/12 | 0.906 | 39/48 | 48/48 | 0.0004998 | 0.1904 |
| hits | public-vs-unmarked | 11/12 | 0.820 | 39/48 | 33/48 | 0.0004998 | 0.1956 |
| poshits | control-vs-unmarked | 9/12 | 0.510 | 0/48 | 41/48 | 0.02349 | 0.2408 |
| poshits | public-vs-control | 12/12 | 0.906 | 39/48 | 48/48 | 0.0004998 | 0.1910 |
| poshits | public-vs-unmarked | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 0.1818 |
| hashpool | control-vs-unmarked | 9/12 | 0.617 | 6/48 | 38/48 | 0.01249 | 0.2487 |
| hashpool | public-vs-control | 8/12 | 0.697 | 29/48 | 42/48 | 0.0004998 | 0.2026 |
| hashpool | public-vs-unmarked | 11/12 | 0.788 | 29/48 | 38/48 | 0.0004998 | 0.1784 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

hits control-vs-unmarked auc=0.458 mean_pos=0.0000 mean_neg=-0.2107 diff=0.2107 pos>0=0/48 neg<=0=33/48 perm_p=0.1649 binom_p=1 youden_t=-0.0183 youden_sens=1.000 youden_spec=0.229 J=0.229 brier=0.2552 prompts=8/12
hits public-vs-control auc=0.906 mean_pos=1.2994 mean_neg=0.0000 diff=1.2994 pos>0=39/48 neg<=0=48/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=1.000 J=0.812 brier=0.1904 prompts=12/12
hits public-vs-unmarked auc=0.820 mean_pos=1.2994 mean_neg=-0.2107 diff=1.5101 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0400 youden_sens=0.812 youden_spec=0.792 J=0.604 brier=0.1956 prompts=11/12
poshits control-vs-unmarked auc=0.510 mean_pos=0.0000 mean_neg=-0.3382 diff=0.3382 pos>0=0/48 neg<=0=41/48 perm_p=0.02349 binom_p=1 youden_t=-0.6122 youden_sens=1.000 youden_spec=0.167 J=0.167 brier=0.2408 prompts=9/12
poshits public-vs-control auc=0.906 mean_pos=1.2933 mean_neg=0.0000 diff=1.2933 pos>0=39/48 neg<=0=48/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=1.000 J=0.812 brier=0.1910 prompts=12/12
poshits public-vs-unmarked auc=0.873 mean_pos=1.2933 mean_neg=-0.3382 diff=1.6315 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667 brier=0.1818 prompts=12/12
hashpool control-vs-unmarked auc=0.617 mean_pos=-0.2772 mean_neg=-0.5702 diff=0.2930 pos>0=6/48 neg<=0=38/48 perm_p=0.01249 binom_p=1 youden_t=-0.2320 youden_sens=0.583 youden_spec=0.750 J=0.333 brier=0.2487 prompts=9/12
hashpool public-vs-control auc=0.697 mean_pos=0.8847 mean_neg=-0.2772 diff=1.1620 pos>0=29/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.09671 youden_t=0.0000 youden_sens=0.604 youden_spec=0.875 J=0.479 brier=0.2026 prompts=8/12
hashpool public-vs-unmarked auc=0.788 mean_pos=0.8847 mean_neg=-0.5702 diff=1.4550 pos>0=29/48 neg<=0=38/48 perm_p=0.0004998 binom_p=0.09671 youden_t=0.6512 youden_sens=0.521 youden_spec=1.000 J=0.521 brier=0.1784 prompts=11/12

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
