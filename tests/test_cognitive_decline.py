import pytest

from dissociated_control_systems.cognitive_decline import (
    SimulationConfig,
    default_configs,
    optimal_compensation,
    simulate,
    summarize,
)


def test_metacognitive_gap_converges_to_known_answer() -> None:
    config = SimulationConfig(
        name="gap-known-answer",
        steps=200,
        initial_capability=1.0,
        initial_self_estimate=1.0,
        decline_rate=0.001,
        feedback_gain=0.2,
    )
    rows = simulate(config)
    expected = config.decline_rate / config.feedback_gain
    assert rows[-1].metacognitive_gap == pytest.approx(expected, abs=1e-10)


def test_compensation_optimum_is_bounded_and_improves_function() -> None:
    capability = 0.5
    r = optimal_compensation(capability, cost=0.2)
    assert 0.0 < r < 1.0

    config = SimulationConfig(
        name="compensated",
        steps=1,
        initial_capability=capability,
        decline_rate=0.0,
        compensation_enabled=True,
    )
    row = simulate(config)[0]
    assert row.functional_performance > row.capability


def test_unassisted_observation_has_no_variance_amplification() -> None:
    row = simulate(
        SimulationConfig(name="baseline", steps=1, decline_rate=0.0)
    )[0]
    assert row.observability_amplification == 1.0


def test_compensation_increases_observation_noise_amplification() -> None:
    row = simulate(
        SimulationConfig(
            name="compensated",
            steps=1,
            initial_capability=0.5,
            decline_rate=0.0,
            compensation_enabled=True,
        )
    )[0]
    assert row.observability_amplification > 1.0


def test_dual_track_preserves_more_function_than_baseline() -> None:
    results = {
        config.name: summarize(simulate(config))
        for config in default_configs()
    }
    assert (
        results["dual_track"]["mean_functional_performance"]
        > results["baseline"]["mean_functional_performance"]
    )
    assert (
        results["dual_track"]["final_capability"]
        > results["baseline"]["final_capability"]
    )


@pytest.mark.parametrize(
    ("bad_capability", "bad_cost"),
    [(-0.1, 0.2), (1.1, 0.2), (0.5, 0.0)],
)
def test_invalid_optimal_compensation_inputs_fail_closed(
    bad_capability: float,
    bad_cost: float,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        optimal_compensation(bad_capability, bad_cost)
