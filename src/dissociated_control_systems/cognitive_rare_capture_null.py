"""CGD-SIM-033: exact random-capture null and causal-selection biopsy.

Synthetic experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from bisect import bisect_left
from functools import lru_cache
from math import comb
from random import Random
from statistics import fmean

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_intervention_probe import noisy_probe, train_thresholds
from .cognitive_rare_state import (
    HELDOUT_SAMPLES_PER_HYPOTHESIS,
    episode_row,
    is_rare,
    rare_state_experiment,
)

MONTE_CARLO_TRIALS = 100_000


def hypergeom_pmf(x, *, population, successes, draws):
    if x < 0 or x > successes or x > draws:
        return 0.0
    failures = population - successes
    if draws - x < 0 or draws - x > failures:
        return 0.0
    return (
        comb(successes, x)
        * comb(failures, draws - x)
        / comb(population, draws)
    )


def random_capture_distribution(*, population, successes, draws):
    maximum = min(successes, draws)
    pmf = [
        hypergeom_pmf(
            x,
            population=population,
            successes=successes,
            draws=draws,
        )
        for x in range(maximum + 1)
    ]
    total = sum(pmf)
    pmf = [p / total for p in pmf]
    cdf = []
    running = 0.0
    for p in pmf:
        running += p
        cdf.append(running)
    return pmf, cdf


def quantile_from_cdf(cdf, q):
    return bisect_left(cdf, q)


def classify_fault_set(fault_set, hypothesis_index, sample, thresholds):
    predicted = set()
    values = {}
    for target_index, target_fault in enumerate(FAULT_NAMES):
        value = noisy_probe(
            fault_set,
            target_fault,
            2_300_000_000
            + target_index * 100_000_000
            + hypothesis_index * 1_000_000
            + sample,
        )
        values[target_fault] = value
        if value >= thresholds[target_fault]["threshold"]:
            predicted.add(target_fault)
    return frozenset(predicted), values


@lru_cache(maxsize=1)
def null_and_selection_experiment():
    rare_result = rare_state_experiment()
    rare_threshold = rare_result["threshold"]
    selected_label = rare_result["selected_label"]
    thresholds = train_thresholds(samples_per_hypothesis=40)

    rows = []
    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(HELDOUT_SAMPLES_PER_HYPOTHESIS):
            seed = 2_400_000_000 + hypothesis_index * 1_000_000 + sample
            state = episode_row(fault_set, seed)
            predicted, values = classify_fault_set(
                fault_set,
                hypothesis_index,
                sample,
                thresholds,
            )
            rows.append(
                {
                    "fault_set": fault_set,
                    "predicted": predicted,
                    "rare": is_rare(state, rare_threshold),
                    "probe_values": values,
                }
            )

    causal = [row for row in rows if row["predicted"] == selected_label]
    oracle = [row for row in rows if row["fault_set"] == selected_label]

    population = len(rows)
    rare_total = sum(row["rare"] for row in rows)
    draws = len(causal)
    captured = sum(row["rare"] for row in causal)

    pmf, cdf = random_capture_distribution(
        population=population,
        successes=rare_total,
        draws=draws,
    )
    exact_tail = sum(pmf[captured:])
    random_mean = draws * rare_total / population
    random_q95 = quantile_from_cdf(cdf, 0.95)
    random_q99 = quantile_from_cdf(cdf, 0.99)
    random_q999 = quantile_from_cdf(cdf, 0.999)

    rng = Random(2_600_000_000)
    mc_counts = []
    for _ in range(MONTE_CARLO_TRIALS):
        u = rng.random()
        mc_counts.append(bisect_left(cdf, u))
    mc_tail = fmean(float(x >= captured) for x in mc_counts)

    causal_true_selected = [
        row for row in causal if row["fault_set"] == selected_label
    ]
    causal_contaminants = [
        row for row in causal if row["fault_set"] != selected_label
    ]
    rare_true_selected = sum(row["rare"] for row in causal_true_selected)
    rare_contaminants = sum(row["rare"] for row in causal_contaminants)

    oracle_rare = sum(row["rare"] for row in oracle)
    oracle_nonrare = len(oracle) - oracle_rare
    causal_true_selected_nonrare = (
        len(causal_true_selected) - rare_true_selected
    )
    nonrare_pruned_from_oracle = (
        oracle_nonrare - causal_true_selected_nonrare
    )
    rare_pruned_from_oracle = oracle_rare - rare_true_selected

    contaminant_counts = {}
    for row in causal_contaminants:
        label = (
            "healthy"
            if not row["fault_set"]
            else "+".join(sorted(row["fault_set"]))
        )
        bucket = contaminant_counts.setdefault(
            label,
            {"selected": 0, "rare": 0},
        )
        bucket["selected"] += 1
        bucket["rare"] += int(row["rare"])

    contaminant_rows = sorted(
        (
            {
                "label": label,
                "selected": bucket["selected"],
                "rare": bucket["rare"],
            }
            for label, bucket in contaminant_counts.items()
        ),
        key=lambda row: (-row["rare"], -row["selected"], row["label"]),
    )

    causal_precision = captured / draws
    oracle_precision = oracle_rare / len(oracle)

    return {
        "population": population,
        "rare_total": rare_total,
        "draws": draws,
        "captured": captured,
        "exact_tail": exact_tail,
        "random_mean": random_mean,
        "random_q95": random_q95,
        "random_q99": random_q99,
        "random_q999": random_q999,
        "mc_trials": MONTE_CARLO_TRIALS,
        "mc_tail": mc_tail,
        "causal_precision": causal_precision,
        "oracle_precision": oracle_precision,
        "causal_true_selected_count": len(causal_true_selected),
        "causal_contaminant_count": len(causal_contaminants),
        "rare_true_selected": rare_true_selected,
        "rare_contaminants": rare_contaminants,
        "oracle_rare": oracle_rare,
        "nonrare_pruned_from_oracle": nonrare_pruned_from_oracle,
        "rare_pruned_from_oracle": rare_pruned_from_oracle,
        "contaminant_rows": contaminant_rows,
    }


def format_markdown() -> str:
    result = null_and_selection_experiment()
    lines = [
        "# CGD-SIM-033 exact random-capture null + causal-selection biopsy",
        "",
        "> Synthetic result only. Clinical authority: NONE.",
        "",
        "Random same-budget null:",
        "",
        f"- population episodes: {result['population']}",
        f"- rare specimens in population: {result['rare_total']}",
        f"- biopsy budget: {result['draws']}",
        f"- causal specimens captured: {result['captured']}",
        f"- random expected captured specimens: {result['random_mean']:.3f}",
        f"- random 95th percentile captured: {result['random_q95']}",
        f"- random 99th percentile captured: {result['random_q99']}",
        f"- random 99.9th percentile captured: {result['random_q999']}",
        f"- exact P(random captures >= causal): {result['exact_tail']:.8g}",
        (
            f"- {result['mc_trials']:,}-trial seeded Monte Carlo tail: "
            f"{result['mc_tail']:.8g}"
        ),
        "",
        "Why causal precision exceeded the oracle-stratum precision:",
        "",
        f"- causal precision: {result['causal_precision']:.3%}",
        f"- oracle-stratum precision: {result['oracle_precision']:.3%}",
        f"- causal selected with true oracle label: {result['causal_true_selected_count']}",
        f"- causal selected contaminants: {result['causal_contaminant_count']}",
        f"- rare captured from true oracle label: {result['rare_true_selected']}",
        f"- rare captured from contaminant strata: {result['rare_contaminants']}",
        f"- nonrare oracle-stratum rows pruned by causal classifier: {result['nonrare_pruned_from_oracle']}",
        f"- rare oracle-stratum rows pruned by causal classifier: {result['rare_pruned_from_oracle']}",
        "",
        "Top contaminant strata among causal selections:",
        "",
        "| true stratum | selected | rare |",
        "| --- | ---: | ---: |",
    ]
    for row in result["contaminant_rows"][:8]:
        lines.append(
            f"| {row['label']} | {row['selected']} | {row['rare']} |"
        )

    lines.extend(
        [
            "",
            "~~~text",
            "One Lucky Random Baseline != Evidence",
            "Exact Null Distribution > Anecdotal Random Draw",
            "Causal Selection Precision > Oracle-Stratum Precision",
            "    does not imply causal classifier > oracle",
            "    because selection sets and budgets differ",
            "~~~",
            "",
            "The exact hypergeometric null quantifies the chance of obtaining the "
            "same rare capture count with an equally sized random biopsy budget.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
