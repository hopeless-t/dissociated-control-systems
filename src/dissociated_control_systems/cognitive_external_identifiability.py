"""CGD-SIM-038: structural identifiability of external observation channels.

Synthetic algebraic observation model only. Clinical authority: NONE.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from fractions import Fraction

STATE_NAMES = ("Z_current_state", "A_self_bias", "B_informant_bias", "E_scaffold")

CHANNEL_ROWS = {
    # S = Z - A
    "self_report": (1, -1, 0, 0),
    # I = Z + B
    "informant_report": (1, 0, 1, 0),
    # O = Z
    "objective_performance": (1, 0, 0, 0),
    # F = Z + E
    "daily_function": (1, 0, 0, 1),
}


@dataclass(frozen=True)
class IdentifiabilityResult:
    channels: tuple[str, ...]
    rank: int
    state_dimension: int

    @property
    def identifiable(self) -> bool:
        return self.rank == self.state_dimension

    @property
    def nullity(self) -> int:
        return self.state_dimension - self.rank


def matrix_rank(rows: list[tuple[int, ...]]) -> int:
    if not rows:
        return 0
    matrix = [list(map(Fraction, row)) for row in rows]
    row_count = len(matrix)
    col_count = len(matrix[0])
    rank = 0
    pivot_col = 0

    while rank < row_count and pivot_col < col_count:
        pivot = next(
            (r for r in range(rank, row_count) if matrix[r][pivot_col] != 0),
            None,
        )
        if pivot is None:
            pivot_col += 1
            continue

        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][pivot_col]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]

        for r in range(row_count):
            if r == rank:
                continue
            factor = matrix[r][pivot_col]
            if factor == 0:
                continue
            matrix[r] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[r], matrix[rank], strict=True)
            ]

        rank += 1
        pivot_col += 1

    return rank


def analyze_channels(channels: tuple[str, ...]) -> IdentifiabilityResult:
    rows = [CHANNEL_ROWS[channel] for channel in channels]
    return IdentifiabilityResult(
        channels=channels,
        rank=matrix_rank(rows),
        state_dimension=len(STATE_NAMES),
    )


def noiseless_observations(*, z: float, a: float, b: float, e: float):
    return {
        "self_report": z - a,
        "informant_report": z + b,
        "objective_performance": z,
        "daily_function": z + e,
    }


def recover_with_four_channels(observations):
    z = observations["objective_performance"]
    a = z - observations["self_report"]
    b = observations["informant_report"] - z
    e = observations["daily_function"] - z
    return {
        "Z_current_state": z,
        "A_self_bias": a,
        "B_informant_bias": b,
        "E_scaffold": e,
    }


@lru_cache(maxsize=1)
def identifiability_experiment():
    scenarios = (
        ("self_only", ("self_report",)),
        ("self_plus_informant", ("self_report", "informant_report")),
        (
            "dyad_plus_objective",
            ("self_report", "informant_report", "objective_performance"),
        ),
        (
            "dyad_plus_function",
            ("self_report", "informant_report", "daily_function"),
        ),
        (
            "full_four_channel",
            (
                "self_report",
                "informant_report",
                "objective_performance",
                "daily_function",
            ),
        ),
    )

    rows = []
    for name, channels in scenarios:
        result = analyze_channels(channels)
        rows.append(
            {
                "name": name,
                "channels": channels,
                "rank": result.rank,
                "nullity": result.nullity,
                "identifiable": result.identifiable,
            }
        )

    example_state = {
        "z": 0.62,
        "a": 0.18,
        "b": -0.07,
        "e": 0.11,
    }
    obs = noiseless_observations(**example_state)
    recovered = recover_with_four_channels(obs)

    # Dyadic discrepancy alone aliases awareness and informant bias.
    dyadic_discrepancy = obs["informant_report"] - obs["self_report"]
    expected_alias = example_state["a"] + example_state["b"]

    return {
        "rows": rows,
        "example_state": example_state,
        "observations": obs,
        "recovered": recovered,
        "dyadic_discrepancy": dyadic_discrepancy,
        "expected_alias": expected_alias,
        "full_rank_only_with_all_four": (
            sum(row["identifiable"] for row in rows) == 1
            and rows[-1]["identifiable"]
        ),
    }


def format_markdown() -> str:
    result = identifiability_experiment()
    lines = [
        "# CGD-SIM-038 external observation structural identifiability",
        "",
        "> Synthetic algebraic observation model only. Clinical authority: NONE.",
        "",
        "Latent state used only for the structural test:",
        "",
        "~~~text",
        "Z = current task-relevant state",
        "A = self-model / awareness bias",
        "B = informant bias/context",
        "E = scaffold/environment contribution to daily function",
        "~~~",
        "",
        "Observation model:",
        "",
        "~~~text",
        "S = Z - A       # self report",
        "I = Z + B       # informant report",
        "O = Z           # objective standardized performance",
        "F = Z + E       # daily function under current scaffold",
        "~~~",
        "",
        "| scenario | channels | rank / 4 | nullity | full state identifiable |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in result["rows"]:
        lines.append(
            f"| {row['name']} | {', '.join(row['channels'])} | "
            f"{row['rank']}/4 | {row['nullity']} | {row['identifiable']} |"
        )

    ex = result["example_state"]
    lines.extend(
        [
            "",
            "Dyadic discrepancy alias:",
            "",
            f"- example A (self bias): {ex['a']:+.3f}",
            f"- example B (informant bias): {ex['b']:+.3f}",
            f"- observed I-S discrepancy: {result['dyadic_discrepancy']:+.3f}",
            f"- A+B: {result['expected_alias']:+.3f}",
            "",
            "Therefore:",
            "",
            "~~~text",
            "Informant - Self = Awareness Bias + Informant Bias",
            "Self/Informant Discordance != Pure Awareness Measurement",
            "~~~",
            "",
            "With all four channels, the noiseless model has direct reconstruction:",
            "",
            "~~~text",
            "Z = O",
            "A = O - S",
            "B = I - O",
            "E = F - O",
            "~~~",
            "",
            f"- only tested scenario with full rank: {result['full_rank_only_with_all_four']}",
            "",
            "Interpretation boundary:",
            "",
            "This is a structural rank result, not a claim that real ECog, FAQ or "
            "cognitive-test measurements satisfy the linear equations exactly. It "
            "shows why independent objective and functional channels are valuable "
            "before fitting any clinical observational model.",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_markdown())
