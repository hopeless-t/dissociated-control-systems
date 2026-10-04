from dissociated_control_systems.cognitive_external_evidence import (
    frozen_candidates,
    qualification_experiment,
    qualify,
)


def test_engineering_reference_is_method_only():
    source=next(
        s for s in frozen_candidates()
        if s.source_id=="finite_ram_reference_bundle"
    )
    assert qualify(source).decision=="ADMIT_METHOD_ONLY"


def test_mutable_or_anecdotal_human_sources_do_not_enter_observation_lane():
    for source_id in (
        "mutable_web_summary_without_snapshot",
        "personal_anecdote",
        "identifiable_private_human_rows",
        "dcs_generated_human_challenge",
    ):
        source=next(s for s in frozen_candidates() if s.source_id==source_id)
        assert qualify(source).decision!="ADMIT_OBSERVATIONAL_LANE"


def test_only_domain_matched_bound_human_source_is_canonical_candidate():
    result=qualification_experiment()
    assert result["canonical_human"]==["versioned_public_cognitive_cohort"]
    assert not result["false_cross_domain_admission"]
