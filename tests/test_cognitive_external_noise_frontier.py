from dissociated_control_systems.cognitive_external_noise_frontier import (
    REPEATS,
    external_noise_frontier,
    theoretical_rmse,
)


def test_objective_state_rmse_shrinks_with_repetition():
    values = [theoretical_rmse(n)["Z_current_state"] for n in REPEATS]
    assert values == sorted(values, reverse=True)


def test_reporter_state_rmse_has_nonzero_noise_floor():
    result = external_noise_frontier()
    last = result["rows"][-1]["theoretical_rmse"]
    assert last["A_self_bias"] > 0.10
    assert last["B_informant_bias"] > 0.10
    assert last["E_scaffold"] > 0.10


def test_monte_carlo_matches_analytic_frontier():
    result = external_noise_frontier()
    assert result["max_formula_error"] < 0.01


def test_declared_marginal_gain_knee_exists():
    result = external_noise_frontier()
    assert result["practical_knee"] in REPEATS
