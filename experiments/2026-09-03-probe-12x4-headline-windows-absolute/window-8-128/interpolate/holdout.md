indicate holdout mode=rotate n_prompts=12 n_files=96 marked_above_unmarked=20 prompts_marked_above=4 prompts_marked_ge=4 prompt_ties=0 prompt_losses=8 ranking_without_isolated_tp=1/4 ranking_losses_with_isolated_tp=7 marked_lr_positive=17 unmarked_lr_nonpositive=25 margin=0 context_len=4 score_kind=interpolate@w8-128 auc=0.435 perm_p=0.7881 (file-level, descriptive) prompt_sign_p=0.8991 used_keys=False hash_iv=False g_values=False instance=key-free-interpolate
single-file auc=0.435 mean_pos=-0.0387 mean_neg=-0.0019 diff=-0.0368 pos>0=17/48 neg<=0=25/48 perm_p=0.7881 (file-level, descriptive) binom_p=0.9853 (file-level, descriptive) youden_t=0.3097 youden_sens=0.083 youden_spec=0.958 J=0.042
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
01-harbour-marked.txt: lr=0.054883 instance=key-free-interpolate
01-harbour-unmarked-gen.txt: lr=0.223198 instance=key-free-interpolate
01-harbour#1: unmarked_higher
01-harbour-marked-2.txt: lr=0.115548 instance=key-free-interpolate
01-harbour-unmarked-gen-2.txt: lr=0.031222 instance=key-free-interpolate
01-harbour#2: marked_higher
01-harbour-marked-3.txt: lr=-0.025318 instance=key-free-interpolate
01-harbour-unmarked-gen-3.txt: lr=0.072211 instance=key-free-interpolate
01-harbour#3: unmarked_higher
01-harbour-marked-4.txt: lr=0.063110 instance=key-free-interpolate
01-harbour-unmarked-gen-4.txt: lr=0.036978 instance=key-free-interpolate
01-harbour#4: marked_higher
02-night-bus-marked.txt: lr=-0.736903 instance=key-free-interpolate
02-night-bus-unmarked-gen.txt: lr=-0.031175 instance=key-free-interpolate
02-night-bus#1: unmarked_higher
02-night-bus-marked-2.txt: lr=-0.325087 instance=key-free-interpolate
02-night-bus-unmarked-gen-2.txt: lr=-0.257836 instance=key-free-interpolate
02-night-bus#2: unmarked_higher
02-night-bus-marked-3.txt: lr=-0.091242 instance=key-free-interpolate
02-night-bus-unmarked-gen-3.txt: lr=-0.145125 instance=key-free-interpolate
02-night-bus#3: marked_higher
02-night-bus-marked-4.txt: lr=-0.003206 instance=key-free-interpolate
02-night-bus-unmarked-gen-4.txt: lr=-0.338285 instance=key-free-interpolate
02-night-bus#4: marked_higher
03-library-marked.txt: lr=-0.138122 instance=key-free-interpolate
03-library-unmarked-gen.txt: lr=-0.000596 instance=key-free-interpolate
03-library#1: unmarked_higher
03-library-marked-2.txt: lr=0.104427 instance=key-free-interpolate
03-library-unmarked-gen-2.txt: lr=-0.064325 instance=key-free-interpolate
03-library#2: marked_higher
03-library-marked-3.txt: lr=-0.375262 instance=key-free-interpolate
03-library-unmarked-gen-3.txt: lr=-0.090735 instance=key-free-interpolate
03-library#3: unmarked_higher
03-library-marked-4.txt: lr=-0.108910 instance=key-free-interpolate
03-library-unmarked-gen-4.txt: lr=-0.084083 instance=key-free-interpolate
03-library#4: unmarked_higher
04-market-marked.txt: lr=-0.018151 instance=key-free-interpolate
04-market-unmarked-gen.txt: lr=0.233731 instance=key-free-interpolate
04-market#1: unmarked_higher
04-market-marked-2.txt: lr=0.118439 instance=key-free-interpolate
04-market-unmarked-gen-2.txt: lr=-0.116555 instance=key-free-interpolate
04-market#2: marked_higher
04-market-marked-3.txt: lr=-0.348823 instance=key-free-interpolate
04-market-unmarked-gen-3.txt: lr=0.037613 instance=key-free-interpolate
04-market#3: unmarked_higher
04-market-marked-4.txt: lr=0.389038 instance=key-free-interpolate
04-market-unmarked-gen-4.txt: lr=0.112870 instance=key-free-interpolate
04-market#4: marked_higher
05-kitchen-marked.txt: lr=0.350099 instance=key-free-interpolate
05-kitchen-unmarked-gen.txt: lr=-0.203026 instance=key-free-interpolate
05-kitchen#1: marked_higher
05-kitchen-marked-2.txt: lr=-0.038998 instance=key-free-interpolate
05-kitchen-unmarked-gen-2.txt: lr=-0.279498 instance=key-free-interpolate
05-kitchen#2: marked_higher
05-kitchen-marked-3.txt: lr=-0.132484 instance=key-free-interpolate
05-kitchen-unmarked-gen-3.txt: lr=0.557246 instance=key-free-interpolate
05-kitchen#3: unmarked_higher
05-kitchen-marked-4.txt: lr=0.014450 instance=key-free-interpolate
05-kitchen-unmarked-gen-4.txt: lr=0.096074 instance=key-free-interpolate
05-kitchen#4: unmarked_higher
06-station-marked.txt: lr=0.178552 instance=key-free-interpolate
06-station-unmarked-gen.txt: lr=0.140466 instance=key-free-interpolate
06-station#1: marked_higher
06-station-marked-2.txt: lr=-0.122240 instance=key-free-interpolate
06-station-unmarked-gen-2.txt: lr=0.222501 instance=key-free-interpolate
06-station#2: unmarked_higher
06-station-marked-3.txt: lr=-0.163126 instance=key-free-interpolate
06-station-unmarked-gen-3.txt: lr=-0.036381 instance=key-free-interpolate
06-station#3: unmarked_higher
06-station-marked-4.txt: lr=-0.182706 instance=key-free-interpolate
06-station-unmarked-gen-4.txt: lr=-0.089872 instance=key-free-interpolate
06-station#4: unmarked_higher
07-rain-marked.txt: lr=-0.138437 instance=key-free-interpolate
07-rain-unmarked-gen.txt: lr=0.044411 instance=key-free-interpolate
07-rain#1: unmarked_higher
07-rain-marked-2.txt: lr=0.067430 instance=key-free-interpolate
07-rain-unmarked-gen-2.txt: lr=0.201682 instance=key-free-interpolate
07-rain#2: unmarked_higher
07-rain-marked-3.txt: lr=-0.000019 instance=key-free-interpolate
07-rain-unmarked-gen-3.txt: lr=0.059189 instance=key-free-interpolate
07-rain#3: unmarked_higher
07-rain-marked-4.txt: lr=-0.069038 instance=key-free-interpolate
07-rain-unmarked-gen-4.txt: lr=0.043029 instance=key-free-interpolate
07-rain#4: unmarked_higher
08-letter-marked.txt: lr=0.583608 instance=key-free-interpolate
08-letter-unmarked-gen.txt: lr=-0.121878 instance=key-free-interpolate
08-letter#1: marked_higher
08-letter-marked-2.txt: lr=-0.349184 instance=key-free-interpolate
08-letter-unmarked-gen-2.txt: lr=0.380443 instance=key-free-interpolate
08-letter#2: unmarked_higher
08-letter-marked-3.txt: lr=-0.302518 instance=key-free-interpolate
08-letter-unmarked-gen-3.txt: lr=0.075838 instance=key-free-interpolate
08-letter#3: unmarked_higher
08-letter-marked-4.txt: lr=-0.110409 instance=key-free-interpolate
08-letter-unmarked-gen-4.txt: lr=0.260240 instance=key-free-interpolate
08-letter#4: unmarked_higher
09-workshop-marked.txt: lr=-0.106006 instance=key-free-interpolate
09-workshop-unmarked-gen.txt: lr=0.037858 instance=key-free-interpolate
09-workshop#1: unmarked_higher
09-workshop-marked-2.txt: lr=0.078882 instance=key-free-interpolate
09-workshop-unmarked-gen-2.txt: lr=-0.046388 instance=key-free-interpolate
09-workshop#2: marked_higher
09-workshop-marked-3.txt: lr=-0.130259 instance=key-free-interpolate
09-workshop-unmarked-gen-3.txt: lr=0.309682 instance=key-free-interpolate
09-workshop#3: unmarked_higher
09-workshop-marked-4.txt: lr=0.214093 instance=key-free-interpolate
09-workshop-unmarked-gen-4.txt: lr=-0.148944 instance=key-free-interpolate
09-workshop#4: marked_higher
10-office-marked.txt: lr=-0.122860 instance=key-free-interpolate
10-office-unmarked-gen.txt: lr=-0.064374 instance=key-free-interpolate
10-office#1: unmarked_higher
10-office-marked-2.txt: lr=0.717510 instance=key-free-interpolate
10-office-unmarked-gen-2.txt: lr=0.167319 instance=key-free-interpolate
10-office#2: marked_higher
10-office-marked-3.txt: lr=0.011745 instance=key-free-interpolate
10-office-unmarked-gen-3.txt: lr=0.070272 instance=key-free-interpolate
10-office#3: unmarked_higher
10-office-marked-4.txt: lr=0.087974 instance=key-free-interpolate
10-office-unmarked-gen-4.txt: lr=-0.029175 instance=key-free-interpolate
10-office#4: marked_higher
11-garden-marked.txt: lr=-0.073717 instance=key-free-interpolate
11-garden-unmarked-gen.txt: lr=-0.256837 instance=key-free-interpolate
11-garden#1: marked_higher
11-garden-marked-2.txt: lr=-0.288973 instance=key-free-interpolate
11-garden-unmarked-gen-2.txt: lr=-0.233607 instance=key-free-interpolate
11-garden#2: unmarked_higher
11-garden-marked-3.txt: lr=-0.107461 instance=key-free-interpolate
11-garden-unmarked-gen-3.txt: lr=-0.230713 instance=key-free-interpolate
11-garden#3: marked_higher
11-garden-marked-4.txt: lr=0.032539 instance=key-free-interpolate
11-garden-unmarked-gen-4.txt: lr=-0.096382 instance=key-free-interpolate
11-garden#4: marked_higher
12-ferry-queue-marked.txt: lr=-0.014959 instance=key-free-interpolate
12-ferry-queue-unmarked-gen.txt: lr=0.199190 instance=key-free-interpolate
12-ferry-queue#1: unmarked_higher
12-ferry-queue-marked-2.txt: lr=-0.011658 instance=key-free-interpolate
12-ferry-queue-unmarked-gen-2.txt: lr=-0.110428 instance=key-free-interpolate
12-ferry-queue#2: marked_higher
12-ferry-queue-marked-3.txt: lr=-0.093487 instance=key-free-interpolate
12-ferry-queue-unmarked-gen-3.txt: lr=-0.394683 instance=key-free-interpolate
12-ferry-queue#3: marked_higher
12-ferry-queue-marked-4.txt: lr=-0.311599 instance=key-free-interpolate
12-ferry-queue-unmarked-gen-4.txt: lr=-0.232560 instance=key-free-interpolate
12-ferry-queue#4: unmarked_higher
