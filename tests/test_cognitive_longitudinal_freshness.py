from dissociated_control_systems.cognitive_longitudinal_freshness import (
    HORIZONS,
    RMSE_CONTRACT,
    analytic_rmse,
    freshness_experiment,
)


def test_rmse_increases_with_anchor_age():
    values = [analytic_rmse(horizon) for horizon in HORIZONS]
    assert values == sorted(values)


def test_freshness_boundary_is_nontrivial():
    result = freshness_experiment()
    assert result["freshness_lease"] > 0
    assert result["first_expired"] is not None
    assert analytic_rmse(result["freshness_lease"]) <= RMSE_CONTRACT
    assert analytic_rmse(result["first_expired"]) > RMSE_CONTRACT


def test_monte_carlo_matches_analytic_drift_model():
    result = freshness_experiment()
    assert result["max_formula_error"] < 0.005
