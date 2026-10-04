"""CGD-SIM-037: two-stage causal-screen -> current-state challenge cascade.

Synthetic observability/control study only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache

from .cognitive_active_diagnosis import FAULT_NAMES, hypotheses
from .cognitive_current_state_challenge import (
    GAP_FLOORS,
    PERFORMANCE_CEILINGS,
    SELF_REPORT_NOISE_STD,
    clamp,
)
from .cognitive_harness_repair import run_episode
from .cognitive_intervention_probe import noisy_probe, train_thresholds
from .cognitive_rare_state import CAPABILITY_CEILING, rare_state_experiment
from random import Random

TRIAL_COUNTS = (32, 64, 128)
HARM_MULTIPLIERS = (1, 2, 4)
PILOT_PER_STRATUM = 250
HELDOUT_PER_STRATUM = 600


def make_dataset(samples_per_stratum, seed_base):
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
                    "fault_set": fault_set,
                    "hypothesis_index": hypothesis_index,
                    "sample": sample,
                    "row_id": hypothesis_index * 100_000 + sample,
                    "capability": capability,
                    "self_estimate": self_estimate,
                    "rare": (
                        capability <= CAPABILITY_CEILING
                        and self_estimate - capability >= threshold
                    ),
                }
            )
    return rows


def causal_stage_mask(rows, thresholds, selected_label, seed_base):
    mask = []
    for row in rows:
        predicted = set()
        for target_index, target_fault in enumerate(FAULT_NAMES):
            value = noisy_probe(
                row["fault_set"],
                target_fault,
                seed_base
                + target_index * 100_000_000
                + row["hypothesis_index"] * 1_000_000
                + row["sample"],
            )
            if value >= thresholds[target_fault]["threshold"]:
                predicted.add(target_fault)
        mask.append(frozenset(predicted) == selected_label)
    return mask


def observations(rows, *, trials, seed_base):
    out = []
    for row in rows:
        rng = Random(seed_base + row["row_id"] * 257 + trials * 65_537)
        successes = sum(
            rng.random() < row["capability"]
            for _ in range(trials)
        )
        perf = successes / trials
        report = clamp(
            row["self_estimate"]
            + rng.gauss(0.0, SELF_REPORT_NOISE_STD)
        )
        out.append(
            {
                "objective_performance": perf,
                "observed_gap": report - perf,
            }
        )
    return out


def evaluate(rows, stage_mask, obs, *, performance_ceiling, gap_floor, k):
    tp = fp = tn = fn = 0
    challenged = sum(stage_mask)
    for row, admitted, o in zip(rows, stage_mask, obs, strict=True):
        positive = (
            admitted
            and o["objective_performance"] <= performance_ceiling
            and o["observed_gap"] >= gap_floor
        )
        truth = row["rare"]
        tp += int(positive and truth)
        fp += int(positive and not truth)
        tn += int((not positive) and (not truth))
        fn += int((not positive) and truth)

    total = len(rows)
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
        "challenge_count": challenged,
        "challenge_fraction": challenged / total,
        "margin": (tp - k * fp) / total,
    }


def select_policy(rows, stage_mask, obs, k):
    candidates = []
    for performance_ceiling in PERFORMANCE_CEILINGS:
        for gap_floor in GAP_FLOORS:
            m = evaluate(
                rows,
                stage_mask,
                obs,
                performance_ceiling=performance_ceiling,
                gap_floor=gap_floor,
                k=k,
            )
            if m["tp"] < 2:
                continue
            candidates.append(
                (
                    m["margin"],
                    m["precision"],
                    m["sensitivity"],
                    -m["selection_rate"],
                    performance_ceiling,
                    gap_floor,
                )
            )
    if not candidates:
        return None
    best = max(candidates)
    return {
        "performance_ceiling": best[4],
        "gap_floor": best[5],
        "pilot_margin": best[0],
    }


@lru_cache(maxsize=1)
def cascade_experiment():
    selected_label = rare_state_experiment()["selected_label"]
    thresholds = train_thresholds(samples_per_hypothesis=40)

    pilot = make_dataset(PILOT_PER_STRATUM, 3_000_000_000)
    heldout = make_dataset(HELDOUT_PER_STRATUM, 3_100_000_000)

    pilot_causal = causal_stage_mask(
        pilot, thresholds, selected_label, 3_010_000_000
    )
    heldout_causal = causal_stage_mask(
        heldout, thresholds, selected_label, 3_110_000_000
    )
    pilot_all = [True] * len(pilot)
    heldout_all = [True] * len(heldout)

    results = []
    for trials in TRIAL_COUNTS:
        pilot_obs = observations(
            pilot, trials=trials, seed_base=3_020_000_000
        )
        heldout_obs = observations(
            heldout, trials=trials, seed_base=3_120_000_000
        )

        for k in HARM_MULTIPLIERS:
            one_policy = select_policy(pilot, pilot_all, pilot_obs, k)
            cascade_policy = select_policy(
                pilot, pilot_causal, pilot_obs, k
            )

            for name, policy, stage_mask in (
                ("current_state_only", one_policy, heldout_all),
                ("causal_then_current_state", cascade_policy, heldout_causal),
            ):
                if policy is None:
                    results.append(
                        {
                            "name": name,
                            "trials": trials,
                            "k": k,
                            "policy": None,
                            "metrics": None,
                        }
                    )
                    continue
                m = evaluate(
                    heldout,
                    stage_mask,
                    heldout_obs,
                    performance_ceiling=policy["performance_ceiling"],
                    gap_floor=policy["gap_floor"],
                    k=k,
                )
                results.append(
                    {
                        "name": name,
                        "trials": trials,
                        "k": k,
                        "policy": policy,
                        "metrics": m,
                    }
                )

    best_cascade = max(
        (
            row for row in results
            if row["name"] == "causal_then_current_state"
            and row["metrics"] is not None
        ),
        key=lambda row: row["metrics"]["margin"],
    )

    return {
        "selected_stratum": (
            "healthy"
            if not selected_label
            else "+".join(sorted(selected_label))
        ),
        "pilot_rare": sum(row["rare"] for row in pilot),
        "heldout_rare": sum(row["rare"] for row in heldout),
        "pilot_total": len(pilot),
        "heldout_total": len(heldout),
        "heldout_causal_candidates": sum(heldout_causal),
        "results": results,
        "best_cascade": best_cascade,
    }


def format_markdown() -> str:
    r = cascade_experiment()
    lines = [
        "# CGD-SIM-037 causal screen -> current-state challenge cascade",
        "",
        "> Synthetic result only. Clinical authority: NONE.",
        "",
        f"- frozen causal target stratum: {r['selected_stratum']}",
        f"- pilot rare: {r['pilot_rare']}/{r['pilot_total']}",
        f"- held-out rare: {r['heldout_rare']}/{r['heldout_total']}",
        (
            "- held-out episodes admitted to expensive current-state challenge "
            f"by causal screen: {r['heldout_causal_candidates']}/{r['heldout_total']} "
            f"({r['heldout_causal_candidates']/r['heldout_total']:.3%})"
        ),
        "",
        "| policy | trials | harm k | perf ceiling | gap floor | sensitivity | specificity | PPV | positive rate | expensive-challenge fraction | margin/B | eligible |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for row in r["results"]:
        if row["policy"] is None:
            lines.append(
                f"| {row['name']} | {row['trials']} | {row['k']} | none | "
                "none | n/a | n/a | n/a | n/a | n/a | n/a | False |"
            )
            continue
        p = row["policy"]
        m = row["metrics"]
        lines.append(
            f"| {row['name']} | {row['trials']} | {row['k']} | "
            f"{p['performance_ceiling']:.2f} | {p['gap_floor']:.2f} | "
            f"{m['sensitivity']:.3%} | {m['specificity']:.3%} | "
            f"{m['precision']:.3%} | {m['selection_rate']:.3%} | "
            f"{m['challenge_fraction']:.3%} | {m['margin']:.6f} | "
            f"{m['margin'] > 0.0} |"
        )

    best = r["best_cascade"]
    bm = best["metrics"]
    bp = best["policy"]
    lines.extend(
        [
            "",
            "Best held-out cascade margin:",
            "",
            f"- trials: {best['trials']}",
            f"- harm k: {best['k']}",
            f"- performance ceiling: {bp['performance_ceiling']:.2f}",
            f"- gap floor: {bp['gap_floor']:.2f}",
            f"- sensitivity: {bm['sensitivity']:.3%}",
            f"- specificity: {bm['specificity']:.3%}",
            f"- PPV: {bm['precision']:.3%}",
            f"- expensive challenge fraction: {bm['challenge_fraction']:.3%}",
            f"- margin/B per episode: {bm['margin']:.6f}",
            "",
            "~~~text",
            "Cause Screen",
            "  -> Current-State Verification",
            "  -> Positive Action Gate",
            "",
            "Cause Screen != Action Authority",
            "Current-State Challenge != Clinical Test",
            "Two-Stage Synthetic Margin > 0 != Deployment Permission",
            "~~~",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
