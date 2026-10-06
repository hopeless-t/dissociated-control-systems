"""Dependency-free primitives for the DCS cancer latent-state digital twin.

This module is a synthetic research model. It is not a clinical predictor and
must not be interpreted as treatment guidance.
"""

from __future__ import annotations

from dataclasses import dataclass


def _nonnegative(value: float, name: str) -> float:
    value = float(value)
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0")
    return value


def _unit(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


@dataclass(frozen=True)
class CancerState:
    """Synthetic latent biological state.

    bs: treatment-sensitive tumor burden
    br: resistant / escape-capable tumor burden
    effector: effective anti-tumor immune activity in [0,1]
    suppressive: suppressive microenvironment pressure in [0,1]
    host: host reserve / treatment tolerance state in [0,1]
    """

    bs: float
    br: float
    effector: float
    suppressive: float
    host: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "bs", _nonnegative(self.bs, "bs"))
        object.__setattr__(self, "br", _nonnegative(self.br, "br"))
        object.__setattr__(self, "effector", _unit(self.effector, "effector"))
        object.__setattr__(self, "suppressive", _unit(self.suppressive, "suppressive"))
        object.__setattr__(self, "host", _unit(self.host, "host"))

    @property
    def total(self) -> float:
        return self.bs + self.br

    @property
    def resistant_fraction(self) -> float:
        if self.total == 0.0:
            return 0.0
        return self.br / self.total


@dataclass(frozen=True)
class CancerDynamics:
    growth_s: float
    growth_r: float
    immune_kill_s: float
    immune_kill_r: float
    drug_kill_s: float
    drug_kill_r: float
    selection: float = 0.0
    effector_activation: float = 0.01
    effector_decay: float = 0.005
    suppressive_coupling: float = 0.015
    suppressive_production: float = 0.006
    suppressive_clearance: float = 0.008
    host_recovery: float = 0.004
    host_toxicity: float = 0.008
    host_burden_cost: float = 0.002

    def __post_init__(self) -> None:
        for name in self.__dataclass_fields__:
            _nonnegative(getattr(self, name), name)


@dataclass(frozen=True)
class CancerSensors:
    """Observation nuisance parameters; sensors are explicitly not biology."""

    shedding_s: float = 1.0
    shedding_r: float = 1.0
    resistance_detectability: float = 1.0

    def __post_init__(self) -> None:
        _nonnegative(self.shedding_s, "shedding_s")
        _nonnegative(self.shedding_r, "shedding_r")
        _unit(self.resistance_detectability, "resistance_detectability")


def ctdna(state: CancerState, sensors: CancerSensors) -> float:
    """Noise-free synthetic ctDNA signal.

    The deliberate confounding is:
        signal = shedding_s * bs + shedding_r * br
    so signal alone cannot uniquely recover burden and shedding.
    """

    return sensors.shedding_s * state.bs + sensors.shedding_r * state.br


def imaging(state: CancerState) -> float:
    """Coarse synthetic imaging burden; intentionally blind to clone identity."""

    return state.total


def resistance_signal(state: CancerState, sensors: CancerSensors) -> float:
    return sensors.resistance_detectability * state.resistant_fraction


def resistant_net_drift(
    state: CancerState,
    dynamics: CancerDynamics,
    treatment: float,
) -> float:
    """Instantaneous per-burden drift for the resistant compartment.

    This separates current state from transition law. Two patients with the same
    observed state can have different future dynamics because this quantity can
    differ even when imaging/ctDNA match.
    """

    treatment = _unit(treatment, "treatment")
    effective_immune = state.effector / (1.0 + 1.8 * state.suppressive)
    return (
        dynamics.growth_r
        - dynamics.immune_kill_r * effective_immune
        - treatment * dynamics.drug_kill_r
    )


def step(
    state: CancerState,
    dynamics: CancerDynamics,
    treatment: float,
) -> CancerState:
    """One bounded Euler step of a deliberately simple synthetic model."""

    treatment = _unit(treatment, "treatment")
    total = state.total
    effective_immune = state.effector / (1.0 + 1.5 * state.suppressive)

    sensitive_drift = (
        dynamics.growth_s
        - dynamics.immune_kill_s * effective_immune
        - treatment * dynamics.drug_kill_s
    )
    resistant_drift = (
        dynamics.growth_r
        - dynamics.immune_kill_r * effective_immune
        - treatment * dynamics.drug_kill_r
    )

    selected = treatment * dynamics.selection * state.bs
    bs = max(0.0, state.bs + sensitive_drift * state.bs - selected)
    br = max(0.0, state.br + resistant_drift * state.br + selected)

    activation = dynamics.effector_activation * total / (0.4 + total) if total else 0.0
    effector = state.effector + activation * (1.0 - state.effector)
    effector -= dynamics.effector_decay * state.effector
    effector -= dynamics.suppressive_coupling * state.suppressive * state.effector
    effector = min(1.0, max(0.0, effector))

    suppressive = state.suppressive
    if total:
        suppressive += (
            dynamics.suppressive_production
            * total / (0.5 + total)
            * (1.0 - suppressive)
        )
    suppressive -= dynamics.suppressive_clearance * suppressive
    suppressive = min(1.0, max(0.0, suppressive))

    host = state.host
    host += dynamics.host_recovery * (1.0 - host)
    host -= treatment * dynamics.host_toxicity * host
    host -= dynamics.host_burden_cost * min(total, 3.0) * host
    host = min(1.0, max(0.0, host))

    return CancerState(bs=bs, br=br, effector=effector, suppressive=suppressive, host=host)


def simulate(
    initial: CancerState,
    dynamics: CancerDynamics,
    treatment_schedule: tuple[float, ...],
) -> tuple[CancerState, ...]:
    states = [initial]
    current = initial
    for treatment in treatment_schedule:
        current = step(current, dynamics, treatment)
        states.append(current)
    return tuple(states)
