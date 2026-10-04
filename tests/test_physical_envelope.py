import pytest

from dissociated_control_systems.physical_envelope import (
    contact_compression,
    envelope_scale,
    load_fraction,
    solve_vertical_support_pair,
)


def test_support_pair_known_answer() -> None:
    result = solve_vertical_support_pair(
        left_x=0.0,
        right_x=1.0,
        com_x=0.56,
        mass=4.0,
        gravity=9.81,
    )
    assert result.total_weight == pytest.approx(39.24)
    assert result.left_force == pytest.approx(17.2656)
    assert result.right_force == pytest.approx(21.9744)
    assert result.force_residual == pytest.approx(0.0)
    assert result.moment_residual == pytest.approx(0.0)
    assert result.stable


def test_unstable_com_outside_support_fails_stability_flag() -> None:
    result = solve_vertical_support_pair(
        left_x=0.0,
        right_x=1.0,
        com_x=1.2,
        mass=4.0,
    )
    assert not result.stable
    assert result.left_force < 0.0


def test_load_fraction_and_envelope_scale() -> None:
    result = solve_vertical_support_pair(
        left_x=0.0,
        right_x=1.0,
        com_x=0.56,
        mass=4.0,
    )
    fore = load_fraction(result.right_force, result.total_weight)
    assert fore == pytest.approx(0.56)

    proximal, distal = envelope_scale(
        load_fraction_value=fore,
        depth_scale=1.12,
    )
    assert proximal == pytest.approx(1.40224)
    assert distal == pytest.approx(1.195264)
    assert proximal > distal


def test_far_side_projection_is_narrower() -> None:
    near = envelope_scale(load_fraction_value=0.56, depth_scale=1.12)
    far = envelope_scale(load_fraction_value=0.56, depth_scale=0.86)
    assert far[0] < near[0]
    assert far[1] < near[1]


def test_contact_compression_proxy() -> None:
    assert contact_compression(force=21.9744, stiffness=120.0) == pytest.approx(
        0.18312
    )


@pytest.mark.parametrize(
    ("left_x", "right_x", "mass"),
    [
        (1.0, 1.0, 4.0),
        (2.0, 1.0, 4.0),
        (0.0, 1.0, 0.0),
    ],
)
def test_invalid_support_configuration_fails_closed(
    left_x: float,
    right_x: float,
    mass: float,
) -> None:
    with pytest.raises(ValueError):
        solve_vertical_support_pair(
            left_x=left_x,
            right_x=right_x,
            com_x=0.5,
            mass=mass,
        )
