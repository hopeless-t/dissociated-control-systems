"""Second-stage synthetic experiments for cognitive graceful degradation.

All results are consequences of declared toy equations. They have no clinical
authority and do not identify a biological mechanism.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from random import Random
from statistics import fmean

from .cognitive_decline import optimal_compensation


def _unit(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def _nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0")
    return value


def _clamp(value: float) -> float:
    return min(1.0, max(0.0, value))


@dataclass(frozen=True)
class LayeredConfig:
    name: str
    steps: int = 100
    initial_capability: float = 1.0
    initial_self_estimate: float = 1.0
    decline_rate: float = 0.005
    feedback_gain: float = 0.2
    compensation_cost: float = 0.2
    decline_rate_reduction: float = 0.0
    compensation_enabled: bool = True
    policy_reliability: float = 1.0
    feedback_noise: float = 0.0
    shock_probability: float = 0.0
    shock_magnitude: float = 0.0
    calibration_threshold: float = 0.05


@dataclass(frozen=True)
class LayeredStep:
    t: int
    capability: float
    self_estimate: float
    metacognitive_gap: float
    desired_compensation: float
    applied_compensation: float
    functional_performance: float
    observability_amplification: float
    handoff_deficit: float
    calibration_breach: bool


@dataclass(frozen=True)
class LayeredSummary:
    mean_function: float
    minimum_function: float
    final_capability: float
    final_self_estimate: float
    final_gap: float
    max_observability_amplification: float
    calibration_breach_fraction: float
    mean_handoff_deficit: float


def simulate_layered(
    config: LayeredConfig,
    *,
    seed: int = 0,
) -> tuple[LayeredStep, ...]:
    """Simulate an L0/L1/L2 control stack with bounded synthetic noise."""
    if isinstance(config.steps, bool) or not isinstance(config.steps, int):
        raise TypeError("steps must be an integer")
    if config.steps < 1:
        raise ValueError("steps must be >= 1")

    capability = _unit(config.initial_capability, "initial_capability")
    self_estimate = _unit(config.initial_self_estimate, "initial_self_estimate")
    feedback_gain = _unit(config.feedback_gain, "feedback_gain")
    decline_rate_reduction = _unit(
        config.decline_rate_reduction, "decline_rate_reduction"
    )
    policy_reliability = _unit(config.policy_reliability, "policy_reliability")
    shock_probability = _unit(config.shock_probability, "shock_probability")
    decline_rate = _nonnegative(config.decline_rate, "decline_rate")
    feedback_noise = _nonnegative(config.feedback_noise, "feedback_noise")
    shock_magnitude = _nonnegative(config.shock_magnitude, "shock_magnitude")
    calibration_threshold = _nonnegative(
        config.calibration_threshold, "calibration_threshold"
    )
    if config.compensation_cost <= 0.0:
        raise ValueError("compensation_cost must be > 0")

    rng = Random(seed)
    rows: list[LayeredStep] = []

    for t in range(config.steps + 1):
        desired = (
            optimal_compensation(self_estimate, config.compensation_cost)
            if config.compensation_enabled
            else 0.0
        )
        applied = policy_reliability * desired
        performance = capability + (1.0 - capability) * applied
        amplification = 1.0 / ((1.0 - applied) ** 2)

        true_optimum = (
            optimal_compensation(capability, config.compensation_cost)
            if config.compensation_enabled
            else 0.0
        )
        gap = self_estimate - capability

        rows.append(
            LayeredStep(
                t=t,
                capability=capability,
                self_estimate=self_estimate,
                metacognitive_gap=gap,
                desired_compensation=desired,
                applied_compensation=applied,
                functional_performance=performance,
                observability_amplification=amplification,
                handoff_deficit=max(0.0, true_optimum - applied),
                calibration_breach=abs(gap) > calibration_threshold,
            )
        )

        if t == config.steps:
            break

        # L1: self/monitor estimate updates toward an objective observation.
        observed = _clamp(capability + rng.gauss(0.0, feedback_noise))
        self_estimate = _clamp(
            self_estimate + feedback_gain * (observed - self_estimate)
        )

        # L0 slow dynamics, plus optional bounded rare decline shock.
        decline = decline_rate * (1.0 - decline_rate_reduction)
        if shock_probability and rng.random() < shock_probability:
            decline += shock_magnitude
        capability = _clamp(capability - decline)

    return tuple(rows)


def summarize_layered(rows: tuple[LayeredStep, ...]) -> LayeredSummary:
    if not rows:
        raise ValueError("rows must not be empty")
    return LayeredSummary(
        mean_function=fmean(row.functional_performance for row in rows),
        minimum_function=min(row.functional_performance for row in rows),
        final_capability=rows[-1].capability,
        final_self_estimate=rows[-1].self_estimate,
        final_gap=rows[-1].metacognitive_gap,
        max_observability_amplification=max(
            row.observability_amplification for row in rows
        ),
        calibration_breach_fraction=fmean(
            float(row.calibration_breach) for row in rows
        ),
        mean_handoff_deficit=fmean(row.handoff_deficit for row in rows),
    )


def quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("values must not be empty")
    q = _unit(q, "q")
    ordered = sorted(float(v) for v in values)
    position = (len(ordered) - 1) * q
    lower = int(position)
    upper = min(len(ordered) - 1, lower + 1)
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def parameter_sweep() -> dict[str, object]:
    decline_rates = (0.0025, 0.005, 0.0075)
    feedback_gains = (0.05, 0.1, 0.2, 0.4)
    compensation_costs = (0.05, 0.1, 0.2, 0.5)
    decline_reductions = (0.25, 0.5, 0.75)

    total = 0
    dual_beats_baseline = 0
    dual_beats_both_single_tracks = 0
    high_observability_cost = 0
    masked_success_cases: list[dict[str, float]] = []
    gains_vs_best_single: list[float] = []
    best_under_amp_two: dict[str, float] | None = None

    for d, k, cost, q in product(
        decline_rates,
        feedback_gains,
        compensation_costs,
        decline_reductions,
    ):
        common = dict(
            steps=100,
            decline_rate=d,
            feedback_gain=k,
            compensation_cost=cost,
        )
        baseline = summarize_layered(
            simulate_layered(
                LayeredConfig(
                    name="baseline",
                    compensation_enabled=False,
                    **common,
                )
            )
        )
        compensation = summarize_layered(
            simulate_layered(
                LayeredConfig(
                    name="compensation_only",
                    compensation_enabled=True,
                    **common,
                )
            )
        )
        root = summarize_layered(
            simulate_layered(
                LayeredConfig(
                    name="decline_reduction_only",
                    compensation_enabled=False,
                    decline_rate_reduction=q,
                    **common,
                )
            )
        )
        dual = summarize_layered(
            simulate_layered(
                LayeredConfig(
                    name="dual_track",
                    compensation_enabled=True,
                    decline_rate_reduction=q,
                    **common,
                )
            )
        )

        total += 1
        if dual.mean_function > baseline.mean_function:
            dual_beats_baseline += 1
        if (
            dual.mean_function > compensation.mean_function
            and dual.mean_function > root.mean_function
        ):
            dual_beats_both_single_tracks += 1

        gain = dual.mean_function - max(
            compensation.mean_function,
            root.mean_function,
        )
        gains_vs_best_single.append(gain)

        if dual.max_observability_amplification >= 4.0:
            high_observability_cost += 1

        # Masked-success signature: compensation-only looks at least as good on
        # surface function while retaining materially less latent capability
        # and paying substantially more observability amplification.
        if (
            compensation.mean_function >= dual.mean_function
            and dual.final_capability - compensation.final_capability >= 0.15
            and compensation.max_observability_amplification
            > dual.max_observability_amplification * 2.0
        ):
            masked_success_cases.append(
                {
                    "decline_rate": d,
                    "feedback_gain": k,
                    "compensation_cost": cost,
                    "decline_reduction": q,
                    "comp_only_mean_function": compensation.mean_function,
                    "dual_mean_function": dual.mean_function,
                    "comp_only_final_capability": compensation.final_capability,
                    "dual_final_capability": dual.final_capability,
                    "comp_only_max_amp": compensation.max_observability_amplification,
                    "dual_max_amp": dual.max_observability_amplification,
                }
            )

        if dual.max_observability_amplification <= 2.0:
            candidate = {
                "mean_function": dual.mean_function,
                "minimum_function": dual.minimum_function,
                "final_capability": dual.final_capability,
                "max_amp": dual.max_observability_amplification,
                "decline_rate": d,
                "feedback_gain": k,
                "compensation_cost": cost,
                "decline_reduction": q,
            }
            if (
                best_under_amp_two is None
                or candidate["mean_function"] > best_under_amp_two["mean_function"]
            ):
                best_under_amp_two = candidate

    return {
        "cells": total,
        "dual_beats_baseline": dual_beats_baseline,
        "dual_beats_both_single_tracks": dual_beats_both_single_tracks,
        "median_gain_vs_best_single": quantile(gains_vs_best_single, 0.5),
        "high_observability_cost_cells": high_observability_cost,
        "masked_success_cases": masked_success_cases,
        "best_dual_under_amp_two": best_under_amp_two,
    }


def monte_carlo(
    *,
    samples: int = 500,
) -> dict[str, dict[str, float]]:
    if isinstance(samples, bool) or not isinstance(samples, int) or samples < 1:
        raise ValueError("samples must be a positive integer")

    scenarios = (
        ("baseline", False, 0.0),
        ("compensation_only", True, 0.0),
        ("decline_reduction_only", False, 0.5),
        ("dual_track", True, 0.5),
    )
    output: dict[str, dict[str, float]] = {}

    for name, compensation_enabled, decline_rate_reduction in scenarios:
        summaries: list[LayeredSummary] = []
        for seed in range(samples):
            summaries.append(
                summarize_layered(
                    simulate_layered(
                        LayeredConfig(
                            name=name,
                            steps=100,
                            decline_rate=0.005,
                            feedback_gain=0.2,
                            compensation_cost=0.2,
                            decline_rate_reduction=decline_rate_reduction,
                            compensation_enabled=compensation_enabled,
                            feedback_noise=0.03,
                            shock_probability=0.04,
                            shock_magnitude=0.01,
                        ),
                        seed=seed,
                    )
                )
            )
        output[name] = {
            "mean_function": fmean(s.mean_function for s in summaries),
            "p05_minimum_function": quantile(
                [s.minimum_function for s in summaries], 0.05
            ),
            "mean_final_capability": fmean(
                s.final_capability for s in summaries
            ),
            "p95_abs_final_gap": quantile(
                [abs(s.final_gap) for s in summaries], 0.95
            ),
            "mean_calibration_breach_fraction": fmean(
                s.calibration_breach_fraction for s in summaries
            ),
            "mean_max_observability_amplification": fmean(
                s.max_observability_amplification for s in summaries
            ),
        }

    return output


def layer_ablation() -> dict[str, LayeredSummary]:
    cases = (
        ("reference", 0.4, 1.0),
        ("l1_slow_calibration", 0.05, 1.0),
        ("l2_unreliable_handoff", 0.4, 0.35),
        ("l1_l2_combined", 0.05, 0.35),
    )
    return {
        name: summarize_layered(
            simulate_layered(
                LayeredConfig(
                    name=name,
                    steps=120,
                    decline_rate=0.005,
                    feedback_gain=feedback_gain,
                    compensation_cost=0.2,
                    decline_rate_reduction=0.0,
                    compensation_enabled=True,
                    policy_reliability=policy_reliability,
                    calibration_threshold=0.05,
                )
            )
        )
        for name, feedback_gain, policy_reliability in cases
    }


def format_markdown() -> str:
    sweep = parameter_sweep()
    monte = monte_carlo()
    ablation = layer_ablation()

    lines = [
        "# CGD-SIM-002 robustness and meta-layer experiments",
        "",
        "> Synthetic control-model results only. Clinical authority: NONE.",
        "",
        "## Parameter sweep",
        "",
        f"- cells: {sweep['cells']}",
        f"- dual-track mean function > baseline: {sweep['dual_beats_baseline']}/{sweep['cells']}",
        (
            "- dual-track mean function > both single tracks: "
            f"{sweep['dual_beats_both_single_tracks']}/{sweep['cells']}"
        ),
        (
            "- median dual-track mean-function gain vs best single track: "
            f"{sweep['median_gain_vs_best_single']:.6f}"
        ),
        (
            "- dual-track cells with max observability amplification >= 4x: "
            f"{sweep['high_observability_cost_cells']}/{sweep['cells']}"
        ),
        (
            "- masked-success cases (surface function favors compensation-only "
            "despite >=0.15 less latent capability and >2x observability cost): "
            f"{len(sweep['masked_success_cases'])}"
        ),
        "",
    ]

    masked = sweep["masked_success_cases"]
    if masked:
        first = masked[0]
        lines.extend(
            [
                "First masked-success example:",
                "",
                (
                    f"- d={first['decline_rate']}, k={first['feedback_gain']}, "
                    f"lambda={first['compensation_cost']}, q={first['decline_reduction']}"
                ),
                (
                    "- compensation-only: "
                    f"mean_function={first['comp_only_mean_function']:.6f}, "
                    f"final_capability={first['comp_only_final_capability']:.3f}, "
                    f"max_amp={first['comp_only_max_amp']:.3f}"
                ),
                (
                    "- dual-track: "
                    f"mean_function={first['dual_mean_function']:.6f}, "
                    f"final_capability={first['dual_final_capability']:.3f}, "
                    f"max_amp={first['dual_max_amp']:.3f}"
                ),
                "",
            ]
        )

    best = sweep["best_dual_under_amp_two"]
    if best is not None:
        lines.extend(
            [
                "Best dual-track cell under <=2x observability amplification:",
                "",
                (
                    f"- d={best['decline_rate']}, k={best['feedback_gain']}, "
                    f"lambda={best['compensation_cost']}, q={best['decline_reduction']}"
                ),
                (
                    f"- mean_function={best['mean_function']:.6f}, "
                    f"minimum_function={best['minimum_function']:.6f}, "
                    f"final_capability={best['final_capability']:.3f}, "
                    f"max_amp={best['max_amp']:.3f}"
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Monte Carlo",
            "",
            "500 deterministic seeds; feedback noise sd=0.03; 4%/step rare decline shock of 0.01.",
            "",
            "| arm | mean function | p05 minimum function | mean final capability | p95 abs final gap | mean calibration breach | mean max amp |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for name in (
        "baseline",
        "compensation_only",
        "decline_reduction_only",
        "dual_track",
    ):
        result = monte[name]
        lines.append(
            f"| {name} | {result['mean_function']:.3f} | "
            f"{result['p05_minimum_function']:.3f} | "
            f"{result['mean_final_capability']:.3f} | "
            f"{result['p95_abs_final_gap']:.3f} | "
            f"{result['mean_calibration_breach_fraction']:.3f} | "
            f"{result['mean_max_observability_amplification']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Meta-layer ablation",
            "",
            "L1 = self/monitor calibration. L2 = compensation/handoff reliability.",
            "",
            "| case | mean function | min function | final gap | calibration breach | mean handoff deficit | max amp |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for name in (
        "reference",
        "l1_slow_calibration",
        "l2_unreliable_handoff",
        "l1_l2_combined",
    ):
        result = ablation[name]
        lines.append(
            f"| {name} | {result.mean_function:.3f} | "
            f"{result.minimum_function:.3f} | {result.final_gap:.3f} | "
            f"{result.calibration_breach_fraction:.3f} | "
            f"{result.mean_handoff_deficit:.3f} | "
            f"{result.max_observability_amplification:.3f} |"
        )

    lines.extend(
        [
            "",
            "Interpretation ceiling: these experiments compare declared control "
            "architectures under synthetic degradation, noise, and failure injection. "
            "They do not model dementia progression or treatment efficacy.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("markdown",), default="markdown")
    parser.parse_args()
    print(format_markdown())


if __name__ == "__main__":
    main()
