"""Structured claim semantics for activating HF01 proof barriers.

The semantic flags are explicit capabilities of the endpoint claim.  They are
preferable to a free self-label because the strongest active capability derives
the required claim class.
"""

from __future__ import annotations

from dataclasses import dataclass

from .projection_protocol import ClaimType


@dataclass(frozen=True)
class ClaimSemantics:
    describes_observation: bool = False
    infers_latent_state: bool = False
    infers_intervention_response: bool = False
    asserts_target_reachability: bool = False

    def __post_init__(self) -> None:
        if not any(
            (
                self.describes_observation,
                self.infers_latent_state,
                self.infers_intervention_response,
                self.asserts_target_reachability,
            )
        ):
            raise ValueError("claim semantics must declare at least one capability")


def derive_claim_type(semantics: ClaimSemantics) -> ClaimType:
    """Derive the strongest HF01 claim class implied by endpoint semantics."""
    if semantics.asserts_target_reachability:
        return ClaimType.REACHABILITY
    if semantics.infers_intervention_response:
        return ClaimType.RESPONSE_INFERENCE
    if semantics.infers_latent_state:
        return ClaimType.STATE_INFERENCE
    return ClaimType.DESCRIPTIVE


def claim_type_matches(
    semantics: ClaimSemantics,
    declared: ClaimType,
) -> bool:
    return derive_claim_type(semantics) is declared
