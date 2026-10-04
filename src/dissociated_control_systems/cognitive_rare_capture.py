"""CGD-SIM-032: causal rare-state capture policy.

Synthetic experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_intervention_probe import noisy_probe, train_thresholds
from .cognitive_rare_state import (
    CAPABILITY_CEILING,
    HELDOUT_SAMPLES_PER_HYPOTHESIS,
    is_rare,
    rare_state_experiment,
    episode_row,
)


def classify_fault_set(fault_set, hypothesis_index, sample, thresholds):
    predicted = set()
    for target_index, target_fault in enumerate(FAULT_NAMES):
        value = noisy_probe(
            fault_set,
            target_fault,
            2_300_000_000
            + target_index * 100_000_000
            + hypothesis_index * 1_000_000
            + sample,
        )
        threshold = thresholds[target_fault]["threshold"]
        if value >= threshold:
            predicted.add(target_fault)
    return frozenset(predicted)


def metrics(rows, selected_indices):
    selected = [rows[index] for index in selected_indices]
    rare_total = sum(row["rare"] for row in rows)
    rare_selected = sum(row["rare"] for row in selected)
    biopsy_count = len(selected)
    total = len(rows)
    return {
        "biopsy_count": biopsy_count,
        "biopsy_fraction": biopsy_count / total,
        "rare_captured": rare_selected,
        "rare_total": rare_total,
        "rare_recall": (
            rare_selected / rare_total if rare_total else 1.0
        ),
        "biopsy_precision": (
            rare_selected / biopsy_count if biopsy_count else 0.0
        ),
        "episodes_per_specimen": (
            biopsy_count / rare_selected if rare_selected else float("inf")
        ),
    }


@lru_cache(maxsize=1)
def capture_policy_experiment():
    rare_result = rare_state_experiment()
    threshold = rare_result["threshold"]
    selected_label = rare_result["selected_label"]
    thresholds = train_thresholds(samples_per_hypothesis=40)

    rows = []
    causal_indices = []
    oracle_indices = []

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(HELDOUT_SAMPLES_PER_HYPOTHESIS):
            seed = 2_400_000_000 + hypothesis_index * 1_000_000 + sample
            row = episode_row(fault_set, seed)
            rare = is_rare(row, threshold)
            predicted = classify_fault_set(
                fault_set,
                hypothesis_index,
                sample,
                thresholds,
            )
            index = len(rows)
            rows.append(
                {
                    "fault_set": fault_set,
                    "predicted": predicted,
                    "rare": rare,
                }
            )
            if predicted == selected_label:
                causal_indices.append(index)
            if fault_set == selected_label:
                oracle_indices.append(index)

    causal = metrics(rows, causal_indices)
    oracle = metrics(rows, oracle_indices)

    rng = Random(2_500_000_000)
    random_order = list(range(len(rows)))
    rng.shuffle(random_order)
    random_indices = random_order[: len(causal_indices)]
    random = metrics(rows, random_indices)

    all_metrics = metrics(rows, list(range(len(rows))))

    precision_enrichment_vs_random = (
        causal["biopsy_precision"] / random["biopsy_precision"]
        if random["biopsy_precision"] > 0.0
        else float("inf")
    )
    biopsy_reduction_vs_all = 1.0 - causal["biopsy_fraction"]

    useful = (
        causal["rare_captured"] >= 3
        and causal["biopsy_precision"] > random["biopsy_precision"]
        and biopsy_reduction_vs_all >= 0.80
    )

    return {
        "threshold": threshold,
        "capability_ceiling": CAPABILITY_CEILING,
        "selected_stratum": (
            "healthy" if not selected_label else "+".join(sorted(selected_label))
        ),
        "all": all_metrics,
        "causal": causal,
        "random": random,
        "oracle": oracle,
        "precision_enrichment_vs_random": precision_enrichment_vs_random,
        "biopsy_reduction_vs_all": biopsy_reduction_vs_all,
        "useful": useful,
    }


def _fmt(value):
    return "inf" if value == float("inf") else f"{value:.2f}"


def format_markdown() -> str:
    result = capture_policy_experiment()
    lines = [
        "# CGD-SIM-032 causal rare-state capture policy",
        "",
        "> Synthetic result only. Clinical authority: NONE.",
        "",
        f"- rare threshold: signed overconfidence >= {result['threshold']:.2f}",
        f"- capability ceiling: {result['capability_ceiling']:.2f}",
        f"- frozen enriched stratum: {result['selected_stratum']}",
        "",
        "| policy | admissibility | biopsies | biopsy fraction | rare captured | rare recall | biopsy precision | episodes/specimen |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, admissibility in (
        ("all", "baseline"),
        ("random", "baseline"),
        ("causal", "ADMIT_SYNTHETIC"),
        ("oracle", "NOT_ADMISSIBLE_LATENT_TRUTH"),
    ):
        row = result[name]
        lines.append(
            f"| {name} | {admissibility} | {row['biopsy_count']} | "
            f"{row['biopsy_fraction']:.3%} | "
            f"{row['rare_captured']}/{row['rare_total']} | "
            f"{row['rare_recall']:.3%} | "
            f"{row['biopsy_precision']:.3%} | "
            f"{_fmt(row['episodes_per_specimen'])} |"
        )

    lines.extend(
        [
            "",
            (
                "- causal biopsy precision enrichment vs same-budget random: "
                f"{result['precision_enrichment_vs_random']:.2f}x"
            ),
            (
                "- causal biopsy reduction vs biopsy-all: "
                f"{result['biopsy_reduction_vs_all']:.1%}"
            ),
            f"- declared capture-policy usefulness criterion: {result['useful']}",
            "",
            "~~~text",
            "latent stratum label -> oracle upper bound only",
            "causal probe response -> admissible synthetic targeting signal",
            "",
            "Rare-State Enrichment != Permission To Treat",
            "Synthetic Stratum != Human Phenotype",
            "~~~",
            "",
            "The policy spends expensive biopsy effort only after a bounded causal "
            "probe predicts the pilot-frozen enrichment stratum.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
