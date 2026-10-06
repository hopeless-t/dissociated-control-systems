"""Simple clustered-information surrogate for HF01 experimental design.

Multiple follicles from one donor are not independent human replicates.  For an
equal-size exchangeable cluster model, the classic design-effect surrogate is

    DE = 1 + (m - 1) * rho
    n_eff = n_total / DE

This helper is only a planning/diagnostic approximation.  Real analyses should
model donor/region/follicle hierarchy directly.
"""

from __future__ import annotations


def design_effect(cluster_size: int, intraclass_correlation: float) -> float:
    if cluster_size < 1:
        raise ValueError("cluster_size must be >= 1")
    if not 0.0 <= intraclass_correlation <= 1.0:
        raise ValueError("intraclass_correlation must be in [0, 1]")
    return 1.0 + (cluster_size - 1) * intraclass_correlation


def effective_sample_size(
    total_observations: int,
    cluster_size: int,
    intraclass_correlation: float,
) -> float:
    if total_observations < 1:
        raise ValueError("total_observations must be >= 1")
    if total_observations % cluster_size != 0:
        raise ValueError("equal-cluster surrogate requires total divisible by cluster_size")
    return total_observations / design_effect(cluster_size, intraclass_correlation)
