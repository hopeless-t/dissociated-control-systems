"""CGD-SIM-043: repeated-test practice-effect robustness attack.

Synthetic unitless measurement model only. Clinical authority: NONE.
"""

from __future__ import annotations

from functools import lru_cache
from math import sqrt

MAX_REPEATS = 256
SIGMA_OBJECTIVE_SINGLE = 0.20
SIGMA_SELF = 0.10
SIGMA_INFORMANT = 0.10
SIGMA_FUNCTION = 0.10
PRACTICE_BIAS_PER_REPEAT = (0.0, 0.00025, 0.0005, 0.001, 0.002, 0.005)
REFERENCE_REPEATS = (1, 4, 16, 64, 256)


def objective_bias(repeats: int, practice_bias_per_repeat: float) -> float:
    """Mean bias of an equally weighted sequence with linear repeat bias.

    Observation j has synthetic mean shift beta*(j-1), j=1..n.
    The average therefore has bias beta*(n-1)/2.
    """
    if repeats < 1:
        raise ValueError("repeats must be positive")
    if practice_bias_per_repeat < 0.0:
        raise ValueError("practice bias magnitude must be nonnegative")
    return practice_bias_per_repeat * (repeats - 1) / 2.0


def objective_mse(repeats: int, practice_bias_per_repeat: float) -> float:
    variance = SIGMA_OBJECTIVE_SINGLE**2 / repeats
    bias = objective_bias(repeats, practice_bias_per_repeat)
    return variance + bias**2


def full_state_trace_mse(repeats: int, practice_bias_per_repeat: float) -> float:
    """Trace MSE for [Z,A,B,E] with one S/I/F observation each.

    The objective estimation error enters all four reconstructed states.
    """
    return (
        4.0 * objective_mse(repeats, practice_bias_per_repeat)
        + SIGMA_SELF**2
        + SIGMA_INFORMANT**2
        + SIGMA_FUNCTION**2
    )


def best_repeat_count(practice_bias_per_repeat: float) -> int:
    return min(
        range(1, MAX_REPEATS + 1),
        key=lambda repeats: (
            full_state_trace_mse(repeats, practice_bias_per_repeat),
            repeats,
        ),
    )


@lru_cache(maxsize=1)
def practice_effect_experiment():
    rows = []
    for beta in PRACTICE_BIAS_PER_REPEAT:
        optimum = best_repeat_count(beta)
        optimum_trace = full_state_trace_mse(optimum, beta)
        references = {
            repeats: {
                "objective_rmse": sqrt(objective_mse(repeats, beta)),
                "trace_mse": full_state_trace_mse(repeats, beta),
                "bias": objective_bias(repeats, beta),
            }
            for repeats in REFERENCE_REPEATS
        }
        rows.append(
            {
                "beta": beta,
                "optimum_repeats": optimum,
                "optimum_objective_rmse": sqrt(objective_mse(optimum, beta)),
                "optimum_trace_mse": optimum_trace,
                "references": references,
                "loss_256_over_optimum": (
                    references[256]["trace_mse"] / optimum_trace
                ),
                "repeat_256_is_worse_than_64": (
                    references[256]["trace_mse"]
                    > references[64]["trace_mse"]
                ),
            }
        )

    nonzero_optima = [
        row["optimum_repeats"] for row in rows if row["beta"] > 0.0
    ]
    return {
        "rows": rows,
        "zero_bias_optimum": rows[0]["optimum_repeats"],
        "nonzero_optima_monotone": nonzero_optima == sorted(
            nonzero_optima,
            reverse=True,
        ),
    }


def format_markdown() -> str:
    result = practice_effect_experiment()
    lines = [
        "# CGD-SIM-043 repeated-test practice-effect robustness attack",
        "",
        "> Synthetic unitless measurement scenario only. Clinical authority: NONE.",
        "",
        "SIM-039 assumed iid unbiased objective repetitions. SIM-043 attacks that",
        "assumption with a frozen linear repeat-bias scenario:",
        "",
        "~~~text",
        "objective observation j = Z + beta*(j-1) + noise_j",
        "",
        "bias(mean of n repeats) = beta*(n-1)/2",
        "variance(mean)          = sigma_O^2/n",
        "MSE(mean)               = variance + bias^2",
        "~~~",
        "",
        f"- single-test noise std: {SIGMA_OBJECTIVE_SINGLE:.3f}",
        f"- maximum repeat count searched: {MAX_REPEATS}",
        "- beta values are synthetic sensitivity scenarios, not empirical practice-effect estimates",
        "",
        "| practice bias beta / repeat | optimal objective repeats | objective RMSE at optimum | full-state trace MSE | 256-repeat loss / optimum | 256 worse than 64 |",
        "| ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['beta']:.5f} | {row['optimum_repeats']} | "
            f"{row['optimum_objective_rmse']:.4f} | "
            f"{row['optimum_trace_mse']:.6f} | "
            f"{row['loss_256_over_optimum']:.2f}x | "
            f"{row['repeat_256_is_worse_than_64']} |"
        )

    lines.extend(
        [
            "",
            "Selected repeat frontiers:",
            "",
            "| beta | repeats | objective bias | objective RMSE | trace MSE |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in result["rows"]:
        for repeats in REFERENCE_REPEATS:
            ref = row["references"][repeats]
            lines.append(
                f"| {row['beta']:.5f} | {repeats} | {ref['bias']:.4f} | "
                f"{ref['objective_rmse']:.4f} | {ref['trace_mse']:.6f} |"
            )

    lines.extend(
        [
            "",
            f"- zero-bias optimum reaches search boundary: {result['zero_bias_optimum']}",
            f"- nonzero-bias optimum decreases monotonically as bias grows: {result['nonzero_optima_monotone']}",
            "",
            "Key result:",
            "",
            "~~~text",
            "Measurement != Passive Observation",
            "Variance Reduction != Error Reduction When Bias Accumulates",
            "More Repeats Can Become Worse",
            "Practice-Effect Model Must Precede Real Evidence Allocation",
            "~~~",
            "",
            "The linear bias model is deliberately simple. Public cognitive-testing",
            "literature motivates testing practice effects but does not calibrate the",
            "beta values used here. Real retest effects can be instrument-, interval-,",
            "domain-, and disease-state-dependent.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
