"""Tiny causal counterexample for P (progenitor) and F* (structural remodeling).

The purpose is to show that the same observational covariance can be generated
by opposite causal directions while interventions predict different outcomes.
This is a synthetic identifiability result, not a biological causal model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GaussianMoments:
    var_p: float
    var_f: float
    cov_pf: float


@dataclass(frozen=True)
class LinearSCM:
    direction: str
    coefficient: float
    residual_variance: float

    def observational_moments(self) -> GaussianMoments:
        a = self.coefficient
        rv = self.residual_variance
        if self.direction == "F_TO_P":
            # F ~ N(0,1); P = aF + eps, Var(eps)=rv
            return GaussianMoments(
                var_p=a * a + rv,
                var_f=1.0,
                cov_pf=a,
            )
        if self.direction == "P_TO_F":
            # P ~ N(0,1); F = aP + eps, Var(eps)=rv
            return GaussianMoments(
                var_p=1.0,
                var_f=a * a + rv,
                cov_pf=a,
            )
        raise ValueError("direction must be F_TO_P or P_TO_F")

    def expected_p_under_do_f(self, f_value: float) -> float:
        if self.direction == "F_TO_P":
            return self.coefficient * f_value
        if self.direction == "P_TO_F":
            # Intervening on child F does not move root P in this SCM.
            return 0.0
        raise ValueError("direction must be F_TO_P or P_TO_F")

    def expected_f_under_do_p(self, p_value: float) -> float:
        if self.direction == "P_TO_F":
            return self.coefficient * p_value
        if self.direction == "F_TO_P":
            return 0.0
        raise ValueError("direction must be F_TO_P or P_TO_F")


def observationally_equivalent_pair(correlation: float = 0.6) -> tuple[LinearSCM, LinearSCM]:
    """Return opposite-direction standardized SCMs with identical moments."""
    if not -1.0 < correlation < 1.0:
        raise ValueError("correlation must lie strictly between -1 and 1")
    residual = 1.0 - correlation * correlation
    return (
        LinearSCM("F_TO_P", correlation, residual),
        LinearSCM("P_TO_F", correlation, residual),
    )
