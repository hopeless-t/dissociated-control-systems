import pytest

from dissociated_control_systems.survivor_baseline import (
    binary_auc,
    binary_log_loss,
    fixed_horizon_survivor_label,
    fit_logistic,
    predict_logistic,
    risk_difference,
    standardized_mean_difference,
)


def test_fixed_horizon_labels_fail_closed_on_censoring() -> None:
    assert fixed_horizon_survivor_label(48, "Died of Disease") == "STS"
    assert fixed_horizon_survivor_label(121, "Living") == "LTS"
    assert fixed_horizon_survivor_label(121, "Died of Disease") == "LTS"
    assert fixed_horizon_survivor_label(40, "Living") is None
    assert fixed_horizon_survivor_label(80, "Died of Disease") is None
    assert fixed_horizon_survivor_label(50, "Died of Other Causes") is None


def test_standardized_mean_difference_known_direction() -> None:
    value = standardized_mean_difference([1, 1, 2, 2], [4, 4, 5, 5])
    assert value < -3.0


def test_small_logistic_fit_separates_known_answer() -> None:
    x = [
        [1.0, -2.0],
        [1.0, -1.0],
        [1.0, 1.0],
        [1.0, 2.0],
    ]
    y = [0, 0, 1, 1]
    weights = fit_logistic(x, y, steps=3000)
    p = predict_logistic(x, weights)

    assert p[0] < p[1] < p[2] < p[3]
    assert binary_auc(y, p) == 1.0
    assert binary_log_loss(y, p) < 0.2


def test_auc_ties_are_averaged() -> None:
    assert binary_auc([0, 1], [0.5, 0.5]) == 0.5


def test_risk_difference_known_answer() -> None:
    assert risk_difference([True, True, False], [True, False, False]) == pytest.approx(
        1 / 3
    )
