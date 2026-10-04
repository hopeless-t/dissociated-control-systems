# CGD-SIM-054 — Effective failure-mode diversity pressure knee

> Status: SYNTHETIC PARTIAL-INDEPENDENCE TEST  
> Clinical authority: NONE

SIM-053 showed that an orthogonal audit can recover observability that is lost
when a primary context channel and watchdog share a common-mode bias.

SIM-054 attacks the binary label **orthogonal**.

## Partial-independence model

The audit is allowed to inherit only a fraction `rho` of the primary channel's
hidden common bias:

~~~text
primary = environment + B_common + eps_primary
audit   = environment + rho * B_common + eps_audit
~~~

The disagreement channel therefore contains:

~~~text
primary - audit = (1-rho) * B_common + noise
~~~

Define:

~~~text
effective diversity D = 1-rho
~~~

`rho=0` is the idealized SIM-053 orthogonal case. `rho=1` is a fully shared
failure mode equivalent to the SIM-052 blind spot.

## Frozen detector geometry

~~~text
B_common = 0.08
sigma_primary = 0.01
sigma_audit = 0.015
samples / audit batch = 16
trigger threshold = 0.03
rho grid = 0, 0.25, 0.50, 0.625, 0.75, 0.90, 1.0
~~~

For a 16-sample batch mean, the disagreement-noise standard deviation is:

~~~text
sqrt(sigma_primary^2 + sigma_audit^2) / sqrt(16)
~~~

Because the batch mean is Gaussian under the frozen model, trigger power can be
calculated analytically and independently checked by Monte Carlo without
simulating all 16 raw samples on every trial.

## Pressure-knee hypothesis

The positive mean disagreement is:

~~~text
mu = (1-rho) * B_common
~~~

When `mu` reaches the trigger threshold, a one-sided dominant Gaussian crossing
has approximately 50% trigger power.

Therefore the geometric prediction is:

~~~text
(1-rho) * 0.08 = 0.03
rho = 0.625
D = 0.375
~~~

This is not asserted as a universal diversity threshold. It is a predicted knee
for the frozen bias magnitude, sample count, noises and trigger threshold.

## Metrics

For each shared-bias fraction:

- effective diversity `D`;
- observable unshared bias;
- disagreement signal-to-noise ratio;
- analytic trigger probability;
- Monte Carlo trigger probability;
- analytic / Monte Carlo mismatch;
- whether trigger power remains at least 90%.

## New invariants

~~~text
Independence Is A Continuum, Not A Boolean
Declared Diversity != Effective Failure-Mode Separation
Audit Value Scales With The Unshared Failure Component
Redundancy Count Should Be Replaced By Failure-Mode Geometry
~~~

## Claim ceiling

All shared-bias fractions, thresholds, noises, sample counts and trigger-power
criteria are synthetic scenario parameters.

A PASS establishes only that partial common-mode leakage has a measurable and
predictable effect in this frozen detector. It does not assign an independence
score to any real clinical assessment, caregiver, digital IADL, sensor or other
observation source.
