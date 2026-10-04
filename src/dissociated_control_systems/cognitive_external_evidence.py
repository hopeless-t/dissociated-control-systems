"""CGD-SIM-033: external observation-lane qualification.

Research evidence-governance model only. Clinical authority: NONE.
No real human dataset is ingested by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

Decision = Literal[
    "ADMIT_OBSERVATIONAL_LANE",
    "ADMIT_METHOD_ONLY",
    "DEFER_REVALIDATE",
    "REJECT_CANONICAL_EVIDENCE",
]


@dataclass(frozen=True)
class ExternalSourceSpec:
    source_id: str
    domain: Literal["COGNITIVE_HUMAN", "ENGINEERING_ANALOGY", "SYNTHETIC"]
    immutable_or_snapshot_bound: bool
    provenance_bound: bool
    measurement_definition_bound: bool
    population_scope_bound: bool
    freshness_bound: bool
    missingness_semantics_bound: bool
    deidentified_or_aggregate: bool
    public_or_authorized_access: bool
    intervention_generated_by_dcs: bool
    anecdotal_only: bool
    claim_scope_matches_domain: bool


@dataclass(frozen=True)
class Qualification:
    source_id: str
    decision: Decision
    reasons: tuple[str, ...]


def qualify(source: ExternalSourceSpec) -> Qualification:
    if source.intervention_generated_by_dcs:
        return Qualification(
            source.source_id,
            "REJECT_CANONICAL_EVIDENCE",
            ("DCS_GENERATED_HUMAN_INTERVENTION_OUT_OF_SCOPE",),
        )
    if source.anecdotal_only:
        return Qualification(
            source.source_id,
            "REJECT_CANONICAL_EVIDENCE",
            ("ANECDOTE_NOT_CANONICAL_EVIDENCE",),
        )
    if not source.public_or_authorized_access:
        return Qualification(
            source.source_id,
            "REJECT_CANONICAL_EVIDENCE",
            ("ACCESS_OR_GOVERNANCE_UNBOUND",),
        )
    if not source.deidentified_or_aggregate and source.domain == "COGNITIVE_HUMAN":
        return Qualification(
            source.source_id,
            "REJECT_CANONICAL_EVIDENCE",
            ("IDENTIFIABLE_HUMAN_DATA_NOT_ADMITTED",),
        )

    revalidate = []
    if not source.immutable_or_snapshot_bound:
        revalidate.append("SOURCE_IDENTITY_OR_SNAPSHOT_UNBOUND")
    if not source.provenance_bound:
        revalidate.append("PROVENANCE_UNBOUND")
    if not source.measurement_definition_bound:
        revalidate.append("MEASUREMENT_DEFINITION_UNBOUND")
    if not source.freshness_bound:
        revalidate.append("FRESHNESS_UNBOUND")
    if not source.missingness_semantics_bound:
        revalidate.append("MISSINGNESS_SEMANTICS_UNBOUND")

    if revalidate:
        return Qualification(
            source.source_id,
            "DEFER_REVALIDATE",
            tuple(revalidate),
        )

    if source.domain != "COGNITIVE_HUMAN":
        return Qualification(
            source.source_id,
            "ADMIT_METHOD_ONLY",
            ("CROSS_DOMAIN_METHOD_TRANSFER_ONLY",),
        )

    if not source.population_scope_bound:
        return Qualification(
            source.source_id,
            "DEFER_REVALIDATE",
            ("POPULATION_SCOPE_UNBOUND",),
        )
    if not source.claim_scope_matches_domain:
        return Qualification(
            source.source_id,
            "ADMIT_METHOD_ONLY",
            ("CLAIM_SCOPE_EXCEEDS_SOURCE_DOMAIN",),
        )

    return Qualification(
        source.source_id,
        "ADMIT_OBSERVATIONAL_LANE",
        (),
    )


def frozen_candidates() -> tuple[ExternalSourceSpec, ...]:
    base = dict(
        immutable_or_snapshot_bound=True,
        provenance_bound=True,
        measurement_definition_bound=True,
        population_scope_bound=True,
        freshness_bound=True,
        missingness_semantics_bound=True,
        deidentified_or_aggregate=True,
        public_or_authorized_access=True,
        intervention_generated_by_dcs=False,
        anecdotal_only=False,
        claim_scope_matches_domain=True,
    )
    return (
        ExternalSourceSpec(
            source_id="versioned_public_cognitive_cohort",
            domain="COGNITIVE_HUMAN",
            **base,
        ),
        ExternalSourceSpec(
            source_id="finite_ram_reference_bundle",
            domain="ENGINEERING_ANALOGY",
            **base,
        ),
        ExternalSourceSpec(
            source_id="dcs_synthetic_reference",
            domain="SYNTHETIC",
            **base,
        ),
        ExternalSourceSpec(
            source_id="mutable_web_summary_without_snapshot",
            domain="COGNITIVE_HUMAN",
            immutable_or_snapshot_bound=False,
            **{k:v for k,v in base.items() if k != "immutable_or_snapshot_bound"},
        ),
        ExternalSourceSpec(
            source_id="human_dataset_without_missingness_contract",
            domain="COGNITIVE_HUMAN",
            missingness_semantics_bound=False,
            **{k:v for k,v in base.items() if k != "missingness_semantics_bound"},
        ),
        ExternalSourceSpec(
            source_id="unscoped_human_population",
            domain="COGNITIVE_HUMAN",
            population_scope_bound=False,
            **{k:v for k,v in base.items() if k != "population_scope_bound"},
        ),
        ExternalSourceSpec(
            source_id="personal_anecdote",
            domain="COGNITIVE_HUMAN",
            anecdotal_only=True,
            **{k:v for k,v in base.items() if k != "anecdotal_only"},
        ),
        ExternalSourceSpec(
            source_id="identifiable_private_human_rows",
            domain="COGNITIVE_HUMAN",
            deidentified_or_aggregate=False,
            public_or_authorized_access=False,
            **{
                k:v for k,v in base.items()
                if k not in {"deidentified_or_aggregate","public_or_authorized_access"}
            },
        ),
        ExternalSourceSpec(
            source_id="dcs_generated_human_challenge",
            domain="COGNITIVE_HUMAN",
            intervention_generated_by_dcs=True,
            **{k:v for k,v in base.items() if k != "intervention_generated_by_dcs"},
        ),
    )


@lru_cache(maxsize=1)
def qualification_experiment():
    rows=[]
    for source in frozen_candidates():
        result=qualify(source)
        rows.append({
            "source_id":source.source_id,
            "domain":source.domain,
            "decision":result.decision,
            "reasons":result.reasons,
        })

    counts={}
    for row in rows:
        counts[row["decision"]]=counts.get(row["decision"],0)+1

    canonical_human=[
        row["source_id"]
        for row in rows
        if row["decision"]=="ADMIT_OBSERVATIONAL_LANE"
    ]
    false_cross_domain_admission=any(
        row["decision"]=="ADMIT_OBSERVATIONAL_LANE"
        and row["domain"]!="COGNITIVE_HUMAN"
        for row in rows
    )

    return {
        "rows":rows,
        "counts":counts,
        "canonical_human":canonical_human,
        "false_cross_domain_admission":false_cross_domain_admission,
    }


def format_markdown() -> str:
    result=qualification_experiment()
    lines=[
        "# CGD-SIM-033 external observation-lane qualification",
        "",
        "> Evidence-governance model only. Clinical authority: NONE.",
        "> No real human dataset is ingested by this experiment.",
        "",
        "| source | domain | qualification | reasons |",
        "| --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        reasons=", ".join(row["reasons"]) or "none"
        lines.append(
            f"| {row['source_id']} | {row['domain']} | "
            f"{row['decision']} | {reasons} |"
        )

    lines.extend([
        "",
        f"- admitted cognitive observational candidates: {len(result['canonical_human'])}",
        (
            "- cross-domain source falsely admitted as cognitive evidence: "
            f"{result['false_cross_domain_admission']}"
        ),
        "",
        "~~~text",
        "Engineering Reproducibility != Cognitive External Validity",
        "Public URL != Bound Evidence",
        "Published / Public != Population-Matched",
        "Anecdote != Canonical Evidence",
        "Synthetic Accuracy != Clinical Validity",
        "Observational Admission != Treatment Authority",
        "~~~",
        "",
        "A source may update the cognitive observational lane only when its identity, "
        "provenance, measurement semantics, population scope, freshness, missingness, "
        "access/governance, and claim scope are explicitly bound.",
    ])
    return "\n".join(lines)


if __name__=="__main__":
    print(format_markdown())
