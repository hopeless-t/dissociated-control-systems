"""Synthetic counterexample for collapsing ECM remodeling and mechanics.

E = ECM/fibrogenic remodeling coordinate.
M = mechanical/contractile coordinate.
F_reduced = (E + M) / 2 is a deliberately lossy reduced representation.

The model shows that equal F_reduced does not determine response when an
actuator targets only one structural coordinate.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralState:
    ecm: float
    mechanical: float

    @property
    def reduced_f(self) -> float:
        return 0.5 * (self.ecm + self.mechanical)


@dataclass(frozen=True)
class StructuralResponse:
    initial: StructuralState
    final: StructuralState

    @property
    def reduced_change(self) -> float:
        return self.final.reduced_f - self.initial.reduced_f


def mechanical_relaxation(
    state: StructuralState,
    *,
    strength: float = 1.0,
) -> StructuralResponse:
    """Actuator reduces M only; E is unchanged in this counterexample."""
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be in [0, 1]")
    final = StructuralState(
        ecm=state.ecm,
        mechanical=state.mechanical * (1.0 - strength),
    )
    return StructuralResponse(initial=state, final=final)


def ecm_remodeling_intervention(
    state: StructuralState,
    *,
    strength: float = 1.0,
) -> StructuralResponse:
    """Actuator reduces E only; M is unchanged in this counterexample."""
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be in [0, 1]")
    final = StructuralState(
        ecm=state.ecm * (1.0 - strength),
        mechanical=state.mechanical,
    )
    return StructuralResponse(initial=state, final=final)


def matched_reduced_states() -> tuple[StructuralState, StructuralState]:
    """Two hidden structural states with identical reduced F=0.5."""
    return (
        StructuralState(ecm=1.0, mechanical=0.0),
        StructuralState(ecm=0.0, mechanical=1.0),
    )
