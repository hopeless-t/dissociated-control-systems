from dissociated_control_systems.cognitive_disagreement_resolver import optimize


def test_resolver_is_bounded_by_oracle_union():
    result = optimize()
    assert result["resolver_accuracy"] <= result["oracle_union_accuracy"] + 1e-12


def test_resolver_does_not_materially_underperform_bayes():
    result = optimize()
    assert result["resolver_accuracy"] >= result["bayes_accuracy"] - 0.01
