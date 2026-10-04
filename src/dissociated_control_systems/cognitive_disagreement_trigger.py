"""CGD-SIM-044: disagreement-trigger informativeness audit.

Synthetic longitudinal sufficient-statistic test only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

SAMPLES = 100_000
TARGET_QUANTILE = 0.90
SCENARIOS = (
    ("equal_drift", 0.04, 0.04),
    ("informant_2x", 0.04, 0.08),
    ("informant_4x", 0.04, 0.16),
    ("self_2x", 0.08, 0.04),
)


def analytic_signed_correlation(sigma_a: float, sigma_b: float) -> float:
    """Corr(disagreement change, propagated state error).

    d = delta_A + delta_B
    e = (delta_B - delta_A) / 2

    For independent zero-mean drifts:
        corr(d, e) = (var_B - var_A) / (var_A + var_B)
    """
    va = sigma_a**2
    vb = sigma_b**2
    return (vb - va) / (va + vb)


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(q * len(ordered)))
    return ordered[index]


def auc_from_scores(labels: list[bool], scores: list[float]) -> float:
    """AUC via Mann-Whitney rank sum with exact tie averaging."""
    paired = sorted(zip(scores, labels, strict=True), key=lambda item: item[0])
    positive_count = sum(labels)
    negative_count = len(labels) - positive_count
    if positive_count == 0 or negative_count == 0:
        raise ValueError("AUC requires both classes")

    positive_rank_sum = 0.0
    i = 0
    while i < len(paired):
        j = i + 1
        while j < len(paired) and paired[j][0] == paired[i][0]:
            j += 1
        average_rank = ((i + 1) + j) / 2.0
        positive_rank_sum += average_rank * sum(
            1 for _, label in paired[i:j] if label
        )
        i = j

    u = positive_rank_sum - positive_count * (positive_count + 1) / 2.0
    return u / (positive_count * negative_count)


def pearson(xs: list[float], ys: list[float]) -> float:
    mean_x = fmean(xs)
    mean_y = fmean(ys)
    dx = [x - mean_x for x in xs]
    dy = [y - mean_y for y in ys]
    numerator = sum(x * y for x, y in zip(dx, dy, strict=True))
    denom_x = sqrt(sum(x * x for x in dx))
    denom_y = sqrt(sum(y * y for y in dy))
    return numerator / (denom_x * denom_y)


def evaluate_scenario(name: str, sigma_a: float, sigma_b: float, seed: int):
    rng = Random(seed)
    disagreement = []
    state_error = []
    signed_disagreement = []
    signed_error = []

    for _ in range(SAMPLES):
        delta_a = rng.gauss(0.0, sigma_a)
        delta_b = rng.gauss(0.0, sigma_b)
        d = delta_a + delta_b
        e = (delta_b - delta_a) / 2.0
        signed_disagreement.append(d)
        signed_error.append(e)
        disagreement.append(abs(d))
        state_error.append(abs(e))

    threshold = quantile(state_error, TARGET_QUANTILE)
    high_error = [value >= threshold for value in state_error]
    auc = auc_from_scores(high_error, disagreement)

    return {
        "name": name,
        "sigma_a": sigma_a,
        "sigma_b": sigma_b,
        "analytic_signed_corr": analytic_signed_correlation(sigma_a, sigma_b),
        "empirical_signed_corr": pearson(signed_disagreement, signed_error),
        "absolute_corr": pearson(disagreement, state_error),
        "high_error_threshold": threshold,
        "disagreement_auc_for_high_error": auc,
    }


@lru_cache(maxsize=1)
def disagreement_trigger_experiment():
    rows = [
        evaluate_scenario(
            name,
            sigma_a,
            sigma_b,
            3_700_000_000 + index * 1_000_000,
        )
        for index, (name, sigma_a, sigma_b) in enumerate(SCENARIOS)
    ]
    equal = rows[0]
    asymmetric = rows[1:]
    return {
        "rows": rows,
        "equal_auc_near_chance": abs(
            equal["disagreement_auc_for_high_error"] - 0.5
        ) < 0.02,
        "equal_signed_corr_near_zero": abs(equal["empirical_signed_corr"]) < 0.02,
        "asymmetry_creates_signal": max(
            abs(row["disagreement_auc_for_high_error"] - 0.5)
            for row in asymmetric
        ) > 0.05,
    }


def format_markdown() -> str:
    result = disagreement_trigger_experiment()
    lines = [
        "# CGD-SIM-044 disagreement-trigger informativeness audit",
        "",
        "> Synthetic sufficient-statistic test only. Clinical authority: NONE.",
        "",
        "Between objective anchors, let self- and informant-bias drift be:",
        "",
        "~~~text",
        "delta_A = self-model bias change",
        "delta_B = informant-bias change",
        "",
        "observed dyadic-disagreement change:",
        "    D = delta_A + delta_B",
        "",
        "propagated current-state estimation error from dyadic averaging:",
        "    E = (delta_B - delta_A) / 2",
        "~~~",
        "",
        "For independent Gaussian drift, the signed correlation is analytic:",
        "",
        "~~~text",
        "Corr(D,E) = (Var(B) - Var(A)) / (Var(A) + Var(B))",
        "~~~",
        "",
        "Therefore equal self/informant drift variance makes D and E orthogonal.",
        "For Gaussian variables, zero correlation here also gives independence.",
        "",
        f"- samples / scenario: {SAMPLES:,}",
        f"- high-error target: top {(1-TARGET_QUANTILE):.0%} of |E|",
        "",
        "| scenario | sigma_A | sigma_B | analytic signed corr | empirical signed corr | corr(|D|,|E|) | AUC of |D| for top-error state |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['name']} | {row['sigma_a']:.3f} | {row['sigma_b']:.3f} | "
            f"{row['analytic_signed_corr']:+.3f} | "
            f"{row['empirical_signed_corr']:+.3f} | "
            f"{row['absolute_corr']:+.3f} | "
            f"{row['disagreement_auc_for_high_error']:.3f} |"
        )

    lines.extend(
        [
            "",
            f"- equal-drift AUC approximately chance: {result['equal_auc_near_chance']}",
            f"- equal-drift signed correlation approximately zero: {result['equal_signed_corr_near_zero']}",
            f"- variance asymmetry can create disagreement/error signal: {result['asymmetry_creates_signal']}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Disagreement Signal != State-Estimate Error Signal",
            "Clinically Associated Statistic != Freshness Sensor",
            "Wrong Sufficient Statistic Can Reappear In The External Lane",
            "Adaptive Re-observation Requires Trigger Validation",
            "~~~",
            "",
            "A self-informant discrepancy can be scientifically associated with decline",
            "and still be uninformative about this particular propagated state-error",
            "quantity under a symmetric-drift world. The trigger becomes informative",
            "only after additional assumptions about reporter drift asymmetry.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
