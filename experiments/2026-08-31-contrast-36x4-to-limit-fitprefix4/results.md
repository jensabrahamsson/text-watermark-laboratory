# Key-free instance contrast

instance-contrast n_rows=9 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-limit control=experiments/2026-08-17-pair-limit n_control=12 n_aligned=12 fit_prefix=4 used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| hits | control-vs-unmarked | 8/12 | 0.417 | 0/12 | 8/12 | 0.2394 | 0.2422 |
| hits | public-vs-control | 12/12 | 0.917 | 10/12 | 12/12 | 0.0004998 | 0.1971 |
| hits | public-vs-unmarked | 12/12 | 0.854 | 10/12 | 8/12 | 0.0009995 | 0.1893 |
| poshits | control-vs-unmarked | 9/12 | 0.417 | 0/12 | 9/12 | 0.4993 | 0.2518 |
| poshits | public-vs-control | 12/12 | 0.917 | 10/12 | 12/12 | 0.0004998 | 0.1979 |
| poshits | public-vs-unmarked | 12/12 | 0.854 | 10/12 | 9/12 | 0.0009995 | 0.1996 |
| hashpool | control-vs-unmarked | 8/12 | 0.750 | 2/12 | 10/12 | 0.01449 | 0.2263 |
| hashpool | public-vs-control | 6/12 | 0.625 | 6/12 | 10/12 | 0.02999 | 0.2130 |
| hashpool | public-vs-unmarked | 10/12 | 0.833 | 6/12 | 10/12 | 0.0009995 | 0.1741 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

hits control-vs-unmarked auc=0.417 mean_pos=0.0000 mean_neg=-0.2355 diff=0.2355 pos>0=0/12 neg<=0=8/12 perm_p=0.2394 binom_p=1 youden_t=-0.8654 youden_sens=1.000 youden_spec=0.167 J=0.167 brier=0.2422 prompts=8/12
hits public-vs-control auc=0.917 mean_pos=0.8759 mean_neg=0.0000 diff=0.8759 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=1.000 J=0.833 brier=0.1971 prompts=12/12
hits public-vs-unmarked auc=0.854 mean_pos=0.8759 mean_neg=-0.2355 diff=1.1114 pos>0=10/12 neg<=0=8/12 perm_p=0.0009995 binom_p=0.01929 youden_t=0.1075 youden_sens=0.833 youden_spec=0.833 J=0.667 brier=0.1893 prompts=12/12
poshits control-vs-unmarked auc=0.417 mean_pos=0.0000 mean_neg=-0.0081 diff=0.0081 pos>0=0/12 neg<=0=9/12 perm_p=0.4993 binom_p=1 youden_t=-0.8654 youden_sens=1.000 youden_spec=0.083 J=0.083 brier=0.2518 prompts=9/12
poshits public-vs-control auc=0.917 mean_pos=0.8685 mean_neg=0.0000 diff=0.8685 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=1.000 J=0.833 brier=0.1979 prompts=12/12
poshits public-vs-unmarked auc=0.854 mean_pos=0.8685 mean_neg=-0.0081 diff=0.8766 pos>0=10/12 neg<=0=9/12 perm_p=0.0009995 binom_p=0.01929 youden_t=0.1075 youden_sens=0.833 youden_spec=0.833 J=0.667 brier=0.1996 prompts=12/12
hashpool control-vs-unmarked auc=0.750 mean_pos=-0.2750 mean_neg=-0.7253 diff=0.4503 pos>0=2/12 neg<=0=10/12 perm_p=0.01449 binom_p=0.9968 youden_t=-0.2955 youden_sens=0.667 youden_spec=0.833 J=0.500 brier=0.2263 prompts=8/12
hashpool public-vs-control auc=0.625 mean_pos=0.4920 mean_neg=-0.2750 diff=0.7670 pos>0=6/12 neg<=0=10/12 perm_p=0.02999 binom_p=0.6128 youden_t=0.6476 youden_sens=0.500 youden_spec=1.000 J=0.500 brier=0.2130 prompts=6/12
hashpool public-vs-unmarked auc=0.833 mean_pos=0.4920 mean_neg=-0.7253 diff=1.2173 pos>0=6/12 neg<=0=10/12 perm_p=0.0009995 binom_p=0.6128 youden_t=-0.6662 youden_sens=1.000 youden_spec=0.667 J=0.667 brier=0.1741 prompts=10/12

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-limit n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 12/12 | 0.854 | 10/12 | 8/12 | 0.0009995 | 1.1114 |
| poshits | 12/12 | 0.854 | 10/12 | 9/12 | 0.0009995 | 0.8766 |
| hashpool | 10/12 | 0.833 | 6/12 | 10/12 | 0.0009995 | 1.2173 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.854 mean_pos=0.8759 mean_neg=-0.2355 diff=1.1114 pos>0=10/12 neg<=0=8/12 perm_p=0.0009995 binom_p=0.01929 youden_t=0.1075 youden_sens=0.833 youden_spec=0.833 J=0.667
hits prompts_marked_above=12/12 instance=key-free-hits used_keys=False
poshits auc=0.854 mean_pos=0.8685 mean_neg=-0.0081 diff=0.8766 pos>0=10/12 neg<=0=9/12 perm_p=0.0009995 binom_p=0.01929 youden_t=0.1075 youden_sens=0.833 youden_spec=0.833 J=0.667
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
hashpool auc=0.833 mean_pos=0.4920 mean_neg=-0.7253 diff=1.2173 pos>0=6/12 neg<=0=10/12 perm_p=0.0009995 binom_p=0.6128 youden_t=-0.6662 youden_sens=1.000 youden_spec=0.667 J=0.667
hashpool prompts_marked_above=10/12 instance=key-free-hashpool used_keys=False
