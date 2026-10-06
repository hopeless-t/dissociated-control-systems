"""Longitudinal observation primitives for HF01.

Synthetic only. The purpose is to test whether an early hidden-state response
can reveal later recoverability before the coarse output itself clearly does.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .hair_follicle_model import (
    HFControl,
    HFState,
    simulate,
    state_from_lock,
)


@dataclass(frozen=True)
class InterventionProbeResult:
    early_regeneration_gain: float
    early_output_gain: float
    late_output_gain: float
    early_controlled: HFState
    early_counterfactual: HFState
    late_controlled: HFState
    late_counterfactual: HFState


def matched_visible_states(
    visible_output: float = 0.50,
    recoverable_lock: float = 0.20,
    locked_lock: float = 0.60,
) -> tuple[HFState, HFState]:
    """Return two latent states with identical visible H."""
    recoverable = replace(
        state_from_lock(recoverable_lock),
        hair_output=visible_output,
    )
    locked = replace(
        state_from_lock(locked_lock),
        hair_output=visible_output,
    )
    return recoverable, locked


def intervention_probe(
    initial: HFState,
    control: HFControl,
    early_steps: int = 80,
    late_steps: int = 2000,
) -> InterventionProbeResult:
    """Compare controlled trajectory against the no-input counterfactual."""
    early_controlled = simulate(initial, control, steps=early_steps)
    early_counterfactual = simulate(initial, HFControl(), steps=early_steps)
    late_controlled = simulate(initial, control, steps=late_steps)
    late_counterfactual = simulate(initial, HFControl(), steps=late_steps)

    return InterventionProbeResult(
        early_regeneration_gain=(
            early_controlled.regeneration - early_counterfactual.regeneration
        ),
        early_output_gain=(
            early_controlled.hair_output - early_counterfactual.hair_output
        ),
        late_output_gain=(
            late_controlled.hair_output - late_counterfactual.hair_output
        ),
        early_controlled=early_controlled,
        early_counterfactual=early_counterfactual,
        late_controlled=late_controlled,
        late_counterfactual=late_counterfactual,
    )


def canonical_longitudinal_probe() -> dict[str, InterventionProbeResult]:
    recoverable, locked = matched_visible_states()
    control = HFControl(behavioral=1.0, antiandrogen=1.0)
    return {
        "recoverable": intervention_probe(recoverable, control),
        "locked": intervention_probe(locked, control),
    }
