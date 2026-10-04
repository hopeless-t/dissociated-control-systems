from dissociated_control_systems.cognitive_ood_fixed_point import (
    replicated_ood_audit,
)


def test_replicated_ood_audit_has_five_blocks():
    result = replicated_ood_audit()
    assert len(result["rows"]) == 5


def test_replicated_ood_decision_is_boolean():
    result = replicated_ood_audit()
    assert isinstance(result["robust"], bool)
