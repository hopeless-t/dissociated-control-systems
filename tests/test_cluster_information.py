import pytest

from dissociated_control_systems.cluster_information import (
    design_effect,
    effective_sample_size,
)


def test_independent_within_cluster_case_has_design_effect_one() -> None:
    assert design_effect(10, 0.0) == pytest.approx(1.0)
    assert effective_sample_size(30, 10, 0.0) == pytest.approx(30.0)


def test_correlated_follicles_reduce_effective_information() -> None:
    assert design_effect(10, 0.5) == pytest.approx(5.5)
    assert effective_sample_size(30, 10, 0.5) == pytest.approx(30 / 5.5)


def test_perfect_within_donor_correlation_collapses_each_cluster_to_one_unit() -> None:
    assert design_effect(10, 1.0) == pytest.approx(10.0)
    assert effective_sample_size(30, 10, 1.0) == pytest.approx(3.0)


def test_invalid_icc_rejected() -> None:
    with pytest.raises(ValueError):
        design_effect(10, 1.1)


def test_unequal_cluster_shape_rejected_by_simple_surrogate() -> None:
    with pytest.raises(ValueError):
        effective_sample_size(31, 10, 0.5)
