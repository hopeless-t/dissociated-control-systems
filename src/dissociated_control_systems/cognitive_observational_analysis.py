"""CGD-OBS-003: preregistered observational analysis contract.

Protocol code only. No participant-level human data are processed.
Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Assessment = Literal["CONSISTENT", "INCONSISTENT", "INCONCLUSIVE"]


@dataclass(frozen=True)
class AnalysisContract:
    primary_endpoint: str
    primary_direction: str
    negative_control: str
    missingness_rule: str
    secondary_correction: str
    longitudinal_endpoint: str
    claim_ceiling: str


FROZEN = AnalysisContract(
    primary_endpoint="spearman(D_SI, objective_impairment)",
    primary_direction="positive",
    negative_control="within_stratum_informant_dyad_permutation",
    missingness_rule="report_channel_coverage_and_never_coerce_missing_to_zero",
    secondary_correction="Benjamini-Hochberg_FDR_for_domain_secondary_endpoints",
    longitudinal_endpoint="spearman(slope_D_SI, slope_objective_impairment)",
    claim_ceiling="observational_projection_only_no_causal_or_clinical_claim",
)


def assess_primary(
    observed_rho: float,
    permutation_p: float,
    shuffled_rho_abs_median: float,
    coverage: float,
    *,
    min_coverage: float=0.60,
) -> Assessment:
    """Frozen decision logic for a future authorized dataset execution."""
    if coverage < min_coverage:
        return "INCONCLUSIVE"
    if permutation_p > 0.05:
        return "INCONCLUSIVE"
    if observed_rho <= 0.0:
        return "INCONSISTENT"
    if abs(observed_rho) <= shuffled_rho_abs_median:
        return "INCONCLUSIVE"
    return "CONSISTENT"


def assess_longitudinal(
    discrepancy_slope_rho: float | None,
    permutation_p: float | None,
    longitudinal_coverage: float,
    *,
    min_coverage: float=0.50,
) -> Assessment:
    if (
        discrepancy_slope_rho is None
        or permutation_p is None
        or longitudinal_coverage < min_coverage
    ):
        return "INCONCLUSIVE"
    if permutation_p > 0.05:
        return "INCONCLUSIVE"
    if discrepancy_slope_rho <= 0.0:
        return "INCONSISTENT"
    return "CONSISTENT"


def protocol_checks() -> tuple[str,...]:
    return (
        "PRIMARY_ENDPOINT_FROZEN_BEFORE_DATA",
        "PRIMARY_DIRECTION_FROZEN_BEFORE_DATA",
        "DYAD_PERMUTATION_NEGATIVE_CONTROL_REQUIRED",
        "MISSINGNESS_COVERAGE_REPORTED",
        "SECONDARY_DOMAIN_MULTIPLICITY_CONTROLLED",
        "CROSS_SECTIONAL_AND_LONGITUDINAL_CLAIMS_SEPARATED",
        "NO_THRESHOLD_TUNING_ON_HELDOUT_OUTCOME",
        "NO_CAUSAL_MECHANISM_FROM_ASSOCIATION",
    )


def format_markdown() -> str:
    return "\n".join([
        "# CGD-OBS-003 preregistered observational analysis contract",
        "",
        "> Protocol only. Human rows processed: NONE. Clinical authority: NONE.",
        "",
        f"- primary endpoint: {FROZEN.primary_endpoint}",
        f"- primary direction: {FROZEN.primary_direction}",
        f"- negative control: {FROZEN.negative_control}",
        f"- missingness: {FROZEN.missingness_rule}",
        f"- secondary correction: {FROZEN.secondary_correction}",
        f"- longitudinal endpoint: {FROZEN.longitudinal_endpoint}",
        f"- claim ceiling: {FROZEN.claim_ceiling}",
        "",
        "Frozen decision vocabulary:",
        "",
        "~~~text",
        "CONSISTENT",
        "INCONSISTENT",
        "INCONCLUSIVE",
        "~~~",
        "",
        "A statistically non-significant or low-coverage result is not rewritten as ",
        "evidence of no discrepancy mechanism; it remains INCONCLUSIVE.",
        "",
        "An effect in the opposite preregistered direction is INCONSISTENT rather ",
        "than repaired post hoc by taking an absolute value.",
    ])


if __name__=="__main__":
    print(format_markdown())
