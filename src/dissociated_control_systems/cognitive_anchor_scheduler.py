"""CGD-SIM-042: objective-anchor reacquisition scheduler.

Synthetic unitless scheduling model only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt

INTERVALS = (1, 2, 4, 8, 16, 32, 64)
ANCHOR_COSTS = (0.001, 0.005, 0.010, 0.020, 0.040, 0.080, 0.160)
SIGMA_OBJECTIVE_ANCHOR = 0.03
SIGMA_SELF_MEAS = 0.05
SIGMA_INFORMANT_MEAS = 0.05
SIGMA_SELF_DRIFT = 0.04
SIGMA_INFORMANT_DRIFT = 0.04
RMSE_CONTRACT = 0.10


def propagated_variance(age: int) -> float:
    """State-estimation variance at age visits since the objective anchor."""
    if age < 0:
        raise ValueError("age must be nonnegative")
    if age == 0:
        return SIGMA_OBJECTIVE_ANCHOR**2

    endpoint_measurement_var = (
        2.0 * SIGMA_SELF_MEAS**2
        + 2.0 * SIGMA_INFORMANT_MEAS**2
    ) / 4.0
    drift_var = age * (
        SIGMA_SELF_DRIFT**2 + SIGMA_INFORMANT_DRIFT**2
    ) / 4.0
    return (
        SIGMA_OBJECTIVE_ANCHOR**2
        + endpoint_measurement_var
        + drift_var
    )


def interval_mean_variance(interval: int) -> float:
    if interval < 1:
        raise ValueError("interval must be positive")
    return sum(propagated_variance(age) for age in range(interval)) / interval


def interval_max_rmse(interval: int) -> float:
    return sqrt(max(propagated_variance(age) for age in range(interval)))


def interval_contract_safe(interval: int) -> bool:
    return interval_max_rmse(interval) <= RMSE_CONTRACT


def schedule_loss(interval: int, anchor_cost: float) -> float:
    if anchor_cost < 0.0:
        raise ValueError("anchor_cost must be nonnegative")
    return interval_mean_variance(interval) + anchor_cost / interval


def select_unconstrained(anchor_cost: float):
    return min(
        INTERVALS,
        key=lambda interval: (
            schedule_loss(interval, anchor_cost),
            interval,
        ),
    )


def select_contract_constrained(anchor_cost: float):
    eligible = [
        interval for interval in INTERVALS
        if interval_contract_safe(interval)
    ]
    if not eligible:
        return None
    return min(
        eligible,
        key=lambda interval: (
            schedule_loss(interval, anchor_cost),
            interval,
        ),
    )


@lru_cache(maxsize=1)
def anchor_scheduler_experiment():
    interval_rows = []
    for interval in INTERVALS:
        interval_rows.append(
            {
                "interval": interval,
                "mean_variance": interval_mean_variance(interval),
                "max_rmse": interval_max_rmse(interval),
                "contract_safe": interval_contract_safe(interval),
                "anchor_rate": 1.0 / interval,
            }
        )

    cost_rows = []
    for cost in ANCHOR_COSTS:
        unconstrained = select_unconstrained(cost)
        constrained = select_contract_constrained(cost)
        cost_rows.append(
            {
                "anchor_cost": cost,
                "unconstrained_interval": unconstrained,
                "unconstrained_loss": schedule_loss(unconstrained, cost),
                "unconstrained_safe": interval_contract_safe(unconstrained),
                "constrained_interval": constrained,
                "constrained_loss": (
                    None if constrained is None
                    else schedule_loss(constrained, cost)
                ),
                "constraint_binds": constrained != unconstrained,
            }
        )

    safe_intervals = [
        row["interval"] for row in interval_rows if row["contract_safe"]
    ]
    first_unsafe = next(
        (row["interval"] for row in interval_rows if not row["contract_safe"]),
        None,
    )

    return {
        "interval_rows": interval_rows,
        "cost_rows": cost_rows,
        "largest_safe_interval": max(safe_intervals) if safe_intervals else None,
        "first_unsafe_interval": first_unsafe,
        "binding_costs": [
            row["anchor_cost"] for row in cost_rows if row["constraint_binds"]
        ],
    }


def format_markdown() -> str:
    result = anchor_scheduler_experiment()
    lines = [
        "# CGD-SIM-042 objective-anchor reacquisition scheduler",
        "",
        "> Synthetic unitless scheduling scenario only. Clinical authority: NONE.",
        "",
        "Objective-anchor scheduling separates two objectives:",
        "",
        "~~~text",
        "economic/statistical loss = mean state-estimation variance",
        "                           + anchor_cost / interval",
        "",
        "safety/evidence contract  = max RMSE before next anchor <= 0.10",
        "~~~",
        "",
        "| anchor interval (visits) | mean state variance | worst RMSE before next anchor | anchor rate | freshness-contract safe |",
        "| ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["interval_rows"]:
        lines.append(
            f"| {row['interval']} | {row['mean_variance']:.6f} | "
            f"{row['max_rmse']:.4f} | {row['anchor_rate']:.4f} | "
            f"{row['contract_safe']} |"
        )

    lines.extend(
        [
            "",
            f"- largest frozen safe interval: {result['largest_safe_interval']} visits",
            f"- first frozen unsafe interval: {result['first_unsafe_interval']} visits",
            "",
            "Cost sweep:",
            "",
            "| synthetic anchor cost | unconstrained optimum | unconstrained safe | contract-constrained optimum | unconstrained loss | constrained loss | contract binds |",
            "| ---: | ---: | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in result["cost_rows"]:
        constrained_loss = (
            "n/a" if row["constrained_loss"] is None
            else f"{row['constrained_loss']:.6f}"
        )
        lines.append(
            f"| {row['anchor_cost']:.3f} | "
            f"{row['unconstrained_interval']} | "
            f"{row['unconstrained_safe']} | "
            f"{row['constrained_interval']} | "
            f"{row['unconstrained_loss']:.6f} | "
            f"{constrained_loss} | {row['constraint_binds']} |"
        )

    lines.extend(
        [
            "",
            "Key result:",
            "",
            "~~~text",
            "Cost Optimum != Safety-Admissible Optimum",
            "Cheaper Measurement Schedule != Fresh Evidence",
            "Freshness Contract Can Bind The Scheduler",
            "Re-observation Cost Does Not Create Permission To Use Stale Evidence",
            "~~~",
            "",
            "The numerical intervals and costs are properties of the frozen synthetic",
            "scenario only. They are not retest intervals, monitoring recommendations,",
            "or estimates of burden in any human population.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
