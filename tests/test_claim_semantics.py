import pytest

from dissociated_control_systems.claim_semantics import (
    ClaimSemantics,
    claim_type_matches,
    derive_claim_type,
)
from dissociated_control_systems.projection_protocol import ClaimType


def test_pure_observation_is_descriptive() -> None:
    semantics = ClaimSemantics(describes_observation=True)

    assert derive_claim_type(semantics) is ClaimType.DESCRIPTIVE


def test_latent_state_inference_activates_state_class() -> None:
    semantics = ClaimSemantics(
        describes_observation=True,
        infers_latent_state=True,
    )

    assert derive_claim_type(semantics) is ClaimType.STATE_INFERENCE


def test_response_capability_dominates_state_capability() -> None:
    semantics = ClaimSemantics(
        infers_latent_state=True,
        infers_intervention_response=True,
    )

    assert derive_claim_type(semantics) is ClaimType.RESPONSE_INFERENCE


def test_reachability_is_strongest_claim_class() -> None:
    semantics = ClaimSemantics(
        describes_observation=True,
        infers_latent_state=True,
        infers_intervention_response=True,
        asserts_target_reachability=True,
    )

    assert derive_claim_type(semantics) is ClaimType.REACHABILITY


def test_reachability_cannot_be_self_labeled_descriptive() -> None:
    semantics = ClaimSemantics(asserts_target_reachability=True)

    assert not claim_type_matches(semantics, ClaimType.DESCRIPTIVE)
    assert claim_type_matches(semantics, ClaimType.REACHABILITY)


def test_empty_semantics_fail_closed() -> None:
    with pytest.raises(ValueError):
        ClaimSemantics()
