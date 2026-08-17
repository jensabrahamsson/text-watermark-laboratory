"""Key-free surrogate fit on a recorded query batch. No keys / g-values."""

from text_watermark_tools.surrogate import (
    QueryObservation,
    fit_surrogate,
    observations_from_sequence,
    rewrite_token_ids,
)


def _batch() -> list[QueryObservation]:
    # Tiny recorded next-token samples, as if collected from generate().
    ctx_a = (10, 11, 12, 13)
    ctx_b = (20, 21, 22, 23)
    return [
        QueryObservation(context=ctx_a, next_token=100),
        QueryObservation(context=ctx_a, next_token=100),
        QueryObservation(context=ctx_a, next_token=101),
        QueryObservation(context=ctx_b, next_token=200),
        QueryObservation(context=ctx_b, next_token=201),
    ]


def test_fit_does_not_touch_keys_or_g_values() -> None:
    sur = fit_surrogate(_batch(), n_queries=5)
    assert sur.used_keys is False
    assert sur.used_hash_iv is False
    assert sur.used_g_values is False
    assert sur.n_queries == 5
    assert sur.n_observations == 5
    assert sur.preferred((10, 11, 12, 13), 100)
    assert not sur.preferred((0, 0, 0, 0), 100)
    assert sur.alternative((10, 11, 12, 13), 100) == 101


def test_rewrite_uses_fitted_rule_not_a_second_scorer() -> None:
    sur = fit_surrogate(_batch(), n_queries=5)
    # Sequence whose 4-token windows match the recorded contexts.
    src = [10, 11, 12, 13, 100, 20, 21, 22, 23, 200]
    out = rewrite_token_ids(
        src,
        sur,
        unmarked_replacements={4: 999, 9: 888},
    )
    # Unmarked substitutes win over other marked samples.
    assert out[4] == 999
    assert out[9] == 888
    assert out[:4] == src[:4]


def test_rewrite_keeps_original_contexts_after_earlier_flips() -> None:
    ctx_a = (10, 11, 12, 13)
    ctx_b = (13, 100, 20, 21)
    sur = fit_surrogate(
        [
            QueryObservation(context=ctx_a, next_token=100),
            QueryObservation(context=ctx_b, next_token=22),
        ],
        n_queries=2,
    )
    src = [10, 11, 12, 13, 100, 20, 21, 22]
    # Flip at index 4 changes the live prefix; index 7 must still flip
    # because lookup uses the original source context.
    out = rewrite_token_ids(src, sur, unmarked_replacements={4: 77, 7: 88})
    assert out[4] == 77
    assert out[7] == 88


def test_source_sequence_marks_every_token_preferred() -> None:
    ids = [1, 2, 3, 4, 5, 6, 7, 8]
    sur = fit_surrogate(observations_from_sequence(ids, context_len=4), n_queries=8)
    assert sur.preferred((1, 2, 3, 4), 5)
    assert sur.preferred((4, 5, 6, 7), 8)
    out = rewrite_token_ids(
        ids, sur, unmarked_replacements={4: 50, 5: 60, 6: 70, 7: 80}
    )
    assert out[4:] == [50, 60, 70, 80]


def test_rewrite_falls_back_to_unmarked_when_no_alt() -> None:
    obs = [QueryObservation(context=(1, 2, 3, 4), next_token=7)]
    sur = fit_surrogate(obs, n_queries=1)
    src = [1, 2, 3, 4, 7]
    out = rewrite_token_ids(src, sur, unmarked_replacements={4: 42})
    assert out[4] == 42
