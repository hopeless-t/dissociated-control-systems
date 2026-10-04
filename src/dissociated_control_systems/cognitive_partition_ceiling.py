"""CGD-SIM-035: oracle fault-partition information ceiling.

Synthetic information-bound analysis only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

from .cognitive_active_diagnosis import hypotheses
from .cognitive_rare_state import (
    HELDOUT_SAMPLES_PER_HYPOTHESIS,
    episode_row,
    is_rare,
    rare_state_experiment,
)

HARM_MULTIPLIERS = (1, 2, 4, 8)


def label_name(label):
    return "healthy" if not label else "+".join(sorted(label))


@lru_cache(maxsize=1)
def partition_ceiling_experiment():
    rare_result = rare_state_experiment()
    threshold = rare_result["threshold"]

    strata = []
    population = 0
    rare_total = 0

    for hypothesis_index, fault_set in enumerate(hypotheses()):
        rare = 0
        total = HELDOUT_SAMPLES_PER_HYPOTHESIS
        for sample in range(total):
            seed = 2_400_000_000 + hypothesis_index * 1_000_000 + sample
            row = episode_row(fault_set, seed)
            rare += int(is_rare(row, threshold))
        strata.append(
            {
                "label": fault_set,
                "name": label_name(fault_set),
                "rare": rare,
                "total": total,
                "nonrare": total - rare,
                "rate": rare / total,
            }
        )
        population += total
        rare_total += rare

    nonrare_total = population - rare_total

    subset_rows = []
    for mask in range(1, 1 << len(strata)):
        tp = fp = selected = 0
        names = []
        for index, stratum in enumerate(strata):
            if mask & (1 << index):
                tp += stratum["rare"]
                fp += stratum["nonrare"]
                selected += stratum["total"]
                names.append(stratum["name"])
        if tp == 0:
            continue
        fn = rare_total - tp
        tn = nonrare_total - fp
        sensitivity = tp / rare_total
        specificity = tn / nonrare_total
        precision = tp / selected
        subset_rows.append(
            {
                "names": tuple(names),
                "tp": tp,
                "fp": fp,
                "fn": fn,
                "tn": tn,
                "sensitivity": sensitivity,
                "specificity": specificity,
                "precision": precision,
                "selected": selected,
            }
        )

    best_precision = max(
        subset_rows,
        key=lambda row: (row["precision"], row["sensitivity"]),
    )

    best_by_min_recall = {}
    for min_recall in (0.25, 0.50, 7 / 12, 0.75, 1.0):
        eligible = [
            row for row in subset_rows
            if row["sensitivity"] >= min_recall
        ]
        best_by_min_recall[min_recall] = max(
            eligible,
            key=lambda row: (row["specificity"], row["precision"]),
        )

    action_best = {}
    q = rare_total / population
    for k in HARM_MULTIPLIERS:
        scored = []
        for row in subset_rows:
            expected_margin = (
                q * row["sensitivity"]
                - (1.0 - q) * (1.0 - row["specificity"]) * k
            )
            scored.append((expected_margin, row))
        margin, row = max(scored, key=lambda item: item[0])
        action_best[k] = {
            "margin": margin,
            "row": row,
            "positive": margin > 0.0,
        }

    top_strata = sorted(
        strata,
        key=lambda row: (-row["rate"], -row["rare"], row["name"]),
    )

    ppv_requirements = {
        k: k / (1.0 + k)
        for k in HARM_MULTIPLIERS
    }
    best_ppv = best_precision["precision"]
    ppv_gap_factors = {
        k: (
            ppv_requirements[k] / best_ppv
            if best_ppv > 0.0
            else float("inf")
        )
        for k in HARM_MULTIPLIERS
    }

    return {
        "population": population,
        "rare_total": rare_total,
        "prevalence": q,
        "strata": top_strata,
        "best_precision": best_precision,
        "best_by_min_recall": best_by_min_recall,
        "action_best": action_best,
        "ppv_requirements": ppv_requirements,
        "ppv_gap_factors": ppv_gap_factors,
    }


def names(row):
    return "; ".join(row["names"])


def format_markdown() -> str:
    r = partition_ceiling_experiment()
    best = r["best_precision"]
    lines = [
        "# CGD-SIM-035 oracle fault-partition information ceiling",
        "",
        "> Synthetic information-bound result only. Clinical authority: NONE.",
        "",
        f"- held-out population: {r['population']}",
        f"- rare states: {r['rare_total']}",
        f"- pooled prevalence: {r['prevalence']:.4%}",
        "",
        "Rare incidence by true four-fault stratum:",
        "",
        "| stratum | rare / total | rate |",
        "| --- | ---: | ---: |",
    ]
    for row in r["strata"]:
        lines.append(
            f"| {row['name']} | {row['rare']}/{row['total']} | "
            f"{row['rate']:.3%} |"
        )

    lines.extend(
        [
            "",
            "Best possible non-empty selector if true fault stratum were known perfectly:",
            "",
            f"- selected strata: {names(best)}",
            f"- sensitivity: {best['sensitivity']:.3%}",
            f"- specificity: {best['specificity']:.3%}",
            f"- precision / PPV: {best['precision']:.3%}",
            f"- TP/FP: {best['tp']}/{best['fp']}",
            "",
            "Oracle-partition frontier by minimum rare-state recall:",
            "",
            "| minimum recall | achieved recall | best specificity | precision | selected episodes | strata |",
            "| ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for min_recall, row in r["best_by_min_recall"].items():
        lines.append(
            f"| {min_recall:.3%} | {row['sensitivity']:.3%} | "
            f"{row['specificity']:.3%} | {row['precision']:.3%} | "
            f"{row['selected']} | {names(row)} |"
        )

    lines.extend(
        [
            "",
            "Action-utility ceiling with perfect fault-stratum knowledge:",
            "",
            "| harm k | best expected margin / episode (B units) | any positive-action subset viable | best subset PPV |",
            "| ---: | ---: | --- | ---: |",
        ]
    )
    for k in HARM_MULTIPLIERS:
        item = r["action_best"][k]
        lines.append(
            f"| {k} | {item['margin']:.6f} | {item['positive']} | "
            f"{item['row']['precision']:.3%} |"
        )

    lines.extend(
        [
            "",
            "Within-selected-set PPV requirement for positive action:",
            "",
            "| false-positive harm k*B | required PPV | best oracle fault-partition PPV | required further enrichment |",
            "| ---: | ---: | ---: | ---: |",
        ]
    )
    for k in HARM_MULTIPLIERS:
        lines.append(
            f"| {k} | {r['ppv_requirements'][k]:.3%} | "
            f"{best['precision']:.3%} | "
            f"{r['ppv_gap_factors'][k]:.1f}x |"
        )

    lines.extend(
        [
            "",
            "~~~text",
            "Perfect Fault Localization != Current-State Identification",
            "More Accurate Fault-Stratum Probe Cannot Exceed Its Partition Information",
            "Cause Class != Current Severity / Current Hazard State",
            "~~~",
            "",
            "Even an oracle that knows the exact four-dimensional fault subset cannot "
            "make the rare event action-eligible under the tested asymmetric-loss "
            "models. The missing information lives inside the fault stratum.",
            "",
            "Therefore the next information gain must come from a finer current-state "
            "observable or a different decomposition, not from endlessly improving "
            "fault-set classification accuracy.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
