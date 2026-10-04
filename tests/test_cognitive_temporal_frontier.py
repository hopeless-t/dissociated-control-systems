from dissociated_control_systems.cognitive_harness_repair import run_episode
from dissociated_control_systems.cognitive_temporal_frontier import (
    TEMPORAL_FEATURES,
    temporal_frontier,
)


def test_episode_exposes_temporal_features():
    features = run_episode(frozenset(), 7, steps=60).features
    for feature in TEMPORAL_FEATURES:
        assert feature in features


def test_temporal_frontier_is_bounded_by_its_oracle_union():
    result = temporal_frontier()
    temporal = result["temporal"]
    assert temporal["ensemble_accuracy"] <= temporal["oracle_union_accuracy"] + 1e-12
