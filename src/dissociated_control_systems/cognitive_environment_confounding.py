"""CGD-SIM-047: environment-confounded functional sentinel.

Synthetic observation-confounding test only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random

from .cognitive_disagreement_trigger import auc_from_scores, quantile

SAMPLES = 100_000
SIGMA_SELF_DRIFT = 0.04
SIGMA_INFORMANT_DRIFT = 0.04
TARGET_QUANTILE = 0.90
SENTINEL_MEAS_NOISE = 0.02
CONTEXT_MEAS_NOISE = 0.01
ENV_SHIFT_MAGNITUDE = 0.12
ENV_SHIFT_PROBABILITIES = (0.0, 0.01, 0.05, 0.10, 0.20, 0.50)


def evaluate_environment_level(probability: float, seed: int):
    rng = Random(seed)
    errors = []
    raw_scores = []
    normalized_scores = []
    environment_shifted = []

    for _ in range(SAMPLES):
        delta_a = rng.gauss(0.0, SIGMA_SELF_DRIFT)
        delta_b = rng.gauss(0.0, SIGMA_INFORMANT_DRIFT)
        state_error = (delta_b - delta_a) / 2.0

        shifted = rng.random() < probability
        if shifted:
            environment = ENV_SHIFT_MAGNITUDE * (
                1.0 if rng.random() < 0.5 else -1.0
            )
        else:
            environment = 0.0

        sentinel_noise = rng.gauss(0.0, SENTINEL_MEAS_NOISE)
        context_noise = rng.gauss(0.0, CONTEXT_MEAS_NOISE)

        # Predicted state is true state + state_error.
        # Functional observation is true state + environment + measurement noise.
        raw_innovation = environment + sentinel_noise - state_error

        # An independent context channel estimates the environment contribution.
        observed_context = environment + context_noise
        normalized_innovation = raw_innovation - observed_context

        errors.append(abs(state_error))
        raw_scores.append(abs(raw_innovation))
        normalized_scores.append(abs(normalized_innovation))
        environment_shifted.append(shifted)

    error_threshold = quantile(errors, TARGET_QUANTILE)
    high_error = [value >= error_threshold for value in errors]

    raw_auc = auc_from_scores(high_error, raw_scores)
    normalized_auc = auc_from_scores(high_error, normalized_scores)

    # Freeze each score's top-decile trigger to expose environment-driven false
    # alarms at equal trigger coverage.
    raw_trigger_threshold = quantile(raw_scores, TARGET_QUANTILE)
    normalized_trigger_threshold = quantile(normalized_scores, TARGET_QUANTILE)

    def trigger_stats(scores, threshold):
        triggers = [score >= threshold for score in scores]
        true_positive = sum(t and y for t, y in zip(triggers, high_error, strict=True))
        false_positive = sum(t and not y for t, y in zip(triggers, high_error, strict=True))
        shifted_false_positive = sum(
            t and (not y) and shifted
            for t, y, shifted in zip(
                triggers,
                high_error,
                environment_shifted,
                strict=True,
            )
        )
        positive = sum(high_error)
        negative = len(high_error) - positive
        return {
            "sensitivity": true_positive / positive,
            "false_positive_rate": false_positive / negative,
            "shifted_fraction_of_false_positives": (
                shifted_false_positive / false_positive
                if false_positive
                else 0.0
            ),
        }

    return {
        "environment_shift_probability": probability,
        "raw_auc": raw_auc,
        "normalized_auc": normalized_auc,
        "raw_trigger": trigger_stats(raw_scores, raw_trigger_threshold),
        "normalized_trigger": trigger_stats(
            normalized_scores,
            normalized_trigger_threshold,
        ),
    }


@lru_cache(maxsize=1)
def environment_confounding_experiment():
    rows = [
        evaluate_environment_level(
            probability,
            4_400_000_000 + index * 1_000_000,
        )
        for index, probability in enumerate(ENV_SHIFT_PROBABILITIES)
    ]

    raw_aucs = [row["raw_auc"] for row in rows]
    normalized_aucs = [row["normalized_auc"] for row in rows]
    return {
        "rows": rows,
        "raw_auc_degrades_monotonically": raw_aucs == sorted(
            raw_aucs,
            reverse=True,
        ),
        "normalized_min_auc": min(normalized_aucs),
        "raw_pressure_knee": next(
            (
                row["environment_shift_probability"]
                for row in rows
                if row["raw_auc"] < 0.70
            ),
            None,
        ),
    }


def format_markdown() -> str:
    result = environment_confounding_experiment()
    lines = [
        "# CGD-SIM-047 environment-confounded functional sentinel",
        "",
        "> Synthetic observation-confounding test only. Clinical authority: NONE.",
        "",
        "SIM-045/046 used a functional sentinel as an independent current-state",
        "innovation channel. SIM-047 restores the external-variable-map term that",
        "those experiments simplified away:",
        "",
        "~~~text",
        "function = current state + environment/scaffold + measurement noise",
        "~~~",
        "",
        "Frozen synthetic environment event:",
        "",
        f"- persistent visit-level shift magnitude: +/- {ENV_SHIFT_MAGNITUDE:.2f}",
        f"- functional measurement noise std: {SENTINEL_MEAS_NOISE:.2f}",
        f"- environment-context measurement noise std: {CONTEXT_MEAS_NOISE:.2f}",
        f"- target: top {(1-TARGET_QUANTILE):.0%} of propagated current-state error",
        "",
        "Two trigger scores are compared:",
        "",
        "~~~text",
        "raw functional innovation",
        "    = environment + sentinel_noise - state_error",
        "",
        "context-normalized innovation",
        "    = raw innovation - observed_environment_context",
        "~~~",
        "",
        "| environment-shift probability | raw sentinel AUC | context-normalized AUC | raw sensitivity @10% trigger | raw FPR | fraction of raw FPs from shifted environment | normalized sensitivity @10% trigger | normalized FPR |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in result["rows"]:
        raw = row["raw_trigger"]
        normalized = row["normalized_trigger"]
        lines.append(
            f"| {row['environment_shift_probability']:.1%} | "
            f"{row['raw_auc']:.3f} | {row['normalized_auc']:.3f} | "
            f"{raw['sensitivity']:.3%} | {raw['false_positive_rate']:.3%} | "
            f"{raw['shifted_fraction_of_false_positives']:.3%} | "
            f"{normalized['sensitivity']:.3%} | "
            f"{normalized['false_positive_rate']:.3%} |"
        )

    lines.extend(
        [
            "",
            f"- raw sentinel AUC degrades monotonically: {result['raw_auc_degrades_monotonically']}",
            f"- first frozen environment probability with raw AUC < 0.70: {result['raw_pressure_knee']}",
            f"- minimum context-normalized AUC across frozen grid: {result['normalized_min_auc']:.3f}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Functional Change != Cognitive-State Change",
            "Independent Observation != State-Specific Observation",
            "Environment / Scaffold Is A Latent State, Not Mere Noise",
            "Context Binding Can Restore Observation Specificity",
            "~~~",
            "",
            "The environment-shift probabilities and magnitudes are synthetic. The",
            "experiment tests a structural confounding problem, not the performance",
            "of any real IADL instrument, sensor, home environment or support system.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
