from dissociated_control_systems.cognitive_practice_effect_frontier import (
    PRACTICE_BIAS_PER_REPEAT,
    best_repeat_count,
    objective_mse,
    practice_effect_experiment,
)


def test_zero_bias_prefers_maximum_repetition():
    assert best_repeat_count(0.0) == 256


def test_nonzero_bias_produces_finite_optimum():
    for beta in PRACTICE_BIAS_PER_REPEAT[1:]:
        assert best_repeat_count(beta) < 256


def test_more_repeats_can_be_worse_under_bias():
    beta = 0.001
    assert objective_mse(256, beta) > objective_mse(64, beta)


def test_optimal_repeat_count_falls_as_bias_grows():
    result = practice_effect_experiment()
    assert result["nonzero_optima_monotone"]
