"""Local identifiability helpers for split androgen-response branches.

This module is synthetic design logic, not a biological estimator.  It asks
whether a declared intervention set can, in principle, separate canonical
AR-linked and mechanical/contractile response coefficients in a local linear
approximation.

For one functional output y, the local model is

    y = b - alpha * A_AR - mu * M

where each intervention contributes a declared branch-activity row
[A_AR, M].  The two coefficients are locally identifiable only when the design
matrix has rank 2.  Because almost-parallel rows can technically have rank 2
while remaining numerically fragile, the module also reports a normalized
separation score equal to |sin(theta)| between intervention directions.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import hypot, isclose
from typing import Iterable


@dataclass(frozen=True)
class BranchProbe:
    name: str
    ar_activity: float
    mechanical_activity: float

    def __post_init__(self) -> None:
        for value in (self.ar_activity, self.mechanical_activity):
            if not 0.0 <= value <= 1.0:
                raise ValueError("branch activities must be in [0, 1]")
        if not self.name:
            raise ValueError("probe name must be non-empty")

    @property
    def row(self) -> tuple[float, float]:
        return (self.ar_activity, self.mechanical_activity)


def design_rank(probes: Iterable[BranchProbe], *, tolerance: float = 1e-12) -> int:
    """Return the exact small-matrix rank for two branch columns."""
    rows = [probe.row for probe in probes]
    nonzero = [row for row in rows if abs(row[0]) > tolerance or abs(row[1]) > tolerance]
    if not nonzero:
        return 0

    for left, right in combinations(nonzero, 2):
        determinant = left[0] * right[1] - left[1] * right[0]
        if abs(determinant) > tolerance:
            return 2
    return 1


def branches_locally_identifiable(probes: Iterable[BranchProbe]) -> bool:
    return design_rank(probes) == 2


def pair_separation_score(
    first: BranchProbe,
    second: BranchProbe,
    *,
    tolerance: float = 1e-12,
) -> float:
    """Return normalized intervention-direction separation in [0, 1].

    score = |det(p1, p2)| / (||p1|| ||p2||) = |sin(theta)|.
    Zero means collinear/no branch separation. One means orthogonal directions.
    """
    n1 = hypot(first.ar_activity, first.mechanical_activity)
    n2 = hypot(second.ar_activity, second.mechanical_activity)
    if n1 <= tolerance or n2 <= tolerance:
        return 0.0
    determinant = abs(
        first.ar_activity * second.mechanical_activity
        - first.mechanical_activity * second.ar_activity
    )
    score = determinant / (n1 * n2)
    # Defend against tiny floating error above 1.
    return min(1.0, max(0.0, score))


def best_pair_separation(probes: Iterable[BranchProbe]) -> float:
    probes_t = tuple(probes)
    if len(probes_t) < 2:
        return 0.0
    return max(
        pair_separation_score(left, right)
        for left, right in combinations(probes_t, 2)
    )


def canonical_probe_set() -> tuple[BranchProbe, ...]:
    """Idealized interventions motivated by current HF01 source mapping.

    These rows encode intervention semantics only.  They do not assert that a
    real drug produces complete or perfectly selective blockade.
    """
    return (
        BranchProbe("DHT_challenge", ar_activity=1.0, mechanical_activity=1.0),
        BranchProbe("AR_specific_block", ar_activity=0.0, mechanical_activity=1.0),
        BranchProbe("mechanical_relaxation", ar_activity=1.0, mechanical_activity=0.0),
    )


def solve_two_branch_effects(
    first: BranchProbe,
    second: BranchProbe,
    first_effect: float,
    second_effect: float,
    *,
    tolerance: float = 1e-12,
) -> tuple[float, float]:
    """Solve alpha and mu from two independent local intervention equations.

    effect = alpha * A_AR + mu * M.  The caller owns the sign convention and
    biological interpretation of effect.
    """
    determinant = (
        first.ar_activity * second.mechanical_activity
        - first.mechanical_activity * second.ar_activity
    )
    if isclose(determinant, 0.0, abs_tol=tolerance):
        raise ValueError("probe pair is rank deficient")

    alpha = (
        first_effect * second.mechanical_activity
        - first.mechanical_activity * second_effect
    ) / determinant
    mu = (
        first.ar_activity * second_effect
        - first_effect * second.ar_activity
    ) / determinant
    return alpha, mu
