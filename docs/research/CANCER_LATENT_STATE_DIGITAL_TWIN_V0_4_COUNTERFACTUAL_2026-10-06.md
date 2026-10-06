# Cancer Latent-State Digital Twin v0.4 — counterfactual / intervention-conditional forecast

Date: 2026-10-06
Status: simulation-stage working theory / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_3_ADVERSARIAL_2026-10-06.md`

## Core correction

A cancer Twin must not forecast one unconditional future from the current patient state.

The target is not:

```text
P(Y_future | x_t)
```

but a treatment-history- and intervention-conditional quantity:

```text
P(Y_future | x_t, Theta, Phi, u_history, u_future)
```

or, in explicit counterfactual notation:

```text
P(Y_future^(u) | evidence_to_t)
```

where:

- `x_t` is current latent biological state;
- `Theta` is the patient-specific transition law;
- `Phi` is the observation / sensor law;
- `u_history` is prior clinically justified treatment history;
- `u_future` is the declared future intervention path being simulated.

This creates the invariant:

```text
Same Patient State != Same Future Under Different Intervention Paths
Forecast Without Declared u_future != Complete Forecast
```

## Synthetic counterfactual attack

The v0.3 primary apparent-response cohort contained 20,484 virtual patients selected to have similar day-30 imaging response.

Each exact day-30 latent state and exact patient-specific dynamics were then cloned into four synthetic future intervention paths.

The path labels below are simulation labels only; they are not treatment recommendations.

```text
EARLY_STOP      treatment input set to zero after day30
MAINTENANCE     lower constant synthetic treatment input
STANDARD_MODEL  original synthetic schedule
SUSTAINED       full synthetic treatment input through the horizon
```

Synthetic day-180 escape frequencies were approximately:

```text
EARLY_STOP      98.8%
MAINTENANCE     45.8%
STANDARD_MODEL  36.2%
SUSTAINED       16.3%
```

Again, these percentages are properties of the declared toy model, not clinical estimates.

More important than the rates themselves is the counterfactual flip rate: the same day-30 patient state changed outcome class under alternative future inputs for a large fraction of synthetic patients.

Approximate pairwise basin-flip fractions:

```text
STANDARD_MODEL vs EARLY_STOP   62.6%
STANDARD_MODEL vs SUSTAINED    20.0%
MAINTENANCE vs SUSTAINED       29.5%
EARLY_STOP vs SUSTAINED        82.6%
```

This is a structural demonstration that the future is not a property of `x_t` alone in an intervention-dependent system.

## Selection pressure warning

The synthetic sustained-input arm often produced lower total burden while the resistant fraction increased substantially.

Therefore:

```text
Low Total Burden != Low Resistant Fraction
Short-Term Control != Absence Of Selection
```

The Twin must track both total burden and composition / transition law.

This is not evidence that any real treatment should be extended, stopped, reduced, or changed.

## Forecast product

A credible simulation output should be a scenario bundle rather than one point prediction.

Candidate output:

```text
Scenario A: declared u_future_A
    posterior trajectory distribution
    basin probabilities
    uncertainty interval
    dominant failure modes

Scenario B: declared u_future_B
    ...

Scenario C: no declared future path
    FORECAST_UNDERSPECIFIED
```

The Twin should fail closed if intervention semantics are missing or ambiguous.

## Causal separation

Observed treatment response does not identify intrinsic disease dynamics unless treatment input is modeled.

For example, a falling tumor burden can arise from:

```text
low intrinsic growth
strong treatment sensitivity
strong immune pressure
high combination of the above
```

and those worlds may diverge after the input changes.

Therefore:

```text
Observed Response != Intrinsic Natural History
Observed Response != Treatment Sensitivity Alone
```

## New posterior target

The Twin posterior should include transition parameters conditioned on treatment history:

```text
p(x_t, Theta, Phi | z_(0:t), u_(0:t))
```

A future scenario is then propagated under an explicit candidate path:

```text
p(x_(t+1:T) | posterior_t, u_(t+1:T))
```

## Decision-value objective

v0.3 introduced observation delay cost.

v0.4 adds scenario-separation value:

```text
q* = argmax_q [
    expected_information_gain(q)
  + lambda * scenario_discrimination(q)
  + gamma * decision_value(q)
  - mu * observation_burden(q)
  - nu * delay_cost(q)
  - xi * redundancy(q)
]
```

A measurement is valuable if it helps distinguish not only latent states but also materially different counterfactual trajectories under the declared candidate paths.

## Known-answer implementation

`tests/test_cancer_twin.py` now requires that an identical current latent state propagated through different synthetic future intervention schedules can produce different future states.

This test prevents future code from silently collapsing an intervention-conditional system into an unconditional patient-risk predictor.

## Next falsifiers

1. Unknown / misrecorded treatment history.
2. Delayed treatment-effect kinetics.
3. Treatment-response hysteresis.
4. Dose / exposure mismeasurement.
5. Future-path uncertainty rather than one fixed planned schedule.
6. Confounding by indication when learning from observational human data.
7. Competing treatment toxicity / host-reserve objectives.

## Claim boundary

This note defines a causal simulation requirement. It does not estimate the effect of any actual oncology treatment and cannot be used to recommend treatment changes.
