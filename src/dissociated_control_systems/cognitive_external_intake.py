"""CGD-OBS-001: external observational source intake.

This module stores qualification decisions only.
It does not download or process participant-level human data.
Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

Use = Literal[
    "ADMIT_LITERATURE_PRIOR",
    "HOLD_ACCESS_OR_DUA",
    "HOLD_COLLABORATION_OR_VENDOR_APPROVAL",
    "REJECT_AS_RAW_CANONICAL_EVIDENCE",
]


@dataclass(frozen=True)
class SourceCandidate:
    source_id: str
    source_kind: str
    supports_self_informant_discrepancy: bool
    raw_participant_data: bool
    access_approval_required: bool
    collaboration_required: bool
    ai_use_boundary_present: bool
    aggregate_publication_only: bool
    use: Use


def candidates() -> tuple[SourceCandidate, ...]:
    return (
        SourceCandidate(
            source_id="ADNI_ECOG_RAW",
            source_kind="longitudinal observational cohort",
            supports_self_informant_discrepancy=True,
            raw_participant_data=True,
            access_approval_required=True,
            collaboration_required=False,
            ai_use_boundary_present=True,
            aggregate_publication_only=False,
            use="HOLD_ACCESS_OR_DUA",
        ),
        SourceCandidate(
            source_id="ADNI_ECOG_PUBLISHED_ANALYSES",
            source_kind="peer-reviewed aggregate literature",
            supports_self_informant_discrepancy=True,
            raw_participant_data=False,
            access_approval_required=False,
            collaboration_required=False,
            ai_use_boundary_present=False,
            aggregate_publication_only=True,
            use="ADMIT_LITERATURE_PRIOR",
        ),
        SourceCandidate(
            source_id="BHR_EVAL_RAW",
            source_kind="deidentified observational collaboration dataset",
            supports_self_informant_discrepancy=True,
            raw_participant_data=True,
            access_approval_required=True,
            collaboration_required=True,
            ai_use_boundary_present=False,
            aggregate_publication_only=False,
            use="HOLD_COLLABORATION_OR_VENDOR_APPROVAL",
        ),
        SourceCandidate(
            source_id="INDEPENDENT_MCI_DISCREPANCY_PUBLISHED_ANALYSIS",
            source_kind="peer-reviewed aggregate literature",
            supports_self_informant_discrepancy=True,
            raw_participant_data=False,
            access_approval_required=False,
            collaboration_required=False,
            ai_use_boundary_present=False,
            aggregate_publication_only=True,
            use="ADMIT_LITERATURE_PRIOR",
        ),
        SourceCandidate(
            source_id="PERSONAL_OR_UNCONTROLLED_ANECDOTE",
            source_kind="anecdotal report",
            supports_self_informant_discrepancy=False,
            raw_participant_data=False,
            access_approval_required=False,
            collaboration_required=False,
            ai_use_boundary_present=False,
            aggregate_publication_only=False,
            use="REJECT_AS_RAW_CANONICAL_EVIDENCE",
        ),
    )


@lru_cache(maxsize=1)
def intake():
    rows=[candidate.__dict__ for candidate in candidates()]
    raw_ingestion_authorized=any(
        row["raw_participant_data"]
        and row["use"]=="ADMIT_LITERATURE_PRIOR"
        for row in rows
    )
    literature_prior_count=sum(
        row["use"]=="ADMIT_LITERATURE_PRIOR"
        for row in rows
    )
    return {
        "rows":rows,
        "raw_ingestion_authorized":raw_ingestion_authorized,
        "literature_prior_count":literature_prior_count,
    }


def format_markdown() -> str:
    result=intake()
    lines=[
        "# CGD-OBS-001 external observational source intake",
        "",
        "> Intake/qualification only. Clinical authority: NONE.",
        "> Participant-level human data processed: NONE.",
        "",
        "| source | source kind | discrepancy construct | raw human rows | disposition |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['source_id']} | {row['source_kind']} | "
            f"{row['supports_self_informant_discrepancy']} | "
            f"{row['raw_participant_data']} | {row['use']} |"
        )

    lines.extend([
        "",
        f"- literature-prior sources admitted: {result['literature_prior_count']}",
        f"- participant-level raw-data ingestion authorized: {result['raw_ingestion_authorized']}",
        "",
        "~~~text",
        "Literature Prior != Raw Dataset Access",
        "Data Access != Permission To Send Data To An AI Tool",
        "Observational Association != Causal Mechanism",
        "Self/Informant Discrepancy != DCS Latent State Ground Truth",
        "~~~",
    ])
    return "\n".join(lines)


if __name__=="__main__":
    print(format_markdown())
