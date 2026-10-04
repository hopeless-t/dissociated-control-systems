from dissociated_control_systems.projection_gap import (
    ProjectionGap,
    classify_projection_gap,
    recommended_response,
)


def test_epistemic_gap_is_not_repaired_by_more_explanation() -> None:
    gap = classify_projection_gap(epistemic_gap=0.9, cognitive_gap=0.1)

    assert gap is ProjectionGap.EPISTEMIC
    assert "collect_or_validate_evidence" in recommended_response(gap)
    assert "insert_intermediate_representation" not in recommended_response(gap)


def test_cognitive_gap_prefers_intermediate_projection() -> None:
    gap = classify_projection_gap(epistemic_gap=0.1, cognitive_gap=0.9)

    assert gap is ProjectionGap.COGNITIVE
    assert "insert_intermediate_representation" in recommended_response(gap)
    assert "collect_or_validate_evidence" not in recommended_response(gap)


def test_both_gap_requires_both_actions() -> None:
    gap = classify_projection_gap(epistemic_gap=0.8, cognitive_gap=0.8)
    actions = recommended_response(gap)

    assert gap is ProjectionGap.BOTH
    assert "collect_or_validate_evidence" in actions
    assert "insert_intermediate_representation" in actions


def test_low_low_gap_collapses_redundant_steps() -> None:
    gap = classify_projection_gap(epistemic_gap=0.1, cognitive_gap=0.1)

    assert gap is ProjectionGap.NONE
    assert recommended_response(gap) == (
        "collapse_redundant_projection_steps",
    )
