"""Fail-closed reachability decisions for HF01 synthetic state sets."""

from __future__ import annotations

from enum import Enum
from typing import Iterable

from .hair_follicle_model import HFControl, HFState, simulate


class ReachabilityDecision(str, Enum):
    RECOVERABLE = "RECOVERABLE"
    NONRECOVERABLE = "NONRECOVERABLE"
    UNKNOWN = "UNKNOWN"


def state_reaches_output(
    state: HFState,
    control: HFControl,
    output_threshold: float = 0.50,
    steps: int = 2000,
) -> bool:
    final = simulate(state, control=control, steps=steps)
    return final.hair_output >= output_threshold


def robust_reachability_decision(
    candidate_states: Iterable[HFState],
    control: HFControl,
    output_threshold: float = 0.50,
    steps: int = 2000,
) -> ReachabilityDecision:
    """Classify only when every state still compatible with evidence agrees."""
    states = tuple(candidate_states)
    if not states:
        return ReachabilityDecision.UNKNOWN

    outcomes = {
        state_reaches_output(
            state,
            control=control,
            output_threshold=output_threshold,
            steps=steps,
        )
        for state in states
    }

    if outcomes == {True}:
        return ReachabilityDecision.RECOVERABLE
    if outcomes == {False}:
        return ReachabilityDecision.NONRECOVERABLE
    return ReachabilityDecision.UNKNOWN
