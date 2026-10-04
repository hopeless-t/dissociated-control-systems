import pytest

from dissociated_control_systems.cognitive_observational_protocol import (
    VisitObservation,
    discrepancy,
    longitudinal_delta,
    validate_visit,
)


def visit(s,i,o,t=0.0):
    return VisitObservation(
        self_impairment=s,
        informant_impairment=i,
        objective_impairment=o,
        self_informant_instrument_id=(
            "same-scale-v1" if s is not None and i is not None else None
        ),
        normalization_id=("norm-v1" if o is not None else None),
        visit_time_years=t,
    )


def test_signed_triad_known_answer():
    d=discrepancy(visit(0.20,0.65,0.80))
    assert d.status=="COMPLETE"
    assert d.d_self_informant==pytest.approx(0.45)
    assert d.d_self_objective==pytest.approx(0.60)
    assert d.d_informant_objective==pytest.approx(0.15)
    assert d.triad_identity_error==pytest.approx(0.0)


def test_missing_informant_is_not_zero():
    d=discrepancy(visit(0.20,None,0.80))
    assert d.status=="SELF_OBJECTIVE_ONLY"
    assert d.d_self_informant is None
    assert d.d_self_objective==pytest.approx(0.60)


def test_longitudinal_discrepancy_slope_keeps_sign():
    baseline=visit(0.20,0.30,0.35,0.0)
    followup=visit(0.25,0.60,0.70,2.0)
    result=longitudinal_delta(baseline,followup)
    assert result["self_informant_discrepancy_slope"]==pytest.approx(0.125)
    assert result["objective_impairment_slope"]==pytest.approx(0.175)


def test_unbound_objective_normalization_is_invalid():
    v=VisitObservation(
        self_impairment=0.2,
        informant_impairment=None,
        objective_impairment=0.7,
        self_informant_instrument_id=None,
        normalization_id=None,
        visit_time_years=0.0,
    )
    valid,reasons=validate_visit(v)
    assert not valid
    assert "OBJECTIVE_NORMALIZATION_ID_REQUIRED" in reasons
