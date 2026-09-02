# Key-free probe

probe n_methods=15 pair_dir=experiments/2026-09-01-pair-100x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 99/100 | 0.968 | 379/400 | 353/400 | 0.0004998 | 2.6077 |
| hard | 100/100 | 0.979 | 388/400 | 345/400 | 0.0004998 | 3.7545 |
| backoff | 100/100 | 0.976 | 388/400 | 332/400 | 0.0004998 | 3.7114 |
| interpolate | 99/100 | 0.960 | 374/400 | 353/400 | 0.0004998 | 4.5745 |
| hits | 99/100 | 0.980 | 393/400 | 335/400 | 0.0004998 | 3.7914 |
| freqhits | 99/100 | 0.970 | 391/400 | 342/400 | 0.0004998 | 3.6948 |
| hitmass | 100/100 | 0.977 | 393/400 | 335/400 | 0.0004998 | 2.8113 |
| gated | 99/100 | 0.973 | 391/400 | 336/400 | 0.0004998 | 3.7598 |
| shrinkage | 99/100 | 0.977 | 391/400 | 335/400 | 0.0004998 | 3.7433 |
| mix | 100/100 | 0.978 | 387/400 | 346/400 | 0.0004998 | 3.6865 |
| hashpool | 100/100 | 0.977 | 388/400 | 335/400 | 0.0004998 | 3.6386 |
| rankpath | 96/100 | 0.822 | 314/400 | 302/400 | 0.0004998 | 0.8431 |
| rankuni | 81/100 | 0.640 | 297/400 | 210/400 | 0.0004998 | 0.0821 |
| stack | 100/100 | 0.977 | 370/400 | 389/400 | 0.0004998 | 0.0144 |
| logit | 100/100 | 0.976 | 379/400 | 387/400 | 0.0004998 | 8.3678 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| unigram | 1/400 | 7/400 | 379/20 | 47/346 | 0.890 |
| hard | 0/400 | 1/400 | 388/12 | 55/344 | 0.876 |
| backoff | 0/400 | 1/400 | 388/12 | 68/331 | 0.851 |
| interpolate | 0/400 | 1/400 | 374/26 | 47/352 | 0.888 |
| hits | 0/400 | 172/400 | 393/7 | 65/163 | 0.858 |
| freqhits | 0/400 | 184/400 | 391/9 | 58/158 | 0.871 |
| hitmass | 0/400 | 172/400 | 393/7 | 65/163 | 0.858 |
| gated | 0/400 | 173/400 | 391/9 | 64/163 | 0.859 |
| shrinkage | 0/400 | 172/400 | 391/9 | 65/163 | 0.857 |
| mix | 0/400 | 1/400 | 387/13 | 54/345 | 0.878 |
| hashpool | 0/400 | 0/400 | 388/12 | 65/335 | 0.857 |
| rankpath | 0/400 | 0/400 | 314/86 | 98/302 | 0.762 |
| rankuni | 0/400 | 0/400 | 297/103 | 190/210 | 0.610 |
| stack | 0/400 | 0/400 | 370/30 | 11/389 | 0.971 |
| logit | 0/400 | 0/400 | 379/21 | 13/387 | 0.967 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| unigram | 367/400 | 375/400 | 0.5629 | 0.917 | 0.938 |
| hard | 378/400 | 382/400 | 0.7469 | 0.945 | 0.955 |
| backoff | 376/400 | 380/400 | 0.8473 | 0.940 | 0.950 |
| interpolate | 368/400 | 375/400 | 0.3548 | 0.920 | 0.938 |
| hits | 392/400 | 379/400 | 0.1795 | 0.980 | 0.948 |
| freqhits | 390/400 | 380/400 | 0.1795 | 0.975 | 0.950 |
| hitmass | 385/400 | 380/400 | 0.3725 | 0.963 | 0.950 |
| gated | 390/400 | 380/400 | 0.1795 | 0.975 | 0.950 |
| shrinkage | 382/400 | 379/400 | 0.2161 | 0.955 | 0.948 |
| mix | 376/400 | 381/400 | 0.8891 | 0.940 | 0.953 |
| hashpool | 371/400 | 383/400 | 0.9778 | 0.927 | 0.958 |
| rankpath | 312/400 | 319/400 | 0.0637 | 0.780 | 0.797 |
| rankuni | 248/400 | 275/400 | 0.0405 | 0.620 | 0.688 |
| stack | 377/400 | 388/400 | -0.0004 | 0.943 | 0.970 |
| logit | 379/400 | 385/400 | -0.0824 | 0.948 | 0.963 |

unigram auc=0.968 mean_pos=1.7411 mean_neg=-0.8666 diff=2.6077 pos>0=379/400 neg<=0=353/400 perm_p=0.0004998 binom_p=2.068e-86 youden_t=0.5732 youden_sens=0.917 youden_spec=0.950 J=0.867
unigram prompts_marked_above=99/100 instance=key-free-unigram used_keys=False
hard auc=0.979 mean_pos=2.8477 mean_neg=-0.9068 diff=3.7545 pos>0=388/400 neg<=0=345/400 perm_p=0.0004998 binom_p=1.185e-98 youden_t=0.7473 youden_sens=0.945 youden_spec=0.958 J=0.902
hard prompts_marked_above=100/100 instance=key-free-counts used_keys=False
backoff auc=0.976 mean_pos=2.8748 mean_neg=-0.8366 diff=3.7114 pos>0=388/400 neg<=0=332/400 perm_p=0.0004998 binom_p=1.185e-98 youden_t=0.8486 youden_sens=0.940 youden_spec=0.955 J=0.895
backoff prompts_marked_above=100/100 instance=key-free-backoff used_keys=False
interpolate auc=0.960 mean_pos=2.8102 mean_neg=-1.7643 diff=4.5745 pos>0=374/400 neg<=0=353/400 perm_p=0.0004998 binom_p=2.025e-80 youden_t=0.3550 youden_sens=0.920 youden_spec=0.940 J=0.860
interpolate prompts_marked_above=99/100 instance=key-free-interpolate used_keys=False
hits auc=0.980 mean_pos=3.0886 mean_neg=-0.7027 diff=3.7914 pos>0=393/400 neg<=0=335/400 perm_p=0.0004998 binom_p=1.216e-106 youden_t=0.1795 youden_sens=0.980 youden_spec=0.948 J=0.927
hits prompts_marked_above=99/100 instance=key-free-hits used_keys=False
freqhits auc=0.970 mean_pos=3.0065 mean_neg=-0.6883 diff=3.6948 pos>0=391/400 neg<=0=342/400 perm_p=0.0004998 binom_p=2.615e-103 youden_t=0.1795 youden_sens=0.975 youden_spec=0.950 J=0.925
freqhits prompts_marked_above=99/100 instance=key-free-freqhits used_keys=False
hitmass auc=0.977 mean_pos=2.5950 mean_neg=-0.2163 diff=2.8113 pos>0=393/400 neg<=0=335/400 perm_p=0.0004998 binom_p=1.216e-106 youden_t=0.3811 youden_sens=0.963 youden_spec=0.958 J=0.920
hitmass prompts_marked_above=100/100 instance=key-free-hitmass used_keys=False
gated auc=0.973 mean_pos=3.0598 mean_neg=-0.7000 diff=3.7598 pos>0=391/400 neg<=0=336/400 perm_p=0.0004998 binom_p=2.615e-103 youden_t=0.1795 youden_sens=0.975 youden_spec=0.950 J=0.925
gated prompts_marked_above=99/100 instance=key-free-gated used_keys=False
shrinkage auc=0.977 mean_pos=3.0425 mean_neg=-0.7008 diff=3.7433 pos>0=391/400 neg<=0=335/400 perm_p=0.0004998 binom_p=2.615e-103 youden_t=0.1795 youden_sens=0.975 youden_spec=0.948 J=0.922
shrinkage prompts_marked_above=99/100 instance=key-free-shrinkage used_keys=False
mix auc=0.978 mean_pos=2.7874 mean_neg=-0.8991 diff=3.6865 pos>0=387/400 neg<=0=346/400 perm_p=0.0004998 binom_p=3.545e-97 youden_t=0.8943 youden_sens=0.940 youden_spec=0.960 J=0.900
mix prompts_marked_above=100/100 instance=key-free-mix used_keys=False
hashpool auc=0.977 mean_pos=2.8290 mean_neg=-0.8095 diff=3.6386 pos>0=388/400 neg<=0=335/400 perm_p=0.0004998 binom_p=1.185e-98 youden_t=0.9859 youden_sens=0.927 youden_spec=0.970 J=0.897
hashpool prompts_marked_above=100/100 instance=key-free-hashpool used_keys=False
rankpath auc=0.822 mean_pos=0.3037 mean_neg=-0.5394 diff=0.8431 pos>0=314/400 neg<=0=302/400 perm_p=0.0004998 binom_p=6.801e-32 youden_t=0.0637 youden_sens=0.780 youden_spec=0.800 J=0.580
rankpath prompts_marked_above=96/100 instance=key-free-rankpath used_keys=False
rankuni auc=0.640 mean_pos=0.0395 mean_neg=-0.0426 diff=0.0821 pos>0=297/400 neg<=0=210/400 perm_p=0.0004998 binom_p=3.33e-23 youden_t=0.0406 youden_sens=0.620 youden_spec=0.690 J=0.310
rankuni prompts_marked_above=81/100 instance=key-free-rankuni used_keys=False
stack auc=0.977 mean_pos=0.0072 mean_neg=-0.0072 diff=0.0144 pos>0=370/400 neg<=0=389/400 perm_p=0.0004998 binom_p=6.002e-76 youden_t=-0.0004 youden_sens=0.943 youden_spec=0.973 J=0.915
stack prompts_marked_above=100/100 instance=key-free-stack used_keys=False
logit auc=0.976 mean_pos=5.1249 mean_neg=-3.2429 diff=8.3678 pos>0=379/400 neg<=0=387/400 perm_p=0.0004998 binom_p=2.068e-86 youden_t=-0.0769 youden_sens=0.950 youden_spec=0.968 J=0.917
logit prompts_marked_above=100/100 instance=key-free-logit used_keys=False
