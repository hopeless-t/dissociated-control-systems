"""Evidence gate for measurement back-action in longitudinal observers.

A non-significant imaging-vs-sham difference is not evidence of negligible
back-action.  This helper uses a predeclared equivalence margin: PASS requires
the full confidence interval for the measurement effect on a downstream
functional outcome to lie inside [-margin, +margin], plus basic design
obligations.  It is generic experimental-design logic, not a claim that any
specific HF01 observer is already safe.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BackactionStatus(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class BackactionEvidence:
    effect: float
    ci_low: float
    ci_high: float
    equivalence_margin: float
    sham_controlled: bool
    environment_matched: bool
    time_matched: bool
    downstream_function_measured: bool
    dose_or_frequency_challenge: bool

    def __post_init__(self) -> None:
        if self.ci_low > self.ci_high:
            raise ValueError("ci_low must be <= ci_high")
        if self.equivalence_margin <= 0:
            raise ValueError("equivalence_margin must be > 0")


@dataclass(frozen=True)
class BackactionAssessment:
    status: BackactionStatus
    violations: tuple[str, ...]


def assess_backaction(evidence: BackactionEvidence) -> BackactionAssessment:
    """Classify a measurement observer as PASS / UNKNOWN / FAIL.

    FAIL is reserved for a confidence interval that lies wholly outside the
    declared equivalence region.  Overlap with a boundary remains UNKNOWN.
    PASS additionally requires the declared design controls.
    """
    violations: list[str] = []
    controls = {
        "missing_sham_control": evidence.sham_controlled,
        "environment_not_matched": evidence.environment_matched,
        "time_not_matched": evidence.time_matched,
        "downstream_function_not_measured": evidence.downstream_function_measured,
        "missing_dose_or_frequency_challenge": evidence.dose_or_frequency_challenge,
    }
    for name, satisfied in controls.items():
        if not satisfied:
            violations.append(name)

    margin = evidence.equivalence_margin
    if evidence.ci_low > margin or evidence.ci_high < -margin:
        return BackactionAssessment(
            BackactionStatus.FAIL,
            tuple(violations + ["effect_interval_outside_equivalence_region"]),
        )

    interval_equivalent = evidence.ci_low >= -margin and evidence.ci_high <= margin
    if interval_equivalent and not violations:
        return BackactionAssessment(BackactionStatus.PASS, ())

    if not interval_equivalent:
        violations.append("backaction_equivalence_not_established")
    return BackactionAssessment(BackactionStatus.UNKNOWN, tuple(violations))
