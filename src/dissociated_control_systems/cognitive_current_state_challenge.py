"""CGD-SIM-036: standardized current-state challenge.

Synthetic observability experiment only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random

from .cognitive_active_diagnosis import hypotheses
from .cognitive_harness_repair import run_episode
from .cognitive_rare_state import (
    CAPABILITY_CEILING,
    rare_state_experiment,
)

TRIAL_COUNTS = (8, 16, 32, 64, 128)
PERFORMANCE_CEILINGS = (0.45, 0.50, 0.55, 0.60, 0.65)
GAP_FLOORS = (0.15, 0.20, 0.25, 0.30, 0.35, 0.40)
HARM_MULTIPLIERS = (1, 2, 4, 8)
SELF_REPORT_NOISE_STD = 0.05
PILOT_PER_STRATUM = 120
HELDOUT_PER_STRATUM = 300


def clamp(x):
    return min(1.0, max(0.0, x))


def make_latent_dataset(samples_per_stratum, seed_base):
    threshold = rare_state_experiment()["threshold"]
    rows = []
    for hypothesis_index, fault_set in enumerate(hypotheses()):
        for sample in range(samples_per_stratum):
            seed = seed_base + hypothesis_index * 1_000_000 + sample
            episode = run_episode(fault_set, seed, steps=70)
            capability = episode.state.capability
            self_estimate = episode.state.self_estimate
            rows.append(
                {
                    "capability": capability,
                    "self_estimate": self_estimate,
                    "rare": (
                        capability <= CAPABILITY_CEILING
                        and self_estimate - capability >= threshold
                    ),
                    "row_id": hypothesis_index * 100_000 + sample,
                }
            )
    return rows


def observe_current_state(row, *, trials, seed_base):
    rng = Random(seed_base + row["row_id"] * 257 + trials * 65_537)
    successes = sum(
        rng.random() < row["capability"]
        for _ in range(trials)
    )
    objective_performance = successes / trials
    reported_confidence = clamp(
        row["self_estimate"] + rng.gauss(0.0, SELF_REPORT_NOISE_STD)
    )
    observed_gap = reported_confidence - objective_performance
    return {
        "objective_performance": objective_performance,
        "reported_confidence": reported_confidence,
        "observed_gap": observed_gap,
    }


def confusion(rows, observations, *, performance_ceiling, gap_floor):
    tp = fp = tn = fn = 0
    for row, obs in zip(rows, observations, strict=True):
        predicted = (
            obs["objective_performance"] <= performance_ceiling
            and obs["observed_gap"] >= gap_floor
        )
        truth = row["rare"]
        tp += int(predicted and truth)
        fp += int(predicted and not truth)
        tn += int((not predicted) and (not truth))
        fn += int((not predicted) and truth)
    total = tp + fp + tn + fn
    rare_total = tp + fn
    nonrare_total = tn + fp
    sensitivity = tp / rare_total if rare_total else 0.0
    specificity = tn / nonrare_total if nonrare_total else 1.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    selection_rate = (tp + fp) / total
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "precision": precision,
        "selection_rate": selection_rate,
        "total": total,
    }


def margin(metrics, harm_multiplier):
    # Per-episode expected margin in units of correct-action benefit B.
    return (
        metrics["tp"] - harm_multiplier * metrics["fp"]
    ) / metrics["total"]


def choose_pilot_policy(rows, observations, harm_multiplier):
    candidates = []
    for performance_ceiling in PERFORMANCE_CEILINGS:
        for gap_floor in GAP_FLOORS:
            metrics = confusion(
                rows,
                observations,
                performance_ceiling=performance_ceiling,
                gap_floor=gap_floor,
            )
            if metrics["tp"] < 3:
                continue
            candidates.append(
                (
                    margin(metrics, harm_multiplier),
                    metrics["precision"],
                    metrics["sensitivity"],
                    -metrics["selection_rate"],
                    performance_ceiling,
                    gap_floor,
                    metrics,
                )
            )
    if not candidates:
        return None
    best = max(candidates)
    return {
        "performance_ceiling": best[4],
        "gap_floor": best[5],
        "pilot_metrics": best[6],
        "pilot_margin": best[0],
    }


@lru_cache(maxsize=1)
def current_state_challenge_experiment():
    pilot = make_latent_dataset(PILOT_PER_STRATUM, 2_700_000_000)
    heldout = make_latent_dataset(HELDOUT_PER_STRATUM, 2_800_000_000)

    rows = []
    for trials in TRIAL_COUNTS:
        pilot_obs = [
            observe_current_state(
                row,
                trials=trials,
                seed_base=2_710_000_000,
            )
            for row in pilot
        ]
        heldout_obs = [
            observe_current_state(
                row,
                trials=trials,
                seed_base=2_810_000_000,
            )
            for row in heldout
        ]

        for k in HARM_MULTIPLIERS:
            policy = choose_pilot_policy(pilot, pilot_obs, k)
            if policy is None:
                rows.append(
                    {
                        "trials": trials,
                        "harm_multiplier": k,
                        "policy": None,
                        "heldout_metrics": None,
                        "heldout_margin": None,
                        "eligible": False,
                    }
                )
                continue

            metrics = confusion(
                heldout,
                heldout_obs,
                performance_ceiling=policy["performance_ceiling"],
                gap_floor=policy["gap_floor"],
            )
            heldout_margin = margin(metrics, k)
            rows.append(
                {
                    "trials": trials,
                    "harm_multiplier": k,
                    "policy": policy,
                    "heldout_metrics": metrics,
                    "heldout_margin": heldout_margin,
                    "eligible": heldout_margin > 0.0,
                }
            )

    best_research = max(
        (
            row for row in rows
            if row["heldout_metrics"] is not None
        ),
        key=lambda row: row["heldout_metrics"]["precision"],
    )

    return {
        "rare_threshold": rare_state_experiment()["threshold"],
        "pilot_rare": sum(row["rare"] for row in pilot),
        "pilot_total": len(pilot),
        "heldout_rare": sum(row["rare"] for row in heldout),
        "heldout_total": len(heldout),
        "rows": rows,
        "best_research": best_research,
    }


def format_markdown() -> str:
    r = current_state_challenge_experiment()
    lines = [
        "# CGD-SIM-036 standardized current-state challenge",
        "",
        "> Synthetic observability result only. Clinical authority: NONE.",
        "",
        "Challenge observation:",
        "",
        "~~~text",
        "fixed number of standardized task trials",
        "    -> objective success rate",
        "",
        "noisy self report",
        "    -> reported confidence",
        "",
        "observed gap = reported confidence - objective success rate",
        "~~~",
        "",
        f"- latent rare definition capability ceiling: {CAPABILITY_CEILING:.2f}",
        f"- latent rare definition overconfidence threshold: {r['rare_threshold']:.2f}",
        f"- self-report measurement noise std: {SELF_REPORT_NOISE_STD:.2f}",
        f"- pilot rare prevalence: {r['pilot_rare']}/{r['pilot_total']} ({r['pilot_rare']/r['pilot_total']:.3%})",
        f"- held-out rare prevalence: {r['heldout_rare']}/{r['heldout_total']} ({r['heldout_rare']/r['heldout_total']:.3%})",
        "",
        "Pilot-selected policy -> held-out result:",
        "",
        "| task trials | harm k | perf ceiling | gap floor | held-out sensitivity | specificity | PPV | selection rate | margin/B per episode | eligible |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for row in r["rows"]:
        if row["policy"] is None:
            lines.append(
                f"| {row['trials']} | {row['harm_multiplier']} | none | none | "
                "n/a | n/a | n/a | n/a | n/a | False |"
            )
            continue
        p = row["policy"]
        m = row["heldout_metrics"]
        lines.append(
            f"| {row['trials']} | {row['harm_multiplier']} | "
            f"{p['performance_ceiling']:.2f} | {p['gap_floor']:.2f} | "
            f"{m['sensitivity']:.3%} | {m['specificity']:.3%} | "
            f"{m['precision']:.3%} | {m['selection_rate']:.3%} | "
            f"{row['heldout_margin']:.6f} | {row['eligible']} |"
        )

    best = r["best_research"]
    bm = best["heldout_metrics"]
    bp = best["policy"]
    lines.extend(
        [
            "",
            "Best held-out PPV among pilot-selected policies:",
            "",
            f"- trials: {best['trials']}",
            f"- pilot-selected for harm k: {best['harm_multiplier']}",
            f"- performance ceiling: {bp['performance_ceiling']:.2f}",
            f"- observed-gap floor: {bp['gap_floor']:.2f}",
            f"- sensitivity: {bm['sensitivity']:.3%}",
            f"- specificity: {bm['specificity']:.3%}",
            f"- PPV: {bm['precision']:.3%}",
            "",
            "~~~text",
            "Fault Class != Current State",
            "Standardized Objective Challenge + Self Report",
            "    can add within-stratum information",
            "",
            "More Trials -> Less Objective-Performance Sampling Noise",
            "but",
            "Synthetic Challenge Success != Clinical Validation",
            "~~~",
            "",
            "The challenge never emits latent capability or latent self estimate. "
            "They are used only by the generator and truth evaluator.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
