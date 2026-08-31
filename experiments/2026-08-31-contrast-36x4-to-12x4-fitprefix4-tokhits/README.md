# Key-free instance contrast (tokhits / postokhits)

**Result.** Observed-token `postokhits` on the same 4-token gate still
assigns `lr>0` to **0/48** control-shuffled-30 files. Public vs unmarked
is **12/12** with isolated **16/48** (precision 1.0 among decided).
Public vs control is **12/12**, AUC 0.667, all 48 control files `≤ 0`.
poshits remains **0/48** control / **39/48** public. Quote **0/48**, not
the 12/12 control-vs-unmarked prompt-mean artifact. Not key recovery.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md),
[../../research/key-free-contrast.md](../../research/key-free-contrast.md).

# Key-free instance contrast

instance-contrast n_rows=12 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 control=experiments/2026-08-31-pair-12x4-controlkeys n_control=48 n_aligned=48 fit_prefix=4 used_keys=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | comparison | prompt wins | file auc | pos>0 | neg<=0 | perm p | brier |
|---|---|---|---|---|---|---|---|
| hits | control-vs-unmarked | 8/12 | 0.458 | 0/48 | 33/48 | 0.1649 | 0.2552 |
| hits | public-vs-control | 12/12 | 0.906 | 39/48 | 48/48 | 0.0004998 | 0.1904 |
| hits | public-vs-unmarked | 11/12 | 0.820 | 39/48 | 33/48 | 0.0004998 | 0.1956 |
| tokhits | control-vs-unmarked | 11/12 | 0.531 | 0/48 | 45/48 | 0.1609 | 0.2532 |
| tokhits | public-vs-control | 12/12 | 0.667 | 16/48 | 48/48 | 0.0004998 | 0.2090 |
| tokhits | public-vs-unmarked | 11/12 | 0.674 | 16/48 | 45/48 | 0.0004998 | 0.2123 |
| poshits | control-vs-unmarked | 9/12 | 0.510 | 0/48 | 41/48 | 0.02349 | 0.2408 |
| poshits | public-vs-control | 12/12 | 0.906 | 39/48 | 48/48 | 0.0004998 | 0.1910 |
| poshits | public-vs-unmarked | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 0.1818 |
| postokhits | control-vs-unmarked | 12/12 | 0.542 | 0/48 | 48/48 | 0.05497 | 0.2396 |
| postokhits | public-vs-control | 12/12 | 0.667 | 16/48 | 48/48 | 0.0004998 | 0.2090 |
| postokhits | public-vs-unmarked | 12/12 | 0.694 | 16/48 | 48/48 | 0.0004998 | 0.1986 |

public-vs-unmarked: can the key-free reader still see the public mark. control-vs-unmarked: does a *different* key instance look marked. public-vs-control: can it tell the two instances apart. pos is the first class in each name (control, public, public).

hits control-vs-unmarked auc=0.458 mean_pos=0.0000 mean_neg=-0.2107 diff=0.2107 pos>0=0/48 neg<=0=33/48 perm_p=0.1649 binom_p=1 youden_t=-0.0183 youden_sens=1.000 youden_spec=0.229 J=0.229 brier=0.2552 prompts=8/12
hits public-vs-control auc=0.906 mean_pos=1.2994 mean_neg=0.0000 diff=1.2994 pos>0=39/48 neg<=0=48/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=1.000 J=0.812 brier=0.1904 prompts=12/12
hits public-vs-unmarked auc=0.820 mean_pos=1.2994 mean_neg=-0.2107 diff=1.5101 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0400 youden_sens=0.812 youden_spec=0.792 J=0.604 brier=0.1956 prompts=11/12
tokhits control-vs-unmarked auc=0.531 mean_pos=0.0000 mean_neg=-0.2135 diff=0.2135 pos>0=0/48 neg<=0=45/48 perm_p=0.1609 binom_p=1 youden_t=-1.4930 youden_sens=1.000 youden_spec=0.125 J=0.125 brier=0.2532 prompts=11/12
tokhits public-vs-control auc=0.667 mean_pos=1.1351 mean_neg=0.0000 diff=1.1351 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333 brier=0.2090 prompts=12/12
tokhits public-vs-unmarked auc=0.674 mean_pos=1.1351 mean_neg=-0.2135 diff=1.3486 pos>0=16/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.9934 youden_t=1.1386 youden_sens=0.333 youden_spec=0.958 J=0.292 brier=0.2123 prompts=11/12
poshits control-vs-unmarked auc=0.510 mean_pos=0.0000 mean_neg=-0.3382 diff=0.3382 pos>0=0/48 neg<=0=41/48 perm_p=0.02349 binom_p=1 youden_t=-0.6122 youden_sens=1.000 youden_spec=0.167 J=0.167 brier=0.2408 prompts=9/12
poshits public-vs-control auc=0.906 mean_pos=1.2933 mean_neg=0.0000 diff=1.2933 pos>0=39/48 neg<=0=48/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=1.000 J=0.812 brier=0.1910 prompts=12/12
poshits public-vs-unmarked auc=0.873 mean_pos=1.2933 mean_neg=-0.3382 diff=1.6315 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667 brier=0.1818 prompts=12/12
postokhits control-vs-unmarked auc=0.542 mean_pos=0.0000 mean_neg=-0.3353 diff=0.3353 pos>0=0/48 neg<=0=48/48 perm_p=0.05497 binom_p=1 youden_t=-3.8311 youden_sens=1.000 youden_spec=0.083 J=0.083 brier=0.2396 prompts=12/12
postokhits public-vs-control auc=0.667 mean_pos=1.1351 mean_neg=0.0000 diff=1.1351 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333 brier=0.2090 prompts=12/12
postokhits public-vs-unmarked auc=0.694 mean_pos=1.1351 mean_neg=-0.3353 diff=1.4705 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333 brier=0.1986 prompts=12/12

transfer n_methods=4 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Tables fit on public-key marked vs unmarked only. Control-gen used control-shuffled-30 at sampling. If control ranks with unmarked, the key-free reader is instance-specific without keys. If it ranks with marked, the reader is detecting tournament sampling, not this instance. Not key recovery. Not Claude.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 0.0004998 | 1.5101 |
| tokhits | 11/12 | 0.674 | 16/48 | 45/48 | 0.0004998 | 1.3486 |
| poshits | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 1.6315 |
| postokhits | 12/12 | 0.694 | 16/48 | 48/48 | 0.0004998 | 1.4705 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hits | 9/48 | 22/48 | 39/0 | 15/11 | 0.722 |
| tokhits | 32/48 | 39/48 | 16/0 | 3/6 | 0.842 |
| poshits | 9/48 | 33/48 | 39/0 | 7/8 | 0.848 |
| postokhits | 32/48 | 44/48 | 16/0 | 0/4 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|

hits auc=0.820 mean_pos=1.2994 mean_neg=-0.2107 diff=1.5101 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0400 youden_sens=0.812 youden_spec=0.792 J=0.604
hits zeros=9/48 vs 22/48 decided_tp=39 fn=0 fp=15 tn=11 precision=0.722 decided_acc=0.769
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
tokhits auc=0.674 mean_pos=1.1351 mean_neg=-0.2135 diff=1.3486 pos>0=16/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.9934 youden_t=1.1386 youden_sens=0.333 youden_spec=0.958 J=0.292
tokhits zeros=32/48 vs 39/48 decided_tp=16 fn=0 fp=3 tn=6 precision=0.842 decided_acc=0.880
tokhits prompts_marked_above=11/12 instance=key-free-tokhits used_keys=False
poshits auc=0.873 mean_pos=1.2933 mean_neg=-0.3382 diff=1.6315 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667
poshits zeros=9/48 vs 33/48 decided_tp=39 fn=0 fp=7 tn=8 precision=0.848 decided_acc=0.870
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
postokhits auc=0.694 mean_pos=1.1351 mean_neg=-0.3353 diff=1.4705 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333
postokhits zeros=32/48 vs 44/48 decided_tp=16 fn=0 fp=0 tn=4 precision=1.000 decided_acc=1.000
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
