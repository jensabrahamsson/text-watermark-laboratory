# Key-free instance contrast

**Result (full 700-token pair-limit).** hits public vs control AUC **1.000**,
12/12. Control vs unmarked AUC **0.556**. poshits control `lr>0` **0/12**.
Write-up: [../../research/key-free-contrast.md](../../research/key-free-contrast.md).

instance-contrast n_rows=9 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-limit control=experiments/2026-08-17-pair-limit n_control=12 n_aligned=12 fit_prefix=None used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| hits | control-vs-unmarked | 8/12 | 0.556 | 7/12 | 8/12 | 0.4458 | 0.2499 |
| hits | public-vs-control | 12/12 | 1.000 | 12/12 | 5/12 | 0.0004998 | 0.1999 |
| hits | public-vs-unmarked | 11/12 | 0.965 | 12/12 | 8/12 | 0.0004998 | 0.1992 |
| poshits | control-vs-unmarked | 9/12 | 0.417 | 0/12 | 9/12 | 0.7391 | 0.2528 |
| poshits | public-vs-control | 12/12 | 0.917 | 10/12 | 12/12 | 0.0004998 | 0.2182 |
| poshits | public-vs-unmarked | 11/12 | 0.806 | 10/12 | 9/12 | 0.04548 | 0.2210 |
| hashpool | control-vs-unmarked | 6/12 | 0.431 | 0/12 | 12/12 | 0.5747 | 0.2501 |
| hashpool | public-vs-control | 12/12 | 0.965 | 10/12 | 12/12 | 0.0004998 | 0.2457 |
| hashpool | public-vs-unmarked | 12/12 | 0.944 | 10/12 | 12/12 | 0.0004998 | 0.2459 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

hits control-vs-unmarked auc=0.556 mean_pos=-0.0181 mean_neg=-0.0265 diff=0.0084 pos>0=7/12 neg<=0=8/12 perm_p=0.4458 binom_p=0.3872 youden_t=0.0000 youden_sens=0.583 youden_spec=0.667 J=0.250 brier=0.2499 prompts=8/12
hits public-vs-control auc=1.000 mean_pos=0.4608 mean_neg=-0.0181 diff=0.4789 pos>0=12/12 neg<=0=5/12 perm_p=0.0004998 binom_p=0.0002441 youden_t=0.1284 youden_sens=1.000 youden_spec=1.000 J=1.000 brier=0.1999 prompts=12/12
hits public-vs-unmarked auc=0.965 mean_pos=0.4608 mean_neg=-0.0265 diff=0.4872 pos>0=12/12 neg<=0=8/12 perm_p=0.0004998 binom_p=0.0002441 youden_t=0.1735 youden_sens=0.833 youden_spec=1.000 J=0.833 brier=0.1992 prompts=11/12
poshits control-vs-unmarked auc=0.417 mean_pos=0.0000 mean_neg=0.0162 diff=-0.0162 pos>0=0/12 neg<=0=9/12 perm_p=0.7391 binom_p=1 youden_t=-0.3327 youden_sens=1.000 youden_spec=0.083 J=0.083 brier=0.2528 prompts=9/12
poshits public-vs-control auc=0.917 mean_pos=0.7125 mean_neg=0.0000 diff=0.7125 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=1.000 J=0.833 brier=0.2182 prompts=12/12
poshits public-vs-unmarked auc=0.806 mean_pos=0.7125 mean_neg=0.0162 diff=0.6963 pos>0=10/12 neg<=0=9/12 perm_p=0.04548 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=0.750 J=0.583 brier=0.2210 prompts=11/12
hashpool control-vs-unmarked auc=0.431 mean_pos=-0.0154 mean_neg=-0.0143 diff=-0.0010 pos>0=0/12 neg<=0=12/12 perm_p=0.5747 binom_p=1 youden_t=-0.0306 youden_sens=0.917 youden_spec=0.250 J=0.167 brier=0.2501 prompts=6/12
hashpool public-vs-control auc=0.965 mean_pos=0.0191 mean_neg=-0.0154 diff=0.0345 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=-0.0015 youden_sens=0.917 youden_spec=1.000 J=0.917 brier=0.2457 prompts=12/12
hashpool public-vs-unmarked auc=0.944 mean_pos=0.0191 mean_neg=-0.0143 diff=0.0335 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=1.000 J=0.833 brier=0.2459 prompts=12/12

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-limit n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.965 | 12/12 | 8/12 | 0.0004998 | 0.4872 |
| poshits | 11/12 | 0.806 | 10/12 | 9/12 | 0.04548 | 0.6963 |
| hashpool | 12/12 | 0.944 | 10/12 | 12/12 | 0.0004998 | 0.0335 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.965 mean_pos=0.4608 mean_neg=-0.0265 diff=0.4872 pos>0=12/12 neg<=0=8/12 perm_p=0.0004998 binom_p=0.0002441 youden_t=0.1735 youden_sens=0.833 youden_spec=1.000 J=0.833
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
poshits auc=0.806 mean_pos=0.7125 mean_neg=0.0162 diff=0.6963 pos>0=10/12 neg<=0=9/12 perm_p=0.04548 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=0.750 J=0.583
poshits prompts_marked_above=11/12 instance=key-free-poshits used_keys=False
hashpool auc=0.944 mean_pos=0.0191 mean_neg=-0.0143 diff=0.0335 pos>0=10/12 neg<=0=12/12 perm_p=0.0004998 binom_p=0.01929 youden_t=0.0000 youden_sens=0.833 youden_spec=1.000 J=0.833
hashpool prompts_marked_above=12/12 instance=key-free-hashpool used_keys=False
