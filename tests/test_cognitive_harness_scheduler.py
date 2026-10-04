from dissociated_control_systems.cognitive_harness_scheduler import (
    diagnostic_window_loss,
    run_scheduler_experiment,
)


def test_l0_diagnostic_evidence_can_disappear_when_repair_is_deferred():
    assert diagnostic_window_loss(samples=50) > 0.50


def test_evidence_preserving_scheduler_improves_pair_recovery():
    result = run_scheduler_experiment(samples=50)
    assert (
        result["preserving_pair"]["exact_recovery_rate"]
        > result["legacy_pair"]["exact_recovery_rate"]
    )
    assert result["preserving_pair"]["exact_recovery_rate"] > 0.90
    assert result["preserving_pair"]["mean_extra_repairs"] < 0.05


def test_evidence_preserving_scheduler_rescues_triple_faults():
    result = run_scheduler_experiment(samples=50)
    assert result["legacy_triple"]["exact_recovery_rate"] < 0.40
    assert result["preserving_triple"]["exact_recovery_rate"] > 0.70
    assert (
        result["preserving_triple"]["exact_recovery_rate"]
        > result["legacy_triple"]["exact_recovery_rate"] + 0.40
    )
