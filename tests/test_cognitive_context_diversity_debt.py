from itertools import pairwise

from dissociated_control_systems.cognitive_context_diversity_debt import (
    ASYMPTOTIC_TOLERANCE,
    diversity_debt_experiment,
)


def test_required_samples_increase_as_effective_diversity_falls():
    result = diversity_debt_experiment()
    positive = [level for level in result["levels"] if level["minimum_samples"] is not None]
    samples = [level["minimum_samples"] for level in positive]
    assert all(left <= right for left, right in pairwise(samples))


def test_halving_low_diversity_costs_about_four_times_more_samples():
    result = diversity_debt_experiment()
    assert 3.8 <= result["half_diversity_sample_ratio"] <= 4.2


def test_low_diversity_n_d2_constant_matches_inverse_square_scaling():
    result = diversity_debt_experiment()
    assert result["max_low_diversity_constant_error"] <= ASYMPTOTIC_TOLERANCE


def test_frozen_sample_counts_show_quadratic_blowup():
    result = diversity_debt_experiment()
    by_d = {level["effective_diversity"]: level for level in result["levels"]}
    assert by_d[0.10]["minimum_samples"] == 76
    assert by_d[0.05]["minimum_samples"] == 303
    assert by_d[0.02]["minimum_samples"] == 1889
    assert by_d[0.01]["minimum_samples"] == 7556


def test_zero_effective_diversity_has_no_finite_sample_solution():
    result = diversity_debt_experiment()
    zero = next(level for level in result["levels"] if level["effective_diversity"] == 0.0)
    assert zero["minimum_samples"] is None
    assert zero["achieved_power"] == 0.01
