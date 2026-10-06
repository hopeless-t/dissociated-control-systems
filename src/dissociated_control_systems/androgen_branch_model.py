"""Synthetic branch model for shared DHT input with distinct downstream paths.

D = upstream DHT-like input.
A = canonical AR-dependent branch.
M = noncanonical mechanical/contractile branch.

The model is a control counterexample: collapsing A and M into one 'androgen
pressure' coordinate loses actuator specificity.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AndrogenBranchState:
    upstream_dht: float
    ar_branch: float
    mechanical_branch: float

    @property
    def reduced_androgen_burden(self) -> float:
        return 0.5 * (self.ar_branch + self.mechanical_branch)


def state_from_dht(dht: float = 1.0) -> AndrogenBranchState:
    if not 0.0 <= dht <= 1.0:
        raise ValueError("dht must be in [0,1]")
    return AndrogenBranchState(
        upstream_dht=dht,
        ar_branch=dht,
        mechanical_branch=dht,
    )


def inhibit_dht_production(
    state: AndrogenBranchState,
    *,
    strength: float = 1.0,
) -> AndrogenBranchState:
    """Upstream perturbation lowers both DHT-dependent branches."""
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be in [0,1]")
    remaining = state.upstream_dht * (1.0 - strength)
    return AndrogenBranchState(remaining, remaining, remaining)


def block_ar(
    state: AndrogenBranchState,
    *,
    strength: float = 1.0,
) -> AndrogenBranchState:
    """AR-specific perturbation leaves the mechanical branch unchanged."""
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be in [0,1]")
    return AndrogenBranchState(
        upstream_dht=state.upstream_dht,
        ar_branch=state.ar_branch * (1.0 - strength),
        mechanical_branch=state.mechanical_branch,
    )


def relax_mechanics(
    state: AndrogenBranchState,
    *,
    strength: float = 1.0,
) -> AndrogenBranchState:
    """Mechanical-path perturbation leaves AR signaling unchanged."""
    if not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be in [0,1]")
    return AndrogenBranchState(
        upstream_dht=state.upstream_dht,
        ar_branch=state.ar_branch,
        mechanical_branch=state.mechanical_branch * (1.0 - strength),
    )
