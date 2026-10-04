"""CGD-SIM-034: enrichment utility vs intervention-authority frontier.

Synthetic decision-support only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache

from .cognitive_rare_capture_null import null_and_selection_experiment

HARM_MULTIPLIERS = (1, 2, 4, 8, 16, 32)
PREVALENCE_SCENARIOS = (0.001, 0.002, 0.005, 0.01, 0.05)


def required_specificity(q, sensitivity, harm_multiplier):
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0,1)")
    if not 0.0 <= sensitivity <= 1.0:
        raise ValueError("sensitivity must be in [0,1]")
    if harm_multiplier <= 0.0:
        raise ValueError("harm multiplier must be positive")
    # q*t*benefit > (1-q)*(1-s)*harm, with harm=k*benefit
    return 1.0 - (q * sensitivity) / ((1.0 - q) * harm_multiplier)


@lru_cache(maxsize=1)
def authority_frontier_experiment():
    base = null_and_selection_experiment()
    population = base["population"]
    rare_total = base["rare_total"]
    selected = base["draws"]
    captured = base["captured"]

    tp = captured
    fn = rare_total - captured
    fp = selected - captured
    tn = population - rare_total - fp

    prevalence = rare_total / population
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    precision = tp / (tp + fp)
    selection_rate = selected / population
    enrichment = precision / prevalence

    measured_frontier = {
        k: required_specificity(prevalence, sensitivity, k)
        for k in HARM_MULTIPLIERS
    }
    scenario_frontier = {
        q: {
            k: required_specificity(q, sensitivity, k)
            for k in HARM_MULTIPLIERS
        }
        for q in PREVALENCE_SCENARIOS
    }

    action_eligible = {
        k: specificity >= threshold
        for k, threshold in measured_frontier.items()
    }

    # Research-biopsy efficiency uses cost-only selection semantics rather than
    # treatment harm. Same captured rare events with far fewer biopsies is useful
    # even when positive predictive value is low.
    biopsy_efficiency_gain = (
        population / rare_total
    ) / (
        selected / captured
    )

    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "prevalence": prevalence,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "precision": precision,
        "selection_rate": selection_rate,
        "enrichment": enrichment,
        "biopsy_efficiency_gain": biopsy_efficiency_gain,
        "measured_frontier": measured_frontier,
        "scenario_frontier": scenario_frontier,
        "action_eligible": action_eligible,
    }


def format_markdown() -> str:
    r = authority_frontier_experiment()
    lines = [
        "# CGD-SIM-034 enrichment utility vs intervention-authority frontier",
        "",
        "> Synthetic decision-support only. Clinical authority: NONE.",
        "",
        "Measured rare-state selector:",
        "",
        f"- TP/FP/TN/FN: {r['tp']}/{r['fp']}/{r['tn']}/{r['fn']}",
        f"- prevalence: {r['prevalence']:.4%}",
        f"- sensitivity: {r['sensitivity']:.3%}",
        f"- specificity: {r['specificity']:.3%}",
        f"- precision: {r['precision']:.3%}",
        f"- selection rate: {r['selection_rate']:.3%}",
        f"- enrichment over pooled prevalence: {r['enrichment']:.2f}x",
        f"- biopsy efficiency gain: {r['biopsy_efficiency_gain']:.2f}x",
        "",
        "Research use:",
        "",
        "The selector is useful for rare-state harvesting because expensive biopsy "
        "effort is concentrated about tenfold relative to pooled sampling.",
        "",
        "Intervention-authority stress:",
        "",
        "Assume a correct action produces benefit B and a false-positive action "
        "produces harm k*B. A positive-action gate has positive expected value only if:",
        "",
        "~~~text",
        "q * sensitivity * B > (1-q) * (1-specificity) * k * B",
        "",
        "specificity > 1 - q*sensitivity / ((1-q)*k)",
        "~~~",
        "",
        "| harm multiplier k | required specificity at measured prevalence | measured specificity | action eligible |",
        "| ---: | ---: | ---: | --- |",
    ]
    for k in HARM_MULTIPLIERS:
        lines.append(
            f"| {k} | {r['measured_frontier'][k]:.5%} | "
            f"{r['specificity']:.5%} | {r['action_eligible'][k]} |"
        )

    lines.extend(
        [
            "",
            "Specificity requirement across prevalence scenarios:",
            "",
            "| prevalence q | k=1 | k=2 | k=4 | k=8 | k=16 | k=32 |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for q in PREVALENCE_SCENARIOS:
        vals = r["scenario_frontier"][q]
        lines.append(
            "| "
            + " | ".join(
                [f"{q:.3%}"]
                + [f"{vals[k]:.4%}" for k in HARM_MULTIPLIERS]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "~~~text",
            "Research Enrichment != Intervention Authority",
            "High Enrichment != High Precision",
            "Diagnostic Usefulness != Action Safety",
            "Rare-State Capture != Permission To Treat",
            "~~~",
            "",
            "The same selector can be valuable for selecting research specimens while "
            "remaining far below the specificity required for a high-consequence "
            "positive action in a rare-state population.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
