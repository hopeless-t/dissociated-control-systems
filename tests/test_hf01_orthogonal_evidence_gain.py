from dissociated_control_systems.evidence_topology import role_root_cut
from dissociated_control_systems.projection_assurance import (
    EvidenceWitness,
    ObligationStatus,
    WitnessObligations,
)
from dissociated_control_systems.projection_protocol import CheckpointRole


def good() -> WitnessObligations:
    return WitnessObligations(
        source_authenticity=ObligationStatus.PASS,
        claim_relevance=ObligationStatus.PASS,
        scope_compatibility=ObligationStatus.PASS,
        transformation_reproducibility=ObligationStatus.PASS,
    )


def test_orthogonal_measurement_family_raises_regenerative_candidate_root_cut() -> None:
    transcript_only = (
        EvidenceWitness(
            "gse36169",
            CheckpointRole.PROVENANCE,
            frozenset(
                {
                    "GSE36169-raw",
                    "analyze_gse36169.py",
                    "HF01_GSE36169_AXES.json",
                }
            ),
            good(),
        ),
        EvidenceWitness(
            "gse93766",
            CheckpointRole.PROVENANCE,
            frozenset(
                {
                    "GSE93766-raw",
                    "analyze_gse93766.py",
                    "HF01_GSE36169_AXES.json",
                }
            ),
            good(),
        ),
    )

    assert role_root_cut(CheckpointRole.PROVENANCE, transcript_only) == 1

    orthogonal = transcript_only + (
        EvidenceWitness(
            "lu-2016-protein-localization",
            CheckpointRole.PROVENANCE,
            frozenset({"PMID-27472703-protein-localization-perturbation"}),
            good(),
        ),
    )

    assert role_root_cut(CheckpointRole.PROVENANCE, orthogonal) == 2
