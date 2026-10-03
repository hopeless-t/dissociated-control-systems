import math

import pytest

from dissociated_control_systems.fixed_point import (
    contraction_ratios,
    convergence_depth,
    drive_gain,
    fixed_point_residual,
    iterate_affine_contraction,
    orthogonal_injection,
    step_norms,
)


def test_affine_contraction_has_known_geometric_step_ratio() -> None:
    trajectory = iterate_affine_contraction(
        (8.0, -4.0),
        (0.0, 0.0),
        retention=0.5,
        steps=6,
    )
    assert len(trajectory) == 7
    assert all(math.isclose(ratio, 0.5) for ratio in contraction_ratios(trajectory))


def test_convergence_depth_requires_persistent_settling() -> None:
    trajectory = iterate_affine_contraction(
        (1.0,),
        (0.0,),
        retention=0.5,
        steps=6,
    )
    assert convergence_depth(trajectory, (0.0,), tolerance=0.13) == 3


def test_fixed_point_residual_is_zero_at_exact_endpoint() -> None:
    assert fixed_point_residual((2.0, -1.0), (2.0, -1.0)) == 0.0


def test_orthogonal_injection_keeps_drive_gain_constant() -> None:
    drive = (2.0, 0.0)
    states = (
        (10.0, 1.0),
        (-7.0, 4.0),
        (0.0, -3.0),
    )
    injected = tuple(orthogonal_injection(state, drive) for state in states)
    assert all(math.isclose(drive_gain(state, drive), 1.0) for state in injected)
    assert tuple(state[1] for state in injected) == (1.0, 4.0, -3.0)


def test_step_norms_reject_mixed_dimensions() -> None:
    with pytest.raises(ValueError):
        step_norms(((0.0, 1.0), (0.0,)))


def test_invalid_contraction_retention_fails_closed() -> None:
    with pytest.raises(ValueError):
        iterate_affine_contraction((1.0,), (0.0,), retention=1.0, steps=1)


def test_zero_drive_fails_closed() -> None:
    with pytest.raises(ValueError):
        orthogonal_injection((1.0, 2.0), (0.0, 0.0))
