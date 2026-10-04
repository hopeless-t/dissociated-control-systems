"""CGD-EXT-001: external observation and data-rights admission contract.

Public metadata/literature governance only. Clinical authority: NONE.
No participant-level external dataset is ingested by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

MaterialKind = Literal[
    "PUBLIC_METADATA",
    "PUBLIC_LITERATURE",
    "PARTICIPANT_LEVEL_DATA",
]
AIPolicy = Literal[
    "PUBLIC_MATERIAL_OK",
    "PARTICIPANT_DATA_AI_INGEST_PROHIBITED",
    "PARTICIPANT_DATA_AI_POLICY_REQUIRES_REVIEW",
]
Admission = Literal[
    "ADMIT_PUBLIC_EVIDENCE",
    "ADMIT_SCHEMA_ONLY",
    "DEFER_RIGHTS_REVIEW",
    "NO_INGEST",
]


@dataclass(frozen=True)
class ExternalSource:
    source_id: str
    material_kind: MaterialKind
    ai_policy: AIPolicy
    requires_data_application: bool
    has_self_report: bool
    has_informant_report: bool
    has_objective_performance: bool
    has_functional_measure: bool
    longitudinal: bool
    notes: str


@dataclass(frozen=True)
class SourceDecision:
    source_id: str
    admission: Admission
    reasons: tuple[str, ...]
    observation_value: tuple[str, ...]


def observation_value(source: ExternalSource) -> tuple[str, ...]:
    value = []
    if source.has_self_report:
        value.append("SELF_REPORT")
    if source.has_informant_report:
        value.append("INFORMANT_REPORT")
    if source.has_objective_performance:
        value.append("OBJECTIVE_PERFORMANCE")
    if source.has_functional_measure:
        value.append("DAILY_FUNCTION")
    if source.longitudinal:
        value.append("LONGITUDINAL_CHANGE")
    return tuple(value)


def evaluate_source(source: ExternalSource) -> SourceDecision:
    reasons = []

    if source.material_kind in {"PUBLIC_METADATA", "PUBLIC_LITERATURE"}:
        admission: Admission = (
            "ADMIT_SCHEMA_ONLY"
            if source.material_kind == "PUBLIC_METADATA"
            else "ADMIT_PUBLIC_EVIDENCE"
        )
        return SourceDecision(
            source_id=source.source_id,
            admission=admission,
            reasons=(),
            observation_value=observation_value(source),
        )

    if source.ai_policy == "PARTICIPANT_DATA_AI_INGEST_PROHIBITED":
        admission = "NO_INGEST"
        reasons.append("SOURCE_DUA_PROHIBITS_THIS_AI_INGEST_PATH")
    elif source.ai_policy == "PARTICIPANT_DATA_AI_POLICY_REQUIRES_REVIEW":
        admission = "DEFER_RIGHTS_REVIEW"
        reasons.append("AI_DATA_HANDLING_RIGHTS_NOT_ESTABLISHED")
    else:
        admission = "DEFER_RIGHTS_REVIEW"
        reasons.append("PARTICIPANT_DATA_NEEDS_EXPLICIT_DATA_GOVERNANCE")

    if source.requires_data_application:
        reasons.append("CONTROLLED_ACCESS_OR_DUA_REQUIRED")

    return SourceDecision(
        source_id=source.source_id,
        admission=admission,
        reasons=tuple(reasons),
        observation_value=observation_value(source),
    )


def sources() -> tuple[ExternalSource, ...]:
    return (
        ExternalSource(
            source_id="adni_public_documentation",
            material_kind="PUBLIC_METADATA",
            ai_policy="PUBLIC_MATERIAL_OK",
            requires_data_application=False,
            has_self_report=True,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "Public ADNI documentation/data dictionary exposes ECog participant "
                "and study-partner forms, FAQ, CDR and objective cognitive tests."
            ),
        ),
        ExternalSource(
            source_id="adni_published_discordance_literature",
            material_kind="PUBLIC_LITERATURE",
            ai_policy="PUBLIC_MATERIAL_OK",
            requires_data_application=False,
            has_self_report=True,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "Published studies use self/informant ECog discrepancy and relate it "
                "to cognition, biomarkers and progression."
            ),
        ),
        ExternalSource(
            source_id="adni_participant_level_data",
            material_kind="PARTICIPANT_LEVEL_DATA",
            ai_policy="PARTICIPANT_DATA_AI_INGEST_PROHIBITED",
            requires_data_application=True,
            has_self_report=True,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "Controlled-access participant-level ADNI data. Current public DUA "
                "explicitly restricts use of AI tools for ADNI participant data."
            ),
        ),
        ExternalSource(
            source_id="nacc_public_documentation",
            material_kind="PUBLIC_METADATA",
            ai_policy="PUBLIC_MATERIAL_OK",
            requires_data_application=False,
            has_self_report=False,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "Public NACC UDS documentation includes informant-based FAQ and "
                "longitudinal clinical/cognitive data availability."
            ),
        ),
        ExternalSource(
            source_id="nacc_participant_level_data",
            material_kind="PARTICIPANT_LEVEL_DATA",
            ai_policy="PARTICIPANT_DATA_AI_POLICY_REQUIRES_REVIEW",
            requires_data_application=True,
            has_self_report=False,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "NACC participant-level data require a data request. This contract "
                "does not assume AI-use permission without source-specific review."
            ),
        ),
        ExternalSource(
            source_id="bhr_public_documentation",
            material_kind="PUBLIC_METADATA",
            ai_policy="PUBLIC_MATERIAL_OK",
            requires_data_application=False,
            has_self_report=True,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "Public BHR documentation describes participant/study-partner "
                "questionnaires and longitudinal online cognitive assessments."
            ),
        ),
        ExternalSource(
            source_id="bhr_participant_level_data",
            material_kind="PARTICIPANT_LEVEL_DATA",
            ai_policy="PARTICIPANT_DATA_AI_POLICY_REQUIRES_REVIEW",
            requires_data_application=True,
            has_self_report=True,
            has_informant_report=True,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=True,
            notes=(
                "BHR data sharing is governed by a DUA and may require additional "
                "third-party cognitive-assessment approvals."
            ),
        ),
        ExternalSource(
            source_id="prospective_memory_compensation_literature",
            material_kind="PUBLIC_LITERATURE",
            ai_policy="PUBLIC_MATERIAL_OK",
            requires_data_application=False,
            has_self_report=True,
            has_informant_report=False,
            has_objective_performance=True,
            has_functional_measure=True,
            longitudinal=False,
            notes=(
                "Published trials report objective prospective-memory outcomes after "
                "compensatory strategy/reminder training. This supports Track A only."
            ),
        ),
    )


@lru_cache(maxsize=1)
def external_observation_contract():
    rows = []
    for source in sources():
        decision = evaluate_source(source)
        rows.append(
            {
                "source_id": source.source_id,
                "material_kind": source.material_kind,
                "admission": decision.admission,
                "reasons": decision.reasons,
                "observation_value": decision.observation_value,
                "notes": source.notes,
            }
        )

    participant_rows = [
        row for row in rows if row["material_kind"] == "PARTICIPANT_LEVEL_DATA"
    ]
    public_rows = [
        row for row in rows if row["material_kind"] != "PARTICIPANT_LEVEL_DATA"
    ]

    return {
        "rows": rows,
        "public_admitted": sum(
            row["admission"] in {"ADMIT_PUBLIC_EVIDENCE", "ADMIT_SCHEMA_ONLY"}
            for row in public_rows
        ),
        "participant_ingest_admitted": sum(
            row["admission"] in {"ADMIT_PUBLIC_EVIDENCE", "ADMIT_SCHEMA_ONLY"}
            for row in participant_rows
        ),
        "no_ingest": sum(row["admission"] == "NO_INGEST" for row in rows),
        "deferred": sum(row["admission"] == "DEFER_RIGHTS_REVIEW" for row in rows),
    }


def format_markdown() -> str:
    result = external_observation_contract()
    lines = [
        "# CGD-EXT-001 external observation + data-rights admission",
        "",
        "> Public evidence/schema intake only. Clinical authority: NONE.",
        "> No participant-level external dataset is ingested by this experiment.",
        "",
        f"- public metadata/literature sources admitted: {result['public_admitted']}",
        f"- participant-level sources admitted for ingestion here: {result['participant_ingest_admitted']}",
        f"- explicit NO_INGEST sources: {result['no_ingest']}",
        f"- participant sources deferred for rights review: {result['deferred']}",
        "",
        "| source | material | admission | observable dimensions | reasons |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        values = ", ".join(row["observation_value"]) or "none"
        reasons = ", ".join(row["reasons"]) or "none"
        lines.append(
            f"| {row['source_id']} | {row['material_kind']} | "
            f"{row['admission']} | {values} | {reasons} |"
        )

    lines.extend(
        [
            "",
            "Core separations:",
            "",
            "~~~text",
            "Scientific Relevance != Data-Handling Permission",
            "Public Schema != Participant-Level Data",
            "Informant Report != Ground Truth",
            "Self Report != Objective State",
            "Self-Informant Discordance != Root Cause",
            "Cross-Sectional Discrimination != Longitudinal Prognosis",
            "Research Dataset != Clinical Test",
            "Compensation Evidence != Disease Modification",
            "~~~",
            "",
            "The next permitted step is to design an external variable/claim map from "
            "public metadata and published aggregate findings. Controlled participant "
            "data remain outside this ChatGPT execution path unless a source-specific "
            "governance review explicitly authorizes a compatible environment.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
