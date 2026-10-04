from dissociated_control_systems.cognitive_harness_repair import (
    active_pair_recovery,
    passive_pair_recovery,
    passive_single_fault_experiment,
    train_active_thresholds,
)


def test_single_fault_bayes_is_high_accuracy_and_can_abstain():
    result = passive_single_fault_experiment(samples=100)
    assert result["accuracy"] > 0.94
    assert result["abstain_rate"] < 0.05


def test_targeted_repairs_move_each_fault_metric_in_right_direction():
    result = passive_single_fault_experiment(samples=100)["targeted"]
    assert result["l0_decline"]["repaired_target"] > result["l0_decline"]["baseline_target"]
    assert result["l1_calibration"]["repaired_target"] < result["l1_calibration"]["baseline_target"]
    assert result["l2_handoff"]["repaired_target"] < result["l2_handoff"]["baseline_target"]
    assert result["observer_bias"]["repaired_target"] < result["observer_bias"]["baseline_target"]


def test_passive_single_fault_classifier_breaks_on_pair_mixtures():
    result = passive_pair_recovery(samples=50)
    assert result["exact_recovery_rate"] < 0.25


def test_active_repair_reobserve_loop_recovers_pair_faults():
    passive = passive_pair_recovery(samples=50)
    active = active_pair_recovery(samples=50)
    assert active["exact_recovery_rate"] > 0.80
    assert active["exact_recovery_rate"] > passive["exact_recovery_rate"] + 0.60
    assert active["mean_repair_coverage"] > 0.90
    assert active["mean_extra_repairs"] < 0.10


def test_active_threshold_training_is_informative():
    thresholds = train_active_thresholds(samples=100)
    for threshold, balanced_accuracy in thresholds.values():
        assert threshold >= 0.0
        assert balanced_accuracy > 0.90
