from dissociated_control_systems.cognitive_fixed_point import replicated_audit


def test_replicated_audit_returns_all_blocks():
    result = replicated_audit(blocks=2, samples_per_hypothesis=20)
    assert len(result["rows"]) == 2


def test_fixed_point_decision_is_boolean():
    result = replicated_audit(blocks=2, samples_per_hypothesis=20)
    assert isinstance(result["converged"], bool)
