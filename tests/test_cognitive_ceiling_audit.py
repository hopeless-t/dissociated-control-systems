from dissociated_control_systems.cognitive_ceiling_audit import (
    audit,
    evaluate_ceiling,
)


def test_knn_ceiling_audit_is_reasonably_close_to_bayes():
    result = evaluate_ceiling(train_samples=50, test_samples=20, k=7)
    assert abs(result["knn_accuracy"] - result["bayes_accuracy"]) < 0.10


def test_union_accuracy_is_an_upper_bound_for_both_classifiers():
    result = evaluate_ceiling(train_samples=50, test_samples=20, k=7)
    assert result["oracle_union_accuracy"] >= result["bayes_accuracy"]
    assert result["oracle_union_accuracy"] >= result["knn_accuracy"]


def test_full_audit_returns_boolean_stability_decision():
    result = audit()
    assert isinstance(result["ceiling_stable"], bool)
