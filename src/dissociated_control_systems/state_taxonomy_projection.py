"""Lossy projection from HF01 biological taxonomy v2 into legacy coordinates.

The map exists to make explicit when the older reduced-order model can hide
actuator-relevant distinctions.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BiologicalStateV2:
    dht_input: float
    ar_signal: float
    stress_context: float
    regenerative: float
    progenitor: float
    niche: float
    ecm_remodeling: float
    mechanical: float
    hysteretic_lock: float
    hair_output: float


@dataclass(frozen=True)
class LegacyProjection:
    androgen: float
    stress: float
    regeneration: float
    progenitor: float
    niche: float
    structural_lock: float
    hair_output: float


def project_to_legacy(state: BiologicalStateV2) -> LegacyProjection:
    """Deliberately lossy reduced projection used only for counterexamples."""
    androgen = (state.dht_input + state.ar_signal + state.mechanical) / 3.0
    structural = (
        state.ecm_remodeling
        + state.mechanical
        + state.hysteretic_lock
    ) / 3.0
    return LegacyProjection(
        androgen=androgen,
        stress=state.stress_context,
        regeneration=state.regenerative,
        progenitor=state.progenitor,
        niche=state.niche,
        structural_lock=structural,
        hair_output=state.hair_output,
    )


def matched_legacy_states() -> tuple[BiologicalStateV2, BiologicalStateV2]:
    """Two v2 states with equal legacy A/F but different active branches."""
    common = dict(
        stress_context=0.2,
        regenerative=0.7,
        progenitor=0.7,
        niche=0.8,
        hysteretic_lock=0.0,
        hair_output=0.6,
    )
    return (
        BiologicalStateV2(
            dht_input=1.0,
            ar_signal=0.5,
            ecm_remodeling=1.0,
            mechanical=0.0,
            **common,
        ),
        BiologicalStateV2(
            dht_input=0.5,
            ar_signal=0.0,
            ecm_remodeling=0.0,
            mechanical=1.0,
            **common,
        ),
    )
