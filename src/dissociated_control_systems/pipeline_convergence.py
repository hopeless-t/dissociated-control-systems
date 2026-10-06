"""Independent-observer convergence checks for RQ-005 evidence pipelines.

A revision may update one analysis/rendering pipeline while another observer
surface retains an older state. These helpers make that disagreement explicit
without deciding which pipeline is correct.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class PipelineObservation:
    pipeline_id: str
    snapshot_id: str
    analysis_id: str
    estimate: float
    lower: float
    upper: float

    def __post_init__(self) -> None:
        for name in ("pipeline_id", "snapshot_id", "analysis_id"):
            value = getattr(self, name)
            if not value.strip() or value != value.strip():
                raise ValueError(f"{name} must be non-empty and normalized")
        if not all(isfinite(float(value)) and float(value) > 0 for value in (self.estimate, self.lower, self.upper)):
            raise ValueError("ratio-scale observations must be positive and finite")
        if not self.lower <= self.estimate <= self.upper:
            raise ValueError("estimate must lie inside interval")


def reconcile_pipelines(
    observations: Iterable[PipelineObservation],
    *,
    tolerance: float = 0.005,
) -> dict[str, object]:
    items = tuple(observations)
    if len(items) < 2:
        raise ValueError("at least two pipeline observations are required")
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")

    analysis_ids = {item.analysis_id for item in items}
    if len(analysis_ids) != 1:
        raise ValueError("different declared analyses cannot be compared as one pipeline state")

    pipeline_ids = [item.pipeline_id for item in items]
    if len(set(pipeline_ids)) != len(pipeline_ids):
        raise ValueError("pipeline_id must be unique within one reconciliation")

    point_span = max(item.estimate for item in items) - min(item.estimate for item in items)
    lower_span = max(item.lower for item in items) - min(item.lower for item in items)
    upper_span = max(item.upper for item in items) - min(item.upper for item in items)
    snapshots = tuple(sorted({item.snapshot_id for item in items}))

    if point_span <= tolerance and lower_span <= tolerance and upper_span <= tolerance:
        status = "PIPELINES_CONVERGED"
    else:
        status = "PIPELINE_STATE_DIVERGENCE"

    return {
        "analysis_id": items[0].analysis_id,
        "status": status,
        "pipeline_count": len(items),
        "snapshot_ids": snapshots,
        "point_span": point_span,
        "lower_span": lower_span,
        "upper_span": upper_span,
        "observations": tuple(
            {
                "pipeline_id": item.pipeline_id,
                "snapshot_id": item.snapshot_id,
                "estimate": item.estimate,
                "lower": item.lower,
                "upper": item.upper,
            }
            for item in items
        ),
    }
