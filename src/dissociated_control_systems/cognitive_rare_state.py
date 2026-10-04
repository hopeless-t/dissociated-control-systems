"""CGD-SIM-031: rare silent-overconfidence state harvesting.

Synthetic exploratory/confirmatory experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import ceil, log
from statistics import fmean

from .cognitive_active_diagnosis import hypotheses
from .cognitive_harness_repair import run_episode

CAPABILITY_CEILING = 0.55
TARGET_POOLED_RATE = 0.02
THRESHOLD_GRID = (0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55)
PILOT_SAMPLES_PER_HYPOTHESIS = 120
HELDOUT_SAMPLES_PER_HYPOTHESIS = 400


def label_name(label: frozenset[str]) -> str:
    return "healthy" if not label else "+".join(sorted(label))


def episode_row(label, seed):
    episode = run_episode(label, seed, steps=70)
    signed_overconfidence = (
        episode.state.self_estimate - episode.state.capability
    )
    return {
        "label": label,
        "signed_overconfidence": signed_overconfidence,
        "capability": episode.state.capability,
        "self_estimate": episode.state.self_estimate,
        "observer_disagreement": episode.features["observer_disagreement"],
        "handoff_gap": episode.features["handoff_gap"],
        "feedback_error": episode.mean_feedback_error,
        "mean_function": episode.mean_function,
    }


def dataset(samples_per_hypothesis, seed_base):
    rows = []
    for hypothesis_index, label in enumerate(hypotheses()):
        for sample in range(samples_per_hypothesis):
            rows.append(
                episode_row(
                    label,
                    seed_base + hypothesis_index * 1_000_000 + sample,
                )
            )
    return rows


def is_rare(row, threshold):
    return (
        row["capability"] <= CAPABILITY_CEILING
        and row["signed_overconfidence"] >= threshold
    )


def pooled_rate(rows, threshold):
    return fmean(float(is_rare(row, threshold)) for row in rows)


def select_threshold(pilot):
    candidates = []
    for threshold in THRESHOLD_GRID:
        rate = pooled_rate(pilot, threshold)
        # Prefer a genuinely rare but non-empty state, then target ~2%.
        valid = 0.002 <= rate <= 0.08
        candidates.append(
            (
                not valid,
                abs(rate - TARGET_POOLED_RATE),
                -threshold,
                threshold,
                rate,
            )
        )
    _, _, _, threshold, rate = min(candidates)
    return threshold, rate


def stratum_rates(rows, threshold):
    counts = {}
    for label in hypotheses():
        name = label_name(label)
        selected = [row for row in rows if row["label"] == label]
        events = sum(is_rare(row, threshold) for row in selected)
        counts[name] = {
            "label": label,
            "events": events,
            "total": len(selected),
            "rate": events / len(selected),
        }
    return counts


def n_for_at_least_one(rate, probability):
    if rate <= 0.0:
        return None
    if rate >= 1.0:
        return 1
    return ceil(log(1.0 - probability) / log(1.0 - rate))


@lru_cache(maxsize=1)
def rare_state_experiment():
    pilot = dataset(
        PILOT_SAMPLES_PER_HYPOTHESIS,
        2_000_000_000,
    )
    threshold, pilot_pooled_rate = select_threshold(pilot)
    pilot_strata = stratum_rates(pilot, threshold)
    selected_name = max(
        pilot_strata,
        key=lambda name: pilot_strata[name]["rate"],
    )
    selected_label = pilot_strata[selected_name]["label"]

    heldout = dataset(
        HELDOUT_SAMPLES_PER_HYPOTHESIS,
        2_100_000_000,
    )
    heldout_pooled_rate = pooled_rate(heldout, threshold)
    heldout_strata = stratum_rates(heldout, threshold)
    selected = heldout_strata[selected_name]

    rare_rows = [row for row in heldout if is_rare(row, threshold)]
    ordinary_rows = [row for row in heldout if not is_rare(row, threshold)]

    enrichment_ratio = (
        selected["rate"] / heldout_pooled_rate
        if heldout_pooled_rate > 0.0
        else float("inf")
    )
    n95_pooled = n_for_at_least_one(heldout_pooled_rate, 0.95)
    n95_enriched = n_for_at_least_one(selected["rate"], 0.95)

    confirmed_enrichment = (
        selected["events"] >= 3
        and selected["rate"] > heldout_pooled_rate
        and enrichment_ratio >= 2.0
    )

    return {
        "threshold": threshold,
        "pilot_pooled_rate": pilot_pooled_rate,
        "selected_stratum": selected_name,
        "selected_label": selected_label,
        "pilot_selected_rate": pilot_strata[selected_name]["rate"],
        "heldout_pooled_rate": heldout_pooled_rate,
        "heldout_selected_rate": selected["rate"],
        "heldout_selected_events": selected["events"],
        "heldout_selected_total": selected["total"],
        "enrichment_ratio": enrichment_ratio,
        "n95_pooled": n95_pooled,
        "n95_enriched": n95_enriched,
        "confirmed_enrichment": confirmed_enrichment,
        "rare_count": len(rare_rows),
        "total_count": len(heldout),
        "rare_mean_overconfidence": (
            fmean(row["signed_overconfidence"] for row in rare_rows)
            if rare_rows else 0.0
        ),
        "rare_mean_capability": (
            fmean(row["capability"] for row in rare_rows)
            if rare_rows else 0.0
        ),
        "rare_mean_self_estimate": (
            fmean(row["self_estimate"] for row in rare_rows)
            if rare_rows else 0.0
        ),
        "rare_mean_observer_disagreement": (
            fmean(row["observer_disagreement"] for row in rare_rows)
            if rare_rows else 0.0
        ),
        "ordinary_mean_overconfidence": fmean(
            row["signed_overconfidence"] for row in ordinary_rows
        ),
    }


def format_markdown() -> str:
    result = rare_state_experiment()
    n95_pooled = (
        "none" if result["n95_pooled"] is None else str(result["n95_pooled"])
    )
    n95_enriched = (
        "none" if result["n95_enriched"] is None else str(result["n95_enriched"])
    )
    return "\n".join(
        [
            "# CGD-SIM-031 rare silent-overconfidence harvesting",
            "",
            "> Synthetic exploratory/confirmatory result only. Clinical authority: NONE.",
            "",
            "Frozen rare-state family:",
            "",
            "~~~text",
            f"final capability <= {CAPABILITY_CEILING:.2f}",
            "and",
            f"final self_estimate - final capability >= selected threshold",
            "~~~",
            "",
            f"- pilot-selected overconfidence threshold: {result['threshold']:.2f}",
            f"- pilot pooled rare-state rate: {result['pilot_pooled_rate']:.3%}",
            f"- pilot-selected enrichment stratum: {result['selected_stratum']}",
            f"- pilot selected-stratum rate: {result['pilot_selected_rate']:.3%}",
            "",
            "Held-out confirmation:",
            "",
            f"- pooled rare-state rate: {result['heldout_pooled_rate']:.3%}",
            (
                f"- selected-stratum rate: {result['heldout_selected_rate']:.3%} "
                f"({result['heldout_selected_events']}/{result['heldout_selected_total']})"
            ),
            f"- enrichment ratio: {result['enrichment_ratio']:.2f}x",
            f"- confirmed >=2x enrichment: {result['confirmed_enrichment']}",
            f"- 95% chance of >=1 specimen, pooled sampling: {n95_pooled} episodes",
            f"- 95% chance of >=1 specimen, enriched sampling: {n95_enriched} episodes",
            "",
            "Held-out biopsy:",
            "",
            f"- rare specimens: {result['rare_count']}/{result['total_count']}",
            f"- rare mean signed overconfidence: {result['rare_mean_overconfidence']:.3f}",
            f"- ordinary mean signed overconfidence: {result['ordinary_mean_overconfidence']:.3f}",
            f"- rare mean capability: {result['rare_mean_capability']:.3f}",
            f"- rare mean self estimate: {result['rare_mean_self_estimate']:.3f}",
            f"- rare mean observer disagreement: {result['rare_mean_observer_disagreement']:.3f}",
            "",
            "Method transfer:",
            "",
            "~~~text",
            "pilot census",
            "-> select rare-state threshold + enrichment stratum",
            "-> freeze",
            "-> independent-seed confirmation",
            "-> compute capture efficiency",
            "-> biopsy specimens immediately",
            "~~~",
            "",
            "This is the DCS analogue of rare-state harvesting in Finite RAM Lab. "
            "It does not identify a human phenotype or clinical risk threshold.",
        ]
    )


if __name__ == "__main__":
    print(format_markdown())
