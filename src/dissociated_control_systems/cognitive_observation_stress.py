"""CGD-SIM-004: observation-channel stress for bounded L3 (synthetic only)."""
from __future__ import annotations
from dataclasses import dataclass
from random import Random
from statistics import fmean
from .cognitive_decline import optimal_compensation

@dataclass(frozen=True)
class ObservationStressConfig:
    name: str
    mode: str  # clean | biased_primary | redundant
    steps: int = 150
    decline_rate: float = 0.005
    decline_rate_reduction: float = 0.5
    primary_noise: float = 0.03
    primary_bias: float = 0.08
    primary_dropout: float = 0.25
    secondary_noise: float = 0.03
    secondary_dropout: float = 0.10
    shock_probability: float = 0.04
    shock_magnitude: float = 0.01
    compensation_cost: float = 0.2

@dataclass(frozen=True)
class ObservationStressSummary:
    mean_function: float
    minimum_function: float
    mean_abs_gap: float
    mean_handoff_deficit: float
    max_observability_amplification: float
    final_capability: float
    stale_observation_fraction: float
    observer_disagreement_fraction: float

def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))

def simulate(config: ObservationStressConfig, *, seed: int = 0) -> ObservationStressSummary:
    if config.mode not in {"clean","biased_primary","redundant"}:
        raise ValueError("unknown observation stress mode")
    rng=Random(seed)
    c=a=1.0
    cal=hand=False
    last_z=1.0
    stale=disagree=0
    perf=[]; gaps=[]; hdefs=[]; amps=[]

    for t in range(config.steps+1):
        k=0.4 if t < 30 else 0.05
        rho=1.0 if t < 60 else 0.35

        if config.mode=="clean":
            z=_clamp(c+rng.gauss(0.0,config.primary_noise))
        else:
            z1=None
            if rng.random() >= config.primary_dropout:
                z1=_clamp(c+config.primary_bias+rng.gauss(0.0,config.primary_noise))
            if config.mode=="biased_primary":
                if z1 is None:
                    z=last_z; stale+=1
                else:
                    z=z1
            else:
                z2=None
                if rng.random() >= config.secondary_dropout:
                    z2=_clamp(c+rng.gauss(0.0,config.secondary_noise))
                available=[x for x in (z1,z2) if x is not None]
                if not available:
                    z=last_z; stale+=1
                elif len(available)==1:
                    z=available[0]
                else:
                    if abs(z1-z2) > 0.06:
                        disagree+=1
                    z=min(available)  # conservative fusion under disagreement

        last_z=z
        cal_signal=abs(a-z)
        if (not cal) and cal_signal > 0.07: cal=True
        elif cal and cal_signal < 0.035: cal=False

        estimate=z if cal else a
        desired=optimal_compensation(estimate,config.compensation_cost)
        base=rho*desired
        hand_signal=max(0.0,desired-base)
        if (not hand) and hand_signal > 0.05: hand=True
        elif hand and hand_signal < 0.02: hand=False

        rho_eff=rho + (0.8*(1.0-rho) if hand else 0.0)
        applied=min(rho_eff*desired,0.5)  # A_obs <= 4
        p=c+(1.0-c)*applied

        perf.append(p)
        gaps.append(abs(a-c))
        hdefs.append(max(0.0,optimal_compensation(c,config.compensation_cost)-applied))
        amps.append(1.0/((1.0-applied)**2))

        if t==config.steps: break
        k_eff=max(k,0.45) if cal else k
        a=_clamp(a+k_eff*(z-a))
        decline=config.decline_rate*(1.0-config.decline_rate_reduction)
        if rng.random() < config.shock_probability:
            decline += config.shock_magnitude
        c=_clamp(c-decline)

    n=config.steps+1
    return ObservationStressSummary(
        mean_function=fmean(perf),
        minimum_function=min(perf),
        mean_abs_gap=fmean(gaps),
        mean_handoff_deficit=fmean(hdefs),
        max_observability_amplification=max(amps),
        final_capability=c,
        stale_observation_fraction=stale/n,
        observer_disagreement_fraction=disagree/n,
    )

def monte_carlo(samples: int = 500) -> dict[str,dict[str,float]]:
    cfgs=(
        ObservationStressConfig(name="clean",mode="clean"),
        ObservationStressConfig(name="biased_primary",mode="biased_primary"),
        ObservationStressConfig(name="redundant",mode="redundant"),
    )
    out={}
    for cfg in cfgs:
        rows=[simulate(cfg,seed=s) for s in range(samples)]
        floors=sorted(r.minimum_function for r in rows)
        out[cfg.name]={
            "mean_function":fmean(r.mean_function for r in rows),
            "p05_floor":floors[int(0.05*(samples-1))],
            "mean_abs_gap":fmean(r.mean_abs_gap for r in rows),
            "mean_handoff_deficit":fmean(r.mean_handoff_deficit for r in rows),
            "mean_max_amp":fmean(r.max_observability_amplification for r in rows),
            "mean_final_capability":fmean(r.final_capability for r in rows),
            "stale_fraction":fmean(r.stale_observation_fraction for r in rows),
            "disagreement_fraction":fmean(r.observer_disagreement_fraction for r in rows),
        }
    return out

def format_markdown() -> str:
    r=monte_carlo()
    lines=[
        "# CGD-SIM-004 observation-channel stress",
        "",
        "> Synthetic control-model result only. Clinical authority: NONE.",
        "",
        "| case | mean function | p05 floor | mean abs gap | handoff deficit | mean max amp | final capability | stale obs | observer disagreement |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in ("clean","biased_primary","redundant"):
        x=r[name]
        lines.append(
            f"| {name} | {x['mean_function']:.3f} | {x['p05_floor']:.3f} | "
            f"{x['mean_abs_gap']:.3f} | {x['mean_handoff_deficit']:.3f} | "
            f"{x['mean_max_amp']:.3f} | {x['mean_final_capability']:.3f} | "
            f"{x['stale_fraction']:.3f} | {x['disagreement_fraction']:.3f} |"
        )
    lines += [
        "",
        "Primary-only bias/dropout degrades L1 calibration despite a stable L3 policy.",
        "Adding an independent observation channel restores most of the lost calibration and function without adding a deeper meta-controller.",
        "",
        "Interpretation ceiling: synthetic observability result only; no clinical mapping is asserted.",
    ]
    return "\n".join(lines)

if __name__=="__main__":
    print(format_markdown())
