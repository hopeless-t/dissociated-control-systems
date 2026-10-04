from dissociated_control_systems.cognitive_rare_capture_null import (
    null_and_selection_experiment,
    random_capture_distribution,
)


def test_hypergeometric_distribution_normalizes():
    pmf, cdf = random_capture_distribution(
        population=100,
        successes=5,
        draws=10,
    )
    assert abs(sum(pmf) - 1.0) < 1e-12
    assert abs(cdf[-1] - 1.0) < 1e-12


def test_causal_capture_is_extreme_under_random_null():
    result = null_and_selection_experiment()
    assert result["captured"] >= result["random_q999"]
    assert result["exact_tail"] < 0.001


def test_monte_carlo_is_consistent_with_exact_tail():
    result = null_and_selection_experiment()
    # Extremely small tails can produce zero Monte Carlo hits. The exact
    # calculation remains authoritative; MC is only a seeded cross-check.
    assert abs(result["mc_tail"] - result["exact_tail"]) < 0.001
