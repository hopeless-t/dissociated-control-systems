"""CGD-SIM-040: evidence allocation across four observation channels.

Synthetic unitless measurement-budget model only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt

SIGMA_OBJECTIVE = 0.20
SIGMA_SELF = 0.10
SIGMA_INFORMANT = 0.10
SIGMA_FUNCTION = 0.10
BUDGETS = (7, 14, 28, 56, 112)
CHANNELS = ("objective", "self", "informant", "function")


def trace_mse(allocation: tuple[int, int, int, int]) -> float:
    """Expected squared-error trace for [Z, A, B, E].

    Z_hat = O_bar
    A_hat = O_bar - S_bar
    B_hat = I_bar - O_bar
    E_hat = F_bar - O_bar

    Therefore objective noise enters all four state estimates.
    """
    n_o, n_s, n_i, n_f = allocation
    if min(allocation) < 1:
        raise ValueError("every channel requires at least one observation")

    v_o = SIGMA_OBJECTIVE**2 / n_o
    v_s = SIGMA_SELF**2 / n_s
    v_i = SIGMA_INFORMANT**2 / n_i
    v_f = SIGMA_FUNCTION**2 / n_f
    return 4.0 * v_o + v_s + v_i + v_f


def enumerate_allocations(total: int):
    for n_o in range(1, total - 2):
        for n_s in range(1, total - n_o - 1):
            for n_i in range(1, total - n_o - n_s):
                n_f = total - n_o - n_s - n_i
                if n_f >= 1:
                    yield (n_o, n_s, n_i, n_f)


def exhaustive_optimum(total: int):
    return min(
        enumerate_allocations(total),
        key=lambda allocation: (trace_mse(allocation), allocation),
    )


def ratio_allocation(total: int):
    if total % 7 != 0:
        raise ValueError("frozen budgets must be multiples of 7")
    unit = total // 7
    return (4 * unit, unit, unit, unit)


def equal_allocation(total: int):
    base = total // 4
    remainder = total % 4
    values = [base] * 4
    # Deterministic remainder placement starts with objective because it has the
    # largest coefficient in the trace objective.
    for index in range(remainder):
        values[index] += 1
    return tuple(values)


def objective_only_pressure(total: int):
    return (total - 3, 1, 1, 1)


def continuous_ratio():
    # Minimize sum_j c_j/n_j subject to sum n_j=B. Lagrange multipliers give
    # n_j proportional to sqrt(c_j).
    coefficients = {
        "objective": 4.0 * SIGMA_OBJECTIVE**2,
        "self": SIGMA_SELF**2,
        "informant": SIGMA_INFORMANT**2,
        "function": SIGMA_FUNCTION**2,
    }
    roots = {key: sqrt(value) for key, value in coefficients.items()}
    minimum = min(roots.values())
    return {
        key: value / minimum
        for key, value in roots.items()
    }


@lru_cache(maxsize=1)
def evidence_allocator_experiment():
    rows = []
    for total in BUDGETS:
        optimum = exhaustive_optimum(total)
        ratio = ratio_allocation(total)
        equal = equal_allocation(total)
        pressure = objective_only_pressure(total)

        optimum_mse = trace_mse(optimum)
        ratio_mse = trace_mse(ratio)
        equal_mse = trace_mse(equal)
        pressure_mse = trace_mse(pressure)

        rows.append(
            {
                "budget": total,
                "optimum": optimum,
                "ratio": ratio,
                "equal": equal,
                "objective_pressure": pressure,
                "optimum_mse": optimum_mse,
                "ratio_mse": ratio_mse,
                "equal_mse": equal_mse,
                "objective_pressure_mse": pressure_mse,
                "ratio_matches_optimum": ratio == optimum,
                "ratio_gap": (ratio_mse - optimum_mse) / optimum_mse,
                "gain_vs_equal": (equal_mse - optimum_mse) / equal_mse,
                "gain_vs_objective_pressure": (
                    pressure_mse - optimum_mse
                ) / pressure_mse,
            }
        )

    return {
        "continuous_ratio": continuous_ratio(),
        "rows": rows,
        "all_ratio_matches_optimum": all(
            row["ratio_matches_optimum"] for row in rows
        ),
    }


def fmt_allocation(allocation):
    return ":".join(str(value) for value in allocation)


def format_markdown() -> str:
    result = evidence_allocator_experiment()
    ratio = result["continuous_ratio"]
    lines = [
        "# CGD-SIM-040 four-channel evidence allocation",
        "",
        "> Synthetic unitless budget model only. Clinical authority: NONE.",
        "",
        "State-estimation trace loss:",
        "",
        "~~~text",
        "L = 4*sigma_O^2/n_O",
        "    + sigma_S^2/n_S",
        "    + sigma_I^2/n_I",
        "    + sigma_F^2/n_F",
        "~~~",
        "",
        "The factor four on objective evidence appears because O contributes to",
        "Z, A, B, and E reconstruction in the frozen four-channel model.",
        "",
        "Continuous Lagrange solution n_j proportional to sqrt(c_j):",
        "",
        f"- objective: {ratio['objective']:.1f}",
        f"- self: {ratio['self']:.1f}",
        f"- informant: {ratio['informant']:.1f}",
        f"- function: {ratio['function']:.1f}",
        "",
        "Frozen integer budgets are multiples of seven, allowing the exact",
        "candidate ratio 4:1:1:1.",
        "",
        "| total budget | exhaustive optimum O:S:I:F | 4:1:1:1 candidate | equal allocation | objective-pressure allocation | optimum trace MSE | gain vs equal | gain vs objective-pressure |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | ---: |",
    ]

    for row in result["rows"]:
        lines.append(
            f"| {row['budget']} | {fmt_allocation(row['optimum'])} | "
            f"{fmt_allocation(row['ratio'])} | {fmt_allocation(row['equal'])} | "
            f"{fmt_allocation(row['objective_pressure'])} | "
            f"{row['optimum_mse']:.6f} | {row['gain_vs_equal']:.2%} | "
            f"{row['gain_vs_objective_pressure']:.2%} |"
        )

    lines.extend(
        [
            "",
            f"- 4:1:1:1 candidate equals exhaustive integer optimum at every frozen budget: {result['all_ratio_matches_optimum']}",
            "",
            "Key result:",
            "",
            "~~~text",
            "More Measurement != Better Allocation",
            "Single-Channel Pressure Eventually Becomes Waste",
            "Evidence Budget Should Follow Marginal Information Value",
            "~~~",
            "",
            "The 4:1:1:1 ratio is a property of the declared synthetic noise and",
            "linear estimator, not a recommendation for any real cognitive test",
            "battery. Real costs, correlations, bias, fatigue and instrument scaling",
            "would change the allocation problem.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
