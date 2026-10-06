"""Classify whether a projection failure is epistemic, cognitive, or both."""

from __future__ import annotations

from enum import Enum


class ProjectionGap(str, Enum):
    NONE = "NONE"
    COGNITIVE = "COGNITIVE"
    EPISTEMIC = "EPISTEMIC"
    BOTH = "BOTH"


def classify_projection_gap(
    *,
    epistemic_gap: float,
    cognitive_gap: float,
    threshold: float = 0.5,
) -> ProjectionGap:
    """Classify normalized gap scores in [0, 1].

    epistemic_gap:
        Missing measurement/causal/evidence connection.

    cognitive_gap:
        Existing connection is too semantically compressed for reliable
        reconstruction by the intended reader.
    """
    if not 0 <= epistemic_gap <= 1:
        raise ValueError("epistemic_gap must be in [0, 1]")
    if not 0 <= cognitive_gap <= 1:
        raise ValueError("cognitive_gap must be in [0, 1]")
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be in [0, 1]")

    e_high = epistemic_gap >= threshold
    c_high = cognitive_gap >= threshold

    if e_high and c_high:
        return ProjectionGap.BOTH
    if e_high:
        return ProjectionGap.EPISTEMIC
    if c_high:
        return ProjectionGap.COGNITIVE
    return ProjectionGap.NONE


def recommended_response(gap: ProjectionGap) -> tuple[str, ...]:
    if gap is ProjectionGap.EPISTEMIC:
        return ("collect_or_validate_evidence", "preserve_unknown")
    if gap is ProjectionGap.COGNITIVE:
        return ("insert_intermediate_representation", "test_reconstruction")
    if gap is ProjectionGap.BOTH:
        return (
            "collect_or_validate_evidence",
            "insert_intermediate_representation",
            "preserve_unknown",
            "test_reconstruction",
        )
    return ("collapse_redundant_projection_steps",)
