"""CGD-SIM-041: longitudinal freshness under self/informant drift.

Synthetic unitless longitudinal observation model only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

HORIZONS = (1, 2, 4, 8, 16, 32)
SAMPLES = 50_000
SIGMA_SELF_MEAS = 0.05
SIGMA_INFORMANT_MEAS = 0.05
SIGMA_SELF_DRIFT_PER_VISIT = 0.04
SIGMA_INFORMANT_DRIFT_PER_VISIT = 0.04
SIGMA_OBJECTIVE_ANCHOR = 0.03
RMSE_CONTRACT = 0.10


def analytic_rmse(horizon: int) -> float:
    """RMSE for propagating a baseline objective anchor with dyadic change.

    After an objective anchor at t0, estimate current state at th using:

        Zhat_h = O_0 + 0.5 * [(S_h-S_0) + (I_h-I_0)]

    Self/informant biases follow independent random walks.
    """
    anchor_var = SIGMA_OBJECTIVE_ANCHOR**2
    measurement_var = (
        2.0 * SIGMA_SELF_MEAS**2
        + 2.0 * SIGMA_INFORMANT_MEAS**2
    ) / 4.0
    drift_var = horizon * (
        SIGMA_SELF_DRIFT_PER_VISIT**2
        + SIGMA_INFORMANT_DRIFT_PER_VISIT**2
    ) / 4.0
    return sqrt(anchor_var + measurement_var + drift_var)


def simulate_rmse(horizon: int, seed: int) -> float:
    rng = Random(seed)
    squared_errors = []

    for _ in range(SAMPLES):
        z0 = rng.uniform(0.2, 0.8)
        total_state_change = rng.gauss(0.0, 0.08 * sqrt(horizon))
        zh = z0 + total_state_change

        a0 = rng.uniform(-0.2, 0.2)
        b0 = rng.uniform(-0.2, 0.2)
        delta_a = rng.gauss(
            0.0,
            SIGMA_SELF_DRIFT_PER_VISIT * sqrt(horizon),
        )
        delta_b = rng.gauss(
            0.0,
            SIGMA_INFORMANT_DRIFT_PER_VISIT * sqrt(horizon),
        )
        ah = a0 + delta_a
        bh = b0 + delta_b

        s0 = z0 - a0 + rng.gauss(0.0, SIGMA_SELF_MEAS)
        sh = zh - ah + rng.gauss(0.0, SIGMA_SELF_MEAS)
        i0 = z0 + b0 + rng.gauss(0.0, SIGMA_INFORMANT_MEAS)
        ih = zh + bh + rng.gauss(0.0, SIGMA_INFORMANT_MEAS)
        o0 = z0 + rng.gauss(0.0, SIGMA_OBJECTIVE_ANCHOR)

        estimated = o0 + 0.5 * ((sh - s0) + (ih - i0))
        squared_errors.append((estimated - zh) ** 2)

    return sqrt(fmean(squared_errors))


@lru_cache(maxsize=1)
def freshness_experiment():
    rows = []
    for index, horizon in enumerate(HORIZONS):
        analytic = analytic_rmse(horizon)
        simulated = simulate_rmse(horizon, 3_500_000_000 + index * 1_000_000)
        rows.append(
            {
                "horizon": horizon,
                "analytic_rmse": analytic,
                "simulated_rmse": simulated,
                "within_contract": analytic <= RMSE_CONTRACT,
            }
        )

    valid = [row["horizon"] for row in rows if row["within_contract"]]
    freshness_lease = max(valid) if valid else 0
    first_expired = next(
        (row["horizon"] for row in rows if not row["within_contract"]),
        None,
    )
    max_formula_error = max(
        abs(row["simulated_rmse"] - row["analytic_rmse"])
        for row in rows
    )

    return {
        "rows": rows,
        "freshness_lease": freshness_lease,
        "first_expired": first_expired,
        "max_formula_error": max_formula_error,
    }


def format_markdown() -> str:
    result = freshness_experiment()
    lines = [
        "# CGD-SIM-041 longitudinal observation freshness",
        "",
        "> Synthetic unitless drift scenario only. Clinical authority: NONE.",
        "",
        "Frozen scenario parameters (not clinical estimates):",
        "",
        f"- self measurement noise std: {SIGMA_SELF_MEAS:.3f}",
        f"- informant measurement noise std: {SIGMA_INFORMANT_MEAS:.3f}",
        f"- self-bias drift std / visit: {SIGMA_SELF_DRIFT_PER_VISIT:.3f}",
        f"- informant-bias drift std / visit: {SIGMA_INFORMANT_DRIFT_PER_VISIT:.3f}",
        f"- baseline objective-anchor noise std: {SIGMA_OBJECTIVE_ANCHOR:.3f}",
        f"- declared state-estimate RMSE contract: <= {RMSE_CONTRACT:.3f}",
        "",
        "Between objective anchors the estimator propagates state using dyadic change:",
        "",
        "~~~text",
        "Z_hat(h) = O(0)",
        "           + 0.5 * [(S(h)-S(0)) + (I(h)-I(0))]",
        "~~~",
        "",
        "| visits since objective anchor | analytic RMSE | Monte Carlo RMSE | contract current |",
        "| ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['horizon']} | {row['analytic_rmse']:.4f} | "
            f"{row['simulated_rmse']:.4f} | {row['within_contract']} |"
        )

    lines.extend(
        [
            "",
            f"- last frozen horizon within RMSE contract: {result['freshness_lease']} visits",
            f"- first tested expired horizon: {result['first_expired']} visits",
            f"- max Monte Carlo deviation from formula: {result['max_formula_error']:.4f}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Historical Calibration != Current Calibration",
            "Historical Objective Anchor != Permanent Ground Truth",
            "Reporter Drift Accumulates Between Anchors",
            "Freshness Must Be Part Of The Evidence Contract",
            "~~~",
            "",
            "The numerical lease is only a property of the declared synthetic drift",
            "scenario. Real observation schedules require empirically estimated drift,",
            "measurement reliability, burden and longitudinal practice effects.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
