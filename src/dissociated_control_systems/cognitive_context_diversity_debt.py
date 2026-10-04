"""CGD-SIM-055: diversity debt and audit sample complexity.

Synthetic statistical-power experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from statistics import NormalDist

COMMON_BIAS = 0.08
SIGMA_PRIMARY = 0.01
SIGMA_AUDIT = 0.015
FALSE_POSITIVE_RATE = 0.01
TARGET_POWER = 0.90
EFFECTIVE_DIVERSITIES = (1.0, 0.75, 0.50, 0.375, 0.25, 0.10, 0.05, 0.02, 0.01, 0.0)
MAX_SEARCH_SAMPLES = 100_000
ASYMPTOTIC_D2_CONSTANT = 0.756
ASYMPTOTIC_TOLERANCE = 0.02

_NORMAL = NormalDist()
_Z_TWO_SIDED = _NORMAL.inv_cdf(1.0 - FALSE_POSITIVE_RATE / 2.0)
_SINGLE_SAMPLE_SIGMA = sqrt(SIGMA_PRIMARY**2 + SIGMA_AUDIT**2)


def _two_sided_power(samples: int, effective_diversity: float) -> float:
    sigma_mean = _SINGLE_SAMPLE_SIGMA / sqrt(samples)
    threshold = _Z_TWO_SIDED * sigma_mean
    mean = effective_diversity * COMMON_BIAS
    upper = 1.0 - _NORMAL.cdf((threshold - mean) / sigma_mean)
    lower = _NORMAL.cdf((-threshold - mean) / sigma_mean)
    return upper + lower


def _minimum_samples(effective_diversity: float) -> int | None:
    if effective_diversity == 0.0:
        return None
    for samples in range(1, MAX_SEARCH_SAMPLES + 1):
        if _two_sided_power(samples, effective_diversity) >= TARGET_POWER:
            return samples
    raise AssertionError("sample search ceiling too low for frozen diversity grid")


@lru_cache(maxsize=1)
def diversity_debt_experiment():
    levels = []
    for diversity in EFFECTIVE_DIVERSITIES:
        samples = _minimum_samples(diversity)
        if samples is None:
            power = FALSE_POSITIVE_RATE
            scaled_cost = None
        else:
            power = _two_sided_power(samples, diversity)
            scaled_cost = samples * diversity * diversity
        levels.append(
            {
                "effective_diversity": diversity,
                "shared_bias_fraction": 1.0 - diversity,
                "minimum_samples": samples,
                "achieved_power": power,
                "scaled_cost_n_d2": scaled_cost,
            }
        )

    positive = [level for level in levels if level["effective_diversity"] > 0.0]
    low_diversity = [level for level in positive if level["effective_diversity"] <= 0.10]
    max_low_diversity_constant_error = max(
        abs(level["scaled_cost_n_d2"] - ASYMPTOTIC_D2_CONSTANT)
        for level in low_diversity
    )

    by_diversity = {level["effective_diversity"]: level for level in levels}
    half_diversity_sample_ratio = (
        by_diversity[0.05]["minimum_samples"]
        / by_diversity[0.10]["minimum_samples"]
    )

    return {
        "z_two_sided": _Z_TWO_SIDED,
        "single_sample_sigma": _SINGLE_SAMPLE_SIGMA,
        "levels": levels,
        "max_low_diversity_constant_error": max_low_diversity_constant_error,
        "half_diversity_sample_ratio": half_diversity_sample_ratio,
    }


def format_markdown() -> str:
    result = diversity_debt_experiment()
    lines = [
        "# CGD-SIM-055 diversity debt and audit sample complexity",
        "",
        "> Synthetic statistical-power experiment only. Clinical authority: NONE.",
        "",
        f"- common-mode bias magnitude: {COMMON_BIAS:.2f}",
        f"- single-sample disagreement noise std: {result['single_sample_sigma']:.4f}",
        f"- two-sided false-positive rate: {FALSE_POSITIVE_RATE:.1%}",
        f"- target detection power: {TARGET_POWER:.1%}",
        f"- two-sided Gaussian critical z: {result['z_two_sided']:.3f}",
        "",
        "Unlike SIM-054's fixed absolute threshold, SIM-055 fixes the false-positive",
        "rate. The trigger threshold therefore shrinks with the standard error as",
        "more independent audit samples are collected.",
        "",
        "~~~text",
        "observable signal = D * B_common",
        "standard error    = sigma / sqrt(n)",
        "fixed-FPR threshold proportional to 1/sqrt(n)",
        "",
        "therefore required n grows approximately as 1 / D^2",
        "~~~",
        "",
        "| effective diversity D | shared-bias rho | min samples for >=90% power | achieved power | n*D^2 |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]

    for level in result["levels"]:
        samples = "no finite n" if level["minimum_samples"] is None else str(level["minimum_samples"])
        scaled = "n/a" if level["scaled_cost_n_d2"] is None else f"{level['scaled_cost_n_d2']:.4f}"
        lines.append(
            f"| {level['effective_diversity']:.3f} | "
            f"{level['shared_bias_fraction']:.3f} | {samples} | "
            f"{level['achieved_power']:.3%} | {scaled} |"
        )

    lines.extend(
        [
            "",
            f"- halving D from 0.10 to 0.05 multiplies required samples by {result['half_diversity_sample_ratio']:.3f}x",
            f"- low-diversity max |n*D^2 - {ASYMPTOTIC_D2_CONSTANT:.3f}|: {result['max_low_diversity_constant_error']:.4f}",
            "- at D=0, signal is exactly zero and the trigger probability remains the false-positive rate regardless of n",
            "",
            "Key result:",
            "",
            "~~~text",
            "Weak Independence Can Be Bought Back With Samples",
            "Audit Cost Scales Approximately As 1 / D^2",
            "Zero Independence Cannot Be Repaired By More Measurements",
            "Measurement Budget != Structural Independence",
            "~~~",
            "",
            "All power targets, false-positive rates, noises and bias magnitudes are",
            "synthetic. The 1/D^2 scaling follows this Gaussian observation model and",
            "does not define a sampling cadence for any real person or instrument.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
