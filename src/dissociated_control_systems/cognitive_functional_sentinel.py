"""CGD-SIM-045: independent functional-sentinel trigger frontier.

Synthetic longitudinal trigger model only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random

from .cognitive_disagreement_trigger import auc_from_scores, quantile

SAMPLES = 100_000
SIGMA_SELF_DRIFT = 0.04
SIGMA_INFORMANT_DRIFT = 0.04
TARGET_QUANTILE = 0.90
SENTINEL_NUISANCE_SIGMAS = (0.0, 0.01, 0.02, 0.04, 0.08, 0.16)


def generate_equal_drift(seed: int):
    rng = Random(seed)
    rows = []
    for _ in range(SAMPLES):
        delta_a = rng.gauss(0.0, SIGMA_SELF_DRIFT)
        delta_b = rng.gauss(0.0, SIGMA_INFORMANT_DRIFT)
        propagated_error = (delta_b - delta_a) / 2.0
        disagreement_change = delta_a + delta_b
        rows.append(
            {
                "error": propagated_error,
                "dyad_score": abs(disagreement_change),
            }
        )
    return rows


def sentinel_score(error: float, nuisance_sigma: float, rng: Random) -> float:
    """Absolute innovation of an independent functional observation.

    Predicted current state is true_state + propagated_error.
    Functional sentinel is true_state + nuisance.
    Their innovation is nuisance - propagated_error.
    """
    nuisance = rng.gauss(0.0, nuisance_sigma)
    return abs(nuisance - error)


@lru_cache(maxsize=1)
def functional_sentinel_experiment():
    rows = generate_equal_drift(3_900_000_000)
    absolute_errors = [abs(row["error"]) for row in rows]
    threshold = quantile(absolute_errors, TARGET_QUANTILE)
    high_error = [value >= threshold for value in absolute_errors]

    dyad_auc = auc_from_scores(
        high_error,
        [row["dyad_score"] for row in rows],
    )

    sentinel_rows = []
    for index, nuisance_sigma in enumerate(SENTINEL_NUISANCE_SIGMAS):
        rng = Random(3_910_000_000 + index * 1_000_000)
        scores = [
            sentinel_score(row["error"], nuisance_sigma, rng)
            for row in rows
        ]
        auc = auc_from_scores(high_error, scores)
        sentinel_rows.append(
            {
                "nuisance_sigma": nuisance_sigma,
                "auc": auc,
                "gain_over_dyad": auc - dyad_auc,
            }
        )

    aucs = [row["auc"] for row in sentinel_rows]
    pressure_knee = next(
        (
            row["nuisance_sigma"]
            for row in sentinel_rows
            if row["auc"] < 0.70
        ),
        None,
    )

    return {
        "target_threshold": threshold,
        "dyad_auc": dyad_auc,
        "sentinel_rows": sentinel_rows,
        "sentinel_auc_monotone": aucs == sorted(aucs, reverse=True),
        "pressure_knee_auc_below_070": pressure_knee,
    }


def format_markdown() -> str:
    result = functional_sentinel_experiment()
    lines = [
        "# CGD-SIM-045 independent functional-sentinel trigger frontier",
        "",
        "> Synthetic trigger model only. Clinical authority: NONE.",
        "",
        "Equal self/informant drift is frozen so that SIM-044 dyadic disagreement",
        "remains a near-chance freshness trigger.",
        "",
        "The new channel is an independent current-function sentinel:",
        "",
        "~~~text",
        "predicted current state = true state + propagated error E",
        "functional sentinel      = true state + nuisance N",
        "innovation               = sentinel - prediction = N - E",
        "trigger score            = |N - E|",
        "~~~",
        "",
        "Nuisance can represent environmental/scaffold variation plus measurement",
        "error. Values are synthetic sensitivity parameters, not empirical IADL",
        "measurement errors.",
        "",
        f"- samples: {SAMPLES:,}",
        f"- target: top {(1-TARGET_QUANTILE):.0%} of absolute propagated state error",
        f"- dyadic-disagreement AUC: {result['dyad_auc']:.3f}",
        "",
        "| functional-sentinel nuisance std | AUC for top-error state | AUC gain over dyad |",
        "| ---: | ---: | ---: |",
    ]
    for row in result["sentinel_rows"]:
        lines.append(
            f"| {row['nuisance_sigma']:.3f} | {row['auc']:.3f} | "
            f"{row['gain_over_dyad']:+.3f} |"
        )

    lines.extend(
        [
            "",
            f"- sentinel AUC decreases monotonically with nuisance: {result['sentinel_auc_monotone']}",
            (
                "- first frozen nuisance level with AUC < 0.70: "
                f"{result['pressure_knee_auc_below_070']}"
            ),
            "",
            "Key result:",
            "",
            "~~~text",
            "Independent Observation Can Restore Trigger Observability",
            "Functional Sentinel != Ground Truth",
            "Sentinel Value Collapses As Environment / Measurement Noise Rises",
            "Adaptive Re-observation Needs An Independent Innovation Channel",
            "~~~",
            "",
            "The experiment does not claim that any real IADL measure has the frozen",
            "noise levels or AUC values. It tests the architecture: once dyadic change",
            "is non-identifying, an independent function channel can provide a useful",
            "innovation signal only to the extent that its own nuisance is controlled.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
