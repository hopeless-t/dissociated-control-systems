"""HF01 synthetic hair-follicle state/calibration model.

This module is a deliberately synthetic control model. It is not a clinical
model, does not estimate a person's biology, and does not recommend treatment.

The purpose is to test a narrower DCS question:

    can a system retain latent regenerative machinery while losing practical
    reachability of a healthy-output attractor because slow structural state
    variables create hysteresis?

All state variables are normalized to [0, 1].
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import random


def _clip(value: float) -> float:
    return max(0.0, min(1.0, value))


@dataclass(frozen=True)
class HFState:
    androgen_pressure: float
    stress_load: float
    regeneration: float
    progenitor_reserve: float
    niche_integrity: float
    structural_lock: float
    hair_output: float

    def bounded(self) -> "HFState":
        return HFState(*(_clip(v) for v in self.as_tuple()))

    def as_tuple(self) -> tuple[float, ...]:
        return (
            self.androgen_pressure,
            self.stress_load,
            self.regeneration,
            self.progenitor_reserve,
            self.niche_integrity,
            self.structural_lock,
            self.hair_output,
        )


@dataclass(frozen=True)
class HFControl:
    behavioral: float = 0.0
    antiandrogen: float = 0.0
    regenerative: float = 0.0
    structural: float = 0.0


@dataclass(frozen=True)
class HFParams:
    androgen_setpoint: float = 0.58
    antiandrogen_gain: float = 0.50
    stress_setpoint: float = 0.42
    behavioral_stress_gain: float = 0.30

    androgen_relaxation: float = 0.80
    stress_relaxation: float = 0.80

    regen_from_niche: float = 0.55
    regen_from_progenitors: float = 0.30
    regen_external_gain: float = 0.35
    regen_bias: float = 0.12
    regen_suppressed_by_androgen: float = 0.42
    regen_suppressed_by_stress: float = 0.20
    regen_suppressed_by_lock: float = 0.45
    regen_relaxation: float = 0.70

    progenitor_regen_gain: float = 0.30
    progenitor_external_gain: float = 0.18
    progenitor_androgen_damage: float = 0.05
    progenitor_stress_damage: float = 0.04
    progenitor_lock_damage: float = 0.22

    niche_regen_gain: float = 0.06
    niche_structural_repair_gain: float = 0.10
    niche_baseline_loss: float = 0.01
    niche_stress_loss: float = 0.02
    niche_lock_loss: float = 0.12

    overload_stress_weight: float = 0.55
    overload_threshold: float = 0.72
    lock_overload_gain: float = 0.26
    lock_hysteresis_gain: float = 0.14
    lock_regen_repair_gain: float = 0.20
    lock_structural_repair_gain: float = 0.35

    output_floor: float = 0.12
    output_gain: float = 0.88
    output_lock_penalty: float = 0.60
    output_relaxation: float = 0.12


DEFAULT_PARAMS = HFParams()


def canonical_early_state() -> HFState:
    return HFState(
        androgen_pressure=0.20,
        stress_load=0.20,
        regeneration=0.90,
        progenitor_reserve=0.90,
        niche_integrity=0.90,
        structural_lock=0.05,
        hair_output=0.90,
    )


def canonical_late_state() -> HFState:
    return HFState(
        androgen_pressure=0.80,
        stress_load=0.70,
        regeneration=0.30,
        progenitor_reserve=0.35,
        niche_integrity=0.55,
        structural_lock=0.65,
        hair_output=0.35,
    )


def state_from_lock(lock: float) -> HFState:
    """Create a deterministic degeneration trajectory indexed by structural lock."""
    lock = _clip(lock)
    return HFState(
        androgen_pressure=0.58,
        stress_load=0.42,
        regeneration=_clip(0.90 - 0.70 * lock),
        progenitor_reserve=_clip(0.95 - 0.75 * lock),
        niche_integrity=_clip(0.95 - 0.45 * lock),
        structural_lock=lock,
        hair_output=_clip(0.90 - 0.60 * lock),
    )


def step(
    state: HFState,
    control: HFControl = HFControl(),
    params: HFParams = DEFAULT_PARAMS,
    dt: float = 0.05,
) -> HFState:
    a, q, r, p, n, f, h = state.as_tuple()
    b = _clip(control.behavioral)
    d = _clip(control.antiandrogen)
    g = _clip(control.regenerative)
    m = _clip(control.structural)

    a_target = _clip(params.androgen_setpoint - params.antiandrogen_gain * d)
    q_target = _clip(params.stress_setpoint - params.behavioral_stress_gain * b)

    da = params.androgen_relaxation * (a_target - a)
    dq = params.stress_relaxation * (q_target - q)

    regen_drive = (
        params.regen_from_niche * n
        + params.regen_from_progenitors * p
        + params.regen_external_gain * g
        + params.regen_bias
    )
    regen_suppression = (
        params.regen_suppressed_by_androgen * a
        + params.regen_suppressed_by_stress * q
        + params.regen_suppressed_by_lock * f
    )
    r_target = _clip(regen_drive - regen_suppression)
    dr = params.regen_relaxation * (r_target - r)

    dp = (
        params.progenitor_regen_gain * r * n * (1.0 - p)
        + params.progenitor_external_gain * g * (1.0 - p)
        - (
            params.progenitor_androgen_damage * a
            + params.progenitor_stress_damage * q
            + params.progenitor_lock_damage * f
        )
        * p
    )

    dn = (
        params.niche_regen_gain * r * (1.0 - n)
        + params.niche_structural_repair_gain * m * (1.0 - n)
        - (
            params.niche_baseline_loss
            + params.niche_stress_loss * q
            + params.niche_lock_loss * f
        )
        * n
    )

    overload = max(
        0.0,
        a + params.overload_stress_weight * q - params.overload_threshold,
    )
    df = (
        params.lock_overload_gain * overload * (1.0 - f)
        + params.lock_hysteresis_gain * (1.0 - p) * f
        - (
            params.lock_regen_repair_gain * r
            + params.lock_structural_repair_gain * m
        )
        * f
    )

    h_target = _clip(
        params.output_floor
        + params.output_gain * r * p * n * (1.0 - params.output_lock_penalty * f)
    )
    dh = params.output_relaxation * (h_target - h)

    return HFState(
        a + dt * da,
        q + dt * dq,
        r + dt * dr,
        p + dt * dp,
        n + dt * dn,
        f + dt * df,
        h + dt * dh,
    ).bounded()


def simulate(
    initial: HFState,
    control: HFControl = HFControl(),
    params: HFParams = DEFAULT_PARAMS,
    steps: int = 2000,
    dt: float = 0.05,
) -> HFState:
    state = initial
    for _ in range(steps):
        state = step(state, control=control, params=params, dt=dt)
    return state


def recoverability_threshold(
    control: HFControl,
    params: HFParams = DEFAULT_PARAMS,
    output_threshold: float = 0.50,
    grid_step: float = 0.05,
) -> float | None:
    """Largest initial structural-lock value that reaches output_threshold."""
    accepted: list[float] = []
    count = round(1.0 / grid_step)
    for i in range(count + 1):
        lock = round(i * grid_step, 10)
        final = simulate(state_from_lock(lock), control=control, params=params)
        if final.hair_output >= output_threshold:
            accepted.append(lock)
    return max(accepted) if accepted else None


def perturb_params(
    params: HFParams,
    seed: int,
    fraction: float,
) -> HFParams:
    """Deterministically perturb every positive coefficient by ±fraction."""
    rng = random.Random(seed)
    values = {}
    for name, value in params.__dict__.items():
        scale = 1.0 + rng.uniform(-fraction, fraction)
        values[name] = value * scale
    return replace(params, **values)


def ordering_holds(params: HFParams = DEFAULT_PARAMS) -> bool:
    initial = canonical_early_state()
    none = simulate(initial, HFControl(), params).hair_output
    behavior = simulate(initial, HFControl(behavioral=1.0), params).hair_output
    drug = simulate(initial, HFControl(antiandrogen=1.0), params).hair_output
    combo = simulate(
        initial,
        HFControl(behavioral=1.0, antiandrogen=1.0),
        params,
    ).hair_output

    late = canonical_late_state()
    late_combo = simulate(
        late,
        HFControl(behavioral=1.0, antiandrogen=1.0),
        params,
    ).hair_output
    late_structural = simulate(
        late,
        HFControl(behavioral=1.0, antiandrogen=1.0, structural=1.0),
        params,
    ).hair_output

    return (
        combo > drug > behavior >= none
        and late_combo < 0.30
        and late_structural > 0.60
    )


def robustness_fraction(
    samples: int = 300,
    perturbation_fraction: float = 0.20,
) -> float:
    hits = 0
    for seed in range(samples):
        candidate = perturb_params(DEFAULT_PARAMS, seed, perturbation_fraction)
        hits += int(ordering_holds(candidate))
    return hits / samples
