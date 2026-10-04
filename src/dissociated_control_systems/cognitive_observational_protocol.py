"""CGD-OBS-002: preregistered discrepancy variable map.

No participant-level data are processed here.
Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Status = Literal["COMPLETE", "DYAD_ONLY", "SELF_OBJECTIVE_ONLY", "INSUFFICIENT"]


@dataclass(frozen=True)
class VisitObservation:
    """Pre-normalized impairment-oriented observation.

    All provided z-like values must be oriented so larger means greater
    impairment. Norm/transform identities are external protocol inputs; this
    module does not fit them from outcome data.
    """

    self_impairment: float | None
    informant_impairment: float | None
    objective_impairment: float | None
    self_informant_instrument_id: str | None
    normalization_id: str | None
    visit_time_years: float


@dataclass(frozen=True)
class Discrepancy:
    status: Status
    d_self_informant: float | None
    d_self_objective: float | None
    d_informant_objective: float | None
    triad_identity_error: float | None


def discrepancy(visit: VisitObservation) -> Discrepancy:
    s=visit.self_impairment
    i=visit.informant_impairment
    o=visit.objective_impairment

    d_si=None if s is None or i is None else i-s
    d_so=None if s is None or o is None else o-s
    d_io=None if i is None or o is None else o-i

    if s is not None and i is not None and o is not None:
        status: Status="COMPLETE"
        identity_error=abs(d_so-(d_si+d_io))
    elif s is not None and i is not None:
        status="DYAD_ONLY"
        identity_error=None
    elif s is not None and o is not None:
        status="SELF_OBJECTIVE_ONLY"
        identity_error=None
    else:
        status="INSUFFICIENT"
        identity_error=None

    return Discrepancy(
        status=status,
        d_self_informant=d_si,
        d_self_objective=d_so,
        d_informant_objective=d_io,
        triad_identity_error=identity_error,
    )


def validate_visit(visit: VisitObservation) -> tuple[bool, tuple[str,...]]:
    reasons=[]
    if (
        visit.self_impairment is not None
        and visit.informant_impairment is not None
        and not visit.self_informant_instrument_id
    ):
        reasons.append("SELF_INFORMANT_INSTRUMENT_ID_REQUIRED")
    if (
        visit.objective_impairment is not None
        and not visit.normalization_id
    ):
        reasons.append("OBJECTIVE_NORMALIZATION_ID_REQUIRED")
    if visit.visit_time_years < 0:
        reasons.append("NEGATIVE_VISIT_TIME")
    return (not reasons, tuple(reasons))


def longitudinal_delta(
    baseline: VisitObservation,
    followup: VisitObservation,
) -> dict[str,float|None]:
    if followup.visit_time_years <= baseline.visit_time_years:
        raise ValueError("follow-up time must be later than baseline")

    b=discrepancy(baseline)
    f=discrepancy(followup)
    dt=followup.visit_time_years-baseline.visit_time_years

    def slope(left, right):
        if left is None or right is None:
            return None
        return (right-left)/dt

    return {
        "years":dt,
        "self_informant_discrepancy_slope":slope(
            b.d_self_informant,
            f.d_self_informant,
        ),
        "self_objective_discrepancy_slope":slope(
            b.d_self_objective,
            f.d_self_objective,
        ),
        "objective_impairment_slope":slope(
            baseline.objective_impairment,
            followup.objective_impairment,
        ),
    }


def protocol_invariants() -> tuple[str,...]:
    return (
        "SIGNED_DISCREPANCY_NOT_ABSOLUTE_ONLY",
        "MISSING_NOT_ZERO",
        "PARTIAL_TRIAD_NOT_COMPLETE_TRIAD",
        "NORMALIZATION_FROZEN_BEFORE_OUTCOME_ANALYSIS",
        "INSTRUMENT_VERSION_BOUND",
        "OBSERVED_DISCREPANCY_NOT_LATENT_DCS_STATE",
        "ASSOCIATION_NOT_CAUSAL_MECHANISM",
    )


def format_markdown() -> str:
    example=VisitObservation(
        self_impairment=0.20,
        informant_impairment=0.65,
        objective_impairment=0.80,
        self_informant_instrument_id="EXAMPLE_SAME_SCALE_V1",
        normalization_id="EXAMPLE_FROZEN_NORM_V1",
        visit_time_years=0.0,
    )
    d=discrepancy(example)
    lines=[
        "# CGD-OBS-002 preregistered discrepancy variable map",
        "",
        "> Protocol math only. Human rows processed: NONE. Clinical authority: NONE.",
        "",
        "All variables are impairment-oriented before these equations are applied:",
        "",
        "~~~text",
        "S = self-reported impairment",
        "I = informant-reported impairment",
        "O = objective impairment under a frozen normalization",
        "",
        "D_SI = I - S",
        "D_SO = O - S",
        "D_IO = O - I",
        "",
        "positive D_SI / D_SO -> self reports less impairment than comparison channel",
        "negative D_SI / D_SO -> self reports more impairment than comparison channel",
        "~~~",
        "",
        f"- known-answer D_SI: {d.d_self_informant:.3f}",
        f"- known-answer D_SO: {d.d_self_objective:.3f}",
        f"- known-answer D_IO: {d.d_informant_objective:.3f}",
        f"- triad identity error: {d.triad_identity_error:.12f}",
        "",
        "Frozen invariants:",
        "",
    ]
    lines.extend(f"- {item}" for item in protocol_invariants())
    return "\n".join(lines)


if __name__=="__main__":
    print(format_markdown())
