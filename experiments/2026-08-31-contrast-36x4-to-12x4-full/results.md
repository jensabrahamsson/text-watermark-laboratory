# Key-free instance contrast

instance-contrast n_rows=9 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 control=experiments/2026-08-31-pair-12x4-controlkeys n_control=48 n_aligned=48 fit_prefix=None used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| hits | control-vs-unmarked | 7/12 | 0.475 | 29/48 | 24/48 | 0.7161 | 0.2678 |
| hits | public-vs-control | 11/12 | 0.842 | 42/48 | 19/48 | 0.0004998 | 0.1869 |
| hits | public-vs-unmarked | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.2015 |
| poshits | control-vs-unmarked | 9/12 | 0.500 | 0/48 | 40/48 | 0.03398 | 0.2424 |
| poshits | public-vs-control | 12/12 | 0.906 | 39/48 | 48/48 | 0.0004998 | 0.2072 |
| poshits | public-vs-unmarked | 12/12 | 0.861 | 39/48 | 40/48 | 0.0004998 | 0.1995 |
| hashpool | control-vs-unmarked | 7/12 | 0.511 | 17/48 | 36/48 | 0.5577 | 0.2502 |
| hashpool | public-vs-control | 8/12 | 0.718 | 30/48 | 31/48 | 0.0004998 | 0.2432 |
| hashpool | public-vs-unmarked | 11/12 | 0.733 | 30/48 | 36/48 | 0.0004998 | 0.2433 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

hits control-vs-unmarked auc=0.475 mean_pos=-0.0788 mean_neg=-0.0161 diff=-0.0627 pos>0=29/48 neg<=0=24/48 perm_p=0.7161 binom_p=0.09671 youden_t=-0.0052 youden_sens=0.688 youden_spec=0.438 J=0.125 brier=0.2678 prompts=7/12
hits public-vs-control auc=0.842 mean_pos=0.8547 mean_neg=-0.0788 diff=0.9334 pos>0=42/48 neg<=0=19/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.1703 youden_sens=0.625 youden_spec=0.958 J=0.583 brier=0.1869 prompts=11/12
hits public-vs-unmarked auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479 brier=0.2015 prompts=12/12
poshits control-vs-unmarked auc=0.500 mean_pos=0.0000 mean_neg=-0.2370 diff=0.2370 pos>0=0/48 neg<=0=40/48 perm_p=0.03398 binom_p=1 youden_t=-0.1157 youden_sens=1.000 youden_spec=0.167 J=0.167 brier=0.2424 prompts=9/12
poshits public-vs-control auc=0.906 mean_pos=1.2773 mean_neg=0.0000 diff=1.2773 pos>0=39/48 neg<=0=48/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=1.000 J=0.812 brier=0.2072 prompts=12/12
poshits public-vs-unmarked auc=0.861 mean_pos=1.2773 mean_neg=-0.2370 diff=1.5143 pos>0=39/48 neg<=0=40/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.833 J=0.646 brier=0.1995 prompts=12/12
hashpool control-vs-unmarked auc=0.511 mean_pos=-0.0137 mean_neg=-0.0129 diff=-0.0008 pos>0=17/48 neg<=0=36/48 perm_p=0.5577 binom_p=0.9853 youden_t=0.0016 youden_sens=0.312 youden_spec=0.812 J=0.125 brier=0.2502 prompts=7/12
hashpool public-vs-control auc=0.718 mean_pos=0.0429 mean_neg=-0.0137 diff=0.0566 pos>0=30/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0263 youden_sens=0.417 youden_spec=0.958 J=0.375 brier=0.2432 prompts=8/12
hashpool public-vs-unmarked auc=0.733 mean_pos=0.0429 mean_neg=-0.0129 diff=0.0558 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0016 youden_sens=0.625 youden_spec=0.812 J=0.438 brier=0.2433 prompts=11/12

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.793 | 42/48 | 24/48 | 0.0004998 | 0.8708 |
| poshits | 12/12 | 0.861 | 39/48 | 40/48 | 0.0004998 | 1.5143 |
| hashpool | 11/12 | 0.733 | 30/48 | 36/48 | 0.0004998 | 0.0558 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.793 mean_pos=0.8547 mean_neg=-0.0161 diff=0.8708 pos>0=42/48 neg<=0=24/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.4024 youden_sens=0.562 youden_spec=0.917 J=0.479
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
poshits auc=0.861 mean_pos=1.2773 mean_neg=-0.2370 diff=1.5143 pos>0=39/48 neg<=0=40/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.833 J=0.646
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
hashpool auc=0.733 mean_pos=0.0429 mean_neg=-0.0129 diff=0.0558 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=0.0016 youden_sens=0.625 youden_spec=0.812 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
