"""CGD-SIM-027: controlled-input handoff challenge.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_probe_noise_knee import (
    ACCURACY_TARGET,
    _ll,
    _posterior,
    measured_probe,
)

NOISE_LEVELS = (0.020, 0.040, 0.080)
MAX_BUDGETS = (5, 13, 34)
CONFIDENCE = 0.99
CHALLENGE_PULSES = 8
PROBE_COST_WEIGHT = 0.003


def l2_controlled_input_signal(fault_set, seed):
    """Paired known-command loopback through the synthetic handoff channel.

    This adds a new test interface. It does not read latent handoff reliability
    directly; it injects a known command and observes command/receipt response.
    """
    rng = Random(seed)
    improvements = []
    for _ in range(CHALLENGE_PULSES):
        reliability = (
            rng.uniform(0.3, 0.5)
            if "l2_handoff" in fault_set
            else 1.0
        )
        repaired_reliability = reliability + 0.85 * (1.0 - reliability)

        command = 1.0
        baseline_receipt = reliability * command
        repaired_receipt = repaired_reliability * command

        # Small process/receipt jitter exists even before external measurement
        # noise is added.
        baseline_receipt += rng.gauss(0.0, 0.006)
        repaired_receipt += rng.gauss(0.0, 0.006)
        improvements.append(repaired_receipt - baseline_receipt)

    return fmean(improvements)


def redesigned_probe(fault_set, target_fault, seed, noise_std):
    if target_fault != "l2_handoff":
        return measured_probe(
            fault_set,
            target_fault,
            seed,
            noise_std,
        )

    signal = l2_controlled_input_signal(fault_set, seed)
    noise_key = int(round(noise_std * 1_000_000))
    rng = Random(seed ^ 0xA511E9B3 ^ (noise_key * 0x85EBCA6B))
    return signal + rng.gauss(0.0, noise_std)


def fit_models(noise_std, samples_per_hypothesis=40):
    models = {}
    for target_index, target_fault in enumerate(FAULT_NAMES):
        groups = {False: [], True: []}
        for hypothesis_index, fault_set in enumerate(hypotheses()):
            for sample in range(samples_per_hypothesis):
                value = redesigned_probe(
                    fault_set,
                    target_fault,
                    1_500_000_000
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


def evaluate_redesigned_grid(noise_std, *, samples_per_hypothesis=50):
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
                        1_600_000_000
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
                        if confidence_hit is None:
                            decisions[repeat] = (
                                posterior >= 0.5,
                                repeat,
                            )
                        else:
                            decisions[repeat] = (
                                confidence_hit[1],
                                confidence_hit[0],
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
def controlled_input_experiment():
    return {
        "levels": [
            {
                "noise_std": noise,
                "rows": evaluate_redesigned_grid(noise),
            }
            for noise in NOISE_LEVELS
        ]
    }


def format_markdown() -> str:
    result = controlled_input_experiment()
    lines = [
        "# CGD-SIM-027 controlled-input handoff challenge",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- exact-state target: {ACCURACY_TARGET:.2f}",
        f"- confidence stop: {CONFIDENCE:.2f}",
        f"- handoff challenge pulses: {CHALLENGE_PULSES}",
        f"- adaptive caps / dimension: {MAX_BUDGETS}",
        "",
        "| noise std | cap | exact accuracy | macro bit accuracy | mean probes | L2 accuracy | L2 mean probes |",
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
                f"{row['per_fault_accuracy']['l2_handoff']:.3f} | "
                f"{row['per_fault_mean_probes']['l2_handoff']:.3f} |"
            )

    lines.extend(
        [
            "",
            "Largest-cap per-dimension accuracy:",
            "",
            "| noise std | L0 | L1 | L2 controlled-input | observer |",
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
            "old L2 probe:",
            "    infer handoff failure from naturally occurring desired compensation",
            "",
            "new L2 probe:",
            "    inject a known unit command",
            "    observe receipt through the handoff channel",
            "    compare baseline vs redundant-handoff response",
            "~~~",
            "",
            "This explicitly changes the observation interface. If the pressure knee "
            "moves, the prior limit was a probe-design limit rather than a universal "
            "information limit.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
