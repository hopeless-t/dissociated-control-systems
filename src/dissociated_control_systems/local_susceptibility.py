"""Synthetic local susceptibility helpers for HF01.

A baseline latent state and its response gain to a controlled perturbation are
separate coordinates.  Equal baseline state therefore does not imply equal
short-horizon response or equal future trajectory under the same input.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LocalResponseState:
    baseline: float
    susceptibility: float

    def response(self, input_delta: float) -> float:
        return self.baseline + self.susceptibility * input_delta


def finite_difference_susceptibility(
    baseline_output: float,
    perturbed_output: float,
    input_delta: float,
) -> float:
    if input_delta == 0:
        raise ValueError("input_delta must be non-zero")
    return (perturbed_output - baseline_output) / input_delta


def matched_state_divergence(
    baseline: float,
    susceptibility_a: float,
    susceptibility_b: float,
    input_delta: float,
) -> tuple[float, float]:
    """Return two responses from matched baseline but different local gains."""
    a = LocalResponseState(baseline, susceptibility_a)
    b = LocalResponseState(baseline, susceptibility_b)
    return a.response(input_delta), b.response(input_delta)
