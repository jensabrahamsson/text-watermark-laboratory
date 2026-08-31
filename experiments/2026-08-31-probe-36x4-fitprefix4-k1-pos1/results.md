# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-36x4 context_len=1 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 34/36 | 0.936 | 132/144 | 106/144 | 0.0004998 | 2.6865 |
| first | 34/36 | 0.687 | 114/144 | 92/144 | 0.0004998 | 1.2894 |
| poshits | 34/36 | 0.940 | 132/144 | 128/144 | 0.0004998 | 2.6199 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 131/144 | 131/144 | 0.0252 | 0.910 | 0.910 |
| first | 114/144 | 94/144 | 0.0877 | 0.792 | 0.653 |
| poshits | 122/144 | 128/144 | 0.0281 | 0.847 | 0.889 |

hits auc=0.936 mean_pos=2.2842 mean_neg=-0.4023 diff=2.6865 pos>0=132/144 neg<=0=106/144 perm_p=0.0004998 binom_p=5.103e-27 youden_t=0.0252 youden_sens=0.910 youden_spec=0.917 J=0.826
hits prompts_marked_above=34/36 instance=key-free-hits used_keys=False
first auc=0.687 mean_pos=0.6962 mean_neg=-0.5932 diff=1.2894 pos>0=114/144 neg<=0=92/144 perm_p=0.0004998 binom_p=4.966e-13 youden_t=0.0889 youden_sens=0.792 youden_spec=0.674 J=0.465
first prompts_marked_above=34/36 instance=key-free-first used_keys=False
poshits auc=0.940 mean_pos=2.3191 mean_neg=-0.3008 diff=2.6199 pos>0=132/144 neg<=0=128/144 perm_p=0.0004998 binom_p=5.103e-27 youden_t=0.0134 youden_sens=0.903 youden_spec=0.910 J=0.812
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
