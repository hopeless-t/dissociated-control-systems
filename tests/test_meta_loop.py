import pytest

from dissociated_control_systems.meta_loop import (
    ObservationOption,
    choose_observation,
    effective_pressure,
    expected_cascade_cost,
    learning_velocity,
    two_tier_break_even_stop_probability,
)


def test_active_observation_prefers_information_per_cost() -> None:
    coarse = ObservationOption("coarse", information_gain=0.60, cost=1.0)
    fine = ObservationOption("fine", information_gain=0.90, cost=3.0)
    assert choose_observation((coarse, fine)) == coarse


def test_cascade_expected_cost_known_answer() -> None:
    # 256 -> 512 -> 1024 style cascade.
    expected = expected_cascade_cost(
        (13_491.0, 33_244.0, 78_875.0),
        (0.5, 0.5),
    )
    assert expected == pytest.approx(49_831.75)


def test_two_tier_break_even_matches_known_ratio() -> None:
    assert two_tier_break_even_stop_probability(13_491.0, 78_875.0) == pytest.approx(
        13_491.0 / 78_875.0
    )


def test_learning_velocity_rewards_equal_gain_at_lower_cost() -> None:
    slow = learning_velocity(
        1.0,
        render_cost=4.0,
        observation_cost=4.0,
        decision_cost=2.0,
    )
    fast = learning_velocity(
        1.0,
        render_cost=2.0,
        observation_cost=2.0,
        decision_cost=1.0,
    )
    assert fast > slow


def test_effective_pressure_distinguishes_same_issue_count() -> None:
    low_interaction = effective_pressure(
        issue_count=4,
        negative_interaction_strengths=(0.1, 0.0),
        intervention_magnitudes=(0.2, 0.2, 0.2, 0.2),
        execution_cost=1.0,
    )
    high_interaction = effective_pressure(
        issue_count=4,
        negative_interaction_strengths=(0.8, 0.7),
        intervention_magnitudes=(0.8, 0.8, 0.8, 0.8),
        execution_cost=1.0,
    )
    assert high_interaction > low_interaction


@pytest.mark.parametrize(
    ("costs", "stops"),
    [
        ((), ()),
        ((1.0, 2.0), ()),
        ((1.0,), (0.5,)),
    ],
)
def test_invalid_cascade_shapes_fail_closed(
    costs: tuple[float, ...],
    stops: tuple[float, ...],
) -> None:
    with pytest.raises(ValueError):
        expected_cascade_cost(costs, stops)


def test_invalid_probability_fails_closed() -> None:
    with pytest.raises(ValueError):
        expected_cascade_cost((1.0, 2.0), (1.1,))
