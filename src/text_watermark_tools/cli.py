"""Launchable entry: score a file/stdin, or run the known-mark experiment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from text_watermark_tools.experiment import (
    persist_result,
    print_result,
    run_known_mark_experiment,
)
from text_watermark_tools.iterate import (
    DASHSCOPE_KEY_FILE,
    DEEPSEEK_KEY_FILE,
    DEFAULT_BASE_URL,
    DEFAULT_INDICATE_THRESHOLD,
    DEFAULT_MAX_PASSES,
    DEFAULT_MEAN_TOL,
    DEFAULT_MIN_NGRAMS,
    DEFAULT_MODEL,
    STOP_CHANCE,
    STOP_INDICATE,
    OperatorError,
    chat_complete,
    dashscope_api_key,
    deepseek_api_key,
    persist_iterate_run,
    print_iterate_run,
    rewrite_once,
    run_iterate,
)
from text_watermark_tools.blind import (
    DEFAULT_ALPHA,
    DEFAULT_CONTEXT_LEN,
    clip_twins,
    leave_one_prompt_out,
    load_twins,
    persist_blind_eval,
    print_blind_eval,
)
from text_watermark_tools.indicator import (
    CAVEAT,
    INDICATOR_INSTANCE,
    fit_indicator,
    format_indicator,
    holdout_single_text,
    load_tables_meta,
    rotate_holdout,
    persist_holdout,
    persist_indicator,
    print_holdout,
    score_text_from_tables,
)
from text_watermark_tools.pair import (
    collect_prompts,
    persist_pair_run,
    print_pair_run,
    run_control_only,
    run_pairs,
)
from text_watermark_tools.contrast import (
    load_control_draws,
    persist_contrast,
    print_contrast,
    run_instance_contrast,
)
from text_watermark_tools.learn import (
    persist_learn,
    persist_learn_transfer,
    print_learn,
    print_learn_transfer,
    run_learn,
    run_learn_transfer,
    spec_from_args,
)
from text_watermark_tools.probe import (
    persist_probe,
    persist_scrub,
    persist_transfer,
    print_probe,
    print_scrub,
    print_transfer,
    run_probe,
    run_scrub_files,
    run_transfer,
    _parse_prefix_lens,
    _parse_windows,
)
from text_watermark_tools.resample import run_resample
from text_watermark_tools.score import (
    CONTROL_INSTANCE,
    PUBLIC_INSTANCE,
    control_keys,
    format_score,
    load_tokenizer,
    official_score_token_ids,
)

QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-plus"


def _parse_prefix_arg(raw: str | None) -> tuple[int, ...]:
    if not raw:
        return ()
    parts = [p.strip() for p in str(raw).split(",") if p.strip()]
    return _parse_prefix_lens([int(p) for p in parts])


def _parse_windows_arg(raw: str | None) -> tuple[tuple[int, int], ...]:
    if not raw:
        return ()
    parts = [p.strip() for p in str(raw).split(",") if p.strip()]
    return _parse_windows(parts)


def _read_input(path: str | None) -> str:
    if path is None or path == "-":
        return sys.stdin.read()
    return Path(path).read_text()


def _txt_files_in(directory: Path) -> list[Path]:
    return sorted(p for p in directory.glob("*.txt") if p.is_file())


def _print_score_lines(
    label: str,
    text: str,
    *,
    with_control: bool,
    tokenizer=None,
) -> None:
    """Score the same tokens on the official instance, and optionally the control."""
    tok = tokenizer or load_tokenizer()
    ids = tok(text, return_tensors="pt")["input_ids"]
    official = official_score_token_ids(ids, tokenizer=tok)
    print(format_score(label, official, instance=PUBLIC_INSTANCE))
    if with_control:
        control = official_score_token_ids(ids, tokenizer=tok, keys=control_keys())
        print(format_score(label, control, instance=CONTROL_INSTANCE))


def cmd_score(args: argparse.Namespace) -> int:
    path = args.path
    with_control = bool(args.control_shuffled_keys)
    tok = load_tokenizer(getattr(args, "model", None))
    if path and path != "-" and Path(path).is_dir():
        files = _txt_files_in(Path(path))
        if not files:
            print(f"no .txt files in {path}", file=sys.stderr)
            return 2
        for file_path in files:
            _print_score_lines(
                str(file_path),
                file_path.read_text(),
                with_control=with_control,
                tokenizer=tok,
            )
        return 0
    text = _read_input(path)
    _print_score_lines(path or "stdin", text, with_control=with_control, tokenizer=tok)
    return 0


def cmd_iterate(args: argparse.Namespace) -> int:
    if args.stop_on == STOP_INDICATE and not args.tables:
        print(
            "iterate --stop-on indicate needs --tables DIR "
            "(frozen indicate tables; not official score)",
            file=sys.stderr,
        )
        return 2
    text = _read_input(args.path)
    extra: dict | None = None
    if args.backend == "deepseek":
        key = deepseek_api_key()
        if not key:
            print(
                "iterate --backend deepseek needs DEEPSEEK_API_KEY or "
                f"{DEEPSEEK_KEY_FILE} (see {DEEPSEEK_KEY_FILE}.example; never argv)",
                file=sys.stderr,
            )
            return 2
        base_url = args.base_url or DEFAULT_BASE_URL
        model = args.model or DEFAULT_MODEL
        extra = {"thinking": {"type": "disabled"}}
        operator = "deepseek"
    elif args.backend == "qwen":
        key = dashscope_api_key()
        if not key:
            print(
                "iterate --backend qwen needs DASHSCOPE_API_KEY or "
                f"{DASHSCOPE_KEY_FILE} (see {DASHSCOPE_KEY_FILE}.example; never argv)",
                file=sys.stderr,
            )
            return 2
        base_url = (
            args.base_url
            if args.base_url != DEFAULT_BASE_URL
            else QWEN_BASE_URL
        )
        model = args.model if args.model != DEFAULT_MODEL else QWEN_MODEL
        operator = "qwen"
    else:
        print(f"unknown iterate backend: {args.backend}", file=sys.stderr)
        return 2

    def rewrite(current: str) -> str:
        return rewrite_once(
            current,
            via=args.via,
            chat=lambda prompt: chat_complete(
                prompt,
                api_key=key,
                model=model,
                base_url=base_url,
                timeout=args.timeout,
                extra=extra,
            ),
        )

    model_name = model
    indicate_fn = None
    if args.tables:
        tables = Path(args.tables)
        raw_path = tables / "tables.json" if tables.is_dir() else tables
        raw = json.loads(raw_path.read_text())
        if raw.get("used_keys") or raw.get("used_hash_iv") or raw.get("used_g_values"):
            print(
                "loaded indicator used keys / hash_iv / g-values",
                file=sys.stderr,
            )
            return 1
        ind_meta = load_tables_meta(tables)
        tok = load_tokenizer(ind_meta.model_name)

        def indicate_fn(current, _tables=tables, _t=tok):
            lr, _meta, used = score_text_from_tables(
                current, _tables, tokenizer=_t, score_mode="auto"
            )
            if used:
                raise RuntimeError("loaded indicator used keys / hash_iv / g")
            return lr

    try:
        run = run_iterate(
            text,
            rewrite=rewrite,
            operator=operator,
            model=model_name,
            via=args.via,
            max_passes=args.max_passes,
            mean_tol=args.mean_tol,
            min_unmasked_ngrams=args.min_unmasked_ngrams,
            indicate=indicate_fn,
            indicate_threshold=args.indicate_threshold,
            stop_on=args.stop_on,
        )
    except OperatorError as exc:
        print(f"iterate failed: {exc}", file=sys.stderr)
        return 1
    print(print_iterate_run(run))
    if args.out_dir:
        persist_iterate_run(run, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0 if run.met_stop else 3


def cmd_openings(args: argparse.Namespace) -> int:
    from text_watermark_tools.openings import (
        persist_openings,
        print_openings,
        run_openings,
        load_group,
    )
    from text_watermark_tools.probe import apply_overlap
    from text_watermark_tools.score import load_tokenizer as _tok

    tok = _tok(getattr(args, "model", None))
    test = load_twins(Path(args.test_dir), tokenizer=tok)
    extra = list(getattr(args, "extra_train", None) or [])
    all_dirs = [Path(args.pair_dir)] + [Path(p) for p in extra]
    groups = []
    for path in all_dirs:
        group = load_group(path, tok)
        kept, _, _ = apply_overlap(group.twins, test, mode="drop-from-train")
        groups.append(type(group)(group.name, kept))
    methods = [m.strip() for m in str(args.methods).split(",") if m.strip()]
    payload = run_openings(
        groups,
        test,
        methods=methods,
        fit_prefix=int(getattr(args, "fit_prefix", 4) or 0) or 4,
        position_bucket=int(getattr(args, "pos_bucket", 1)),
        include_first=bool(getattr(args, "include_first", False)),
        context_len=int(args.context_len),
        model_name=args.model,
        with_stem_curve=not bool(getattr(args, "skip_stem_curve", False)),
        curve_method=str(getattr(args, "curve_method", "postokbackoff") or "postokbackoff"),
    )
    if payload["used_keys"] or payload["used_hash_iv"] or payload["used_g_values"]:
        print("openings consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_openings(payload))
    if args.out_dir:
        persist_openings(payload, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_resample(args: argparse.Namespace) -> int:
    from text_watermark_tools.resample import PREMARK_DIR, LOGBOOK_PATH, EXPERIMENTS

    try:
        report = run_resample(
            skip_collect=bool(args.skip_collect),
            new_dir=Path(args.new_dir) if args.new_dir else None,
            previous_dir=Path(args.previous_dir) if args.previous_dir else None,
            premark_dir=Path(args.premark_dir) if args.premark_dir else PREMARK_DIR,
            logbook=Path(args.logbook) if args.logbook else LOGBOOK_PATH,
            experiments=EXPERIMENTS,
            date=args.date or None,
            pause_s=int(args.pause),
        )
    except FileNotFoundError as exc:
        print(f"resample failed: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"resample failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"resample date={report.date} n_collected={report.n_collected} "
        f"collected={report.collected} new_dir={report.new_dir} "
        f"logbook={report.logbook_path} used_keys=False"
    )
    for c in report.contrasts:
        print(
            f"contrast={c.name} n_pairs={c.n_pairs} "
            f"last-1={c.last1_wins}/{c.n_pairs} last-4={c.last4_wins}/{c.n_pairs} "
            f"used_keys={c.used_keys}"
        )
    return 0


def cmd_blind(args: argparse.Namespace) -> int:
    twins = load_twins(
        Path(args.pair_dir),
        tokenizer=load_tokenizer(getattr(args, "model", None)),
    )
    ev = leave_one_prompt_out(
        twins,
        context_len=args.context_len,
        alpha=args.alpha,
        backoff=bool(getattr(args, "backoff", False)),
        margin=float(getattr(args, "margin", 0.0)),
    )
    if ev.used_keys or ev.used_hash_iv or ev.used_g_values:
        print("blind model consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_blind_eval(ev))
    if args.out_dir:
        persist_blind_eval(ev, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0 if ev.accuracy > 0.5 else 3


def cmd_pair(args: argparse.Namespace) -> int:
    prompts = collect_prompts(Path(args.path))
    if bool(getattr(args, "control_only", False)):
        run = run_control_only(
            prompts,
            max_new_tokens=args.max_new_tokens,
            seed=args.seed,
            n_samples=int(args.n_samples),
            model_name=args.model,
        )
    else:
        run = run_pairs(
            prompts,
            max_new_tokens=args.max_new_tokens,
            seed=args.seed,
            also_control_keys=bool(args.also_control_keys),
            model_name=args.model,
            n_samples=int(args.n_samples),
        )
    print(print_pair_run(run))
    if args.out_dir:
        persist_pair_run(run, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_indicate_fit(args: argparse.Namespace) -> int:
    twins = load_twins(Path(args.pair_dir), tokenizer=load_tokenizer(args.model))
    method = str(getattr(args, "method", "counts") or "counts")
    if method == "hashpool":
        from text_watermark_tools.transfer import fit_hashpool_twins, persist_hashpool

        model = fit_hashpool_twins(
            twins,
            context_len=args.context_len,
            n_hashes=int(getattr(args, "n_hashes", 8)),
            n_buckets=int(getattr(args, "n_buckets", 256)),
            alpha=args.alpha,
        )
        if model.used_keys or model.used_hash_iv or model.used_g_values:
            print("hashpool fit consulted keys / hash_iv / g-values", file=sys.stderr)
            return 1
        path = persist_hashpool(
            model,
            Path(args.out_dir),
            model_name=args.model,
            pair_dir=str(args.pair_dir),
            n_train_prompts=len(twins),
        )
        print(
            f"wrote {path} instance={model.instance} "
            f"used_keys={model.used_keys} n_train_prompts={len(twins)} "
            f"context_len={model.context_len} n_hashes={model.n_hashes} "
            f"n_buckets={model.n_buckets}"
        )
        print(CAVEAT)
        return 0
    if method == "surface":
        from text_watermark_tools.transfer import (
            DEFAULT_SURFACE_CONTEXT,
            fit_surface_twins,
            persist_hashpool,
        )

        model = fit_surface_twins(
            twins,
            context_len=int(
                getattr(args, "surface_context_len", DEFAULT_SURFACE_CONTEXT)
                or DEFAULT_SURFACE_CONTEXT
            ),
            n_hashes=int(getattr(args, "n_hashes", 8)),
            n_buckets=int(getattr(args, "n_buckets", 256)),
            alpha=args.alpha,
        )
        if model.used_keys or model.used_hash_iv or model.used_g_values:
            print("surface fit consulted keys / hash_iv / g-values", file=sys.stderr)
            return 1
        path = persist_hashpool(
            model,
            Path(args.out_dir),
            model_name=args.model,
            pair_dir=str(args.pair_dir),
            n_train_prompts=len(twins),
        )
        print(
            f"wrote {path} instance={model.instance} "
            f"used_keys={model.used_keys} n_train_prompts={len(twins)} "
            f"context_len={model.context_len} alphabet={model.alphabet} "
            f"n_hashes={model.n_hashes} n_buckets={model.n_buckets}"
        )
        print(CAVEAT)
        return 0
    if method == "pivot":
        from text_watermark_tools.generate import _load_unmarked_model, generate_device
        from text_watermark_tools.pivot import (
            collect_choice_matrices,
            fit_pivot_from_vectors,
            parse_pivot_weights,
            persist_pivot,
            vectors_from_matrices,
        )

        weight = parse_pivot_weights(
            str(getattr(args, "pivot_weight", "uniform") or "uniform")
        )[0]
        lm = _load_unmarked_model(generate_device(), model_name=args.model)
        mats = collect_choice_matrices(twins, lm, prompt_context=False)
        vecs = vectors_from_matrices(mats, weight=weight)
        fit = fit_pivot_from_vectors(vecs, [t.stem for t in twins])
        if fit.used_keys or fit.used_hash_iv or fit.used_g_values:
            print("pivot fit consulted keys / hash_iv / g-values", file=sys.stderr)
            return 1
        path = persist_pivot(
            fit,
            Path(args.out_dir),
            model_name=args.model,
            pair_dir=str(args.pair_dir),
            n_train_prompts=len(twins),
            weight=weight,
            prompt_context=False,
        )
        print(
            f"wrote {path} instance=key-free-pivot-lda "
            f"used_keys={fit.used_keys} n_train_prompts={len(twins)} "
            f"weight={weight} prompt_context=False"
        )
        print(CAVEAT)
        return 0
    if method == "rankpath":
        from text_watermark_tools.generate import _load_unmarked_model, generate_device
        from text_watermark_tools.pivot import collect_choice_matrices
        from text_watermark_tools.rankpath import (
            fit_rankpath_from_symbols,
            persist_rankpath,
            symbols_from_matrices,
        )

        lm = _load_unmarked_model(generate_device(), model_name=args.model)
        mats = collect_choice_matrices(twins, lm, prompt_context=False)
        symbols = symbols_from_matrices(mats)
        model = fit_rankpath_from_symbols(
            symbols,
            [t.stem for t in twins],
            context_len=min(int(args.context_len), 3),
            position_bucket=int(getattr(args, "pos_bucket", 0) or 0),
        )
        if model.used_keys or model.used_hash_iv or model.used_g_values:
            print("rankpath fit consulted keys / hash_iv / g-values", file=sys.stderr)
            return 1
        path = persist_rankpath(
            model,
            Path(args.out_dir),
            model_name=args.model,
            pair_dir=str(args.pair_dir),
            n_train_prompts=len(twins),
            prompt_context=False,
        )
        print(
            f"wrote {path} instance=key-free-rankpath "
            f"used_keys={model.used_keys} n_train_prompts={len(twins)} "
            f"alphabet=5 prompt_context=False"
        )
        print(CAVEAT)
        return 0
    if method not in ("counts", "hard"):
        print(
            f"unknown --method {method}; choose counts, hashpool, surface, "
            f"pivot, or rankpath",
            file=sys.stderr,
        )
        return 2
    model = fit_indicator(
        twins,
        context_len=args.context_len,
        alpha=args.alpha,
        backoff=bool(args.backoff),
        position_bucket=int(getattr(args, "pos_bucket", 0) or 0),
    )
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        print("indicator fit consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    path = persist_indicator(
        model,
        Path(args.out_dir),
        model_name=args.model,
        pair_dir=str(args.pair_dir),
        n_train_prompts=len(twins),
    )
    print(
        f"wrote {path} instance={INDICATOR_INSTANCE} "
        f"used_keys={model.used_keys} n_train_prompts={len(twins)} "
        f"context_len={model.context_len}"
    )
    print(CAVEAT)
    return 0


def cmd_indicate_score(args: argparse.Namespace) -> int:
    from text_watermark_tools.transfer import SURFACE_KIND, peek_tables_kind

    tables = Path(args.tables)
    meta = load_tables_meta(tables)
    kind = peek_tables_kind(tables)
    text = _read_input(args.path)
    tok = None
    if kind != SURFACE_KIND:
        name = args.model or meta.model_name
        tok = load_tokenizer(name)
    try:
        lr, meta, used_keys = score_text_from_tables(
            text,
            tables,
            tokenizer=tok,
            score_mode=str(getattr(args, "score_mode", "auto") or "auto"),
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if used_keys:
        print("loaded indicator used keys / hash_iv / g-values", file=sys.stderr)
        return 1
    if kind == SURFACE_KIND:
        n_tokens = len(text.encode("utf-8"))
    else:
        assert tok is not None
        n_tokens = len(tok(text)["input_ids"])
    label = args.path or "stdin"
    threshold = getattr(args, "threshold", None)
    if threshold is None:
        threshold = meta.decision_threshold
    else:
        threshold = float(threshold)
    print(
        format_indicator(
            label,
            lr,
            n_tokens=n_tokens,
            used_keys=used_keys,
            instance=meta.instance,
            score_kind=meta.score_kind,
            threshold=threshold,
            decision_source=meta.decision_source if threshold is not None else "",
            n_used=meta.n_used,
            n_positions=meta.n_positions,
        )
    )
    return 0


def cmd_indicate_holdout(args: argparse.Namespace) -> int:
    twins = load_twins(Path(args.pair_dir), tokenizer=load_tokenizer(args.model))
    score_kind = str(getattr(args, "score_mode", "hard") or "hard")
    score_fn = None
    instance = INDICATOR_INSTANCE
    extra_rotate = {
        "hashpool": "rotate_hashpool",
        "hashtok": "rotate_hashtok",
        "hashtoklen": "rotate_hashtoklen",
        "hashtokbackoff": "rotate_hashtokbackoff",
        "hashtokbackoff2": "rotate_hashtokbackoff2",
        "hashtoklenbackoff": "rotate_hashtoklenbackoff",
        "hashtoklenbackoff2": "rotate_hashtoklenbackoff2",
        "hashvote": "rotate_hashvote",
        "hybrid": "rotate_hybrid",
        "hashmix": "rotate_hashmix",
        "surface": "rotate_surface",
        "poshits": "rotate_poshits",
        "postokhits": "rotate_postokhits",
        "postokbackoff": "rotate_postokbackoff",
        "postokbackoff2": "rotate_postokbackoff2",
        "poshitmass": "rotate_poshitmass",
    }
    if score_kind in extra_rotate:
        if not args.rotate:
            print(
                f"--score-mode {score_kind} needs --rotate "
                "(or use indicate fit --method hashpool and indicate score)",
                file=sys.stderr,
            )
            return 2
        from text_watermark_tools import probe as probe_mod

        rotator = getattr(probe_mod, extra_rotate[score_kind])
        kwargs = dict(
            twins=twins,
            context_len=args.context_len,
            model_name=args.model,
            margin=float(args.margin),
        )
        if score_kind == "surface":
            kwargs["context_len"] = int(
                getattr(args, "surface_context_len", 8) or 8
            )
        if score_kind in (
            "poshits",
            "poshitmass",
            "postokhits",
            "postokbackoff",
            "postokbackoff2",
        ):
            kwargs["position_bucket"] = int(getattr(args, "pos_bucket", 16))
        elif score_kind != "hard":
            kwargs["n_hashes"] = int(getattr(args, "n_hashes", 8))
            kwargs["n_buckets"] = int(getattr(args, "n_buckets", 256))
        ev = rotator(**kwargs)
    elif score_kind != "hard":
        from text_watermark_tools.transfer import COUNT_SPECS, score_sequence

        if score_kind not in COUNT_SPECS:
            print(
                f"unknown --score-mode {score_kind}; "
                f"choose hard, hashpool, hashtok, hashtoklen, hashtokbackoff, "
                f"hashtokbackoff2, hashtoklenbackoff, hashtoklenbackoff2, "
                f"hashvote, hybrid, surface, "
                f"poshits, poshitmass, postokhits, postokbackoff, "
                f"postokbackoff2, or one of "
                f"{sorted(COUNT_SPECS)}",
                file=sys.stderr,
            )
            return 2
        spec = COUNT_SPECS[score_kind]
        instance = spec.instance
        score_fn = lambda ids, model, s=spec: score_sequence(ids, model, s)
        if args.rotate:
            ev = rotate_holdout(
                twins,
                context_len=args.context_len,
                alpha=args.alpha,
                backoff=bool(args.backoff),
                model_name=args.model,
                margin=float(args.margin),
                score_fn=score_fn,
                instance=instance,
                score_kind=score_kind,
            )
        else:
            if not args.hold or len(args.hold) < 2:
                print(
                    "indicate holdout needs --hold STEM STEM or --rotate",
                    file=sys.stderr,
                )
                return 2
            ev = holdout_single_text(
                twins,
                args.hold,
                context_len=args.context_len,
                alpha=args.alpha,
                backoff=bool(args.backoff),
                model_name=args.model,
                margin=float(args.margin),
            )
    elif args.rotate:
        ev = rotate_holdout(
            twins,
            context_len=args.context_len,
            alpha=args.alpha,
            backoff=bool(args.backoff),
            model_name=args.model,
            margin=float(args.margin),
            score_fn=score_fn,
            instance=instance,
            score_kind=score_kind,
        )
    else:
        if not args.hold or len(args.hold) < 2:
            print("indicate holdout needs --hold STEM STEM or --rotate", file=sys.stderr)
            return 2
        ev = holdout_single_text(
            twins,
            args.hold,
            context_len=args.context_len,
            alpha=args.alpha,
            backoff=bool(args.backoff),
            model_name=args.model,
            margin=float(args.margin),
        )
    if ev.used_keys or ev.used_hash_iv or ev.used_g_values:
        print("indicator holdout consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_holdout(ev))
    if args.out_dir:
        persist_holdout(ev, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_probe(args: argparse.Namespace) -> int:
    twins = load_twins(
        Path(args.pair_dir),
        tokenizer=load_tokenizer(getattr(args, "model", None)),
    )
    max_draws = int(getattr(args, "max_draws", 0) or 0)
    if max_draws > 0:
        twins = clip_twins(twins, max_draws)
    methods = None
    if args.methods:
        methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    with_coverage = bool(getattr(args, "coverage", False))
    if with_coverage and methods is None:
        methods = []
    if getattr(args, "test_dir", ""):
        test_twins = load_twins(
            Path(args.test_dir),
            tokenizer=load_tokenizer(getattr(args, "model", None)),
        )
        if max_draws > 0:
            test_twins = clip_twins(test_twins, max_draws)
        extra_dirs = list(getattr(args, "extra_train", None) or [])
        tok = load_tokenizer(getattr(args, "model", None))
        for extra in extra_dirs:
            more = load_twins(Path(extra), tokenizer=tok)
            if max_draws > 0:
                more = clip_twins(more, max_draws)
            twins = list(twins) + list(more)
        train_label = str(args.pair_dir)
        if extra_dirs:
            train_label = train_label + "+" + "+".join(str(p) for p in extra_dirs)
        run = run_transfer(
            twins,
            test_twins,
            train_dir=train_label,
            test_dir=str(args.test_dir),
            model_name=args.model,
            context_len=args.context_len,
            methods=methods,
            overlap_mode=str(getattr(args, "overlap", "drop-from-train")),
            n_hashes=int(args.n_hashes),
            n_buckets=int(args.n_buckets),
            nested=not bool(getattr(args, "skip_nested", False)),
            shuffle_labels=bool(getattr(args, "shuffle_labels", False)),
            shuffle_seed=int(getattr(args, "shuffle_seed", 0)),
            surface_context_len=int(
                getattr(args, "surface_context_len", 8) or 8
            ),
            prefix_lens=_parse_prefix_arg(getattr(args, "prefix_lens", "")),
            windows=_parse_windows_arg(getattr(args, "windows", "")),
            fit_prefix=int(getattr(args, "fit_prefix", 0) or 0) or None,
            position_bucket=int(getattr(args, "pos_bucket", 16)),
            include_first=bool(getattr(args, "include_first", False)),
            prompt_context=bool(getattr(args, "prompt_context", False)),
            with_pivot=bool(getattr(args, "pivot", False))
            or bool(getattr(args, "cascade", "")),
            pivot_weights=str(getattr(args, "pivot_weight", "uniform") or "uniform"),
            cascade=str(getattr(args, "cascade", "") or ""),
            with_rankpath=bool(getattr(args, "rankpath", False)),
            cascade_fallback=str(getattr(args, "cascade_fallback", "pivot") or "pivot"),
            rankpath_full=bool(getattr(args, "rankpath_full", False)),
            rankpath_pos_bucket=(
                int(args.rankpath_pos_bucket)
                if getattr(args, "rankpath_pos_bucket", None) is not None
                else None
            ),
            cascade_rankpath_end=(
                int(args.cascade_rankpath_end)
                if getattr(args, "cascade_rankpath_end", None)
                else None
            ),
            cascade_when=str(getattr(args, "cascade_when", "coverage") or "coverage"),
            with_snaprate=bool(getattr(args, "snaprate", False)),
        )
        if run.used_keys or run.used_hash_iv or run.used_g_values:
            print("transfer consulted keys / hash_iv / g-values", file=sys.stderr)
            return 1
        print(print_transfer(run))
        if args.out_dir:
            persist_transfer(run, Path(args.out_dir))
            print(f"wrote {args.out_dir}")
        return 0
    run = run_probe(
        twins,
        pair_dir=str(args.pair_dir),
        model_name=args.model,
        context_len=args.context_len,
        methods=methods,
        with_hashpool=not bool(args.skip_hashpool),
        n_hashes=int(args.n_hashes),
        n_buckets=int(args.n_buckets),
        surface_context_len=int(getattr(args, "surface_context_len", 8) or 8),
        max_draws=max_draws if max_draws > 0 else None,
        prefix_lens=_parse_prefix_arg(getattr(args, "prefix_lens", "")),
        windows=_parse_windows_arg(getattr(args, "windows", "")),
        fit_prefix=int(getattr(args, "fit_prefix", 0) or 0) or None,
        position_bucket=int(getattr(args, "pos_bucket", 16)),
        with_coverage=with_coverage,
        include_first=bool(getattr(args, "include_first", False)),
        prompt_context=bool(getattr(args, "prompt_context", False)),
        with_pivot=bool(args.pivot) or bool(getattr(args, "cascade", "")),
        pivot_weights=str(getattr(args, "pivot_weight", "uniform") or "uniform"),
        cascade=str(getattr(args, "cascade", "") or ""),
        with_rankpath=bool(getattr(args, "rankpath", False)),
        cascade_fallback=str(getattr(args, "cascade_fallback", "pivot") or "pivot"),
        rankpath_full=bool(getattr(args, "rankpath_full", False)),
        rankpath_pos_bucket=(
            int(args.rankpath_pos_bucket)
            if getattr(args, "rankpath_pos_bucket", None) is not None
            else None
        ),
        cascade_rankpath_end=(
            int(args.cascade_rankpath_end)
            if getattr(args, "cascade_rankpath_end", None)
            else None
        ),
        cascade_when=str(getattr(args, "cascade_when", "coverage") or "coverage"),
        with_snaprate=bool(getattr(args, "snaprate", False)),
    )
    if run.used_keys or run.used_hash_iv or run.used_g_values:
        print("probe consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_probe(run))
    if args.out_dir:
        persist_probe(run, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_learn(args: argparse.Namespace) -> int:
    train_tok = load_tokenizer(getattr(args, "model", None))
    twins = load_twins(Path(args.pair_dir), tokenizer=train_tok)
    max_draws = int(getattr(args, "max_draws", 0) or 0)
    if max_draws > 0:
        twins = clip_twins(twins, max_draws)
    archs = None
    if args.archs:
        archs = [a.strip() for a in args.archs.split(",") if a.strip()]
    spec = spec_from_args(
        context_len=int(args.context_len),
        pos_bucket=int(getattr(args, "pos_bucket", 1) or 1),
        include_first=bool(getattr(args, "include_first", False)),
        prompt_context=bool(getattr(args, "prompt_context", False)),
        n_hashes=int(args.n_hashes),
        n_buckets=int(args.n_buckets),
        seed=int(getattr(args, "seed", 20260831)),
        epochs=int(getattr(args, "epochs", 40)),
    )
    if getattr(args, "test_dir", ""):
        test_name = getattr(args, "test_model", "") or args.model
        test_tok = load_tokenizer(test_name)
        test_twins = load_twins(Path(args.test_dir), tokenizer=test_tok)
        if max_draws > 0:
            test_twins = clip_twins(test_twins, max_draws)
        run = run_learn_transfer(
            twins,
            test_twins,
            train_dir=str(args.pair_dir),
            test_dir=str(args.test_dir),
            model_name=args.model,
            archs=archs,
            spec=spec,
            fit_prefix=int(getattr(args, "fit_prefix", 0) or 0) or None,
            overlap_mode=str(getattr(args, "overlap", "drop-from-train")),
            nested=not bool(getattr(args, "skip_nested", False)),
            shuffle_labels=bool(getattr(args, "shuffle_labels", False)),
            shuffle_seed=int(getattr(args, "shuffle_seed", 0)),
            tokenizer=train_tok,
            score_tokenizer=test_tok,
        )
        if run.used_keys or run.used_hash_iv or run.used_g_values:
            print("learn transfer consulted keys / hash_iv / g-values", file=sys.stderr)
            return 1
        print(print_learn_transfer(run))
        if args.out_dir:
            persist_learn_transfer(run, Path(args.out_dir))
            print(f"wrote {args.out_dir}")
        return 0
    run = run_learn(
        twins,
        pair_dir=str(args.pair_dir),
        model_name=args.model,
        archs=archs,
        spec=spec,
        fit_prefix=int(getattr(args, "fit_prefix", 0) or 0) or None,
        max_draws=max_draws if max_draws > 0 else None,
        tokenizer=train_tok,
    )
    if run.used_keys or run.used_hash_iv or run.used_g_values:
        print("learn consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_learn(run))
    if args.out_dir:
        persist_learn(run, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_contrast(args: argparse.Namespace) -> int:
    tok = load_tokenizer(getattr(args, "model", None))
    train = load_twins(Path(args.pair_dir), tokenizer=tok)
    test = load_twins(Path(args.test_dir), tokenizer=tok)
    control_dir = Path(getattr(args, "control_dir", "") or args.test_dir)
    draws = load_control_draws(control_dir, tokenizer=tok)
    if not draws:
        print(f"no *-control-gen.txt in {control_dir}", file=sys.stderr)
        return 2
    methods = None
    if args.methods:
        methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    run = run_instance_contrast(
        train,
        test,
        draws,
        train_dir=str(args.pair_dir),
        test_dir=str(args.test_dir),
        control_dir=str(control_dir),
        model_name=args.model,
        context_len=int(args.context_len),
        fit_prefix=int(getattr(args, "fit_prefix", 0) or 0) or None,
        position_bucket=int(getattr(args, "pos_bucket", 1)),
        methods=methods or ("hits", "poshits", "hashpool"),
        rankpath_pos_bucket=(
            int(args.rankpath_pos_bucket)
            if getattr(args, "rankpath_pos_bucket", None) is not None
            else None
        ),
        rankpath_end=int(getattr(args, "rankpath_end", 0) or 0) or None,
        prompt_context=bool(getattr(args, "prompt_context", False)),
    )
    if run.used_keys or run.used_hash_iv or run.used_g_values:
        print("contrast consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_contrast(run))
    if args.out_dir:
        persist_contrast(run, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_scrub(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if path.is_dir():
        files = sorted(
            p
            for p in path.glob("*-marked*.txt")
            if p.is_file() and "unmarked" not in p.name
        )
        if not files:
            print(f"no *-marked*.txt files in {path}", file=sys.stderr)
            return 2
    elif path.is_file():
        files = [path]
    else:
        print(f"not a file or directory: {path}", file=sys.stderr)
        return 2
    run = run_scrub_files(files, model_name=args.model, top_k=int(args.top_k))
    if run.used_keys_for_snap or run.used_hash_iv or run.used_g_values:
        print("scrub snap consulted keys / hash_iv / g-values", file=sys.stderr)
        return 1
    print(print_scrub(run))
    if args.out_dir:
        persist_scrub(run, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def cmd_experiment(args: argparse.Namespace) -> int:
    result = run_known_mark_experiment(
        max_new_tokens=args.max_new_tokens,
        n_positions=args.n_positions,
        samples_per_position=args.samples_per_position,
        seed=args.seed,
    )
    report = print_result(result)
    print(report)
    if args.out_dir:
        persist_result(result, Path(args.out_dir))
        print(f"wrote {args.out_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="text-mark-laboratory",
        description=(
            "Official SynthID-Text scores (public reference keys), a "
            "known-mark mixin experiment, a key-free single-text "
            "indicator, and key-free probe/scrub attacks. Not a Claude detector."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_score = sub.add_parser(
        "score",
        help="Official Mean / Weighted Mean on file, directory of .txt, or stdin",
    )
    p_score.add_argument(
        "path",
        nargs="?",
        help="Text file, directory of .txt files, or omit for stdin",
    )
    p_score.add_argument(
        "--control-shuffled-keys",
        action="store_true",
        help=(
            "Also score the same tokens against a dummy/shuffled keyset "
            "(same-config contrast, not a second vendor instance)"
        ),
    )
    p_score.add_argument(
        "--model",
        default="gpt2",
        help="Tokenizer/model id used at generation (must match the sampler)",
    )
    p_score.set_defaults(func=cmd_score)

    p_exp = sub.add_parser(
        "experiment",
        help="Generate marked text, fit a key-free surrogate, rewrite, official-score",
    )
    p_exp.add_argument("--max-new-tokens", type=int, default=320)
    p_exp.add_argument(
        "--n-positions",
        type=int,
        default=0,
        help="Extra marked generate() queries; 0 = none (source tokens are enough)",
    )
    p_exp.add_argument("--samples-per-position", type=int, default=1)
    p_exp.add_argument("--seed", type=int, default=0)
    p_exp.add_argument(
        "--out-dir",
        type=str,
        default="",
        help="If set, write source.txt, rewrite.txt, results.json, results.md",
    )
    p_exp.set_defaults(func=cmd_experiment)

    p_pair = sub.add_parser(
        "pair",
        help=(
            "Same prompt: score the source text, generate unmarked and "
            "mixin-marked twins, official-score both"
        ),
    )
    p_pair.add_argument(
        "path",
        help="Prompt .txt file, or directory of .txt prompts",
    )
    p_pair.add_argument("--max-new-tokens", type=int, default=128)
    p_pair.add_argument("--seed", type=int, default=0)
    p_pair.add_argument(
        "--n-samples",
        type=int,
        default=1,
        help="Independent mixin on/off draws per prompt (leave-one-prompt-out keeps them together)",
    )
    p_pair.add_argument(
        "--model",
        default="gpt2",
        help="HF causal LM id (default gpt2). Qwen2-1.5B-Instruct is the local non-GPT-2 path.",
    )
    p_pair.add_argument(
        "--also-control-keys",
        action="store_true",
        help=(
            "Also sample a third twin with control-shuffled-30 "
            "(written as *-control-gen.txt, not picked up by blind)"
        ),
    )
    p_pair.add_argument(
        "--control-only",
        action="store_true",
        help=(
            "Sample only control-shuffled-30 twins (no *-marked.txt). "
            "Use with --n-samples for a key-free instance contrast."
        ),
    )
    p_pair.add_argument(
        "--out-dir",
        type=str,
        default="",
        help="If set, write *-prompt.txt, *-marked.txt, *-unmarked-gen.txt, results",
    )
    p_pair.set_defaults(func=cmd_pair)

    p_blind = sub.add_parser(
        "blind",
        help=(
            "Key-free leave-one-prompt-out on pair twins "
            "(no keys / hash_iv / g-values)"
        ),
    )
    p_blind.add_argument(
        "pair_dir",
        help="Directory with *-marked.txt and *-unmarked-gen.txt",
    )
    p_blind.add_argument(
        "--context-len",
        type=int,
        default=DEFAULT_CONTEXT_LEN,
        help="Last-k tokens as context (fit knob, not watermark ngram_len)",
    )
    p_blind.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    p_blind.add_argument(
        "--backoff",
        action="store_true",
        help="If a k-gram context is unseen, try k-1 … 1 before the unigram",
    )
    p_blind.add_argument(
        "--margin",
        type=float,
        default=0.0,
        help=(
            "Count a hit if marked_lr + margin >= unmarked_lr "
            "(0 = strict; 0.02 is a soft bar)"
        ),
    )
    p_blind.add_argument(
        "--model",
        default="gpt2",
        help="Tokenizer id used when the twins were generated",
    )
    p_blind.add_argument(
        "--out-dir",
        type=str,
        default="",
        help="If set, write results.json and results.md",
    )
    p_blind.set_defaults(func=cmd_blind)

    p_ind = sub.add_parser(
        "indicate",
        help=(
            "Key-free single-text indicator: fit count tables, score one file, "
            "or hold out prompts (not detector_mean, not Claude)"
        ),
        description=(
            "Key-free indicator from token counts only. Not detector_mean. "
            "Not Claude. Not Anthropic. ≈0 is not “human” and not "
            "“Claude has no mark”."
        ),
    )
    ind = p_ind.add_subparsers(dest="indicate_cmd", required=True)

    p_fit = ind.add_parser("fit", help="Fit and persist tables from a twin directory")
    p_fit.add_argument("pair_dir", help="Directory with *-marked.txt / *-unmarked-gen.txt")
    p_fit.add_argument("--out-dir", required=True, help="Where to write tables.json")
    p_fit.add_argument("--model", default="gpt2")
    p_fit.add_argument("--context-len", type=int, default=4)
    p_fit.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    p_fit.add_argument("--backoff", action="store_true")
    p_fit.add_argument(
        "--method",
        default="counts",
        choices=("counts", "hashpool", "surface", "pivot", "rankpath"),
        help=(
            "counts = exact n-gram tables (default); "
            "hashpool = random token-context buckets; "
            "surface = UTF-8 byte hashpool, no tokenizer; "
            "pivot = unmarked-LM choice geometry (loads GPT-2; "
            "cannot use prompt context on a lone file); "
            "rankpath = unmarked-LM rank-symbol tables (loads GPT-2; "
            "scores novel openings without token identity)"
        ),
    )
    p_fit.add_argument(
        "--pos-bucket",
        type=int,
        default=0,
        help=(
            "If >0, prepend i//N to last-k context when fitting count "
            "tables (poshits). Not a watermark key. Default 0."
        ),
    )
    p_fit.add_argument("--n-hashes", type=int, default=8)
    p_fit.add_argument("--n-buckets", type=int, default=256)
    p_fit.add_argument(
        "--surface-context-len",
        type=int,
        default=8,
        help="Byte context length for --method surface (default 8)",
    )
    p_fit.set_defaults(func=cmd_indicate_fit)

    p_is = ind.add_parser(
        "score",
        help="Score one text against frozen tables (no twin at inference)",
    )
    p_is.add_argument("path", nargs="?", help="Text file, or omit for stdin")
    p_is.add_argument(
        "--tables",
        required=True,
        help="Directory with tables.json from indicate fit",
    )
    p_is.add_argument(
        "--model",
        default="",
        help="Tokenizer id (default: the id stored in tables.json)",
    )
    p_is.add_argument(
        "--score-mode",
        default="auto",
        help=(
            "How to read count tables: auto (hashpool tables → hashpool, "
            "bucketed count tables → poshits, else hard), or "
            "hard/hits/tokhits/tokbackoff/tokbackoff2/poshits/postokhits/"
            "postokbackoff/postokbackoff2/poshitmass/gated/unigram/… "
            "Hashpool tables ignore count modes except hashtok (skip a hash "
            "unless the observed next token appeared in that bucket). "
            "tokhits skips Laplace scores for a next token never seen under "
            "that context. tokbackoff shrinks last-k until an observed next "
            "token hits. tokbackoff2 stops at last-2."
        ),
    )
    p_is.add_argument(
        "--threshold",
        type=float,
        default=None,
        help=(
            "Optional decision threshold. If omitted, use decision_threshold "
            "stored in tables.json when present. Not a universal detector."
        ),
    )
    p_is.set_defaults(func=cmd_indicate_score)

    p_ih = ind.add_parser(
        "holdout",
        help=(
            "Leave-one-out / hold stems: train count tables on the other "
            "twins, score each held-out file alone (not the Claude pre-mark pile)"
        ),
    )
    p_ih.add_argument("pair_dir")
    p_ih.add_argument(
        "--hold",
        nargs="+",
        default=None,
        help="Prompt stems to hold out (at least two; omit if --rotate)",
    )
    p_ih.add_argument(
        "--rotate",
        action="store_true",
        help=(
            "Leave-one-out: fit tables on all twin prompts except one, "
            "score that held-out prompt's files alone (rotate over every stem)"
        ),
    )
    p_ih.add_argument("--model", default="gpt2")
    p_ih.add_argument("--context-len", type=int, default=4)
    p_ih.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    p_ih.add_argument("--backoff", action="store_true")
    p_ih.add_argument(
        "--margin",
        type=float,
        default=0.0,
        help=(
            "Count a hit if marked_lr + margin >= unmarked_lr; "
            "one-file sign uses lr > -margin (0 = strict)"
        ),
    )
    p_ih.add_argument(
        "--score-mode",
        default="hard",
        help=(
            "How to read the count tables: hard (default), unigram, backoff, "
            "interpolate, hits, tokhits, tokbackoff, tokbackoff2, gated, "
            "shrinkage, mix, hashpool, hashtok, hashtoklen, hashtokbackoff, "
            "hashtokbackoff2, hashtoklenbackoff, hashtoklenbackoff2, "
            "hashvote, hybrid, surface, "
            "poshits, postokhits, postokbackoff, postokbackoff2, poshitmass. "
            "Hashpool/surface/poshits/postokhits/postokbackoff/"
            "postokbackoff2/hashtok/hashtoklen/hashtokbackoff/"
            "hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2 modes "
            "need --rotate. Still key-free."
        ),
    )
    p_ih.add_argument(
        "--pos-bucket",
        type=int,
        default=16,
        help="Token-position bucket size for --score-mode poshits/postokhits/postokbackoff/poshitmass (default 16)",
    )
    p_ih.add_argument("--n-hashes", type=int, default=8)
    p_ih.add_argument("--n-buckets", type=int, default=256)
    p_ih.add_argument(
        "--surface-context-len",
        type=int,
        default=8,
        help="Byte context length for --score-mode surface",
    )
    p_ih.add_argument("--out-dir", default="")
    p_ih.set_defaults(func=cmd_indicate_holdout)

    p_probe = sub.add_parser(
        "probe",
        help=(
            "Compare key-free scorers on pair twins (AUC, permutation, "
            "prompt-grain wins). Optional unmarked-LM pivot. Not detector_mean."
        ),
        description=(
            "Leave-one-prompt-out comparison of key-free scorers. "
            "Not detector_mean. Not Claude. Not key recovery."
        ),
    )
    p_probe.add_argument("pair_dir", help="Directory with *-marked.txt / *-unmarked-gen.txt")
    p_probe.add_argument("--model", default="gpt2")
    p_probe.add_argument("--context-len", type=int, default=4)
    p_probe.add_argument(
        "--methods",
        default="",
        help=(
            "Comma-separated methods: count specs plus hashpool, hashtok, "
            "hashtoklen, hashtokbackoff, hashtokbackoff2, hashtoklenbackoff, "
            "hashtoklenbackoff2, hashvote, hybrid, hashmix, "
            "surface, stack, logit, poshits, postokhits, "
            "postokbackoff, postokbackoff2, poshitmass, pospool, "
            "first, tokhits, tokbackoff, tokbackoff2, rankpath, rankuni, "
            "rankhits, snapleave, snapupset, snapmiss"
        ),
    )
    p_probe.add_argument(
        "--skip-hashpool",
        action="store_true",
        help="Do not fit the random-hash context pool",
    )
    p_probe.add_argument(
        "--pivot",
        action="store_true",
        help="Also score unmarked-LM choice geometry (loads GPT-2, slower)",
    )
    p_probe.add_argument(
        "--pivot-weight",
        default="uniform",
        help=(
            "How to pool unmarked-LM token features: uniform, entropy "
            "(weight near-ties), in_topk. Comma-separated for several."
        ),
    )
    p_probe.add_argument(
        "--cascade",
        default="",
        help=(
            "Isolated-file protocol: use this count or occupancy-free "
            "hashed method when the --cascade-when rule fires, else the "
            "--cascade-fallback reader. Example: postokbackoff or "
            "hashtoklen. Hashed readers skip empty-cell Laplace. Loads GPT-2."
        ),
    )
    p_probe.add_argument(
        "--cascade-fallback",
        default="pivot",
        help=(
            "When --cascade yields: pivot (LDA), rankpath (tokbackoff "
            "on unmarked-LM rank symbols), or rankuni (rank-symbol unigram). "
            "Rank-path fallback uses the opening path, not --rankpath-full. "
            "Default pivot."
        ),
    )
    p_probe.add_argument(
        "--cascade-rankpath-end",
        type=int,
        default=0,
        help=(
            "First N rank symbols for --cascade-fallback rankpath/rankuni. "
            "0 (default) is the --fit-prefix opening. 4 is the unbucketed "
            "prefix-4 reader. Never the full 128-token path. Still no keys."
        ),
    )
    p_probe.add_argument(
        "--cascade-when",
        default="coverage",
        help=(
            "When the count channel yields to --cascade-fallback: coverage "
            "(n_used>0, default) or positive (count lr>0). positive also "
            "sends covered-negative files to the rank-path reader. Still "
            "no keys. Mixed AUC is not a detector."
        ),
    )
    p_probe.add_argument(
        "--rankpath",
        action="store_true",
        help=(
            "Score unmarked-LM rank-symbol tables (rankpath + rankuni). "
            "Loads GPT-2. Token identity is not used. Still no keys."
        ),
    )
    p_probe.add_argument(
        "--snaprate",
        action="store_true",
        help=(
            "Score table-free unmarked-LM snap rates: snapleave (not argmax), "
            "snapupset (in-topk not argmax), snapmiss (missed top-k, negative "
            "control). No twin tables. Loads GPT-2. Still no keys."
        ),
    )
    p_probe.add_argument(
        "--rankpath-full",
        action="store_true",
        help=(
            "Collect rank symbols from the unclipped file even when "
            "--fit-prefix clips count tables. Prefix and window scores "
            "are matched slices of that unclipped path (choice-matrix "
            "rows = generated tokens 1… without prompt context). Still "
            "no keys."
        ),
    )
    p_probe.add_argument(
        "--rankpath-pos-bucket",
        type=int,
        default=None,
        help=(
            "Position bucket for rank-symbol tables. Default: same as "
            "--pos-bucket. 0 is unbucketed (use this for full-file "
            "rankpath). Not a watermark key."
        ),
    )
    p_probe.add_argument("--n-hashes", type=int, default=8)
    p_probe.add_argument("--n-buckets", type=int, default=256)
    p_probe.add_argument(
        "--surface-context-len",
        type=int,
        default=8,
        help="Byte context length for the surface hashpool (default 8)",
    )
    p_probe.add_argument(
        "--test-dir",
        default="",
        help=(
            "If set, fit on pair_dir and score this second twin directory "
            "(cross-corpus transfer; not leave-one-prompt-out)"
        ),
    )
    p_probe.add_argument(
        "--extra-train",
        action="append",
        default=[],
        help=(
            "Additional train twin directories for --test-dir transfer "
            "(same idea as openings --extra-train)"
        ),
    )
    p_probe.add_argument(
        "--overlap",
        default="drop-from-train",
        choices=("drop-from-train", "drop-from-test", "keep"),
        help=(
            "Shared prompt stems: drop-from-train keeps the test set "
            "(default); drop-from-test keeps training"
        ),
    )
    p_probe.add_argument(
        "--skip-nested",
        action="store_true",
        help="Skip leave-one-prompt-out thresholds on the training stems",
    )
    p_probe.add_argument(
        "--shuffle-labels",
        action="store_true",
        help="Negative control: shuffle train marked/unmarked labels per stem",
    )
    p_probe.add_argument("--shuffle-seed", type=int, default=0)
    p_probe.add_argument(
        "--max-draws",
        type=int,
        default=0,
        help=(
            "If >0, keep only the first N marked/unmarked draws per stem "
            "(draw-count ablation on a multi-draw pair directory)"
        ),
    )
    p_probe.add_argument(
        "--prefix-lens",
        default="",
        help=(
            "Comma-separated token (or character, for surface) prefixes to "
            "score as isolated-file curves, e.g. 16,32,64,96,128"
        ),
    )
    p_probe.add_argument(
        "--windows",
        default="",
        help=(
            "Comma-separated half-open token windows to score independently, "
            "e.g. 0:16,16:32,32:64,64:128. Unlike --prefix-lens, later "
            "windows do not include earlier tokens."
        ),
    )
    p_probe.add_argument(
        "--fit-prefix",
        type=int,
        default=0,
        help=(
            "If >0, clip every draw to the first N tokens before fit and "
            "score (matched prefix protocol, not fit-full/score-prefix)"
        ),
    )
    p_probe.add_argument(
        "--pos-bucket",
        type=int,
        default=16,
        help=(
            "Token-position bucket size for poshits/poshitmass/pospool. "
            "Prepends i//N to the last-4 context so early 4-grams do not "
            "share counts with the tail. 0 is unbucketed (same tables as "
            "hits/tokhits). Not a watermark key. Default 16."
        ),
    )
    p_probe.add_argument(
        "--include-first",
        action="store_true",
        help=(
            "Also fit and score generated token 0 as a first-token unigram "
            "(empty last-k). Default skip matches the published tables. "
            "Not a watermark key."
        ),
    )
    p_probe.add_argument(
        "--prompt-context",
        action="store_true",
        help=(
            "Use *-prompt.txt token ids as last-k context only, so token 0 "
            "sees the prompt the way the mixin does. Isolated indicate score "
            "of a lone file cannot reconstruct that prompt."
        ),
    )
    p_probe.add_argument(
        "--coverage",
        action="store_true",
        help=(
            "Leave-one-prompt-out share of last-k contexts seen on both "
            "training sides, by token index and window. Explains why the "
            "key-free 4-gram reader is front-loaded. Unbucketed; uses full "
            "sequences even with --fit-prefix. With no --methods, coverage "
            "only (no scorers)."
        ),
    )
    p_probe.add_argument("--out-dir", default="")
    p_probe.set_defaults(func=cmd_probe)

    p_learn = sub.add_parser(
        "learn",
        help=(
            "Key-free learned scorers (hashed logistic, token MLP, "
            "character CNN) on pair twins. Not detector_mean, not Claude, "
            "not key recovery."
        ),
        description=(
            "Train tiny key-free classifiers on matched twins and evaluate "
            "leave-one-prompt-out or train/test transfer. Same grains as "
            "probe. A neural net is not a universal detector. Not SynthID "
            "key recovery. Do not train this on the Claude pre-mark pile "
            "alone."
        ),
    )
    p_learn.add_argument("pair_dir", help="Directory with *-marked.txt / *-unmarked-gen.txt")
    p_learn.add_argument("--model", default="gpt2")
    p_learn.add_argument(
        "--test-model",
        default="",
        help="Tokenizer for --test-dir (default: --model). Use Qwen id for Qwen twins.",
    )
    p_learn.add_argument("--context-len", type=int, default=4)
    p_learn.add_argument(
        "--archs",
        default="hashlog,tokmlp,charcnn",
        help="Comma-separated: hashlog, tokmlp, charcnn",
    )
    p_learn.add_argument("--n-hashes", type=int, default=4)
    p_learn.add_argument("--n-buckets", type=int, default=64)
    p_learn.add_argument("--seed", type=int, default=20260831)
    p_learn.add_argument(
        "--epochs",
        type=int,
        default=40,
        help="Adam epochs for tokmlp and charcnn (hashlog uses ridge IRLS)",
    )
    p_learn.add_argument(
        "--test-dir",
        default="",
        help="If set, fit on pair_dir and score this second twin directory",
    )
    p_learn.add_argument(
        "--overlap",
        default="drop-from-train",
        choices=("drop-from-train", "drop-from-test", "keep"),
    )
    p_learn.add_argument("--skip-nested", action="store_true")
    p_learn.add_argument("--shuffle-labels", action="store_true")
    p_learn.add_argument("--shuffle-seed", type=int, default=0)
    p_learn.add_argument("--max-draws", type=int, default=0)
    p_learn.add_argument(
        "--fit-prefix",
        type=int,
        default=0,
        help="If >0, clip every draw to the first N tokens before fit and score",
    )
    p_learn.add_argument(
        "--pos-bucket",
        type=int,
        default=1,
        help="Position namespace for hashlog (same meaning as probe poshits)",
    )
    p_learn.add_argument("--include-first", action="store_true")
    p_learn.add_argument("--prompt-context", action="store_true")
    p_learn.add_argument("--out-dir", default="")
    p_learn.set_defaults(func=cmd_learn)

    p_contrast = sub.add_parser(
        "contrast",
        help=(
            "Key-free instance contrast: fit public marked/unmarked tables, "
            "score control-shuffled-30 twins. Not key recovery."
        ),
        description=(
            "Fit on public-key twins. Score a third pile sampled with "
            "control-shuffled-30. If control looks unmarked, the key-free "
            "reader is instance-specific without keys. If it looks marked, "
            "the reader is detecting tournament sampling. Not Claude."
        ),
    )
    p_contrast.add_argument("pair_dir", help="Public-key train twins")
    p_contrast.add_argument("--test-dir", required=True, help="Public-key test twins")
    p_contrast.add_argument(
        "--control-dir",
        default="",
        help="Directory with *-control-gen.txt (default: --test-dir)",
    )
    p_contrast.add_argument("--model", default="gpt2")
    p_contrast.add_argument("--context-len", type=int, default=4)
    p_contrast.add_argument("--methods", default="hits,poshits,hashpool",
        help=(
            "Comma-separated: hits, tokhits, tokbackoff, tokbackoff2, "
            "poshits, postokhits, postokbackoff, postokbackoff2, hashpool, "
            "hashtok, hashtoklen, rankpath, rankuni, "
            "rankhits"
        ),
    )
    p_contrast.add_argument("--fit-prefix", type=int, default=0)
    p_contrast.add_argument("--pos-bucket", type=int, default=1)
    p_contrast.add_argument(
        "--rankpath-pos-bucket",
        type=int,
        default=None,
        help=(
            "Position bucket for rank-symbol tables. Default: same as "
            "--pos-bucket. 0 is unbucketed. Not a watermark key."
        ),
    )
    p_contrast.add_argument(
        "--rankpath-end",
        type=int,
        default=0,
        help=(
            "If >0, score only the first N rank symbols after collection. "
            "Isolated --fit-prefix 4 is three symbols; --fit-prefix 5 is "
            "four (unbucketed prefix-4). Still no keys."
        ),
    )
    p_contrast.add_argument("--prompt-context", action="store_true")
    p_contrast.add_argument("--out-dir", default="")
    p_contrast.set_defaults(func=cmd_contrast)

    p_scrub = sub.add_parser(
        "scrub",
        help=(
            "Key-free argmax snap on marked files, then official-score "
            "before/after as a reference check (not a fluent rewriter)"
        ),
        description=(
            "Replace tokens with the unmarked LM argmax of each original "
            "prefix. The snap does not use watermark keys. Official scores "
            "afterwards are only a reference measurement."
        ),
    )
    p_scrub.add_argument(
        "path",
        help="Marked .txt file, or directory of *-marked*.txt twins",
    )
    p_scrub.add_argument("--model", default="gpt2")
    p_scrub.add_argument("--top-k", type=int, default=40)
    p_scrub.add_argument("--out-dir", default="")
    p_scrub.set_defaults(func=cmd_scrub)

    p_it = sub.add_parser(
        "iterate",
        help=(
            "Rewrite a known-marked file; official-score every pass "
            "(not a remover, not Claude). Optional stop on the possible "
            "key-free indicate LR; light polish is the control"
        ),
        description=(
            "Rewrite a known-marked file and official-score every pass. "
            "Not a remover. Not Claude. Default stop is official chance. "
            "Light polish (--via polish) is the control. "
            "--stop-on indicate is not official score."
        ),
    )
    p_it.add_argument("path", help="Marked text file, or omit for stdin", nargs="?")
    p_it.add_argument(
        "--backend",
        default="deepseek",
        choices=("deepseek", "qwen"),
        help="Non-origin rewrite backend (deepseek or qwen/DashScope)",
    )
    p_it.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Chat model (default: {DEFAULT_MODEL})",
    )
    p_it.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="DeepSeek-compatible chat base (default: api.deepseek.com)",
    )
    p_it.add_argument(
        "--via",
        choices=("paraphrase", "zh", "polish"),
        default="paraphrase",
        help=(
            "paraphrase = substantial token-level rewrite (default); "
            "polish = light word-choice so it sounds better (control); "
            "zh = English→Chinese→English"
        ),
    )
    p_it.add_argument(
        "--stop-on",
        choices=(STOP_CHANCE, STOP_INDICATE),
        default=STOP_CHANCE,
        help=(
            "chance = official mean/weighted mean near 0.50 (default); "
            "indicate = key-free single-file LR at or below --indicate-threshold "
            "(not official score; needs --tables)"
        ),
    )
    p_it.add_argument(
        "--tables",
        default="",
        help="Frozen indicate tables (required for --stop-on indicate)",
    )
    p_it.add_argument(
        "--indicate-threshold",
        type=float,
        default=DEFAULT_INDICATE_THRESHOLD,
        help=(
            "With --stop-on indicate, stop when lr <= this value "
            f"(default {DEFAULT_INDICATE_THRESHOLD})"
        ),
    )
    p_it.add_argument("--max-passes", type=int, default=DEFAULT_MAX_PASSES)
    p_it.add_argument("--mean-tol", type=float, default=DEFAULT_MEAN_TOL)
    p_it.add_argument(
        "--min-unmasked-ngrams",
        type=int,
        default=DEFAULT_MIN_NGRAMS,
    )
    p_it.add_argument("--timeout", type=float, default=120.0)
    p_it.add_argument(
        "--out-dir",
        type=str,
        default="",
        help="If set, write source.txt, pass-N.txt, final.txt, results",
    )
    p_it.set_defaults(func=cmd_iterate)

    p_rs = sub.add_parser(
        "resample",
        help=(
            "Collect the same Claude PROMPTS into a new dated dir, "
            "last-1/last-4 vs pre-mark and the previous sample, append LOGBOOK "
            "(Wed/Fri/Sun 04:00 schedule; not a detector)"
        ),
    )
    p_rs.add_argument(
        "--skip-collect",
        action="store_true",
        help="Analyze an existing corpus; do not scrape claude.ai",
    )
    p_rs.add_argument(
        "--new-dir",
        default="",
        help="Existing or target sample directory",
    )
    p_rs.add_argument(
        "--previous-dir",
        default="",
        help="Previous sample to contrast (default: latest other sample/mark dir)",
    )
    p_rs.add_argument(
        "--premark-dir",
        default="",
        help="Pre-mark control (default: experiments/claude-premark-2026-08)",
    )
    p_rs.add_argument(
        "--logbook",
        default="",
        help="Logbook path (default: research/LOGBOOK.md)",
    )
    p_rs.add_argument(
        "--date",
        default="",
        help="Calendar day YYYY-MM-DD (default: today)",
    )
    p_rs.add_argument("--pause", type=int, default=25)
    p_rs.set_defaults(func=cmd_resample)

    p_open = sub.add_parser(
        "openings",
        help=(
            "Opening-overlap bound: isolated observed-token recall vs train "
            "opening coverage. Not detector_mean, not key recovery."
        ),
        description=(
            "Fit observed-token tables on one or more twin directories and "
            "report how many held-out files share an opening atom. Isolated "
            "recall equals that overlap. Not a universal detector."
        ),
    )
    p_open.add_argument("pair_dir", help="First train twin directory")
    p_open.add_argument("--test-dir", required=True, help="Held-out twin directory")
    p_open.add_argument(
        "--extra-train",
        action="append",
        default=[],
        help="Additional train twin directories, added in order to the coverage curve",
    )
    p_open.add_argument("--model", default="gpt2")
    p_open.add_argument("--context-len", type=int, default=4)
    p_open.add_argument("--fit-prefix", type=int, default=4)
    p_open.add_argument("--pos-bucket", type=int, default=1)
    p_open.add_argument("--include-first", action="store_true")
    p_open.add_argument(
        "--methods",
        default="postokhits,postokbackoff,postokbackoff2",
        help="Comma-separated observed-token readers",
    )
    p_open.add_argument(
        "--curve-method",
        default="postokbackoff",
        help="Method for the per-stem coverage curve (default postokbackoff)",
    )
    p_open.add_argument("--skip-stem-curve", action="store_true")
    p_open.add_argument("--out-dir", default="")
    p_open.set_defaults(func=cmd_openings)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
