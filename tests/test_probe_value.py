from dissociated_control_systems.probe_value import (
    BackactionControl,
    ProbeDesignProfile,
    ProbeObjective,
    UnitLinkage,
    dominates_probe,
    pareto_probe_front,
    prefer_probe_by_structural_gain,
    probe_eligibility,
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


def profile(
    name: str,
    *,
    gain: int = 1,
    separation: float = 1.0,
    linkage: UnitLinkage = UnitLinkage.GROUP_ONLY,
    backaction: BackactionControl = BackactionControl.UNKNOWN,
    cost: float = 1.0,
) -> ProbeDesignProfile:
    return ProbeDesignProfile(
        name=name,
        structural_independence_gain=gain,
        branch_separation=separation,
        unit_linkage=linkage,
        backaction_control=backaction,
        cost=cost,
    )


def test_destructive_orthogonal_probe_cannot_buy_within_follicle_authority() -> None:
    destructive = profile(
        "destructive-protein",
        gain=3,
        separation=1.0,
        linkage=UnitLinkage.GROUP_ONLY,
        backaction=BackactionControl.PASS,
        cost=0.1,
    )

    result = probe_eligibility(
        destructive,
        ProbeObjective.WITHIN_FOLLICLE_TEMPORAL_PREDICTION,
    )

    assert not result.eligible
    assert (
        "within_follicle_prediction_requires_same_follicle_linkage"
        in result.violations
    )


def test_same_follicle_observer_with_unknown_backaction_is_not_yet_eligible() -> None:
    imaging = profile(
        "live-width-imaging",
        linkage=UnitLinkage.SAME_FOLLICLE,
        backaction=BackactionControl.UNKNOWN,
    )

    result = probe_eligibility(
        imaging,
        ProbeObjective.WITHIN_FOLLICLE_TEMPORAL_PREDICTION,
    )

    assert not result.eligible
    assert "within_follicle_prediction_requires_backaction_control" in result.violations


def test_same_follicle_observer_becomes_eligible_after_backaction_control() -> None:
    imaging = profile(
        "live-width-imaging",
        linkage=UnitLinkage.SAME_FOLLICLE,
        backaction=BackactionControl.PASS,
    )

    assert probe_eligibility(
        imaging,
        ProbeObjective.WITHIN_FOLLICLE_TEMPORAL_PREDICTION,
    ).eligible


def test_branch_identification_requires_nonzero_measured_separation() -> None:
    same_direction = profile("same-direction", separation=0.0)

    result = probe_eligibility(
        same_direction,
        ProbeObjective.BRANCH_IDENTIFICATION,
    )

    assert not result.eligible


def test_eligible_probe_dominates_ineligible_probe_for_target_objective() -> None:
    eligible = profile(
        "same-unit-controlled",
        gain=0,
        separation=0.2,
        linkage=UnitLinkage.SAME_FOLLICLE,
        backaction=BackactionControl.PASS,
        cost=10.0,
    )
    ineligible = profile(
        "cheap-destructive",
        gain=5,
        separation=1.0,
        linkage=UnitLinkage.GROUP_ONLY,
        backaction=BackactionControl.PASS,
        cost=0.1,
    )

    assert dominates_probe(
        eligible,
        ineligible,
        objective=ProbeObjective.WITHIN_FOLLICLE_TEMPORAL_PREDICTION,
    )


def test_pareto_front_retains_non_dominated_tradeoffs_instead_of_magic_score() -> None:
    probes = (
        profile(
            "cheap",
            gain=1,
            separation=0.5,
            linkage=UnitLinkage.SAME_FOLLICLE,
            backaction=BackactionControl.PASS,
            cost=1.0,
        ),
        profile(
            "strong-but-expensive",
            gain=2,
            separation=0.9,
            linkage=UnitLinkage.SAME_FOLLICLE,
            backaction=BackactionControl.PASS,
            cost=4.0,
        ),
        profile(
            "strictly-worse",
            gain=1,
            separation=0.4,
            linkage=UnitLinkage.SAME_FOLLICLE,
            backaction=BackactionControl.PASS,
            cost=2.0,
        ),
    )

    assert pareto_probe_front(
        probes,
        objective=ProbeObjective.WITHIN_FOLLICLE_TEMPORAL_PREDICTION,
    ) == ("cheap", "strong-but-expensive")
