from dissociated_control_systems.cognitive_ood_challenge import (
    combined_shift,
    ood_challenge,
    train_means,
)
from dissociated_control_systems.cognitive_temporal_frontier import (
    BASE_FEATURES,
    make_dataset,
    prepare_representation,
)


def test_combined_shift_preserves_feature_schema():
    train = make_dataset(5, 91_000_000)
    _, norm, _ = prepare_representation(train, BASE_FEATURES)
    shifted = combined_shift(
        train,
        seed=91_100_000,
        norm=norm,
        train_means=train_means(train),
    )
    assert len(shifted) == len(train)
    for _, features in shifted:
        for feature in BASE_FEATURES:
            assert feature in features


def test_ood_challenge_returns_bounded_metrics():
    result = ood_challenge()
    assert 0.0 <= result["results"]["clean"]["ensemble_accuracy"] <= 1.0
    assert 0.0 <= result["adapted_combined"]["ensemble_accuracy"] <= 1.0
    assert isinstance(result["robust_fixed_point"], bool)
    assert isinstance(result["external_evidence_has_value"], bool)
