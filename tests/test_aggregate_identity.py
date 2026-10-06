from dissociated_control_systems.aggregate_identity import compare_aggregate_n


def test_preprint_reported_n_matches_own_trial_counts() -> None:
    pairs = [
        (80, 80),
        (110, 110),
        (64, 65),
        (158, 77),
        (64, 61),
        (62, 62),
        (154, 149),
        (89, 89),
        (147, 80),
        (92, 94),
        (68, 68),
        (136, 135),
    ]
    result = compare_aggregate_n(
        reported_n=2294,
        displayed_pairs=pairs,
        own_identity_pairs=pairs,
    )
    assert result["reported_matches_displayed"] is True
    assert result["reported_matches_own_identity"] is True
    assert result["status"] == "NO_SPECIFIC_DISPLAY_VECTOR_CONFLICT"


def test_final_reported_n_matches_displayed_cross_bound_vector_not_own_trial_vector() -> None:
    displayed = [
        (80, 80),
        (136, 135),
        (92, 94),
        (62, 62),
        (30, 36),
        (114, 113),
        (110, 110),
        (29, 33),
        (89, 89),
        (154, 149),
        (158, 77),
        (64, 61),
        (214, 114),
        (96, 102),
    ]
    own_trial_randomized_or_declared = [
        (80, 80),
        (110, 110),
        (214, 114),
        (96, 102),
        (64, 65),
        (158, 77),
        (64, 61),
        (62, 62),
        (89, 89),
        (92, 94),
        (147, 80),
        (68, 68),
        (136, 135),
        (154, 149),
    ]
    result = compare_aggregate_n(
        reported_n=2683,
        displayed_pairs=displayed,
        own_identity_pairs=own_trial_randomized_or_declared,
    )
    assert result["displayed_count_total"] == 2683
    assert result["own_identity_count_total"] == 2820
    assert result["reported_matches_displayed"] is True
    assert result["reported_matches_own_identity"] is False
    assert result["own_identity_minus_reported"] == 137
    assert result["status"] == "AGGREGATE_N_IDENTITY_CONFLICT_CANDIDATE"
