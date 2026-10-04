from dissociated_control_systems.cognitive_ensemble_frontier import (
    mix_posteriors,
    optimize,
)


def test_mixture_is_convex():
    h1 = frozenset()
    h2 = frozenset({"l0_decline"})
    mixed = mix_posteriors(
        {h1: 0.8, h2: 0.2},
        {h1: 0.4, h2: 0.6},
        bayes_weight=0.5,
    )
    assert mixed[h1] == 0.6
    assert mixed[h2] == 0.4


def test_ensemble_frontier_returns_valid_accuracy():
    result = optimize()
    assert 0.0 <= result["ensemble_accuracy"] <= 1.0
    assert result["oracle_union_accuracy"] >= result["ensemble_accuracy"]
