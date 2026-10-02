from __future__ import annotations

import pytest

from dissociated_control_systems.trajectory import (
    equivalent_constant_loss_probability,
    independent_survival,
)


@pytest.mark.parametrize(
    ("q", "m", "expected"),
    [
        (0.01, 100, 0.3660323412732292),
        (0.005, 100, 0.6057704364907279),
        (0.001, 100, 0.9047921471137089),
    ],
)
def test_independent_trajectory_survival_known_answers(
    q: float, m: int, expected: float
) -> None:
    assert independent_survival(q, m) == pytest.approx(expected)


def test_trajectory_survival_inversion_round_trip() -> None:
    q = 0.007
    m = 80
    survival = independent_survival(q, m)
    assert equivalent_constant_loss_probability(survival, m) == pytest.approx(q)


@pytest.mark.parametrize("q", [-0.1, 1.1])
def test_invalid_loss_probability_fails_closed(q: float) -> None:
    with pytest.raises(ValueError):
        independent_survival(q, 10)
