"""CGD-SIM-054: effective failure-mode diversity pressure knee.

Synthetic partial-independence experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import erf, sqrt
from random import Random

COMMON_BIAS = 0.08
SIGMA_PRIMARY = 0.01
SIGMA_AUDIT = 0.015
AUDIT_SAMPLES = 16
AUDIT_THRESHOLD = 0.03
SHARED_BIAS_FRACTIONS = (0.0, 0.25, 0.50, 0.625, 0.75, 0.90, 1.0)
MONTE_CARLO_TRIALS = 120_000
MC_TOLERANCE = 0.01
HIGH_POWER_TARGET = 0.90


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + erf(value / sqrt(2.0)))


def _analytic_trigger_probability(mean: float, sigma: float, threshold: float) -> float:
    """P(|X| >= threshold) for X ~ Normal(mean, sigma)."""

    upper = 1.0 - _normal_cdf((threshold - mean) / sigma)
    lower = _normal_cdf((-threshold - mean) / sigma)
    return upper + lower


def _monte_carlo_trigger_probability(
    mean: float,
    sigma: float,
    threshold: float,
    trials: int,
    seed: int,
) -> float:
    rng = Random(seed)
    triggers = 0
    for _ in range(trials):
        if abs(rng.gauss(mean, sigma)) >= threshold:
            triggers += 1
    return triggers / trials


@lru_cache(maxsize=1)
def effective_diversity_experiment():
    # Difference of sample means:
    # primary - audit = (1-rho) * B_common + eps_primary - eps_audit
    sigma_mean = sqrt(SIGMA_PRIMARY**2 + SIGMA_AUDIT**2) / sqrt(AUDIT_SAMPLES)
    false_positive_analytic = _analytic_trigger_probability(
        0.0,
        sigma_mean,
        AUDIT_THRESHOLD,
    )

    levels = []
    for level_index, rho in enumerate(SHARED_BIAS_FRACTIONS):
        effective_diversity = 1.0 - rho
        observable_bias = effective_diversity * COMMON_BIAS
        analytic_tpr = _analytic_trigger_probability(
            observable_bias,
            sigma_mean,
            AUDIT_THRESHOLD,
        )
        mc_tpr = _monte_carlo_trigger_probability(
            observable_bias,
            sigma_mean,
            AUDIT_THRESHOLD,
            MONTE_CARLO_TRIALS,
            6_000_000_000 + level_index * 100_000,
        )
        levels.append(
            {
                "shared_bias_fraction": rho,
                "effective_diversity": effective_diversity,
                "observable_bias": observable_bias,
                "signal_to_noise": observable_bias / sigma_mean,
                "analytic_tpr": analytic_tpr,
                "mc_tpr": mc_tpr,
                "mc_abs_error": abs(mc_tpr - analytic_tpr),
                "high_power": analytic_tpr >= HIGH_POWER_TARGET,
            }
        )

    first_below_high_power = next(
        level for level in levels if not level["high_power"]
    )
    half_power_geometry_rho = 1.0 - AUDIT_THRESHOLD / COMMON_BIAS
    closest_half_power = min(
        levels,
        key=lambda level: abs(level["analytic_tpr"] - 0.5),
    )

    return {
        "sigma_mean": sigma_mean,
        "false_positive_analytic": false_positive_analytic,
        "levels": levels,
        "first_below_high_power_rho": first_below_high_power["shared_bias_fraction"],
        "first_below_high_power_effective_diversity": first_below_high_power["effective_diversity"],
        "half_power_geometry_rho": half_power_geometry_rho,
        "closest_half_power_rho": closest_half_power["shared_bias_fraction"],
        "closest_half_power_tpr": closest_half_power["analytic_tpr"],
        "max_mc_abs_error": max(level["mc_abs_error"] for level in levels),
    }


def format_markdown() -> str:
    result = effective_diversity_experiment()
    lines = [
        "# CGD-SIM-054 effective failure-mode diversity pressure knee",
        "",
        "> Synthetic partial-independence experiment only. Clinical authority: NONE.",
        "",
        f"- common-mode bias magnitude: {COMMON_BIAS:.2f}",
        f"- primary noise std: {SIGMA_PRIMARY:.3f}",
        f"- audit noise std: {SIGMA_AUDIT:.3f}",
        f"- audit samples: {AUDIT_SAMPLES}",
        f"- audit threshold: {AUDIT_THRESHOLD:.2f}",
        f"- batch-mean disagreement noise std: {result['sigma_mean']:.4f}",
        f"- Monte Carlo trials / level: {MONTE_CARLO_TRIALS}",
        f"- analytic false-positive probability at zero bias: {result['false_positive_analytic']:.3e}",
        "",
        "Partial independence model:",
        "",
        "~~~text",
        "primary = environment + B_common + eps_primary",
        "audit   = environment + rho * B_common + eps_audit",
        "",
        "primary - audit = (1-rho) * B_common + noise",
        "effective diversity D = 1-rho",
        "~~~",
        "",
        "| shared-bias fraction rho | effective diversity D | observable bias | disagreement SNR | analytic trigger power | Monte Carlo power | |MC-analytic| | high-power >=90% |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for level in result["levels"]:
        lines.append(
            f"| {level['shared_bias_fraction']:.3f} | "
            f"{level['effective_diversity']:.3f} | "
            f"{level['observable_bias']:.3f} | "
            f"{level['signal_to_noise']:.2f} | "
            f"{level['analytic_tpr']:.3%} | "
            f"{level['mc_tpr']:.3%} | "
            f"{level['mc_abs_error']:.4f} | "
            f"{level['high_power']} |"
        )

    lines.extend(
        [
            "",
            f"- first frozen rho with trigger power <90%: {result['first_below_high_power_rho']:.3f}",
            f"- effective diversity at that frozen knee: {result['first_below_high_power_effective_diversity']:.3f}",
            f"- geometric 50% crossing prediction `(1-rho)*B = threshold`: rho={result['half_power_geometry_rho']:.3f}",
            f"- closest frozen 50% point: rho={result['closest_half_power_rho']:.3f}, power={result['closest_half_power_tpr']:.3%}",
            f"- maximum Monte Carlo vs analytic absolute error: {result['max_mc_abs_error']:.4f}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Independence Is A Continuum, Not A Boolean",
            "Declared Diversity != Effective Failure-Mode Separation",
            "Audit Value Scales With The Unshared Failure Component",
            "Redundancy Count Should Be Replaced By Failure-Mode Geometry",
            "~~~",
            "",
            "All bias fractions, thresholds, noises and sample counts are synthetic.",
            "The pressure knee characterizes this frozen detector geometry only; it",
            "does not validate any real clinical, caregiver, sensor or behavioral",
            "measurement channel.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
