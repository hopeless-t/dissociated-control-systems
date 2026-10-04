"""Deterministic synthetic model for cognitive graceful degradation.

This is a control-theory toy model. It has no clinical authority and does not
claim that any variable corresponds to a unique biological mechanism.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from statistics import fmean
from typing import Iterable


def _unit(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


@dataclass(frozen=True)
class SimulationConfig:
    name: str
    steps: int = 100
    initial_capability: float = 1.0
    initial_self_estimate: float = 1.0
    decline_rate: float = 0.005
    feedback_gain: float = 0.2
    compensation_cost: float = 0.2
    decline_rate_reduction: float = 0.0
    compensation_enabled: bool = False


@dataclass(frozen=True)
class CognitiveStep:
    t: int
    capability: float
    self_estimate: float
    metacognitive_gap: float
    compensation: float
    functional_performance: float
    observability_amplification: float


def optimal_compensation(capability: float, cost: float) -> float:
    """Known-answer optimum for J=(1-p)^2 + cost*r^2, p=c+(1-c)r."""
    capability = _unit(capability, "capability")
    if isinstance(cost, bool) or not isinstance(cost, (int, float)):
        raise TypeError("cost must be a real number")
    cost = float(cost)
    if cost <= 0.0:
        raise ValueError("cost must be > 0")
    deficit = 1.0 - capability
    return (deficit * deficit) / ((deficit * deficit) + cost)


def simulate(config: SimulationConfig) -> tuple[CognitiveStep, ...]:
    """Run a deterministic trajectory under the declared synthetic assumptions."""
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

    if isinstance(config.decline_rate, bool) or not isinstance(
        config.decline_rate, (int, float)
    ):
        raise TypeError("decline_rate must be a real number")
    decline_rate = float(config.decline_rate)
    if decline_rate < 0.0:
        raise ValueError("decline_rate must be >= 0")

    if config.compensation_cost <= 0.0:
        raise ValueError("compensation_cost must be > 0")

    rows: list[CognitiveStep] = []
    for t in range(config.steps + 1):
        compensation = (
            optimal_compensation(capability, config.compensation_cost)
            if config.compensation_enabled
            else 0.0
        )
        functional_performance = capability + (1.0 - capability) * compensation

        # If assisted performance p = r + (1-r)c + epsilon is inverted to
        # estimate c, observation-noise variance is amplified by 1/(1-r)^2.
        observability_amplification = 1.0 / ((1.0 - compensation) ** 2)

        rows.append(
            CognitiveStep(
                t=t,
                capability=capability,
                self_estimate=self_estimate,
                metacognitive_gap=self_estimate - capability,
                compensation=compensation,
                functional_performance=functional_performance,
                observability_amplification=observability_amplification,
            )
        )

        if t == config.steps:
            break

        # Self-model update from objective feedback.
        self_estimate = min(
            1.0,
            max(
                0.0,
                self_estimate + feedback_gain * (capability - self_estimate),
            ),
        )

        # Synthetic slow-loop intervention: reduce the declared decline rate.
        effective_decline = decline_rate * (1.0 - decline_rate_reduction)
        capability = min(1.0, max(0.0, capability - effective_decline))

    return tuple(rows)


def summarize(rows: Iterable[CognitiveStep]) -> dict[str, float]:
    rows = tuple(rows)
    if not rows:
        raise ValueError("rows must not be empty")
    return {
        "final_capability": rows[-1].capability,
        "final_self_estimate": rows[-1].self_estimate,
        "final_metacognitive_gap": rows[-1].metacognitive_gap,
        "mean_functional_performance": fmean(
            row.functional_performance for row in rows
        ),
        "minimum_functional_performance": min(
            row.functional_performance for row in rows
        ),
        "final_compensation": rows[-1].compensation,
        "max_observability_amplification": max(
            row.observability_amplification for row in rows
        ),
    }


def default_configs() -> tuple[SimulationConfig, ...]:
    """Four frozen arms for the first GitHub Actions simulation."""
    return (
        SimulationConfig(name="baseline"),
        SimulationConfig(name="compensation_only", compensation_enabled=True),
        SimulationConfig(
            name="decline_reduction_only",
            decline_rate_reduction=0.5,
        ),
        SimulationConfig(
            name="dual_track",
            decline_rate_reduction=0.5,
            compensation_enabled=True,
        ),
    )


def format_markdown() -> str:
    lines = [
        "# CGD synthetic simulation",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| arm | final capability | final self estimate | final gap | mean function | min function | final compensation | max observability amp |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for config in default_configs():
        result = summarize(simulate(config))
        lines.append(
            "| {name} | {final_capability:.3f} | {final_self_estimate:.3f} | "
            "{final_metacognitive_gap:.3f} | {mean_functional_performance:.3f} | "
            "{minimum_functional_performance:.3f} | {final_compensation:.3f} | "
            "{max_observability_amplification:.3f} |".format(
                name=config.name,
                **result,
            )
        )
    lines.extend(
        [
            "",
            "Frozen assumptions: steps=100, decline_rate=0.005, "
            "feedback_gain=0.2, compensation_cost=0.2, "
            "decline-rate reduction=0.5 in the slow-loop arms.",
            "",
            "Interpretation ceiling: this validates arithmetic consequences of "
            "declared equations only; it does not validate a biological or "
            "clinical model of dementia.",
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
