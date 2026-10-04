"""CGD-SIM-028: controlled calibration step-response.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_handoff_challenge import (
    CONFIDENCE,
    PROBE_COST_WEIGHT,
    l2_controlled_input_signal,
)
from .cognitive_probe_noise_knee import (
    ACCURACY_TARGET,
    _ll,
    _posterior,
    measured_probe,
)

NOISE_LEVELS = (0.040, 0.080, 0.120, 0.160)
MAX_BUDGETS = (5, 13, 34)
CALIBRATION_STEPS = 6


def l1_step_response_signal(fault_set, seed):
    """Measure convergence of a known self/reference mismatch.

    The challenge creates a known reference and a known initial self estimate,
    then observes the resulting error trajectory. The latent feedback gain is
    never emitted directly.
    """
    rng = Random(seed)
    feedback_gain = (
        rng.uniform(0.025, 0.075)
        if "l1_calibration" in fault_set
        else 0.35
    )

    reference = 0.45
    self_estimate = 0.95
    initial_error = abs(self_estimate - reference)

    for _ in range(CALIBRATION_STEPS):
        observed_reference = reference + rng.gauss(0.0, 0.006)
        self_estimate = self_estimate + feedback_gain * (
            observed_reference - self_estimate
        )

    final_error = abs(self_estimate - reference)
    # Fault presence means a larger fraction of the initial mismatch survives.
    return final_error / initial_error


def redesigned_probe(fault_set, target_fault, seed, noise_std):
    if target_fault == "l1_calibration":
        signal = l1_step_response_signal(fault_set, seed)
        noise_key = int(round(noise_std * 1_000_000))
        rng = Random(seed ^ 0xC2B2AE35 ^ (noise_key * 0x27D4EB2F))
        return signal + rng.gauss(0.0, noise_std)

    if target_fault == "l2_handoff":
        signal = l2_controlled_input_signal(fault_set, seed)
        noise_key = int(round(noise_std * 1_000_000))
        rng = Random(seed ^ 0xA511E9B3 ^ (noise_key * 0x85EBCA6B))
        return signal + rng.gauss(0.0, noise_std)

    return measured_probe(
        fault_set,
        target_fault,
        seed,
        noise_std,
    )


def fit_models(noise_std, samples_per_hypothesis=40):
    models = {}
    for target_index, target_fault in enumerate(FAULT_NAMES):
        groups = {False: [], True: []}
        for hypothesis_index, fault_set in enumerate(hypotheses()):
            for sample in range(samples_per_hypothesis):
                value = redesigned_probe(
                    fault_set,
                    target_fault,
                    1_700_000_000
                    + target_index * 10_000_000
                    + hypothesis_index * 100_000
                    + sample,
                    noise_std,
                )
                groups[target_fault in fault_set].append(value)

        models[target_fault] = {}
        for present in (False, True):
            values = groups[present]
            mean = fmean(values)
            variance = fmean((x - mean) ** 2 for x in values) + 1e-7
            models[target_fault][present] = (mean, variance)
    return models


def evaluate_grid(noise_std, *, samples_per_hypothesis=50):
    models = fit_models(noise_std)
    max_budget = max(MAX_BUDGETS)
    counters = {
        budget: {
            "exact": 0,
            "bits": [],
            "probes": 0,
            "per_fault_correct": {fault: [] for fault in FAULT_NAMES},
            "per_fault_probes": {fault: [] for fault in FAULT_NAMES},
        }
        for budget in MAX_BUDGETS
    }
    total = 0

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(samples_per_hypothesis):
            predicted = {budget: set() for budget in MAX_BUDGETS}

            for target_index, target_fault in enumerate(FAULT_NAMES):
                model = models[target_fault]
                absent_mean, absent_var = model[False]
                present_mean, present_var = model[True]
                truth = target_fault in fault_set

                llr = 0.0
                confidence_hit = None
                decisions = {}

                for repeat in range(1, max_budget + 1):
                    value = redesigned_probe(
                        fault_set,
                        target_fault,
                        1_800_000_000
                        + target_index * 100_000_000
                        + hypothesis_index * 1_000_000
                        + sample * 100
                        + repeat,
                        noise_std,
                    )
                    llr += (
                        _ll(value, present_mean, present_var)
                        - _ll(value, absent_mean, absent_var)
                    )
                    posterior = _posterior(llr)

                    if (
                        confidence_hit is None
                        and (
                            posterior >= CONFIDENCE
                            or posterior <= 1.0 - CONFIDENCE
                        )
                    ):
                        confidence_hit = (
                            repeat,
                            posterior >= 0.5,
                        )

                    if repeat in MAX_BUDGETS:
                        decisions[repeat] = (
                            (posterior >= 0.5, repeat)
                            if confidence_hit is None
                            else (confidence_hit[1], confidence_hit[0])
                        )

                for budget in MAX_BUDGETS:
                    prediction, used = decisions[budget]
                    bucket = counters[budget]
                    bucket["bits"].append(float(prediction == truth))
                    bucket["probes"] += used
                    bucket["per_fault_correct"][target_fault].append(
                        float(prediction == truth)
                    )
                    bucket["per_fault_probes"][target_fault].append(float(used))
                    if prediction:
                        predicted[budget].add(target_fault)

            for budget in MAX_BUDGETS:
                counters[budget]["exact"] += int(
                    frozenset(predicted[budget]) == fault_set
                )
            total += 1

    rows = []
    for budget in MAX_BUDGETS:
        bucket = counters[budget]
        exact = bucket["exact"] / total
        mean_probes = bucket["probes"] / total
        rows.append(
            {
                "max_repeats_per_dimension": budget,
                "exact_accuracy": exact,
                "macro_bit_accuracy": fmean(bucket["bits"]),
                "mean_total_probes": mean_probes,
                "utility": exact - PROBE_COST_WEIGHT * mean_probes,
                "per_fault_accuracy": {
                    fault: fmean(bucket["per_fault_correct"][fault])
                    for fault in FAULT_NAMES
                },
                "per_fault_mean_probes": {
                    fault: fmean(bucket["per_fault_probes"][fault])
                    for fault in FAULT_NAMES
                },
            }
        )
    return rows


@lru_cache(maxsize=1)
def calibration_challenge_experiment():
    return {
        "levels": [
            {"noise_std": noise, "rows": evaluate_grid(noise)}
            for noise in NOISE_LEVELS
        ]
    }


def format_markdown() -> str:
    result = calibration_challenge_experiment()
    lines = [
        "# CGD-SIM-028 controlled calibration step-response",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- exact-state target: {ACCURACY_TARGET:.2f}",
        f"- confidence stop: {CONFIDENCE:.2f}",
        f"- calibration challenge steps: {CALIBRATION_STEPS}",
        f"- adaptive caps / dimension: {MAX_BUDGETS}",
        "",
        "| noise std | cap | exact accuracy | macro bit accuracy | mean probes | L1 accuracy | L1 mean probes |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for level in result["levels"]:
        for row in level["rows"]:
            lines.append(
                f"| {level['noise_std']:.3f} | "
                f"{row['max_repeats_per_dimension']} | "
                f"{row['exact_accuracy']:.3f} | "
                f"{row['macro_bit_accuracy']:.3f} | "
                f"{row['mean_total_probes']:.3f} | "
                f"{row['per_fault_accuracy']['l1_calibration']:.3f} | "
                f"{row['per_fault_mean_probes']['l1_calibration']:.3f} |"
            )

    lines.extend(
        [
            "",
            "Largest-cap per-dimension accuracy:",
            "",
            "| noise std | L0 | L1 step-response | L2 controlled-input | observer |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for level in result["levels"]:
        row = level["rows"][-1]
        lines.append(
            f"| {level['noise_std']:.3f} | "
            f"{row['per_fault_accuracy']['l0_decline']:.3f} | "
            f"{row['per_fault_accuracy']['l1_calibration']:.3f} | "
            f"{row['per_fault_accuracy']['l2_handoff']:.3f} | "
            f"{row['per_fault_accuracy']['observer_bias']:.3f} |"
        )

    lines.extend(
        [
            "",
            "Probe redesign:",
            "",
            "~~~text",
            "old L1 probe:",
            "    infer calibration failure from naturally evolving self/reference gap",
            "",
            "new L1 probe:",
            "    create a known self/reference mismatch",
            "    apply the feedback loop for a fixed number of steps",
            "    observe how much error remains",
            "~~~",
            "",
            "If the high-noise knee moves again, the new bottleneck should migrate "
            "to another observation channel rather than disappear by recursion.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
