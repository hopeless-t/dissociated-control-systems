"""CGD-SIM-025: evidence-budget frontier under causal-probe noise.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_probe_noise_knee import (
    ACCURACY_TARGET,
    NOISE_LEVELS,
    _ll,
    fit_models,
    measured_probe,
)

REPEAT_BUDGETS = (1, 2, 3, 5, 8, 13)
PROBE_COST_WEIGHT = 0.003


def evaluate_budget_grid(noise_std, *, samples_per_hypothesis=50):
    models = fit_models(noise_std)
    counters = {
        repeats: {"exact": 0, "bits": []}
        for repeats in REPEAT_BUDGETS
    }
    total = 0

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(samples_per_hypothesis):
            predicted_by_budget = {
                repeats: set()
                for repeats in REPEAT_BUDGETS
            }

            for target_index, target_fault in enumerate(FAULT_NAMES):
                model = models[target_fault]
                absent_mean, absent_var = model[False]
                present_mean, present_var = model[True]
                llr = 0.0
                decision_at = {}

                for repeat in range(1, max(REPEAT_BUDGETS) + 1):
                    value = measured_probe(
                        fault_set,
                        target_fault,
                        1_300_000_000
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
                    if repeat in REPEAT_BUDGETS:
                        decision_at[repeat] = llr >= 0.0

                truth = target_fault in fault_set
                for repeats in REPEAT_BUDGETS:
                    prediction = decision_at[repeats]
                    counters[repeats]["bits"].append(
                        float(prediction == truth)
                    )
                    if prediction:
                        predicted_by_budget[repeats].add(target_fault)

            for repeats in REPEAT_BUDGETS:
                counters[repeats]["exact"] += int(
                    frozenset(predicted_by_budget[repeats]) == fault_set
                )
            total += 1

    rows = []
    for repeats in REPEAT_BUDGETS:
        probes = 4 * repeats
        exact = counters[repeats]["exact"] / total
        macro = fmean(counters[repeats]["bits"])
        utility = exact - PROBE_COST_WEIGHT * probes
        rows.append(
            {
                "repeats_per_dimension": repeats,
                "total_probes": probes,
                "exact_accuracy": exact,
                "macro_bit_accuracy": macro,
                "utility": utility,
            }
        )
    return rows


def summarize_level(noise_std, *, samples_per_hypothesis=50):
    rows = evaluate_budget_grid(
        noise_std,
        samples_per_hypothesis=samples_per_hypothesis,
    )
    meeting = [
        row for row in rows
        if row["exact_accuracy"] >= ACCURACY_TARGET
    ]
    minimum = meeting[0] if meeting else None
    best_utility = max(rows, key=lambda row: row["utility"])

    marginal = []
    for previous, current in zip(rows, rows[1:]):
        added = current["total_probes"] - previous["total_probes"]
        gain = current["exact_accuracy"] - previous["exact_accuracy"]
        marginal.append(
            {
                "from_repeats": previous["repeats_per_dimension"],
                "to_repeats": current["repeats_per_dimension"],
                "accuracy_gain": gain,
                "gain_per_added_probe": gain / added,
            }
        )

    return {
        "noise_std": noise_std,
        "rows": rows,
        "minimum_target_row": minimum,
        "best_utility_row": best_utility,
        "marginal": marginal,
    }


@lru_cache(maxsize=1)
def evidence_frontier_experiment():
    levels = [
        summarize_level(noise_std)
        for noise_std in NOISE_LEVELS
    ]
    return {"levels": levels}


def format_markdown() -> str:
    result = evidence_frontier_experiment()
    lines = [
        "# CGD-SIM-025 evidence-budget frontier",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- exact-state target: {ACCURACY_TARGET:.2f}",
        f"- probe-cost weight: {PROBE_COST_WEIGHT:.3f}",
        f"- repeat budgets / dimension: {REPEAT_BUDGETS}",
        "",
        "| noise std | minimum repeats for >=0.90 | minimum total probes | accuracy at minimum | utility-optimal repeats | optimal accuracy | optimal utility |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for level in result["levels"]:
        minimum = level["minimum_target_row"]
        best = level["best_utility_row"]
        if minimum is None:
            min_repeats = "none"
            min_probes = "none"
            min_accuracy = "n/a"
        else:
            min_repeats = str(minimum["repeats_per_dimension"])
            min_probes = str(minimum["total_probes"])
            min_accuracy = f"{minimum['exact_accuracy']:.3f}"
        lines.append(
            f"| {level['noise_std']:.4f} | {min_repeats} | "
            f"{min_probes} | {min_accuracy} | "
            f"{best['repeats_per_dimension']} | "
            f"{best['exact_accuracy']:.3f} | {best['utility']:.3f} |"
        )

    lines.extend(["", "## Full budget curves", ""])
    for level in result["levels"]:
        lines.append(f"### noise std = {level['noise_std']:.4f}")
        lines.append("")
        lines.append("| repeats / dimension | total probes | exact accuracy | macro bit accuracy | utility |")
        lines.append("| ---: | ---: | ---: | ---: | ---: |")
        for row in level["rows"]:
            lines.append(
                f"| {row['repeats_per_dimension']} | "
                f"{row['total_probes']} | "
                f"{row['exact_accuracy']:.3f} | "
                f"{row['macro_bit_accuracy']:.3f} | "
                f"{row['utility']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "Interpretation:",
            "",
            "~~~text",
            "accuracy can often be purchased with more evidence",
            "but evidence has explicit friction",
            "",
            "convergence is therefore not:",
            "    maximize accuracy at any cost",
            "",
            "it is:",
            "    choose the smallest evidence budget that satisfies the contract",
            "    or remain fail-closed when the contract is too expensive/unreachable",
            "~~~",
            "",
            "This converts the noise knee into a resource frontier and makes the "
            "stopping criterion cost-aware rather than recursion-aware.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
