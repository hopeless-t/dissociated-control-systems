"""Transition-specific mechanism scope contracts for RQ-005.

A mechanism proposed for one disease transition must not be silently promoted to
an explanation of another transition.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Transition(str, Enum):
    DIAGNOSIS_TO_RECURRENCE = "diagnosis_to_recurrence"
    RECURRENCE_TO_CANCER_DEATH = "recurrence_to_cancer_death"


@dataclass(frozen=True)
class MechanismClaim:
    name: str
    supported_transitions: frozenset[Transition]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("mechanism name must not be empty")
        if not self.supported_transitions:
            raise ValueError("mechanism must declare at least one transition scope")

    def supports(self, transition: Transition) -> bool:
        return transition in self.supported_transitions


def require_transition_support(
    claim: MechanismClaim,
    transition: Transition,
) -> None:
    if not claim.supports(transition):
        raise ValueError(
            f"mechanism {claim.name!r} is not scoped to transition {transition.value!r}"
        )


def classic_pre_recurrence_dormancy_claim() -> MechanismClaim:
    """Known-answer scope: classic DTC dormancy explains delayed overt recurrence.

    This intentionally does not assert a mechanism for durable control after an
    already established clinical recurrence.
    """
    return MechanismClaim(
        name="classic_pre_recurrence_dtc_dormancy",
        supported_transitions=frozenset({Transition.DIAGNOSIS_TO_RECURRENCE}),
    )
