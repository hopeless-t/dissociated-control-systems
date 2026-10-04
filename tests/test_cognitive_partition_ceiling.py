from dissociated_control_systems.cognitive_partition_ceiling import (
    partition_ceiling_experiment,
)


def test_oracle_partition_still_has_low_ppv():
    result = partition_ceiling_experiment()
    assert result["best_precision"]["precision"] < 0.10


def test_no_positive_action_subset_under_frozen_harm_models():
    result = partition_ceiling_experiment()
    assert not any(
        item["positive"]
        for item in result["action_best"].values()
    )


def test_fault_partition_contains_all_heldout_episodes():
    result = partition_ceiling_experiment()
    assert sum(row["total"] for row in result["strata"]) == 6400
