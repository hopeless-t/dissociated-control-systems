from dissociated_control_systems.cognitive_probe_admission import (
    admission_experiment,
    candidates,
    evaluate_probe,
)


def test_high_accuracy_oracle_is_rejected():
    oracle = next(
        spec for spec in candidates()
        if spec.probe_id == "direct_latent_oracle"
    )
    decision = evaluate_probe(oracle)
    assert oracle.diagnostic_accuracy == 1.0
    assert decision.admission == "REJECT"
    assert "LATENT_TRUTH_LEAKAGE" in decision.reasons


def test_controlled_challenges_are_synthetic_admissible_only():
    for probe_id in (
        "controlled_handoff_challenge",
        "controlled_calibration_step_response",
    ):
        spec = next(spec for spec in candidates() if spec.probe_id == probe_id)
        decision = evaluate_probe(spec)
        assert decision.admission == "ADMIT_SYNTHETIC"
        assert "REQUIRES_ETHICS" in decision.translation


def test_contract_blocks_accuracy_shortcuts():
    result = admission_experiment()
    assert result["unsafe_accuracy_admissions"] == 4
    assert result["contract_false_admissions"] == 0
