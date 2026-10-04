from dissociated_control_systems.cognitive_observational_analysis import (
    FROZEN,
    assess_longitudinal,
    assess_primary,
    protocol_checks,
)


def test_opposite_direction_is_inconsistent_not_absolute_value_rescued():
    assert assess_primary(
        observed_rho=-0.30,
        permutation_p=0.01,
        shuffled_rho_abs_median=0.03,
        coverage=0.90,
    )=="INCONSISTENT"


def test_low_coverage_is_inconclusive():
    assert assess_primary(
        observed_rho=0.50,
        permutation_p=0.001,
        shuffled_rho_abs_median=0.02,
        coverage=0.40,
    )=="INCONCLUSIVE"


def test_positive_effect_must_beat_negative_control():
    assert assess_primary(
        observed_rho=0.35,
        permutation_p=0.01,
        shuffled_rho_abs_median=0.05,
        coverage=0.90,
    )=="CONSISTENT"


def test_longitudinal_missingness_stays_inconclusive():
    assert assess_longitudinal(
        discrepancy_slope_rho=None,
        permutation_p=None,
        longitudinal_coverage=0.30,
    )=="INCONCLUSIVE"


def test_protocol_has_no_posthoc_absolute_direction_escape():
    assert FROZEN.primary_direction=="positive"
    assert "PRIMARY_DIRECTION_FROZEN_BEFORE_DATA" in protocol_checks()
