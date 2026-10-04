from dissociated_control_systems.cognitive_external_observation_contract import (
    external_observation_contract,
    evaluate_source,
    sources,
)


def test_adni_participant_data_is_not_ingested():
    source = next(
        source for source in sources()
        if source.source_id == "adni_participant_level_data"
    )
    decision = evaluate_source(source)
    assert decision.admission == "NO_INGEST"
    assert "SOURCE_DUA_PROHIBITS_THIS_AI_INGEST_PATH" in decision.reasons


def test_public_metadata_and_literature_are_admitted_only_as_public_evidence():
    for source in sources():
        if source.material_kind == "PARTICIPANT_LEVEL_DATA":
            continue
        decision = evaluate_source(source)
        assert decision.admission in {
            "ADMIT_PUBLIC_EVIDENCE",
            "ADMIT_SCHEMA_ONLY",
        }


def test_no_participant_level_source_is_admitted_for_ingestion_here():
    result = external_observation_contract()
    assert result["participant_ingest_admitted"] == 0
    assert result["no_ingest"] >= 1
    assert result["deferred"] >= 1
