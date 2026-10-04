# CGD-SIM-002 — Robustness, noise, and meta-layer failure injection

> Status: SYNTHETIC WORKING MODEL  
> Biological interpretation: UNVALIDATED  
> Clinical authority: NONE

## Why this tranche exists

CGD-SIM-001 gave the compensation controller direct access to latent capability.
That was useful as a known-answer bootstrap but unrealistically privileged.

CGD-SIM-002 removes that privilege.

The controller now acts on an estimated state:

~~~text
L0  latent capability c_t
L1  self / monitor estimate a_t
L2  compensation / handoff controller
~~~

The experiment asks three narrower questions:

1. Does the dual-track result survive a broad parameter sweep?
2. Does it survive observation noise and rare decline shocks?
3. Do L1 calibration failure and L2 handoff failure create distinguishable
   failure signatures?

No L3 or L4 controller is added yet. Higher meta-layers require evidence that
the lower controller needs an adaptive governor rather than merely more
observation.

## Layered equations

L1 receives a noisy objective observation:

~~~text
z_t = clamp(c_t + epsilon_t)
a_(t+1) = clamp(a_t + k(z_t - a_t))
~~~

L2 chooses desired compensation from the estimate rather than the latent truth:

~~~text
r_desired = (1-a_t)^2 / ((1-a_t)^2 + lambda)
r_applied = rho * r_desired
~~~

where rho is synthetic handoff reliability.

Functional performance remains:

~~~text
p_t = c_t + (1-c_t) r_applied
~~~

The counterfactual handoff deficit is:

~~~text
H_t = max(0, r*(c_t) - r_applied)
~~~

where r*(c_t) is used only as synthetic ground truth for validation.

## Sweep

Frozen grid:

~~~text
d      in {0.0025, 0.005, 0.0075}
k      in {0.05, 0.1, 0.2, 0.4}
lambda in {0.05, 0.1, 0.2, 0.5}
q      in {0.25, 0.5, 0.75}
~~~

Total: 144 parameter cells.

The sweep separately records surface functional performance, latent capability,
and observability amplification. This is intentional: a controller that hides
decline by aggressive compensation can score well on surface function while
making latent-state estimation much worse.

## Monte Carlo

The frozen stochastic run uses 500 deterministic seeds with:

~~~text
feedback noise standard deviation = 0.03
rare decline shock probability    = 0.04 per step
rare decline shock magnitude      = 0.01
~~~

The output reports the 5th percentile of each run's minimum functional
performance and the 95th percentile of final absolute metacognitive gap.

The random generator is seeded. Repeated Actions runs are reproducible.

## Meta-layer ablation

Frozen cases:

~~~text
reference               k=0.40  rho=1.00
L1 slow calibration     k=0.05  rho=1.00
L2 unreliable handoff   k=0.40  rho=0.35
L1 + L2 combined        k=0.05  rho=0.35
~~~

The intent is not to claim that these parameters represent human cognition.
They create separable synthetic failure modes:

~~~text
L1 failure -> stale / miscalibrated self-model
L2 failure -> correct-enough estimate but failed compensation handoff
combined   -> both
~~~

If these signatures are not distinguishable, adding deeper meta-layers would
be premature because the lower-level model would already be non-identifiable.

## Claim ceiling

A pass establishes reproducibility and internal consistency of the declared
control model only.

It does not establish:

- a dementia progression equation;
- a clinical threshold for awareness or safety;
- treatment effectiveness;
- that any human subsystem maps one-to-one onto L0/L1/L2;
- that a deeper meta-controller is medically beneficial;
- that surface functional preservation proves preservation of latent cognition.
