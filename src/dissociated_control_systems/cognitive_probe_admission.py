"""CGD-SIM-029: probe-admission contract.

Synthetic research governance only. Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

Admission = Literal["ADMIT_SYNTHETIC", "DEFER", "REJECT"]
Translation = Literal[
    "OBSERVATIONAL_TRANSLATION_REQUIRES_PROTOCOL",
    "INTERVENTIONAL_TRANSLATION_REQUIRES_ETHICS_AND_DOMAIN_VALIDATION",
]

ACCURACY_ONLY_THRESHOLD = 0.90


@dataclass(frozen=True)
class ProbeSpec:
    probe_id: str
    diagnostic_accuracy: float
    interventional: bool
    latent_truth_access: bool
    known_input: bool
    externally_observable_output: bool
    paired_isometric_control: bool
    bounded_perturbation: bool
    reversible_or_observational: bool
    provenance_bound: bool
    environment_bound: bool
    freshness_bound: bool
    missingness_explicit: bool
    risk_coverage_declared: bool
    authority_separate: bool


@dataclass(frozen=True)
class ProbeDecision:
    probe_id: str
    admission: Admission
    reasons: tuple[str, ...]
    translation: Translation


def external_translation(spec: ProbeSpec) -> Translation:
    if spec.interventional:
        return "INTERVENTIONAL_TRANSLATION_REQUIRES_ETHICS_AND_DOMAIN_VALIDATION"
    return "OBSERVATIONAL_TRANSLATION_REQUIRES_PROTOCOL"


def evaluate_probe(spec: ProbeSpec) -> ProbeDecision:
    reject_reasons = []
    defer_reasons = []

    if spec.latent_truth_access:
        reject_reasons.append("LATENT_TRUTH_LEAKAGE")
    if spec.interventional and not spec.bounded_perturbation:
        reject_reasons.append("UNBOUNDED_INTERVENTION")
    if spec.interventional and not spec.reversible_or_observational:
        reject_reasons.append("NONREVERSIBLE_SYNTHETIC_INTERVENTION")
    if not spec.authority_separate:
        reject_reasons.append("PROBE_RESULT_COUPLED_TO_EXECUTION_AUTHORITY")

    if spec.interventional and not spec.known_input:
        defer_reasons.append("INTERVENTION_INPUT_NOT_BOUND")
    if spec.interventional and not spec.paired_isometric_control:
        defer_reasons.append("INTERVENTION_NOT_ISOMETRICALLY_PAIRED")
    if not spec.externally_observable_output:
        defer_reasons.append("OUTPUT_NOT_EXTERNALLY_OBSERVABLE")
    if not spec.provenance_bound:
        defer_reasons.append("MEASUREMENT_PROVENANCE_UNBOUND")
    if not spec.environment_bound:
        defer_reasons.append("ENVIRONMENT_UNBOUND")
    if not spec.freshness_bound:
        defer_reasons.append("EVIDENCE_FRESHNESS_UNBOUND")
    if not spec.missingness_explicit:
        defer_reasons.append("MISSINGNESS_SEMANTICS_UNBOUND")
    if not spec.risk_coverage_declared:
        defer_reasons.append("RISK_COVERAGE_UNDECLARED")

    if reject_reasons:
        admission: Admission = "REJECT"
        reasons = tuple(reject_reasons + defer_reasons)
    elif defer_reasons:
        admission = "DEFER"
        reasons = tuple(defer_reasons)
    else:
        admission = "ADMIT_SYNTHETIC"
        reasons = ()

    return ProbeDecision(
        probe_id=spec.probe_id,
        admission=admission,
        reasons=reasons,
        translation=external_translation(spec),
    )


def candidates() -> tuple[ProbeSpec, ...]:
    common = dict(
        externally_observable_output=True,
        bounded_perturbation=True,
        reversible_or_observational=True,
        provenance_bound=True,
        environment_bound=True,
        freshness_bound=True,
        missingness_explicit=True,
        risk_coverage_declared=True,
        authority_separate=True,
    )
    return (
        ProbeSpec(
            probe_id="direct_latent_oracle",
            diagnostic_accuracy=1.000,
            interventional=False,
            latent_truth_access=True,
            known_input=False,
            paired_isometric_control=False,
            **common,
        ),
        ProbeSpec(
            probe_id="unbounded_superprobe",
            diagnostic_accuracy=0.999,
            interventional=True,
            latent_truth_access=False,
            known_input=True,
            paired_isometric_control=True,
            externally_observable_output=True,
            bounded_perturbation=False,
            reversible_or_observational=False,
            provenance_bound=True,
            environment_bound=True,
            freshness_bound=True,
            missingness_explicit=True,
            risk_coverage_declared=True,
            authority_separate=True,
        ),
        ProbeSpec(
            probe_id="stale_controlled_handoff",
            diagnostic_accuracy=0.990,
            interventional=True,
            latent_truth_access=False,
            known_input=True,
            paired_isometric_control=True,
            externally_observable_output=True,
            bounded_perturbation=True,
            reversible_or_observational=True,
            provenance_bound=True,
            environment_bound=True,
            freshness_bound=False,
            missingness_explicit=True,
            risk_coverage_declared=True,
            authority_separate=True,
        ),
        ProbeSpec(
            probe_id="mean_imputed_missingness_shortcut",
            diagnostic_accuracy=0.950,
            interventional=False,
            latent_truth_access=False,
            known_input=False,
            paired_isometric_control=False,
            externally_observable_output=True,
            bounded_perturbation=True,
            reversible_or_observational=True,
            provenance_bound=True,
            environment_bound=True,
            freshness_bound=True,
            missingness_explicit=False,
            risk_coverage_declared=True,
            authority_separate=True,
        ),
        ProbeSpec(
            probe_id="passive_redundant_observation",
            diagnostic_accuracy=0.940,
            interventional=False,
            latent_truth_access=False,
            known_input=False,
            paired_isometric_control=False,
            **common,
        ),
        ProbeSpec(
            probe_id="paired_repair_probe",
            diagnostic_accuracy=0.929,
            interventional=True,
            latent_truth_access=False,
            known_input=True,
            paired_isometric_control=True,
            **common,
        ),
        ProbeSpec(
            probe_id="controlled_handoff_challenge",
            diagnostic_accuracy=0.984,
            interventional=True,
            latent_truth_access=False,
            known_input=True,
            paired_isometric_control=True,
            **common,
        ),
        ProbeSpec(
            probe_id="controlled_calibration_step_response",
            diagnostic_accuracy=0.990,
            interventional=True,
            latent_truth_access=False,
            known_input=True,
            paired_isometric_control=True,
            **common,
        ),
    )


@lru_cache(maxsize=1)
def admission_experiment():
    rows = []
    for spec in candidates():
        decision = evaluate_probe(spec)
        rows.append(
            {
                "probe_id": spec.probe_id,
                "diagnostic_accuracy": spec.diagnostic_accuracy,
                "accuracy_only_admit": (
                    spec.diagnostic_accuracy >= ACCURACY_ONLY_THRESHOLD
                ),
                "contract_admission": decision.admission,
                "reasons": decision.reasons,
                "translation": decision.translation,
            }
        )

    invalid = {
        "direct_latent_oracle",
        "unbounded_superprobe",
        "stale_controlled_handoff",
        "mean_imputed_missingness_shortcut",
    }
    unsafe_accuracy_admissions = sum(
        row["accuracy_only_admit"] and row["probe_id"] in invalid
        for row in rows
    )
    contract_false_admissions = sum(
        row["contract_admission"] == "ADMIT_SYNTHETIC"
        and row["probe_id"] in invalid
        for row in rows
    )

    return {
        "rows": rows,
        "accuracy_only_threshold": ACCURACY_ONLY_THRESHOLD,
        "unsafe_accuracy_admissions": unsafe_accuracy_admissions,
        "contract_false_admissions": contract_false_admissions,
    }


def format_markdown() -> str:
    result = admission_experiment()
    lines = [
        "# CGD-SIM-029 probe-admission contract",
        "",
        "> Synthetic research governance only. Clinical authority: NONE.",
        "",
        f"- naive accuracy-only threshold: {result['accuracy_only_threshold']:.2f}",
        (
            "- accuracy-only admissions that violate the frozen contract: "
            f"{result['unsafe_accuracy_admissions']}"
        ),
        (
            "- contract false admissions in frozen invalid set: "
            f"{result['contract_false_admissions']}"
        ),
        "",
        "| probe | diagnostic accuracy | accuracy-only | contract | external translation | reasons |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for row in result["rows"]:
        reasons = ", ".join(row["reasons"]) or "none"
        lines.append(
            f"| {row['probe_id']} | {row['diagnostic_accuracy']:.3f} | "
            f"{row['accuracy_only_admit']} | {row['contract_admission']} | "
            f"{row['translation']} | {reasons} |"
        )

    lines.extend(
        [
            "",
            "~~~text",
            "Diagnostic Accuracy != Probe Admission",
            "Probe Qualification != Execution Authority",
            "Synthetic Admission != Human / Clinical Authorization",
            "Historical Evidence != Current Qualified Evidence",
            "Missing Observation != Mean Observation",
            "Mismatch Localization != Root Cause Proof",
            "~~~",
            "",
            "No probe in this experiment receives human or clinical execution authority.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
