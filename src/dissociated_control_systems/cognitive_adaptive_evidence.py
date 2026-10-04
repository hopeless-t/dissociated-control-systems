"""CGD-SIM-026: adaptive evidence allocation under causal-probe noise.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_probe_noise_knee import (
    ACCURACY_TARGET,
    _ll,
    _posterior,
    fit_models,
    measured_probe,
)

NOISE_LEVELS = (0.010, 0.020, 0.040, 0.080)
MAX_BUDGETS = (5, 8, 13, 21, 34)
CONFIDENCE = 0.99
PROBE_COST_WEIGHT = 0.003


def evaluate_adaptive_grid(noise_std, *, samples_per_hypothesis=50):
    """Build one evidence trace and reuse it across all stopping budgets."""
    models = fit_models(noise_std)
    max_budget = max(MAX_BUDGETS)

    counters = {
        budget: {
            "exact": 0,
            "bits": [],
            "total_probes": 0,
            "per_fault_probes": {fault: [] for fault in FAULT_NAMES},
            "per_fault_correct": {fault: [] for fault in FAULT_NAMES},
        }
        for budget in MAX_BUDGETS
    }
    total = 0

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(samples_per_hypothesis):
            predicted_by_budget = {
                budget: set() for budget in MAX_BUDGETS
            }

            for target_index, target_fault in enumerate(FAULT_NAMES):
                model = models[target_fault]
                absent_mean, absent_var = model[False]
                present_mean, present_var = model[True]
                truth = target_fault in fault_set

                llr = 0.0
                decisions = {}
                confidence_hit = None

                for repeat in range(1, max_budget + 1):
                    value = measured_probe(
                        fault_set,
                        target_fault,
                        1_400_000_000
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
                    bucket["total_probes"] += used
                    bucket["per_fault_probes"][target_fault].append(float(used))
                    bucket["per_fault_correct"][target_fault].append(
                        float(prediction == truth)
                    )
                    if prediction:
                        predicted_by_budget[budget].add(target_fault)

            for budget in MAX_BUDGETS:
                counters[budget]["exact"] += int(
                    frozenset(predicted_by_budget[budget]) == fault_set
                )
            total += 1

    rows = []
    for budget in MAX_BUDGETS:
        bucket = counters[budget]
        exact = bucket["exact"] / total
        mean_probes = bucket["total_probes"] / total
        macro = fmean(bucket["bits"])
        utility = exact - PROBE_COST_WEIGHT * mean_probes
        rows.append(
            {
                "max_repeats_per_dimension": budget,
                "exact_accuracy": exact,
                "macro_bit_accuracy": macro,
                "mean_total_probes": mean_probes,
                "utility": utility,
                "per_fault_mean_probes": {
                    fault: fmean(bucket["per_fault_probes"][fault])
                    for fault in FAULT_NAMES
                },
                "per_fault_accuracy": {
                    fault: fmean(bucket["per_fault_correct"][fault])
                    for fault in FAULT_NAMES
                },
            }
        )
    return rows


def summarize_level(noise_std, *, samples_per_hypothesis=50):
    rows = evaluate_adaptive_grid(
        noise_std,
        samples_per_hypothesis=samples_per_hypothesis,
    )
    meeting = [
        row for row in rows
        if row["exact_accuracy"] >= ACCURACY_TARGET
    ]
    minimum = meeting[0] if meeting else None
    best_utility = max(rows, key=lambda row: row["utility"])
    return {
        "noise_std": noise_std,
        "rows": rows,
        "minimum_target_row": minimum,
        "best_utility_row": best_utility,
    }


@lru_cache(maxsize=1)
def adaptive_frontier_experiment():
    levels = [summarize_level(noise) for noise in NOISE_LEVELS]
    return {"levels": levels}


def format_markdown() -> str:
    result = adaptive_frontier_experiment()
    lines = [
        "# CGD-SIM-026 adaptive evidence-allocation frontier",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- exact-state target: {ACCURACY_TARGET:.2f}",
        f"- confidence stop: {CONFIDENCE:.2f}",
        f"- max repeat budgets / dimension: {MAX_BUDGETS}",
        f"- probe-cost weight: {PROBE_COST_WEIGHT:.3f}",
        "",
        "| noise std | first adaptive cap reaching >=0.90 | mean probes there | accuracy there | utility-optimal cap | optimal accuracy | optimal mean probes | optimal utility |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for level in result["levels"]:
        minimum = level["minimum_target_row"]
        best = level["best_utility_row"]
        if minimum is None:
            min_cap = "none"
            min_probes = "none"
            min_accuracy = "n/a"
        else:
            min_cap = str(minimum["max_repeats_per_dimension"])
            min_probes = f"{minimum['mean_total_probes']:.3f}"
            min_accuracy = f"{minimum['exact_accuracy']:.3f}"
        lines.append(
            f"| {level['noise_std']:.3f} | {min_cap} | {min_probes} | "
            f"{min_accuracy} | {best['max_repeats_per_dimension']} | "
            f"{best['exact_accuracy']:.3f} | "
            f"{best['mean_total_probes']:.3f} | {best['utility']:.3f} |"
        )

    lines.extend(["", "## Full adaptive curves", ""])
    for level in result["levels"]:
        lines.append(f"### noise std = {level['noise_std']:.3f}")
        lines.append("")
        lines.append(
            "| max repeats / dimension | exact accuracy | macro bit accuracy | mean total probes | utility |"
        )
        lines.append("| ---: | ---: | ---: | ---: | ---: |")
        for row in level["rows"]:
            lines.append(
                f"| {row['max_repeats_per_dimension']} | "
                f"{row['exact_accuracy']:.3f} | "
                f"{row['macro_bit_accuracy']:.3f} | "
                f"{row['mean_total_probes']:.3f} | "
                f"{row['utility']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Per-dimension allocation at the largest cap",
            "",
            "| noise std | dimension | accuracy | mean probes |",
            "| ---: | --- | ---: | ---: |",
        ]
    )
    for level in result["levels"]:
        row = level["rows"][-1]
        for fault in FAULT_NAMES:
            lines.append(
                f"| {level['noise_std']:.3f} | {fault} | "
                f"{row['per_fault_accuracy'][fault]:.3f} | "
                f"{row['per_fault_mean_probes'][fault]:.3f} |"
            )

    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "~~~text",
            "equal evidence allocation",
            "    -> wastes probes on easy dimensions",
            "",
            "confidence-gated allocation",
            "    -> stops easy dimensions early",
            "    -> spends remaining budget only on unresolved dimensions",
            "",
            "if the 0.90 contract still cannot be reached at a large cap,",
            "the next move is probe redesign, not blind repetition",
            "~~~",
            "",
            "This experiment separates an allocation failure from a probe-channel "
            "failure before changing the synthetic intervention itself.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
