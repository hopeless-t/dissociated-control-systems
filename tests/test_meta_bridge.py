import pytest

from dissociated_control_systems.meta_bridge import exact_shapley_bridge, sequential_bridge


def interacting_score(state):
    a = state["trial_set"]
    b = state["effect_source"]
    return a + b + 2 * a * b


def test_sequential_attribution_changes_with_bridge_order() -> None:
    baseline = {"trial_set": 0.0, "effect_source": 0.0}
    target = {"trial_set": 1.0, "effect_source": 1.0}

    trial_first = sequential_bridge(
        baseline, target, ["trial_set", "effect_source"], interacting_score
    )
    source_first = sequential_bridge(
        baseline, target, ["effect_source", "trial_set"], interacting_score
    )

    assert trial_first == {"trial_set": 1.0, "effect_source": 3.0}
    assert source_first == {"effect_source": 1.0, "trial_set": 3.0}
    assert trial_first["trial_set"] != source_first["trial_set"]
    assert sum(trial_first.values()) == pytest.approx(4.0)
    assert sum(source_first.values()) == pytest.approx(4.0)


def test_exact_shapley_bridge_splits_interaction_symmetrically() -> None:
    baseline = {"trial_set": 0.0, "effect_source": 0.0}
    target = {"trial_set": 1.0, "effect_source": 1.0}

    result = exact_shapley_bridge(
        baseline, target, ["trial_set", "effect_source"], interacting_score
    )

    assert result == {"trial_set": 2.0, "effect_source": 2.0}
    assert sum(result.values()) == pytest.approx(4.0)


def test_exact_bridge_caps_factorial_enumeration() -> None:
    factors = [f"f{i}" for i in range(9)]
    state = {name: 0 for name in factors}
    with pytest.raises(ValueError, match="too many factors"):
        exact_shapley_bridge(state, state, factors, lambda _: 0.0)
