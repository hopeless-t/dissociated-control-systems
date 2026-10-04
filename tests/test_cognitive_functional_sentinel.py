from dissociated_control_systems.cognitive_functional_sentinel import (
    SENTINEL_NUISANCE_SIGMAS,
    functional_sentinel_experiment,
)


def test_dyad_is_near_chance_in_equal_drift_world():
    result = functional_sentinel_experiment()
    assert abs(result["dyad_auc"] - 0.5) < 0.02


def test_low_noise_independent_sentinel_is_informative():
    result = functional_sentinel_experiment()
    low_noise = next(
        row for row in result["sentinel_rows"]
        if row["nuisance_sigma"] == 0.01
    )
    assert low_noise["auc"] > 0.90


def test_high_noise_sentinel_approaches_chance():
    result = functional_sentinel_experiment()
    high_noise = result["sentinel_rows"][-1]
    assert high_noise["nuisance_sigma"] == max(SENTINEL_NUISANCE_SIGMAS)
    assert high_noise["auc"] < 0.60


def test_sentinel_frontier_is_monotone():
    result = functional_sentinel_experiment()
    assert result["sentinel_auc_monotone"]
