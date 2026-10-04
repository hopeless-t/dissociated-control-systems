from dissociated_control_systems.cognitive_external_intake import (
    candidates,
    intake,
)


def test_raw_adni_is_access_hold():
    adni=next(c for c in candidates() if c.source_id=="ADNI_ECOG_RAW")
    assert adni.raw_participant_data
    assert adni.access_approval_required
    assert adni.ai_use_boundary_present
    assert adni.use=="HOLD_ACCESS_OR_DUA"


def test_published_aggregate_analyses_are_literature_prior_only():
    for source_id in (
        "ADNI_ECOG_PUBLISHED_ANALYSES",
        "INDEPENDENT_MCI_DISCREPANCY_PUBLISHED_ANALYSIS",
    ):
        source=next(c for c in candidates() if c.source_id==source_id)
        assert not source.raw_participant_data
        assert source.use=="ADMIT_LITERATURE_PRIOR"


def test_no_raw_human_ingestion_is_authorized():
    assert intake()["raw_ingestion_authorized"] is False
