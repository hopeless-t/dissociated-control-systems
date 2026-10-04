import pytest

from dissociated_control_systems.recoverability_knee import (
    gain_change_rates,
    local_control_gain,
    unique_steepest_gain_loss_interval,
)


def test_local_control_gain_uses_response_difference_per_input() -> None:
    assert local_control_gain(0.8, 0.5, 0.5) == pytest.approx(0.6)


def test_zero_input_cannot_define_control_gain() -> None:
    with pytest.raises(ValueError):
        local_control_gain(0.8, 0.5, 0.0)


def test_unique_sharp_gain_loss_returns_interval() -> None:
    burden = (0, 1, 2, 3, 4)
    gains = (1.0, 0.9, 0.8, 0.3, 0.2)

    assert unique_steepest_gain_loss_interval(burden, gains) == (2.0, 3.0)


def test_linear_gain_decline_has_no_unique_knee() -> None:
    burden = (0, 1, 2, 3, 4)
    gains = (1.0, 0.8, 0.6, 0.4, 0.2)

    assert unique_steepest_gain_loss_interval(burden, gains) is None


def test_nonuniform_burden_spacing_uses_slope_not_raw_difference() -> None:
    rates = gain_change_rates((0, 1, 3), (1.0, 0.8, 0.0))
    assert rates[0][2] == pytest.approx(-0.2)
    assert rates[1][2] == pytest.approx(-0.4)


def test_burden_must_be_strictly_increasing() -> None:
    with pytest.raises(ValueError):
        gain_change_rates((0, 1, 1), (1.0, 0.8, 0.3))
