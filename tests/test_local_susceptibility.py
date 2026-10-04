import pytest

from dissociated_control_systems.local_susceptibility import (
    LocalResponseState,
    finite_difference_susceptibility,
    matched_state_divergence,
)


def test_same_baseline_can_hide_opposite_local_response() -> None:
    first, second = matched_state_divergence(
        baseline=0.5,
        susceptibility_a=0.4,
        susceptibility_b=-0.2,
        input_delta=0.5,
    )

    assert first == pytest.approx(0.7)
    assert second == pytest.approx(0.4)


def test_finite_difference_recovers_declared_local_gain() -> None:
    state = LocalResponseState(baseline=0.3, susceptibility=0.25)
    perturbed = state.response(0.4)

    assert finite_difference_susceptibility(0.3, perturbed, 0.4) == pytest.approx(0.25)


def test_zero_input_cannot_identify_susceptibility() -> None:
    with pytest.raises(ValueError):
        finite_difference_susceptibility(0.3, 0.3, 0.0)
