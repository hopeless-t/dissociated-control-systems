from dissociated_control_systems.cognitive_context_failure_mode_diversity import (
    MAX_EPOCH_SELECTION_REGRET,
    failure_mode_diversity_experiment,
)


def test_orthogonal_audit_detects_common_mode_onset_and_recovery():
    result = failure_mode_diversity_experiment()
    audit = result["orthogonal"]
    trigger_epochs = [
        row["epoch"]
        for row in audit["rows"]
        if row["trigger_reason"] == "orthogonal_audit_change"
    ]
    assert trigger_epochs == [1, 7]
    assert audit["audit_change_triggers"] == 2
    assert audit["hard_expiry_triggers"] == 0


def test_orthogonal_audit_restores_zero_stale_authority():
    result = failure_mode_diversity_experiment()
    audit = result["orthogonal"]
    assert audit["contract_pass"]
    assert audit["stale_authority_epochs"] == 0
    assert audit["max_regret"] <= MAX_EPOCH_SELECTION_REGRET


def test_failure_mode_diversity_beats_same_family_redundancy():
    result = failure_mode_diversity_experiment()
    pairwise = result["pairwise"]
    audit = result["orthogonal"]
    assert pairwise["change_triggers"] == 0
    assert pairwise["stale_authority_epochs"] >= 5
    assert pairwise["max_regret"] > 0.30
    assert audit["stale_authority_epochs"] == 0
    assert audit["max_regret"] < pairwise["max_regret"]


def test_orthogonal_audit_reduces_full_qualification_work():
    result = failure_mode_diversity_experiment()
    assert result["orthogonal"]["qualifications"] == 3
    assert result["qualification_reduction_vs_epochly_gate"] == 0.7


def test_orthogonal_bias_estimate_tracks_shared_bias_regime():
    result = failure_mode_diversity_experiment()
    rows = result["orthogonal"]["rows"]
    assert abs(rows[0]["audit_bias_estimate"]) < 0.03
    assert all(row["audit_bias_estimate"] > 0.05 for row in rows[1:7])
    assert all(abs(row["audit_bias_estimate"]) < 0.03 for row in rows[7:])
