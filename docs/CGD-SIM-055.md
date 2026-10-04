# CGD-SIM-055 — Diversity debt and audit sample complexity

> Status: SYNTHETIC STATISTICAL-POWER TEST  
> Clinical authority: NONE

SIM-054 converted “independent vs not independent” into a continuous effective
diversity variable:

~~~text
D = 1-rho
~~~

where `rho` is the fraction of hidden bias shared by primary and audit channels.
With a fixed absolute trigger threshold, detection power collapsed once the
unshared signal fell below that threshold.

SIM-055 asks whether extra measurement effort can buy back weak but nonzero
failure-mode diversity.

## Fixed-FPR detector

Instead of keeping an absolute threshold fixed, the detector holds the
two-sided false-positive rate at `1%`.

For `n` independent audit samples:

~~~text
signal = D * B_common
SE = sigma_disagreement / sqrt(n)
threshold = z_(1-alpha/2) * SE
~~~

The target is at least `90%` detection power.

Frozen parameters:

~~~text
B_common = 0.08
sigma_primary = 0.01
sigma_audit = 0.015
alpha = 0.01
target power = 0.90
D grid = 1, .75, .50, .375, .25, .10, .05, .02, .01, 0
~~~

## Inverse-square hypothesis

For small positive `D`, maintaining fixed false-positive and detection power
requires approximately constant signal-to-noise ratio:

~~~text
D * B * sqrt(n) / sigma ~= constant
~~~

Therefore:

~~~text
n proportional to 1 / D^2
~~~

Halving effective diversity should require roughly four times as many samples.

## Structural boundary

At `D=0` the audit shares the entire hidden failure mode:

~~~text
observable signal = D * B = 0
~~~

No increase in sample count can create information that is absent from the
observation geometry. With zero signal, trigger probability remains the chosen
false-positive rate.

## Metrics

- minimum sample count reaching 90% analytic power;
- achieved power at that integer sample count;
- scaled cost `n*D^2`;
- sample multiplier when effective diversity halves;
- explicit no-finite-sample state at `D=0`.

## New invariants

~~~text
Weak Independence Can Be Bought Back With Samples
Audit Cost Scales Approximately As 1 / D^2
Zero Independence Cannot Be Repaired By More Measurements
Measurement Budget != Structural Independence
~~~

## Claim ceiling

All power targets, false-positive rates, noises, bias magnitudes and sample
counts are synthetic scenario parameters. The inverse-square scaling is a
property of this Gaussian observation model; it is not a monitoring cadence or
sample-size recommendation for any real clinical, caregiver, sensor or
behavioral assessment.
