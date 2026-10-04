import pytest

from dissociated_control_systems.evidence_binding import (
    CanonicalEvidence,
    DisplayedEvidence,
    build_canonical_index,
    classify_binding,
)


def test_own_identity_consistent_known_answer() -> None:
    canonical = build_canonical_index(
        [CanonicalEvidence("A", 80, 80, 0.512, 0.172, 1.522)]
    )
    row = DisplayedEvidence("r1", "A", 80, 80, 0.51, 0.17, 1.52)
    result = classify_binding(row, canonical)
    assert result["status"] == "OWN_IDENTITY_CONSISTENT"
    assert result["own_count_match"] is True
    assert result["own_effect_match"] is True


def test_counts_can_match_other_trial_while_effect_matches_label() -> None:
    canonical = build_canonical_index(
        [
            CanonicalEvidence("BAO", 110, 110, 0.653, 0.427, 0.998),
            CanonicalEvidence("KUCHLER", 136, 135, 0.653, 0.495, 0.861),
        ]
    )
    row = DisplayedEvidence("r2", "BAO", 136, 135, 0.65, 0.43, 1.00)
    result = classify_binding(row, canonical)
    assert result["status"] == "COUNT_CROSS_BINDING_CANDIDATE"
    assert result["count_matches"] == ("KUCHLER",)
    assert result["effect_matches"] == ("BAO",)


def test_complete_other_trial_tuple_is_cross_binding_candidate() -> None:
    canonical = build_canonical_index(
        [
            CanonicalEvidence("KISSANE", 147, 80, 0.920, 0.690, 1.240),
            CanonicalEvidence("GOODWIN", 158, 77, 1.060, 0.780, 1.450),
        ]
    )
    row = DisplayedEvidence("r11", "KISSANE", 158, 77, 1.06, 0.78, 1.45)
    result = classify_binding(row, canonical)
    assert result["status"] == "CROSS_BINDING_CANDIDATE"
    assert result["count_matches"] == ("GOODWIN",)
    assert result["effect_matches"] == ("GOODWIN",)


def test_same_counts_can_have_multiple_candidate_sources() -> None:
    canonical = build_canonical_index(
        [
            CanonicalEvidence("A", 50, 50),
            CanonicalEvidence("B", 50, 50),
        ]
    )
    row = DisplayedEvidence("r", "C", 50, 50, 1.0, 0.8, 1.2)
    result = classify_binding(row, canonical)
    assert result["count_matches"] == ("A", "B")
    assert result["status"] == "CROSS_BINDING_CANDIDATE"


def test_multiple_population_snapshots_do_not_create_multiple_trials() -> None:
    canonical = build_canonical_index(
        [
            CanonicalEvidence(
                "EDELMAN",
                62,
                62,
                evidence_id="EDELMAN:randomized",
            ),
            CanonicalEvidence(
                "EDELMAN",
                60,
                61,
                1.323,
                0.841,
                2.080,
                evidence_id="EDELMAN:survival-analysis",
            ),
        ]
    )
    row = DisplayedEvidence("r", "EDELMAN", 62, 62, 1.0, 0.8, 1.2)
    result = classify_binding(row, canonical)
    assert result["count_matches"] == ("EDELMAN:randomized",)
    assert result["count_match_trial_ids"] == ("EDELMAN",)
    assert result["own_count_match"] is True
    assert result["status"] == "EFFECT_SOURCE_CONFLICT_OR_DERIVATION"


def test_equal_numbers_with_different_field_semantics_are_not_identity_match() -> None:
    canonical = build_canonical_index(
        [
            CanonicalEvidence(
                "ANDERSEN",
                29,
                33,
                evidence_id="ANDERSEN:recurrence-events",
                count_semantics="recurrence_event_count",
            )
        ]
    )
    row = DisplayedEvidence("r", "EDELMAN", 29, 33, 0.96, 0.78, 1.19)
    result = classify_binding(row, canonical)
    assert result["count_matches"] == ()
    assert result["cross_semantic_count_matches"] == (
        "ANDERSEN:recurrence-events",
    )
    assert result["cross_semantic_count_match_trial_ids"] == ("ANDERSEN",)
    assert result["status"] == "COUNT_SEMANTIC_COLLISION_CANDIDATE"


def test_missing_effect_in_canonical_stays_unresolved_not_fabricated() -> None:
    canonical = build_canonical_index([CanonicalEvidence("A", 10, 10)])
    row = DisplayedEvidence("r", "A", 10, 10, 1.03, 0.87, 1.21)
    result = classify_binding(row, canonical)
    assert result["own_count_match"] is True
    assert result["own_effect_match"] is False
    assert result["status"] == "EFFECT_SOURCE_CONFLICT_OR_DERIVATION"


def test_invalid_canonical_interval_fails_closed() -> None:
    with pytest.raises(ValueError):
        CanonicalEvidence("A", 10, 10, 1.2, 1.3, 1.4)
