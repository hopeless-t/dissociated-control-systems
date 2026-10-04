"""Structural value-of-information helpers for choosing the next HF01 probe.

The metric is deliberately topology-only: it measures how a candidate witness
changes evidence root-cut robustness. It does not convert evidence into a
probability of biological truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .evidence_topology import role_root_cut
from .projection_assurance import EvidenceWitness
from .projection_protocol import CheckpointRole


@dataclass(frozen=True)
class ProbeGain:
    before_cut: int | None
    after_cut: int | None
    cut_gain: int
    cost: float
    gain_per_cost: float


def structural_probe_gain(
    role: CheckpointRole,
    existing: Iterable[EvidenceWitness],
    candidate: EvidenceWitness,
    *,
    cost: float = 1.0,
) -> ProbeGain:
    if cost <= 0:
        raise ValueError("cost must be > 0")

    existing_t = tuple(existing)
    before = role_root_cut(role, existing_t)
    after = role_root_cut(role, existing_t + (candidate,))

    before_n = 0 if before is None else before
    after_n = 0 if after is None else after
    gain = after_n - before_n

    return ProbeGain(
        before_cut=before,
        after_cut=after,
        cut_gain=gain,
        cost=cost,
        gain_per_cost=gain / cost,
    )


def prefer_probe_by_structural_gain(
    role: CheckpointRole,
    existing: Iterable[EvidenceWitness],
    candidates: Iterable[tuple[EvidenceWitness, float]],
) -> tuple[str, ...]:
    """Rank candidate witness IDs by root-cut gain/cost, then raw gain."""
    scored = []
    for witness, cost in candidates:
        gain = structural_probe_gain(role, existing, witness, cost=cost)
        scored.append(
            (
                -gain.gain_per_cost,
                -gain.cut_gain,
                cost,
                witness.witness_id,
            )
        )
    scored.sort()
    return tuple(item[-1] for item in scored)
