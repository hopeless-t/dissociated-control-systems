"""CGD-SIM-022: causal intervention probes for degraded observability.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_harness_repair import (
    REPAIR_FOR,
    _best_balanced_threshold,
    run_episode,
)

PROBE_NOISE_STD = 0.0025
VALIDATION_THRESHOLD = 0.90


def raw_probe(fault_set, target_fault, seed):
    """Paired intervention contrast using the same synthetic seed."""
    baseline = run_episode(
        fault_set,
        seed,
        steps=60,
    )
    repaired = run_episode(
        fault_set,
        seed,
        steps=60,
        repairs=frozenset((REPAIR_FOR[target_fault],)),
    )

    if target_fault == "l0_decline":
        return (
            baseline.features["reference_drop"]
            - repaired.features["reference_drop"]
        )
    if target_fault == "l1_calibration":
        return (
            baseline.features["self_reference_gap"]
            - repaired.features["self_reference_gap"]
        )
    if target_fault == "l2_handoff":
        return (
            baseline.features["handoff_gap"]
            - repaired.features["handoff_gap"]
        )
    if target_fault == "observer_bias":
        return (
            baseline.features["self_reference_gap"]
            - repaired.features["self_reference_gap"]
        )
    raise ValueError(target_fault)


def noisy_probe(fault_set, target_fault, seed):
    signal = raw_probe(fault_set, target_fault, seed)
    noise_seed = seed ^ (hash(target_fault) & 0xFFFFFFFF)
    rng = Random(noise_seed)
    return signal + rng.gauss(0.0, PROBE_NOISE_STD)


def train_thresholds(samples_per_hypothesis=40):
    result = {}
    for target_index, target_fault in enumerate(FAULT_NAMES):
        absent = []
        present = []
        for hypothesis_index, fault_set in enumerate(hypotheses()):
            for sample in range(samples_per_hypothesis):
                value = noisy_probe(
                    fault_set,
                    target_fault,
                    600_000_000
                    + target_index * 10_000_000
                    + hypothesis_index * 100_000
                    + sample,
                )
                if target_fault in fault_set:
                    present.append(value)
                else:
                    absent.append(value)
        threshold, balanced = _best_balanced_threshold(absent, present)
        result[target_fault] = {
            "threshold": threshold,
            "training_balanced_accuracy": balanced,
        }
    return result


def evaluate(samples_per_hypothesis=100):
    thresholds = train_thresholds()
    stats = {
        fault: {
            "tp": 0,
            "tn": 0,
            "fp": 0,
            "fn": 0,
            "values_present": [],
            "values_absent": [],
        }
        for fault in FAULT_NAMES
    }
    exact = 0
    total = 0

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(samples_per_hypothesis):
            predicted = set()
            for target_index, target_fault in enumerate(FAULT_NAMES):
                value = noisy_probe(
                    fault_set,
                    target_fault,
                    700_000_000
                    + target_index * 10_000_000
                    + hypothesis_index * 100_000
                    + sample,
                )
                threshold = thresholds[target_fault]["threshold"]
                prediction = value >= threshold
                truth = target_fault in fault_set
                bucket = stats[target_fault]
                bucket["tp"] += int(prediction and truth)
                bucket["tn"] += int((not prediction) and (not truth))
                bucket["fp"] += int(prediction and (not truth))
                bucket["fn"] += int((not prediction) and truth)
                bucket[
                    "values_present" if truth else "values_absent"
                ].append(value)
                if prediction:
                    predicted.add(target_fault)

            exact += int(frozenset(predicted) == fault_set)
            total += 1

    rows = []
    for fault in FAULT_NAMES:
        bucket = stats[fault]
        tp = bucket["tp"]
        tn = bucket["tn"]
        fp = bucket["fp"]
        fn = bucket["fn"]
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)
        rows.append(
            {
                "fault": fault,
                "threshold": thresholds[fault]["threshold"],
                "training_balanced_accuracy": thresholds[fault][
                    "training_balanced_accuracy"
                ],
                "test_accuracy": accuracy,
                "sensitivity": sensitivity,
                "specificity": specificity,
                "mean_present_probe": fmean(bucket["values_present"]),
                "mean_absent_probe": fmean(bucket["values_absent"]),
                "partial_authority_eligible": accuracy >= VALIDATION_THRESHOLD,
            }
        )

    return {
        "rows": rows,
        "exact_reconstruction": exact / total,
        "macro_accuracy": fmean(row["test_accuracy"] for row in rows),
        "eligible_faults": [
            row["fault"]
            for row in rows
            if row["partial_authority_eligible"]
        ],
    }


@lru_cache(maxsize=1)
def intervention_probe_experiment():
    return evaluate()


def format_markdown() -> str:
    result = intervention_probe_experiment()
    lines = [
        "# CGD-SIM-022 causal intervention probes",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- paired-probe measurement noise std: {PROBE_NOISE_STD:.4f}",
        f"- exact 16-state reconstruction: {result['exact_reconstruction']:.3f}",
        f"- macro per-fault accuracy: {result['macro_accuracy']:.3f}",
        "",
        "| target | threshold | train balanced acc | test acc | sensitivity | specificity | mean probe if present | mean probe if absent | partial authority eligible |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['fault']} | {row['threshold']:.4f} | "
            f"{row['training_balanced_accuracy']:.3f} | "
            f"{row['test_accuracy']:.3f} | "
            f"{row['sensitivity']:.3f} | "
            f"{row['specificity']:.3f} | "
            f"{row['mean_present_probe']:.4f} | "
            f"{row['mean_absent_probe']:.4f} | "
            f"{row['partial_authority_eligible']} |"
        )

    eligible = ", ".join(result["eligible_faults"]) or "none"
    lines.extend(
        [
            "",
            f"- eligible dimensions at >= {VALIDATION_THRESHOLD:.2f}: {eligible}",
            "",
            "Probe semantics:",
            "",
            "~~~text",
            "same latent fault set + same random seed",
            "    -> run without targeted repair",
            "    -> run with exactly one targeted repair",
            "    -> measure paired response",
            "~~~",
            "",
            "This is causal observability rather than passive pattern classification.",
            "",
            "The experiment does not authorize real interventions. It only tests a "
            "synthetic principle: when observation channels collapse, a bounded "
            "paired intervention can sometimes create new diagnostic information.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
