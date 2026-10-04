"""CGD-SIM-048: context-bound adaptive re-anchor under persistent environment shifts.

Synthetic longitudinal scheduler only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from random import Random
from statistics import fmean
from math import sqrt

VISITS = 64
PILOT_TRAJECTORIES = 600
HELDOUT_TRAJECTORIES = 1200
SIGMA_STATE_STEP = 0.03
SIGMA_SELF_DRIFT = 0.04
SIGMA_INFORMANT_DRIFT = 0.04
SIGMA_SELF_MEAS = 0.05
SIGMA_INFORMANT_MEAS = 0.05
SIGMA_OBJECTIVE = 0.03
SIGMA_FUNCTION = 0.02
SIGMA_CONTEXT = 0.01
ENVIRONMENT_SHIFT = 0.12
ENVIRONMENT_EVENT_PROBABILITIES = (0.0, 0.02, 0.05, 0.10)
THRESHOLDS = tuple(step / 100.0 for step in range(5, 36))
MAX_AGE = 16
ANCHOR_COST = 0.08
ACCEPTED_STALE_RMSE_CONTRACT = 0.085
LOW_ERROR_REFERENCE = 0.10


def make_paths(count: int, seed: int, environment_event_probability: float):
    rng = Random(seed)
    paths = []
    for _ in range(count):
        z = rng.uniform(0.2, 0.8)
        a = rng.uniform(-0.2, 0.2)
        b = rng.uniform(-0.2, 0.2)
        environment = 0.0
        visits = []
        for visit in range(VISITS):
            if visit:
                z += rng.gauss(0.0, SIGMA_STATE_STEP)
                a += rng.gauss(0.0, SIGMA_SELF_DRIFT)
                b += rng.gauss(0.0, SIGMA_INFORMANT_DRIFT)
                if rng.random() < environment_event_probability:
                    environment = ENVIRONMENT_SHIFT * (
                        1.0 if rng.random() < 0.5 else -1.0
                    )

            self_report = z - a + rng.gauss(0.0, SIGMA_SELF_MEAS)
            informant = z + b + rng.gauss(0.0, SIGMA_INFORMANT_MEAS)
            objective = z + rng.gauss(0.0, SIGMA_OBJECTIVE)
            function = z + environment + rng.gauss(0.0, SIGMA_FUNCTION)
            context = environment + rng.gauss(0.0, SIGMA_CONTEXT)
            visits.append(
                {
                    "z": z,
                    "self": self_report,
                    "informant": informant,
                    "objective": objective,
                    "function": function,
                    "context": context,
                    "environment": environment,
                }
            )
        paths.append(visits)
    return paths


def evaluate_policy(paths, policy: str, threshold: float | None = None):
    squared_post_errors = []
    accepted_stale_squared = []
    accepted_stale_count = 0
    accepted_stale_large_error = 0
    reacquisitions = 0
    trigger_count = 0
    low_error_trigger_count = 0
    environment_trigger_count = 0

    for visits in paths:
        anchor_index = 0
        for index in range(1, len(visits)):
            current = visits[index]
            anchor = visits[anchor_index]
            age = index - anchor_index

            predicted = anchor["objective"] + 0.5 * (
                (current["self"] - anchor["self"])
                + (current["informant"] - anchor["informant"])
            )
            pre_error = predicted - current["z"]

            triggered = False
            if policy == "fixed8":
                reacquire = age >= 8
            elif policy == "fixed16":
                reacquire = age >= 16
            elif policy in {"raw_function", "context_normalized"}:
                if threshold is None:
                    raise ValueError("adaptive policy requires threshold")
                if age >= MAX_AGE:
                    reacquire = True
                else:
                    if policy == "raw_function":
                        score = abs(current["function"] - predicted)
                    else:
                        score = abs(
                            current["function"]
                            - current["context"]
                            - predicted
                        )
                    reacquire = score >= threshold
                    triggered = reacquire
            else:
                raise ValueError(policy)

            if reacquire:
                anchor_index = index
                reacquisitions += 1
                post_error = current["objective"] - current["z"]
                if triggered:
                    trigger_count += 1
                    if abs(pre_error) <= LOW_ERROR_REFERENCE:
                        low_error_trigger_count += 1
                    if abs(current["environment"]) > 0.0:
                        environment_trigger_count += 1
            else:
                post_error = pre_error
                accepted_stale_count += 1
                accepted_stale_squared.append(pre_error * pre_error)
                if abs(pre_error) > LOW_ERROR_REFERENCE:
                    accepted_stale_large_error += 1

            squared_post_errors.append(post_error * post_error)

    total = len(squared_post_errors)
    post_mse = fmean(squared_post_errors)
    accepted_stale_rmse = (
        sqrt(fmean(accepted_stale_squared))
        if accepted_stale_squared
        else 0.0
    )
    anchor_rate = reacquisitions / total
    return {
        "overall_rmse": sqrt(post_mse),
        "accepted_stale_rmse": accepted_stale_rmse,
        "accepted_stale_contract": (
            accepted_stale_rmse <= ACCEPTED_STALE_RMSE_CONTRACT
        ),
        "accepted_stale_coverage": accepted_stale_count / total,
        "accepted_stale_gt_reference_rate": (
            accepted_stale_large_error / accepted_stale_count
            if accepted_stale_count
            else 0.0
        ),
        "anchor_rate": anchor_rate,
        "trigger_count": trigger_count,
        "low_error_trigger_fraction": (
            low_error_trigger_count / trigger_count
            if trigger_count
            else 0.0
        ),
        "environment_trigger_fraction": (
            environment_trigger_count / trigger_count
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
def context_bound_scheduler_experiment():
    levels = []
    for level_index, event_probability in enumerate(
        ENVIRONMENT_EVENT_PROBABILITIES
    ):
        pilot = make_paths(
            PILOT_TRAJECTORIES,
            4_500_000_000 + level_index * 100_000_000,
            event_probability,
        )
        heldout = make_paths(
            HELDOUT_TRAJECTORIES,
            4_600_000_000 + level_index * 100_000_000,
            event_probability,
        )

        raw_policy = select_threshold(pilot, "raw_function")
        normalized_policy = select_threshold(pilot, "context_normalized")
        if raw_policy is None or normalized_policy is None:
            raise AssertionError("frozen threshold grid yielded no valid policy")

        fixed8 = evaluate_policy(heldout, "fixed8")
        fixed16 = evaluate_policy(heldout, "fixed16")
        raw = evaluate_policy(
            heldout,
            "raw_function",
            raw_policy["threshold"],
        )
        normalized = evaluate_policy(
            heldout,
            "context_normalized",
            normalized_policy["threshold"],
        )

        levels.append(
            {
                "event_probability": event_probability,
                "raw_threshold": raw_policy["threshold"],
                "normalized_threshold": normalized_policy["threshold"],
                "fixed8": fixed8,
                "fixed16": fixed16,
                "raw": raw,
                "normalized": normalized,
                "normalized_loss_gain_vs_raw": (
                    (raw["loss"] - normalized["loss"]) / raw["loss"]
                ),
                "normalized_anchor_reduction_vs_raw": (
                    1.0 - normalized["anchor_rate"] / raw["anchor_rate"]
                ),
                "normalized_loss_gain_vs_fixed8": (
                    (fixed8["loss"] - normalized["loss"])
                    / fixed8["loss"]
                ),
            }
        )

    return {"levels": levels}


def format_markdown() -> str:
    result = context_bound_scheduler_experiment()
    lines = [
        "# CGD-SIM-048 context-bound adaptive re-anchor",
        "",
        "> Synthetic longitudinal scheduler only. Clinical authority: NONE.",
        "",
        f"- visits / trajectory: {VISITS}",
        f"- pilot trajectories / level: {PILOT_TRAJECTORIES}",
        f"- held-out trajectories / level: {HELDOUT_TRAJECTORIES}",
        f"- environment shift magnitude: +/- {ENVIRONMENT_SHIFT:.2f}",
        f"- functional measurement noise std: {SIGMA_FUNCTION:.2f}",
        f"- context measurement noise std: {SIGMA_CONTEXT:.2f}",
        f"- synthetic anchor cost: {ANCHOR_COST:.2f}",
        f"- accepted-stale RMSE contract: <= {ACCEPTED_STALE_RMSE_CONTRACT:.3f}",
        "",
        "Environment state is piecewise persistent. On an event it jumps to a",
        "signed +/-0.12 offset and remains there until a later event changes it.",
        "",
        "| env event prob / visit | policy | threshold | overall RMSE | accepted-stale RMSE | stale coverage | anchor rate | low-error trigger fraction | environment trigger fraction | loss | contract |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for level in result["levels"]:
        for name in ("fixed8", "fixed16", "raw", "normalized"):
            metrics = level[name]
            if name == "raw":
                threshold = f"{level['raw_threshold']:.2f}"
            elif name == "normalized":
                threshold = f"{level['normalized_threshold']:.2f}"
            else:
                threshold = "n/a"
            lines.append(
                f"| {level['event_probability']:.1%} | {name} | {threshold} | "
                f"{metrics['overall_rmse']:.4f} | "
                f"{metrics['accepted_stale_rmse']:.4f} | "
                f"{metrics['accepted_stale_coverage']:.3%} | "
                f"{metrics['anchor_rate']:.3%} | "
                f"{metrics['low_error_trigger_fraction']:.3%} | "
                f"{metrics['environment_trigger_fraction']:.3%} | "
                f"{metrics['loss']:.6f} | "
                f"{metrics['accepted_stale_contract']} |"
            )

        lines.extend(
            [
                "",
                (
                    f"- p={level['event_probability']:.1%}: normalized loss gain "
                    f"vs raw = {level['normalized_loss_gain_vs_raw']:.1%}"
                ),
                (
                    f"- p={level['event_probability']:.1%}: normalized anchor reduction "
                    f"vs raw = {level['normalized_anchor_reduction_vs_raw']:.1%}"
                ),
                (
                    f"- p={level['event_probability']:.1%}: normalized loss gain "
                    f"vs fixed8 = {level['normalized_loss_gain_vs_fixed8']:.1%}"
                ),
                "",
            ]
        )

    lines.extend(
        [
            "Key result:",
            "",
            "~~~text",
            "Function Innovation Without Context Binding",
            "    can mistake scaffold/environment change for state change",
            "",
            "Context-Bound Function Innovation",
            "    can preserve selective freshness with fewer false re-anchors",
            "",
            "Observation Context Is Part Of Evidence Identity",
            "~~~",
            "",
            "All environment rates, offsets, costs and RMSE contracts are synthetic",
            "scenario parameters. The experiment does not define monitoring or retest",
            "rules for any person, instrument, home environment or support system.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
