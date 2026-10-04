from dissociated_control_systems.probe_value import (
    prefer_probe_by_structural_gain,
    structural_probe_gain,
)
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


def w(name: str, *roots: str) -> EvidenceWitness:
    return EvidenceWitness(
        name,
        CheckpointRole.PROVENANCE,
        frozenset(roots),
        good(),
    )


def transcript_baseline():
    return (
        w("gse36169", "raw-36169", "shared-axis"),
        w("gse93766", "raw-93766", "shared-axis"),
    )


def test_third_same_axis_dataset_adds_zero_root_cut_gain() -> None:
    result = structural_probe_gain(
        CheckpointRole.PROVENANCE,
        transcript_baseline(),
        w("third-same-axis", "raw-third", "shared-axis"),
    )

    assert result.before_cut == 1
    assert result.after_cut == 1
    assert result.cut_gain == 0


def test_orthogonal_probe_adds_one_root_cut_unit() -> None:
    result = structural_probe_gain(
        CheckpointRole.PROVENANCE,
        transcript_baseline(),
        w("orthogonal-protein", "protein-localization-root"),
    )

    assert result.before_cut == 1
    assert result.after_cut == 2
    assert result.cut_gain == 1


def test_structural_gain_ranking_prefers_orthogonal_probe_at_equal_cost() -> None:
    ranked = prefer_probe_by_structural_gain(
        CheckpointRole.PROVENANCE,
        transcript_baseline(),
        (
            (w("same-axis", "new-raw", "shared-axis"), 1.0),
            (w("orthogonal", "new-protein-root"), 1.0),
        ),
    )

    assert ranked == ("orthogonal", "same-axis")


def test_cost_can_change_structural_priority() -> None:
    ranked = prefer_probe_by_structural_gain(
        CheckpointRole.PROVENANCE,
        transcript_baseline(),
        (
            (w("cheap-orthogonal", "root-a"), 1.0),
            (w("expensive-orthogonal", "root-b"), 10.0),
        ),
    )

    assert ranked[0] == "cheap-orthogonal"
