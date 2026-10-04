"""Structural and claim-relative value-of-information helpers for HF01 probes.

V1 is deliberately topology-only: it measures how a candidate witness changes
evidence root-cut robustness and never converts evidence into a probability of
biological truth.

V2 adds experimental-design constraints without collapsing them into one magic
number.  Claim-critical properties are hard gates first; eligible probes can
then be compared by Pareto dominance and cost.  This prevents, for example,
strong evidence independence from numerically compensating for missing unit
linkage in a within-follicle prediction claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
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


class UnitLinkage(str, Enum):
    GROUP_ONLY = "GROUP_ONLY"
    DONOR_LINKED_REPLICATES = "DONOR_LINKED_REPLICATES"
    SAME_FOLLICLE = "SAME_FOLLICLE"
    SAME_PARTICIPANT_REGION = "SAME_PARTICIPANT_REGION"


class BackactionControl(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    FAIL = "FAIL"


class ProbeObjective(str, Enum):
    CROSS_SECTIONAL_STATE_COMPATIBILITY = "CROSS_SECTIONAL_STATE_COMPATIBILITY"
    BRANCH_IDENTIFICATION = "BRANCH_IDENTIFICATION"
    WITHIN_FOLLICLE_TEMPORAL_PREDICTION = "WITHIN_FOLLICLE_TEMPORAL_PREDICTION"
    PARTICIPANT_TEMPORAL_PREDICTION = "PARTICIPANT_TEMPORAL_PREDICTION"


@dataclass(frozen=True)
class ProbeDesignProfile:
    name: str
    structural_independence_gain: int
    branch_separation: float
    unit_linkage: UnitLinkage
    backaction_control: BackactionControl
    cost: float = 1.0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("probe name must be non-empty")
        if self.structural_independence_gain < 0:
            raise ValueError("structural_independence_gain must be >= 0")
        if not 0.0 <= self.branch_separation <= 1.0:
            raise ValueError("branch_separation must be in [0, 1]")
        if self.cost <= 0:
            raise ValueError("cost must be > 0")


@dataclass(frozen=True)
class ProbeEligibility:
    eligible: bool
    violations: tuple[str, ...]


def probe_eligibility(
    probe: ProbeDesignProfile,
    objective: ProbeObjective,
) -> ProbeEligibility:
    """Apply non-compensatory gates required by a claim objective."""
    violations: list[str] = []

    if objective is ProbeObjective.BRANCH_IDENTIFICATION:
        if probe.branch_separation <= 0.0:
            violations.append("branch_identification_requires_nonzero_separation")

    elif objective is ProbeObjective.WITHIN_FOLLICLE_TEMPORAL_PREDICTION:
        if probe.unit_linkage is not UnitLinkage.SAME_FOLLICLE:
            violations.append("within_follicle_prediction_requires_same_follicle_linkage")
        if probe.backaction_control is not BackactionControl.PASS:
            violations.append("within_follicle_prediction_requires_backaction_control")

    elif objective is ProbeObjective.PARTICIPANT_TEMPORAL_PREDICTION:
        if probe.unit_linkage is not UnitLinkage.SAME_PARTICIPANT_REGION:
            violations.append("participant_prediction_requires_same_participant_region")
        if probe.backaction_control is BackactionControl.FAIL:
            violations.append("participant_prediction_rejects_known_measurement_backaction")

    return ProbeEligibility(not violations, tuple(violations))


def _quality_vector(probe: ProbeDesignProfile) -> tuple[float, float, float]:
    backaction_quality = {
        BackactionControl.FAIL: 0.0,
        BackactionControl.UNKNOWN: 0.5,
        BackactionControl.PASS: 1.0,
    }[probe.backaction_control]
    return (
        float(probe.structural_independence_gain),
        probe.branch_separation,
        backaction_quality,
    )


def dominates_probe(
    left: ProbeDesignProfile,
    right: ProbeDesignProfile,
    *,
    objective: ProbeObjective,
) -> bool:
    """Return True when left Pareto-dominates right for an objective.

    Ineligible probes cannot dominate eligible probes.  Among eligible probes,
    quality dimensions are maximized and cost is minimized.  Unit-linkage is
    handled as a hard gate for objectives where it is inferentially mandatory,
    rather than assigned an arbitrary numeric weight.
    """
    left_ok = probe_eligibility(left, objective).eligible
    right_ok = probe_eligibility(right, objective).eligible
    if left_ok != right_ok:
        return left_ok
    if not left_ok:
        return False

    lq = _quality_vector(left)
    rq = _quality_vector(right)
    no_worse = all(a >= b for a, b in zip(lq, rq)) and left.cost <= right.cost
    strictly_better = any(a > b for a, b in zip(lq, rq)) or left.cost < right.cost
    return no_worse and strictly_better


def pareto_probe_front(
    probes: Iterable[ProbeDesignProfile],
    *,
    objective: ProbeObjective,
) -> tuple[str, ...]:
    probes_t = tuple(probes)
    eligible = tuple(p for p in probes_t if probe_eligibility(p, objective).eligible)
    front = []
    for candidate in eligible:
        if not any(
            dominates_probe(other, candidate, objective=objective)
            for other in eligible
            if other is not candidate
        ):
            front.append(candidate)
    return tuple(sorted(p.name for p in front))
