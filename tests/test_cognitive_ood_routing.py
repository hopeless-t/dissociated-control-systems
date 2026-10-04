from dissociated_control_systems.cognitive_ood_routing import (
    authority_routing_experiment,
    ood_score,
)
from dissociated_control_systems.cognitive_temporal_frontier import BASE_FEATURES


def test_explicit_missingness_forces_high_ood_score():
    features = {feature: 0.0 for feature in BASE_FEATURES}
    features["_missing_handoff_gap"] = 1.0
    stats = {feature: (0.0, 1.0) for feature in BASE_FEATURES}
    assert ood_score(features, stats) >= 1000.0


def test_authority_routing_metrics_are_bounded():
    result = authority_routing_experiment()
    for row in result["results"].values():
        assert 0.0 <= row["forced_accuracy"] <= 1.0
        assert 0.0 <= row["flag_rate"] <= 1.0
        assert 0.0 <= row["coverage"] <= 1.0
        assert 0.0 <= row["selective_accuracy"] <= 1.0
        assert 0.0 <= row["unsafe_accepted_error_rate"] <= 1.0
