"""CGD-SIM-023: sequential causal-probe evidence budget.

Synthetic harness experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import exp, log, pi
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_intervention_probe import noisy_probe

MAX_REPEATS = 5
CONFIDENCE_GRID = (0.90, 0.95, 0.975, 0.99)
PROBE_COST_WEIGHT = 0.003


def fit_probe_models(samples_per_hypothesis=60):
    models = {}
    for target_index, target_fault in enumerate(FAULT_NAMES):
        values = {False: [], True: []}
        for hypothesis_index, fault_set in enumerate(hypotheses()):
            for sample in range(samples_per_hypothesis):
                value = noisy_probe(
                    fault_set,
                    target_fault,
                    800_000_000
                    + target_index * 10_000_000
                    + hypothesis_index * 100_000
                    + sample,
                )
                values[target_fault in fault_set].append(value)

        models[target_fault] = {}
        for present in (False, True):
            xs = values[present]
            mean = fmean(xs)
            variance = fmean((x - mean) ** 2 for x in xs) + 1e-7
            models[target_fault][present] = (mean, variance)
    return models


def log_likelihood(value, mean, variance):
    return -0.5 * (
        ((value - mean) ** 2) / variance
        + log(2.0 * pi * variance)
    )


def posterior_from_llr(llr):
    if llr >= 0:
        return 1.0 / (1.0 + exp(-min(llr, 700.0)))
    e = exp(max(llr, -700.0))
    return e / (1.0 + e)


def classify_dimension(
    fault_set,
    target_fault,
    model,
    seed_base,
    *,
    confidence,
    max_repeats=MAX_REPEATS,
):
    llr = 0.0
    used = 0
    posterior = 0.5
    for repeat in range(max_repeats):
        value = noisy_probe(
            fault_set,
            target_fault,
            seed_base + repeat * 1_000_000,
        )
        absent_mean, absent_var = model[False]
        present_mean, present_var = model[True]
        llr += (
            log_likelihood(value, present_mean, present_var)
            - log_likelihood(value, absent_mean, absent_var)
        )
        posterior = posterior_from_llr(llr)
        used += 1
        if posterior >= confidence or posterior <= 1.0 - confidence:
            break
    return posterior >= 0.5, posterior, used


def evaluate_policy(models, *, samples_per_hypothesis, seed_base, confidence, max_repeats):
    exact = 0
    total = 0
    total_probes = 0
    bit_correct = []
    per_fault_probes = {fault: [] for fault in FAULT_NAMES}
    per_fault_correct = {fault: [] for fault in FAULT_NAMES}

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(samples_per_hypothesis):
            predicted = set()
            for target_index, target_fault in enumerate(FAULT_NAMES):
                prediction, _posterior, used = classify_dimension(
                    fault_set,
                    target_fault,
                    models[target_fault],
                    seed_base
                    + target_index * 100_000_000
                    + hypothesis_index * 1_000_000
                    + sample * 10,
                    confidence=confidence,
                    max_repeats=max_repeats,
                )
                truth = target_fault in fault_set
                correct = prediction == truth
                bit_correct.append(float(correct))
                per_fault_correct[target_fault].append(float(correct))
                per_fault_probes[target_fault].append(float(used))
                total_probes += used
                if prediction:
                    predicted.add(target_fault)

            exact += int(frozenset(predicted) == fault_set)
            total += 1

    mean_total_probes = total_probes / total
    exact_accuracy = exact / total
    macro_bit_accuracy = fmean(bit_correct)
    utility = exact_accuracy - PROBE_COST_WEIGHT * mean_total_probes
    return {
        "exact_accuracy": exact_accuracy,
        "macro_bit_accuracy": macro_bit_accuracy,
        "mean_total_probes": mean_total_probes,
        "utility": utility,
        "per_fault_accuracy": {
            fault: fmean(per_fault_correct[fault])
            for fault in FAULT_NAMES
        },
        "per_fault_mean_probes": {
            fault: fmean(per_fault_probes[fault])
            for fault in FAULT_NAMES
        },
    }


def select_confidence(models):
    best = None
    best_confidence = CONFIDENCE_GRID[0]
    rows = []
    for confidence in CONFIDENCE_GRID:
        result = evaluate_policy(
            models,
            samples_per_hypothesis=35,
            seed_base=900_000_000,
            confidence=confidence,
            max_repeats=MAX_REPEATS,
        )
        rows.append((confidence, result))
        if best is None or result["utility"] > best["utility"]:
            best = result
            best_confidence = confidence
    return best_confidence, rows


@lru_cache(maxsize=1)
def evidence_budget_experiment():
    models = fit_probe_models()
    selected_confidence, validation_rows = select_confidence(models)

    single = evaluate_policy(
        models,
        samples_per_hypothesis=100,
        seed_base=1_000_000_000,
        confidence=0.999999,
        max_repeats=1,
    )
    fixed_five = evaluate_policy(
        models,
        samples_per_hypothesis=100,
        seed_base=1_000_000_000,
        confidence=0.999999,
        max_repeats=5,
    )
    sequential = evaluate_policy(
        models,
        samples_per_hypothesis=100,
        seed_base=1_000_000_000,
        confidence=selected_confidence,
        max_repeats=MAX_REPEATS,
    )

    accuracy_gap_to_fixed = fixed_five["exact_accuracy"] - sequential["exact_accuracy"]
    cost_reduction = (
        1.0
        - sequential["mean_total_probes"] / fixed_five["mean_total_probes"]
    )
    efficient = (
        accuracy_gap_to_fixed <= 0.01
        and cost_reduction >= 0.30
    )

    return {
        "selected_confidence": selected_confidence,
        "validation_rows": validation_rows,
        "single": single,
        "fixed_five": fixed_five,
        "sequential": sequential,
        "accuracy_gap_to_fixed": accuracy_gap_to_fixed,
        "cost_reduction": cost_reduction,
        "efficient": efficient,
    }


def format_markdown() -> str:
    result = evidence_budget_experiment()
    lines = [
        "# CGD-SIM-023 sequential causal-probe evidence budget",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        f"- max repeats / dimension: {MAX_REPEATS}",
        f"- declared probe-cost weight: {PROBE_COST_WEIGHT:.3f}",
        f"- validation-selected confidence: {result['selected_confidence']:.3f}",
        "",
        "## Validation confidence sweep",
        "",
        "| confidence | exact accuracy | macro bit accuracy | mean total probes | utility |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for confidence, row in result["validation_rows"]:
        lines.append(
            f"| {confidence:.3f} | {row['exact_accuracy']:.3f} | "
            f"{row['macro_bit_accuracy']:.3f} | "
            f"{row['mean_total_probes']:.3f} | {row['utility']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Held-out comparison",
            "",
            "| policy | exact accuracy | macro bit accuracy | mean total probes |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for name in ("single", "fixed_five", "sequential"):
        row = result[name]
        lines.append(
            f"| {name} | {row['exact_accuracy']:.3f} | "
            f"{row['macro_bit_accuracy']:.3f} | "
            f"{row['mean_total_probes']:.3f} |"
        )

    lines.extend(
        [
            "",
            f"- sequential accuracy gap to fixed-five: {result['accuracy_gap_to_fixed']:+.4f}",
            f"- sequential probe reduction vs fixed-five: {result['cost_reduction']:.1%}",
            f"- evidence-budget criterion met: {result['efficient']}",
            "",
            "Per-dimension sequential held-out results:",
            "",
            "| dimension | accuracy | mean probes |",
            "| --- | ---: | ---: |",
        ]
    )
    seq = result["sequential"]
    for fault in FAULT_NAMES:
        lines.append(
            f"| {fault} | {seq['per_fault_accuracy'][fault]:.3f} | "
            f"{seq['per_fault_mean_probes'][fault]:.3f} |"
        )

    lines.extend(
        [
            "",
            "Control rule:",
            "",
            "~~~text",
            "acquire causal evidence",
            "update likelihood ratio",
            "stop probing a dimension once confidence is sufficient",
            "otherwise continue only up to a hard evidence budget",
            "~~~",
            "",
            "This asks whether causal observability can be compiled into a bounded "
            "evidence-acquisition policy instead of repeatedly applying every probe.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
