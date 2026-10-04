"""Evidence-preserving contracts for multi-stage DCS projections."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class EdgeGrounding(str, Enum):
    SUPPORTED = "SUPPORTED"
    ASSUMED = "ASSUMED"
    UNKNOWN = "UNKNOWN"
    FALSIFIED = "FALSIFIED"


class ClaimCeiling(str, Enum):
    GROUNDED = "GROUNDED"
    MODEL_ONLY = "MODEL_ONLY"
    UNKNOWN = "UNKNOWN"
    FALSIFIED = "FALSIFIED"


@dataclass(frozen=True)
class ProjectionEdge:
    source: str
    target: str
    grounding: EdgeGrounding
    mapping_rule: str
    evidence_note: str = ""
    uncertainty_note: str = ""


def claim_ceiling(edges: Iterable[ProjectionEdge]) -> ClaimCeiling:
    """Return the most restrictive epistemic ceiling on a projection path.

    Explanation smoothness must never promote evidence authority.
    """
    edges_t = tuple(edges)
    if not edges_t:
        return ClaimCeiling.UNKNOWN

    groundings = {edge.grounding for edge in edges_t}

    if EdgeGrounding.FALSIFIED in groundings:
        return ClaimCeiling.FALSIFIED
    if EdgeGrounding.UNKNOWN in groundings:
        return ClaimCeiling.UNKNOWN
    if EdgeGrounding.ASSUMED in groundings:
        return ClaimCeiling.MODEL_ONLY
    return ClaimCeiling.GROUNDED


def unsupported_edges(
    edges: Iterable[ProjectionEdge],
) -> tuple[ProjectionEdge, ...]:
    return tuple(
        edge
        for edge in edges
        if edge.grounding is not EdgeGrounding.SUPPORTED
    )


def can_present_as_empirical(edges: Iterable[ProjectionEdge]) -> bool:
    return claim_ceiling(edges) is ClaimCeiling.GROUNDED
