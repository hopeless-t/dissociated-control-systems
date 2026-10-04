"""CGD-SIM-046: adaptive objective re-anchor with an independent sentinel.

Synthetic selective-observation scheduler only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

VISITS = 64
PILOT_TRAJECTORIES = 800
HELDOUT_TRAJECTORIES = 1600
SIGMA_STATE_STEP = 0.03
SIGMA_SELF_DRIFT = 0.04
SIGMA_INFORMANT_DRIFT = 0.04
SIGMA_SELF_MEAS = 0.05
SIGMA_INFORMANT_MEAS = 0.05
SIGMA_OBJECTIVE = 0.03
SENTINEL_NUISANCE_LEVELS = (0.02, 0.04)
THRESHOLDS = tuple(step / 100.0 for step in range(5, 31))
MAX_AGE = 16
ANCHOR_COST = 0.08
ACCEPTED_STALE_RMSE_CONTRACT = 0.085
LOW_ERROR_REFERENCE = 0.10


def make_paths(count: int, seed: int, sentinel_sigma: float):
    rng = Random(seed)
    paths = []
    for _ in range(count):
        z = rng.uniform(0.2, 0.8)
        a = rng.uniform(-0.2, 0.2)
        b = rng.uniform(-0.2, 0.2)
        visits = []
        for visit in range(VISITS):
            if visit:
                z += rng.gauss(0.0, SIGMA_STATE_STEP)
                a += rng.gauss(0.0, SIGMA_SELF_DRIFT)
                b += rng.gauss(0.0, SIGMA_INFORMANT_DRIFT)
            self_report = z - a + rng.gauss(0.0, SIGMA_SELF_MEAS)
            informant = z + b + rng.gauss(0.0, SIGMA_INFORMANT_MEAS)
            objective = z + rng.gauss(0.0, SIGMA_OBJECTIVE)
            sentinel = z + rng.gauss(0.0, sentinel_sigma)
            visits.append((z, self_report, informant, objective, sentinel))
        paths.append(visits)
    return paths


def evaluate_policy(paths, policy: str, threshold: float | None = None):
    squared_post_errors = []
    accepted_stale_squared = []
    accepted_stale_count = 0
    accepted_stale_low_accuracy_count = 0
    trigger_count = 0
    low_error_trigger_count = 0
    reacquisitions = 0

    for visits in paths:
        anchor_index = 0
        for index in range(1, len(visits)):
            z, self_report, informant, objective, sentinel = visits[index]
            (
                _z_anchor,
                self_anchor,
                informant_anchor,
                objective_anchor,
                _sentinel_anchor,
            ) = visits[anchor_index]
            age = index - anchor_index

            predicted = objective_anchor + 0.5 * (
                (self_report - self_anchor)
                + (informant - informant_anchor)
            )
            pre_error = predicted - z

            reacquire = False
            triggered = False
            if policy == "fixed8":
                reacquire = age >= 8
            elif policy == "fixed16":
                reacquire = age >= 16
            elif policy in {"sentinel", "dyad"}:
                if threshold is None:
                    raise ValueError("adaptive policy requires threshold")
                if age >= MAX_AGE:
                    reacquire = True
                else:
                    if policy == "sentinel":
                        score = abs(sentinel - predicted)
                    else:
                        score = abs(
                            (informant - self_report)
                            - (informant_anchor - self_anchor)
                        )
                    if score >= threshold:
                        reacquire = True
                        triggered = True
            else:
                raise ValueError(policy)

            if reacquire:
                anchor_index = index
                reacquisitions += 1
                post_error = objective - z
                if triggered:
                    trigger_count += 1
                    if abs(pre_error) <= LOW_ERROR_REFERENCE:
                        low_error_trigger_count += 1
            else:
                post_error = pre_error
                accepted_stale_count += 1
                accepted_stale_squared.append(pre_error * pre_error)
                if abs(pre_error) > LOW_ERROR_REFERENCE:
                    accepted_stale_low_accuracy_count += 1

            squared_post_errors.append(post_error * post_error)

    total_visits = len(squared_post_errors)
    post_mse = fmean(squared_post_errors)
    accepted_stale_rmse = (
        sqrt(fmean(accepted_stale_squared))
        if accepted_stale_squared
        else 0.0
    )
    anchor_rate = reacquisitions / total_visits
    return {
        "overall_rmse": sqrt(post_mse),
        "accepted_stale_rmse": accepted_stale_rmse,
        "accepted_stale_contract": (
            accepted_stale_rmse <= ACCEPTED_STALE_RMSE_CONTRACT
        ),
        "accepted_stale_coverage": accepted_stale_count / total_visits,
        "accepted_stale_gt_reference_rate": (
            accepted_stale_low_accuracy_count / accepted_stale_count
            if accepted_stale_count
            else 0.0
        ),
        "anchor_rate": anchor_rate,
        "reacquisitions": reacquisitions,
        "trigger_count": trigger_count,
        "low_error_trigger_fraction": (
            low_error_trigger_count / trigger_count
            if trigger_count
            else 0.0
        ),
        "loss": post_mse + ANCHOR_COST * anchor_rate,
    }


def select_threshold(paths, policy: str):
    candidates = []
    for threshold in THRESHOLDS:
        metrics = evaluate_policy(paths, policy, threshold)
        if not metrics["accepted_stale_contract"]:
            continue
        candidates.append(
            (
                metrics["loss"],
                -metrics["accepted_stale_coverage"],
                threshold,
                metrics,
            )
        )
    if not candidates:
        return None
    _, _, threshold, metrics = min(candidates)
    return {"threshold": threshold, "pilot_metrics": metrics}


@lru_cache(maxsize=1)
def adaptive_reanchor_experiment():
    levels = []
    for level_index, sentinel_sigma in enumerate(SENTINEL_NUISANCE_LEVELS):
        pilot = make_paths(
            PILOT_TRAJECTORIES,
            4_100_000_000 + level_index * 100_000_000,
            sentinel_sigma,
        )
        heldout = make_paths(
            HELDOUT_TRAJECTORIES,
            4_200_000_000 + level_index * 100_000_000,
            sentinel_sigma,
        )

        sentinel_policy = select_threshold(pilot, "sentinel")
        dyad_policy = select_threshold(pilot, "dyad")
        if sentinel_policy is None or dyad_policy is None:
            raise AssertionError("frozen threshold grid failed to yield a policy")

        fixed8 = evaluate_policy(heldout, "fixed8")
        fixed16 = evaluate_policy(heldout, "fixed16")
        sentinel = evaluate_policy(
            heldout,
            "sentinel",
            sentinel_policy["threshold"],
        )
        dyad = evaluate_policy(
            heldout,
            "dyad",
            dyad_policy["threshold"],
        )

        levels.append(
            {
                "sentinel_sigma": sentinel_sigma,
                "sentinel_threshold": sentinel_policy["threshold"],
                "dyad_threshold": dyad_policy["threshold"],
                "fixed8": fixed8,
                "fixed16": fixed16,
                "sentinel": sentinel,
                "dyad": dyad,
                "sentinel_anchor_reduction_vs_fixed8": (
                    1.0 - sentinel["anchor_rate"] / fixed8["anchor_rate"]
                ),
                "sentinel_loss_gain_vs_fixed8": (
                    (fixed8["loss"] - sentinel["loss"]) / fixed8["loss"]
                ),
                "sentinel_loss_gain_vs_dyad": (
                    (dyad["loss"] - sentinel["loss"]) / dyad["loss"]
                ),
            }
        )

    return {"levels": levels}


def format_markdown() -> str:
    result = adaptive_reanchor_experiment()
    lines = [
        "# CGD-SIM-046 selective adaptive objective re-anchor",
        "",
        "> Synthetic scheduler only. Clinical authority: NONE.",
        "",
        f"- visits / trajectory: {VISITS}",
        f"- pilot trajectories / nuisance level: {PILOT_TRAJECTORIES}",
        f"- held-out trajectories / nuisance level: {HELDOUT_TRAJECTORIES}",
        f"- hard maximum anchor age: {MAX_AGE} visits",
        f"- synthetic anchor cost: {ANCHOR_COST:.3f}",
        (
            "- accepted-stale RMSE contract: <= "
            f"{ACCEPTED_STALE_RMSE_CONTRACT:.3f}"
        ),
        "",
        "Pilot selection:",
        "",
        "~~~text",
        "for each trigger family and sentinel-noise level:",
        "    sweep frozen threshold grid",
        "    reject policies violating accepted-stale RMSE contract",
        "    among survivors minimize post-policy MSE + anchor_cost*anchor_rate",
        "    freeze threshold",
        "    evaluate on disjoint held-out trajectories",
        "~~~",
        "",
        "Held-out comparison:",
        "",
        "| sentinel nuisance | policy | threshold | overall RMSE | accepted-stale RMSE | stale coverage | anchor rate | low-error trigger fraction | synthetic loss | contract |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for level in result["levels"]:
        for name in ("fixed8", "fixed16", "sentinel", "dyad"):
            metrics = level[name]
            if name == "sentinel":
                threshold = f"{level['sentinel_threshold']:.2f}"
            elif name == "dyad":
                threshold = f"{level['dyad_threshold']:.2f}"
            else:
                threshold = "n/a"
            lines.append(
                f"| {level['sentinel_sigma']:.3f} | {name} | {threshold} | "
                f"{metrics['overall_rmse']:.4f} | "
                f"{metrics['accepted_stale_rmse']:.4f} | "
                f"{metrics['accepted_stale_coverage']:.3%} | "
                f"{metrics['anchor_rate']:.3%} | "
                f"{metrics['low_error_trigger_fraction']:.3%} | "
                f"{metrics['loss']:.6f} | "
                f"{metrics['accepted_stale_contract']} |"
            )

        lines.extend(
            [
                "",
                (
                    f"- sigma={level['sentinel_sigma']:.3f}: sentinel anchor reduction "
                    f"vs fixed8 = {level['sentinel_anchor_reduction_vs_fixed8']:.1%}"
                ),
                (
                    f"- sigma={level['sentinel_sigma']:.3f}: sentinel loss gain "
                    f"vs fixed8 = {level['sentinel_loss_gain_vs_fixed8']:.1%}"
                ),
                (
                    f"- sigma={level['sentinel_sigma']:.3f}: sentinel loss gain "
                    f"vs dyad = {level['sentinel_loss_gain_vs_dyad']:.1%}"
                ),
                "",
            ]
        )

    lines.extend(
        [
            "Key result:",
            "",
            "~~~text",
            "Age-Only Freshness Contract",
            "    can be replaced only by",
            "Current Independent Evidence + Selective Acceptance Contract",
            "",
            "Adaptive Scheduling != Permission To Use Stale Evidence",
            "Trigger Validation Precedes Trigger Authority",
            "Dyadic Disagreement Is A Poor Trigger In The Symmetric-Drift World",
            "~~~",
            "",
            "The RMSE thresholds, costs, visit counts and sentinel noise levels are",
            "synthetic. This is not a monitoring schedule or retest recommendation.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
