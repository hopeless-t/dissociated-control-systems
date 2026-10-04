"""CGD-SIM-039: noisy four-channel observation frontier.

Synthetic unitless measurement model only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt
from random import Random
from statistics import fmean

REPEATS = (1, 4, 16, 64, 256)
SAMPLES = 20_000
SIGMA_SELF = 0.10
SIGMA_INFORMANT = 0.10
SIGMA_FUNCTION = 0.10
SIGMA_OBJECTIVE_SINGLE = 0.20
MARGINAL_GAIN_FLOOR = 0.05


def theoretical_rmse(repeats: int):
    objective_var = SIGMA_OBJECTIVE_SINGLE**2 / repeats
    return {
        "Z_current_state": sqrt(objective_var),
        "A_self_bias": sqrt(objective_var + SIGMA_SELF**2),
        "B_informant_bias": sqrt(objective_var + SIGMA_INFORMANT**2),
        "E_scaffold": sqrt(objective_var + SIGMA_FUNCTION**2),
    }


def simulate_rmse(repeats: int, seed: int):
    """Monte Carlo cross-check using the exact distribution of the sample mean.

    For iid Gaussian objective trials, their mean is Gaussian with standard
    deviation sigma/sqrt(n). Drawing that mean directly is distributionally
    identical and avoids generating up to 256 individual trial noises for every
    Monte Carlo specimen.
    """
    rng = Random(seed)
    objective_mean_sigma = SIGMA_OBJECTIVE_SINGLE / sqrt(repeats)
    errors = {
        "Z_current_state": [],
        "A_self_bias": [],
        "B_informant_bias": [],
        "E_scaffold": [],
    }

    for _ in range(SAMPLES):
        z = rng.uniform(0.0, 1.0)
        a = rng.uniform(-0.3, 0.3)
        b = rng.uniform(-0.3, 0.3)
        e = rng.uniform(-0.3, 0.3)

        s = z - a + rng.gauss(0.0, SIGMA_SELF)
        i = z + b + rng.gauss(0.0, SIGMA_INFORMANT)
        f = z + e + rng.gauss(0.0, SIGMA_FUNCTION)
        o = z + rng.gauss(0.0, objective_mean_sigma)

        estimates = {
            "Z_current_state": o,
            "A_self_bias": o - s,
            "B_informant_bias": i - o,
            "E_scaffold": f - o,
        }
        truth = {
            "Z_current_state": z,
            "A_self_bias": a,
            "B_informant_bias": b,
            "E_scaffold": e,
        }
        for key in errors:
            errors[key].append((estimates[key] - truth[key]) ** 2)

    return {
        key: sqrt(fmean(values))
        for key, values in errors.items()
    }


def reporter_state_mean_rmse(row):
    return fmean(
        row["theoretical_rmse"][key]
        for key in ("A_self_bias", "B_informant_bias", "E_scaffold")
    )


@lru_cache(maxsize=1)
def external_noise_frontier():
    rows = []
    for index, repeats in enumerate(REPEATS):
        theoretical = theoretical_rmse(repeats)
        simulated = simulate_rmse(repeats, 3_300_000_000 + index * 1_000_000)
        rows.append(
            {
                "repeats": repeats,
                "theoretical_rmse": theoretical,
                "simulated_rmse": simulated,
            }
        )

    transitions = []
    practical_knee = None
    for before, after in zip(rows, rows[1:]):
        before_rmse = reporter_state_mean_rmse(before)
        after_rmse = reporter_state_mean_rmse(after)
        gain = (before_rmse - after_rmse) / before_rmse
        transitions.append(
            {
                "from": before["repeats"],
                "to": after["repeats"],
                "relative_gain": gain,
            }
        )
        if practical_knee is None and gain < MARGINAL_GAIN_FLOOR:
            practical_knee = before["repeats"]

    max_formula_error = max(
        abs(row["simulated_rmse"][key] - row["theoretical_rmse"][key])
        for row in rows
        for key in row["theoretical_rmse"]
    )

    asymptotic_floor = {
        "A_self_bias": SIGMA_SELF,
        "B_informant_bias": SIGMA_INFORMANT,
        "E_scaffold": SIGMA_FUNCTION,
    }

    return {
        "rows": rows,
        "transitions": transitions,
        "practical_knee": practical_knee,
        "max_formula_error": max_formula_error,
        "asymptotic_floor": asymptotic_floor,
    }


def format_markdown() -> str:
    result = external_noise_frontier()
    lines = [
        "# CGD-SIM-039 noisy external-observation frontier",
        "",
        "> Synthetic unitless measurement scenario only. Clinical authority: NONE.",
        "",
        "Frozen scenario noise (not clinical estimates):",
        "",
        f"- self-report noise std: {SIGMA_SELF:.3f}",
        f"- informant-report noise std: {SIGMA_INFORMANT:.3f}",
        f"- daily-function noise std: {SIGMA_FUNCTION:.3f}",
        f"- single objective-trial noise std: {SIGMA_OBJECTIVE_SINGLE:.3f}",
        f"- Monte Carlo samples per repeat count: {SAMPLES}",
        "",
        "Estimator:",
        "",
        "~~~text",
        "Z_hat = mean(objective trials)",
        "A_hat = Z_hat - S",
        "B_hat = I - Z_hat",
        "E_hat = F - Z_hat",
        "~~~",
        "",
        "| objective repeats | Z RMSE | A RMSE | B RMSE | E RMSE | simulated max-channel delta from formula |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        theory = row["theoretical_rmse"]
        simulated = row["simulated_rmse"]
        max_delta = max(abs(simulated[key] - theory[key]) for key in theory)
        lines.append(
            f"| {row['repeats']} | {theory['Z_current_state']:.4f} | "
            f"{theory['A_self_bias']:.4f} | {theory['B_informant_bias']:.4f} | "
            f"{theory['E_scaffold']:.4f} | {max_delta:.4f} |"
        )

    lines.extend(
        [
            "",
            "Marginal reporter-state RMSE gain from more objective trials:",
            "",
            "| repeats transition | relative RMSE reduction |",
            "| --- | ---: |",
        ]
    )
    for row in result["transitions"]:
        lines.append(
            f"| {row['from']} -> {row['to']} | {row['relative_gain']:.2%} |"
        )

    lines.extend(
        [
            "",
            f"- declared <5% marginal-gain knee: {result['practical_knee']} objective repeats",
            f"- max Monte Carlo deviation from analytic RMSE: {result['max_formula_error']:.4f}",
            "",
            "As objective repeats approach infinity:",
            "",
            "~~~text",
            "RMSE(Z) -> 0",
            f"RMSE(A) -> sigma_self      = {SIGMA_SELF:.3f}",
            f"RMSE(B) -> sigma_informant = {SIGMA_INFORMANT:.3f}",
            f"RMSE(E) -> sigma_function  = {SIGMA_FUNCTION:.3f}",
            "~~~",
            "",
            "Key result:",
            "",
            "~~~text",
            "Full Rank != Zero Error",
            "More Objective Trials != Infinite Recovery",
            "Objective Measurement Noise Can Be Averaged Down",
            "Reporter / Function Noise Becomes The Residual Floor",
            "~~~",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
