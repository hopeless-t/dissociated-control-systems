"""CGD-SIM-003: adaptive L3 governor experiments (synthetic only)."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from random import Random
from statistics import fmean
from .cognitive_decline import optimal_compensation

@dataclass(frozen=True)
class GovernorConfig:
    name: str
    mode: str = "none"  # none | naive | hysteretic | bounded
    steps: int = 150
    decline_rate: float = 0.005
    decline_rate_reduction: float = 0.0
    feedback_noise: float = 0.03
    shock_probability: float = 0.04
    shock_magnitude: float = 0.01
    compensation_cost: float = 0.2
    l1_failure_step: int = 30
    l2_failure_step: int = 60
    normal_feedback_gain: float = 0.4
    failed_feedback_gain: float = 0.05
    failed_handoff_reliability: float = 0.35
    calibration_on: float = 0.07
    calibration_off: float = 0.035
    handoff_on: float = 0.05
    handoff_off: float = 0.02
    naive_calibration_threshold: float = 0.055
    naive_handoff_threshold: float = 0.035
    calibration_boost_gain: float = 0.45
    redundancy_strength: float = 0.8
    max_observability_amplification: float = 4.0

@dataclass(frozen=True)
class GovernorSummary:
    mean_function: float
    minimum_function: float
    mean_abs_gap: float
    mean_handoff_deficit: float
    max_observability_amplification: float
    mean_governance_cost: float
    switches: int
    final_capability: float

def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))

def simulate_governor(config: GovernorConfig, *, seed: int = 0) -> GovernorSummary:
    if config.mode not in {"none","naive","hysteretic","bounded"}:
        raise ValueError("unknown governor mode")
    if config.max_observability_amplification < 1.0:
        raise ValueError("max_observability_amplification must be >= 1")
    rng=Random(seed)
    c=a=1.0
    cal=hand=False
    prev=(False,False)
    switches=0
    perf=[]; gaps=[]; hdef=[]; amps=[]; costs=[]
    max_r=1.0-1.0/sqrt(config.max_observability_amplification)

    for t in range(config.steps+1):
        k=(config.normal_feedback_gain if t < config.l1_failure_step
           else config.failed_feedback_gain)
        rho=(1.0 if t < config.l2_failure_step
             else config.failed_handoff_reliability)
        z=_clamp(c+rng.gauss(0.0, config.feedback_noise))
        cal_signal=abs(a-z)

        if config.mode=="naive":
            cal=cal_signal > config.naive_calibration_threshold
        elif config.mode in {"hysteretic","bounded"}:
            if (not cal) and cal_signal > config.calibration_on: cal=True
            elif cal and cal_signal < config.calibration_off: cal=False
        else:
            cal=False

        estimate=z if cal else a
        desired=optimal_compensation(estimate, config.compensation_cost)
        base_applied=rho*desired
        hand_signal=max(0.0, desired-base_applied)

        if config.mode=="naive":
            hand=hand_signal > config.naive_handoff_threshold
        elif config.mode in {"hysteretic","bounded"}:
            if (not hand) and hand_signal > config.handoff_on: hand=True
            elif hand and hand_signal < config.handoff_off: hand=False
        else:
            hand=False

        rho_eff=rho + (config.redundancy_strength*(1.0-rho) if hand else 0.0)
        applied=rho_eff*desired
        if config.mode=="bounded":
            applied=min(applied,max_r)

        p=c+(1.0-c)*applied
        amp=1.0/((1.0-applied)**2)
        true_desired=optimal_compensation(c, config.compensation_cost)

        perf.append(p); gaps.append(abs(a-c))
        hdef.append(max(0.0,true_desired-applied)); amps.append(amp)
        costs.append((0.03 if cal else 0.0)+(0.05 if hand else 0.0))

        if t>0 and (cal,hand)!=prev: switches+=1
        prev=(cal,hand)
        if t==config.steps: break

        k_eff=max(k,config.calibration_boost_gain) if cal else k
        a=_clamp(a+k_eff*(z-a))
        decline=config.decline_rate*(1.0-config.decline_rate_reduction)
        if rng.random() < config.shock_probability:
            decline += config.shock_magnitude
        c=_clamp(c-decline)

    return GovernorSummary(
        mean_function=fmean(perf), minimum_function=min(perf),
        mean_abs_gap=fmean(gaps), mean_handoff_deficit=fmean(hdef),
        max_observability_amplification=max(amps),
        mean_governance_cost=fmean(costs), switches=switches,
        final_capability=c,
    )

def monte_carlo(samples: int = 500) -> dict[str,dict[str,float]]:
    configs=(
        GovernorConfig(name="no_governor",mode="none"),
        GovernorConfig(name="naive_l3",mode="naive"),
        GovernorConfig(name="hysteretic_l3",mode="hysteretic"),
        GovernorConfig(name="bounded_l3",mode="bounded"),
        GovernorConfig(name="bounded_l3_dual_track",mode="bounded",decline_rate_reduction=0.5),
    )
    out={}
    for cfg in configs:
        rows=[simulate_governor(cfg,seed=s) for s in range(samples)]
        floors=sorted(r.minimum_function for r in rows)
        out[cfg.name]={
            "mean_function":fmean(r.mean_function for r in rows),
            "p05_floor":floors[int(0.05*(samples-1))],
            "mean_abs_gap":fmean(r.mean_abs_gap for r in rows),
            "mean_handoff_deficit":fmean(r.mean_handoff_deficit for r in rows),
            "mean_max_amp":fmean(r.max_observability_amplification for r in rows),
            "mean_switches":fmean(r.switches for r in rows),
            "mean_cost":fmean(r.mean_governance_cost for r in rows),
            "mean_final_capability":fmean(r.final_capability for r in rows),
        }
    return out

def format_markdown() -> str:
    result=monte_carlo()
    lines=[
        "# CGD-SIM-003 adaptive L3 governor",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| case | mean function | p05 floor | mean abs gap | handoff deficit | mean max amp | switches | governance cost | final capability |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in ("no_governor","naive_l3","hysteretic_l3","bounded_l3","bounded_l3_dual_track"):
        r=result[name]
        lines.append(
            f"| {name} | {r['mean_function']:.3f} | {r['p05_floor']:.3f} | "
            f"{r['mean_abs_gap']:.3f} | {r['mean_handoff_deficit']:.3f} | "
            f"{r['mean_max_amp']:.3f} | {r['mean_switches']:.1f} | "
            f"{r['mean_cost']:.3f} | {r['mean_final_capability']:.3f} |"
        )
    n=result["naive_l3"]; h=result["hysteretic_l3"]; b=result["bounded_l3"]
    reduction=1.0-h["mean_switches"]/n["mean_switches"]
    lines += [
        "",
        f"Hysteresis reduces mean governor switching by {reduction:.1%} relative to naive L3.",
        "Bounded L3 hard-caps observability amplification at 4x by construction.",
        "",
        "Interpretation ceiling: this tests controller stability under declared synthetic failures; it does not model dementia or establish a clinical intervention.",
    ]
    return "\n".join(lines)

if __name__=="__main__":
    print(format_markdown())
