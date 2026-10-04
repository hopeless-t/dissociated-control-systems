import pytest

from dissociated_control_systems.projection_ladder import (
    LocalProjectionSpan,
    continuous_optimum_transitions,
    homogeneous_projection_cost,
    optimal_integer_projection,
    optimal_local_subdivisions,
    weighted_ladder_cost,
)


def test_projection_cost_has_finite_interior_optimum() -> None:
    # D=8, alpha=beta=1 -> continuous optimum n*=8.
    assert continuous_optimum_transitions(8.0) == pytest.approx(8.0)

    optimum = optimal_integer_projection(8.0)
    assert optimum.transitions == 8
    assert optimum.total_cost == pytest.approx(16.0)

    direct = homogeneous_projection_cost(8.0, 1)
    overspecified = homogeneous_projection_cost(8.0, 32)

    assert optimum.total_cost < direct.total_cost
    assert optimum.total_cost < overspecified.total_cost


def test_more_steps_are_not_monotonically_better() -> None:
    costs = [
        homogeneous_projection_cost(8.0, n).total_cost
        for n in (1, 2, 4, 8, 16, 32)
    ]

    assert costs[0] > costs[3]
    assert costs[-1] > costs[3]


def test_novice_like_jump_penalty_yields_more_intermediate_steps() -> None:
    expert = optimal_integer_projection(6.0, alpha=0.5, beta=1.0)
    novice = optimal_integer_projection(6.0, alpha=2.0, beta=1.0)

    assert novice.transitions > expert.transitions


def test_high_difficulty_span_receives_more_subdivision() -> None:
    spans = [
        LocalProjectionSpan(distance=2.0, difficulty=1.0),
        LocalProjectionSpan(distance=2.0, difficulty=9.0),
    ]

    allocation = optimal_local_subdivisions(spans)

    assert allocation[1] > allocation[0]


def test_adaptive_allocation_beats_uniform_under_heterogeneous_difficulty() -> None:
    spans = [
        LocalProjectionSpan(distance=3.0, difficulty=1.0),
        LocalProjectionSpan(distance=3.0, difficulty=9.0),
    ]
    adaptive = optimal_local_subdivisions(spans)
    total_steps = sum(adaptive)

    uniform_left = max(1, total_steps // 2)
    uniform = (uniform_left, max(1, total_steps - uniform_left))

    assert weighted_ladder_cost(spans, adaptive) <= weighted_ladder_cost(
        spans, uniform
    )
