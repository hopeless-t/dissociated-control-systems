from dissociated_control_systems.cognitive_context_effective_diversity import (
    MC_TOLERANCE,
    effective_diversity_experiment,
)


def test_trigger_power_decreases_monotonically_as_shared_bias_increases():
    result = effective_diversity_experiment()
    powers = [level["analytic_tpr"] for level in result["levels"]]
    assert all(left >= right for left, right in zip(powers, powers[1:], strict=True))


def test_frozen_high_power_knee_occurs_at_rho_0625():
    result = effective_diversity_experiment()
    assert result["first_below_high_power_rho"] == 0.625
    assert result["first_below_high_power_effective_diversity"] == 0.375


def test_geometric_half_power_crossing_matches_frozen_detector():
    result = effective_diversity_experiment()
    assert result["half_power_geometry_rho"] == 0.625
    assert result["closest_half_power_rho"] == 0.625
    assert abs(result["closest_half_power_tpr"] - 0.5) < 0.01


def test_high_diversity_retains_power_and_low_diversity_loses_it():
    result = effective_diversity_experiment()
    by_rho = {level["shared_bias_fraction"]: level for level in result["levels"]}
    assert by_rho[0.50]["analytic_tpr"] > 0.98
    assert by_rho[0.75]["analytic_tpr"] < 0.02
    assert by_rho[1.0]["analytic_tpr"] < 1e-6


def test_monte_carlo_matches_analytic_pressure_curve():
    result = effective_diversity_experiment()
    assert result["max_mc_abs_error"] <= MC_TOLERANCE
