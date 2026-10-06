import pytest

from dissociated_control_systems.trajectory_selection import (
    attrition_shift,
    complete_case_covariance,
    retained_pairs,
)
from dissociated_control_systems.temporal_linkage import population_covariance


def test_selective_attrition_can_create_positive_covariance_from_zero() -> None:
    early = (0.0, 0.0, 1.0, 1.0)
    late = (0.0, 1.0, 0.0, 1.0)
    retained = (True, False, False, True)

    assert population_covariance(early, late) == pytest.approx(0.0)
    assert complete_case_covariance(early, late, retained) == pytest.approx(0.25)
    assert attrition_shift(early, late, retained) == pytest.approx(0.25)


def test_selective_attrition_can_create_negative_covariance_too() -> None:
    early = (0.0, 0.0, 1.0, 1.0)
    late = (0.0, 1.0, 0.0, 1.0)
    retained = (False, True, True, False)

    assert complete_case_covariance(early, late, retained) == pytest.approx(-0.25)


def test_retention_mask_length_must_match() -> None:
    with pytest.raises(ValueError):
        retained_pairs((0.0, 1.0), (0.0, 1.0), (True,))


def test_all_trajectories_dropped_is_invalid() -> None:
    with pytest.raises(ValueError):
        retained_pairs((0.0, 1.0), (0.0, 1.0), (False, False))
