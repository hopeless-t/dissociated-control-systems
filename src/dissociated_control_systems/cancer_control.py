"""Synthetic neuroimmune-tumor control model for RQ-005.

This module is a falsifiable mathematical research primitive. It is not a
clinical model, treatment recommendation, prognosis tool, or calibrated model
of any specific cancer.
"""

from __future__ import annotations

from dataclasses import dataclass


def _unit(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def _nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if value < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return value


@dataclass(frozen=True)
class CancerControlState:
    """Normalized latent state used only for synthetic dynamics."""

    tumor: float
    effector: float
    immunosuppression: float
    stress: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "tumor", _nonnegative(self.tumor, "tumor"))
        for name in ("effector", "immunosuppression", "stress"):
            object.__setattr__(self, name, _unit(getattr(self, name), name))


@dataclass(frozen=True)
class CancerControlInputs:
    """Measured/assigned mediators, not a latent "hope" variable.

    The model is intentionally neutral about whether a psychological state
    raises, lowers, or leaves these mediators unchanged. That mapping must be
    estimated from data.
    """

    prescribed_treatment: float = 0.35
    adherence: float = 0.55
    stress_recovery_rate: float = 0.22

    def __post_init__(self) -> None:
        for name in ("prescribed_treatment", "adherence"):
            object.__setattr__(self, name, _unit(getattr(self, name), name))
        object.__setattr__(
            self,
            "stress_recovery_rate",
            _nonnegative(self.stress_recovery_rate, "stress_recovery_rate"),
        )

    @property
    def effective_treatment(self) -> float:
        return self.prescribed_treatment * self.adherence


@dataclass(frozen=True)
class CancerControlParameters:
    """Uncalibrated dimensionless parameters for deterministic experiments."""

    growth_rate: float = 0.65
    carrying_capacity: float = 1.0
    stress_growth: float = 0.22
    immune_kill: float = 0.90
    treatment_kill: float = 0.90

    immune_source: float = 0.16
    immune_decay: float = 0.18
    stress_exhaustion: float = 0.55
    suppression_on_effector: float = 0.60
    treatment_immune_boost: float = 0.12

    suppression_from_tumor: float = 0.18
    suppression_from_stress: float = 0.28
    suppression_clearance: float = 0.35

    stress_input: float = 0.17

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            _nonnegative(value, name)
        if self.carrying_capacity <= 0.0:
            raise ValueError("carrying_capacity must be positive")


def instantaneous_control_margin(
    state: CancerControlState,
    inputs: CancerControlInputs,
    params: CancerControlParameters = CancerControlParameters(),
) -> float:
    """Return the instantaneous shrink/grow margin for tumor burden.

    Positive means the model's kill terms exceed its growth terms at the
    current state. This is a local mathematical condition, not a prognosis.
    """

    growth_pressure = (
        params.growth_rate * (1.0 - state.tumor / params.carrying_capacity)
        + params.stress_growth * state.stress
    )
    control_pressure = (
        params.immune_kill * state.effector
        + params.treatment_kill * inputs.effective_treatment
    )
    return control_pressure - growth_pressure


def step(
    state: CancerControlState,
    inputs: CancerControlInputs,
    params: CancerControlParameters = CancerControlParameters(),
    *,
    dt: float = 0.05,
) -> CancerControlState:
    """Advance one explicit-Euler step of the synthetic dynamical system."""

    dt = _nonnegative(dt, "dt")
    if dt == 0.0:
        return state

    treatment = inputs.effective_treatment
    tumor_saturation = state.tumor / (1.0 + state.tumor)

    d_stress = (
        params.stress_input
        - inputs.stress_recovery_rate * state.stress
    )
    d_suppression = (
        params.suppression_from_tumor * tumor_saturation
        + params.suppression_from_stress * state.stress
        - params.suppression_clearance * state.immunosuppression
    )
    d_effector = (
        params.immune_source
        + params.treatment_immune_boost * treatment
        - params.immune_decay * state.effector
        - params.stress_exhaustion * state.stress * state.effector
        - params.suppression_on_effector
        * state.immunosuppression
        * state.effector
    )
    d_tumor = -state.tumor * instantaneous_control_margin(
        state, inputs, params
    )

    return CancerControlState(
        tumor=max(0.0, state.tumor + dt * d_tumor),
        effector=min(1.0, max(0.0, state.effector + dt * d_effector)),
        immunosuppression=min(
            1.0,
            max(0.0, state.immunosuppression + dt * d_suppression),
        ),
        stress=min(1.0, max(0.0, state.stress + dt * d_stress)),
    )


def simulate(
    initial: CancerControlState,
    inputs: CancerControlInputs,
    params: CancerControlParameters = CancerControlParameters(),
    *,
    steps: int = 200,
    dt: float = 0.05,
) -> tuple[CancerControlState, ...]:
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise TypeError("steps must be an integer")
    if steps < 0:
        raise ValueError("steps must be non-negative")

    trajectory = [initial]
    current = initial
    for _ in range(steps):
        current = step(current, inputs, params, dt=dt)
        trajectory.append(current)
    return tuple(trajectory)
