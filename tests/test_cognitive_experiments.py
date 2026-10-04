import pytest

from dissociated_control_systems.cognitive_experiments import (
    LayeredConfig,
    layer_ablation,
    monte_carlo,
    parameter_sweep,
    quantile,
    simulate_layered,
    summarize_layered,
)


def test_quantile_known_answer() -> None:
    assert quantile([0.0, 1.0], 0.5) == pytest.approx(0.5)


def test_same_seed_reproduces_noisy_trajectory() -> None:
    config = LayeredConfig(
        name="noise",
        feedback_noise=0.03,
        shock_probability=0.1,
        shock_magnitude=0.01,
    )
    assert simulate_layered(config, seed=17) == simulate_layered(config, seed=17)


def test_slow_l1_calibration_creates_more_calibration_breach() -> None:
    results = layer_ablation()
    assert (
        results["l1_slow_calibration"].calibration_breach_fraction
        > results["reference"].calibration_breach_fraction
    )


def test_l2_handoff_failure_hurts_minimum_function_in_frozen_ablation() -> None:
    results = layer_ablation()
    assert (
        results["l2_unreliable_handoff"].minimum_function
        < results["l1_slow_calibration"].minimum_function
    )


def test_combined_l1_l2_failure_has_largest_handoff_deficit() -> None:
    results = layer_ablation()
    assert (
        results["l1_l2_combined"].mean_handoff_deficit
        > results["l1_slow_calibration"].mean_handoff_deficit
    )
    assert (
        results["l1_l2_combined"].mean_handoff_deficit
        > results["l2_unreliable_handoff"].mean_handoff_deficit
    )


def test_parameter_sweep_is_frozen_and_finds_masked_success() -> None:
    result = parameter_sweep()
    assert result["cells"] == 144
    assert result["dual_beats_baseline"] == 144
    assert result["dual_beats_both_single_tracks"] == 139
    assert len(result["masked_success_cases"]) == 5


def test_monte_carlo_dual_track_has_best_frozen_tail_floor() -> None:
    result = monte_carlo(samples=100)
    dual_floor = result["dual_track"]["p05_minimum_function"]
    assert dual_floor > result["baseline"]["p05_minimum_function"]
    assert dual_floor > result["compensation_only"]["p05_minimum_function"]
    assert dual_floor > result["decline_reduction_only"]["p05_minimum_function"]


@pytest.mark.parametrize(
    "bad",
    [
        LayeredConfig(name="bad", policy_reliability=1.1),
        LayeredConfig(name="bad", feedback_noise=-0.1),
        LayeredConfig(name="bad", shock_probability=-0.1),
    ],
)
def test_invalid_layered_inputs_fail_closed(bad: LayeredConfig) -> None:
    with pytest.raises((TypeError, ValueError)):
        simulate_layered(bad)


def test_summary_rejects_empty_rows() -> None:
    with pytest.raises(ValueError):
        summarize_layered(())
