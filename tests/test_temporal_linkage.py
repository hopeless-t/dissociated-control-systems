import pytest

from dissociated_control_systems.temporal_linkage import (
    covariance_identified_from_marginals,
    population_covariance,
    possible_covariances_from_unlinked_marginals,
)


def test_same_marginals_allow_opposite_within_unit_covariance() -> None:
    early = (0.0, 1.0)
    late = (0.0, 1.0)

    possibilities = possible_covariances_from_unlinked_marginals(early, late)

    assert possibilities == pytest.approx((-0.25, 0.25))
    assert not covariance_identified_from_marginals(early, late)


def test_linked_positive_and_negative_pairings_share_same_means() -> None:
    early = (0.0, 1.0)
    late_positive = (0.0, 1.0)
    late_negative = (1.0, 0.0)

    assert sum(late_positive) / 2 == sum(late_negative) / 2
    assert population_covariance(early, late_positive) == pytest.approx(0.25)
    assert population_covariance(early, late_negative) == pytest.approx(-0.25)


def test_constant_marginal_is_degenerate_identifiable_case() -> None:
    early = (1.0, 1.0, 1.0)
    late = (0.0, 1.0, 2.0)

    assert covariance_identified_from_marginals(early, late)
    assert possible_covariances_from_unlinked_marginals(early, late) == (0.0,)


def test_exact_enumerator_rejects_large_n() -> None:
    with pytest.raises(ValueError):
        possible_covariances_from_unlinked_marginals(range(9), range(9))
