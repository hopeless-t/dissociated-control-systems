import pytest

from dissociated_control_systems.checkpoint_risk import (
    interval_decision,
    pass_threshold,
)
from dissociated_control_systems.projection_protocol import CheckStatus


def test_symmetric_costs_yield_half_threshold() -> None:
    assert pass_threshold(
        false_pass_cost=1.0,
        false_block_cost=1.0,
    ) == pytest.approx(0.5)


def test_high_false_pass_cost_requires_high_support() -> None:
    assert pass_threshold(
        false_pass_cost=99.0,
        false_block_cost=1.0,
    ) == pytest.approx(0.99)


def test_interval_above_threshold_passes() -> None:
    assert interval_decision(
        0.995,
        1.0,
        false_pass_cost=99.0,
        false_block_cost=1.0,
    ) is CheckStatus.PASS


def test_interval_below_threshold_fails() -> None:
    assert interval_decision(
        0.80,
        0.95,
        false_pass_cost=99.0,
        false_block_cost=1.0,
    ) is CheckStatus.FAIL


def test_interval_straddling_threshold_is_unknown() -> None:
    assert interval_decision(
        0.95,
        1.0,
        false_pass_cost=99.0,
        false_block_cost=1.0,
    ) is CheckStatus.UNKNOWN


def test_invalid_interval_fails_closed() -> None:
    with pytest.raises(ValueError):
        interval_decision(
            0.9,
            0.8,
            false_pass_cost=1.0,
            false_block_cost=1.0,
        )
