import pytest

from dissociated_control_systems.defeater_saturation import (
    minimum_zero_novel_rounds,
    should_pause_defeater_search,
    zero_novelty_upper_bound,
)


def test_upper_bound_decreases_with_more_zero_novelty_rounds() -> None:
    assert zero_novelty_upper_bound(20) < zero_novelty_upper_bound(5)


def test_fifty_nine_zero_novelty_rounds_put_95pct_upper_bound_below_5pct() -> None:
    assert minimum_zero_novel_rounds(0.05, alpha=0.05) == 59
    assert zero_novelty_upper_bound(58, alpha=0.05) > 0.05
    assert zero_novelty_upper_bound(59, alpha=0.05) <= 0.05


def test_pause_rule_uses_declared_threshold_only() -> None:
    assert not should_pause_defeater_search(
        20,
        target_upper_bound=0.05,
        alpha=0.05,
    )
    assert should_pause_defeater_search(
        59,
        target_upper_bound=0.05,
        alpha=0.05,
    )


def test_one_round_has_very_weak_novelty_bound() -> None:
    assert zero_novelty_upper_bound(1, alpha=0.05) == pytest.approx(0.95)


def test_invalid_inputs_fail_closed() -> None:
    with pytest.raises(ValueError):
        zero_novelty_upper_bound(0)
    with pytest.raises(ValueError):
        minimum_zero_novel_rounds(0.0)
