"""Recovery gate for active diagnostic perturbations.

Estimating local susceptibility requires an input.  That input can itself move
the biological system onto a different trajectory.  Before an early-response
measurement is reused as a predictor of a later baseline-like trajectory, HF01
therefore requires evidence that the diagnostic challenge has washed out to a
predeclared equivalence region on declared state/output proxies.

This is generic experimental-design logic, not a claim that any specific
challenge is biologically reversible.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ProbeRecoveryStatus(str, Enum):
    PASS = "PASS"
    UNKNOWN = "UNKNOWN"
    FAIL = "FAIL"


@dataclass(frozen=True)
class ProbeRecoveryEvidence:
    post_washout_effect: float
    ci_low: float
    ci_high: float
    equivalence_margin: float
    sham_challenge_control: bool
    washout_interval_predeclared: bool
    same_state_proxy_remeasured: bool
    later_function_controlled: bool

    def __post_init__(self) -> None:
        if self.ci_low > self.ci_high:
            raise ValueError("ci_low must be <= ci_high")
        if self.equivalence_margin <= 0:
            raise ValueError("equivalence_margin must be > 0")


@dataclass(frozen=True)
class ProbeRecoveryAssessment:
    status: ProbeRecoveryStatus
    violations: tuple[str, ...]


def assess_probe_recovery(
    evidence: ProbeRecoveryEvidence,
) -> ProbeRecoveryAssessment:
    violations: list[str] = []
    obligations = {
        "missing_sham_challenge_control": evidence.sham_challenge_control,
        "washout_interval_not_predeclared": evidence.washout_interval_predeclared,
        "state_proxy_not_remeasured_after_washout": evidence.same_state_proxy_remeasured,
        "later_function_not_controlled": evidence.later_function_controlled,
    }
    for label, passed in obligations.items():
        if not passed:
            violations.append(label)

    margin = evidence.equivalence_margin
    if evidence.ci_low > margin or evidence.ci_high < -margin:
        return ProbeRecoveryAssessment(
            ProbeRecoveryStatus.FAIL,
            tuple(violations + ["persistent_probe_effect_outside_equivalence_region"]),
        )

    equivalent = evidence.ci_low >= -margin and evidence.ci_high <= margin
    if equivalent and not violations:
        return ProbeRecoveryAssessment(ProbeRecoveryStatus.PASS, ())

    if not equivalent:
        violations.append("post_probe_recovery_not_established")
    return ProbeRecoveryAssessment(ProbeRecoveryStatus.UNKNOWN, tuple(violations))
