"""Failure-injection sentinels for the HF01 proof kernel.

These are not a full mutation-testing framework. Each case encodes a realistic
kernel bug that previously existed or is easy to introduce, then checks that the
current normative path rejects it.
"""

from dissociated_control_systems.projection_assurance import (
    Defeater,
    DefeaterStatus,
    EvidenceWitness,
    ObligationStatus,
    WitnessObligations,
    validate_evidence_bound_certificate,
)
from dissociated_control_systems.projection_protocol import (
    CheckpointRecord,
    CheckpointRole,
    CheckStatus,
    ClaimType,
    ProjectionCertificate,
)
from dissociated_control_systems.projection_validator_v2 import (
    validate_projection_certificate_v2,
)
from dissociated_control_systems.support_graph import (
    SupportEdge,
    SupportNode,
    SupportNodeKind,
    claim_is_grounded,
)


def good() -> WitnessObligations:
    return WitnessObligations(
        source_authenticity=ObligationStatus.PASS,
        claim_relevance=ObligationStatus.PASS,
        scope_compatibility=ObligationStatus.PASS,
        transformation_reproducibility=ObligationStatus.PASS,
    )


def witness(name: str, role: CheckpointRole) -> EvidenceWitness:
    return EvidenceWitness(name, role, frozenset({f"root-{name}"}), good())


def test_sentinel_kills_extra_unknown_false_block_mutant() -> None:
    cert = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.REACHABILITY, CheckStatus.UNKNOWN),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )

    # A mutant that aggregates every record would return UNKNOWN here.
    result = validate_projection_certificate_v2(cert)
    assert result.accepted
    assert result.terminal_status is CheckStatus.PASS


def test_sentinel_kills_duplicate_role_ambiguity_mutant() -> None:
    cert = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )

    result = validate_projection_certificate_v2(cert)
    assert not result.accepted
    assert "duplicate_required_role:PROVENANCE" in result.violations


def test_sentinel_kills_pass_without_applicable_witness_mutant() -> None:
    cert = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )
    irrelevant = EvidenceWitness(
        "irrelevant",
        CheckpointRole.PROVENANCE,
        frozenset({"authentic-paper"}),
        WitnessObligations(
            source_authenticity=ObligationStatus.PASS,
            claim_relevance=ObligationStatus.FAIL,
            scope_compatibility=ObligationStatus.PASS,
            transformation_reproducibility=ObligationStatus.PASS,
        ),
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=(
            irrelevant,
            witness("unc", CheckpointRole.UNCERTAINTY),
        ),
    )
    assert not result.accepted
    assert "pass_without_usable_witness:PROVENANCE" in result.violations


def test_sentinel_kills_open_defeater_ignored_mutant() -> None:
    cert = ProjectionCertificate(
        records=(
            CheckpointRecord(CheckpointRole.PROVENANCE, CheckStatus.PASS),
            CheckpointRecord(CheckpointRole.UNCERTAINTY, CheckStatus.PASS),
        ),
        claim_type=ClaimType.DESCRIPTIVE,
        empirical_authority_requested=True,
    )

    result = validate_evidence_bound_certificate(
        cert,
        witnesses=(
            witness("prov", CheckpointRole.PROVENANCE),
            witness("unc", CheckpointRole.UNCERTAINTY),
        ),
        defeaters=(
            Defeater(
                "open-scope",
                CheckpointRole.UNCERTAINTY,
                DefeaterStatus.OPEN,
            ),
        ),
    )

    assert not result.accepted
    assert result.terminal_status is CheckStatus.UNKNOWN


def test_sentinel_kills_circular_support_mutant() -> None:
    nodes = (
        SupportNode("claim-a", SupportNodeKind.CLAIM),
        SupportNode("claim-b", SupportNodeKind.CLAIM),
    )
    edges = (
        SupportEdge("claim-a", "claim-b"),
        SupportEdge("claim-b", "claim-a"),
    )

    assert not claim_is_grounded("claim-a", nodes, edges)
