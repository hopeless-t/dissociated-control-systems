# CGD-SIM-039 — Noisy external-observation frontier

> Status: SYNTHETIC MEASUREMENT-NOISE TEST  
> Clinical authority: NONE

SIM-038 established structural full-rank identifiability for the four-channel
observation family:

~~~text
self report
informant report
objective performance
daily function
~~~

Full rank does not mean low estimation error.

SIM-039 therefore adds frozen, unitless Gaussian measurement noise. The noise
values are engineering scenario parameters and are not estimates of ECog, FAQ,
MoCA, MMSE or any other clinical instrument.

## Observation model

~~~text
S = Z - A + eps_S
I = Z + B + eps_I
F = Z + E + eps_F
O_j = Z + eps_Oj
~~~

with:

~~~text
sigma_S = 0.10
sigma_I = 0.10
sigma_F = 0.10
sigma_O(single trial) = 0.20
~~~

The objective channel is repeated:

~~~text
n = 1, 4, 16, 64, 256
~~~

and averaged.

## Analytic frontier

For the simple estimator:

~~~text
Z_hat = mean(O)
A_hat = Z_hat - S
B_hat = I - Z_hat
E_hat = F - Z_hat
~~~

objective-state error is:

~~~text
RMSE(Z_hat) = sigma_O / sqrt(n)
~~~

while reporter/scaffold estimates have:

~~~text
RMSE(A_hat) = sqrt(sigma_O^2 / n + sigma_S^2)
RMSE(B_hat) = sqrt(sigma_O^2 / n + sigma_I^2)
RMSE(E_hat) = sqrt(sigma_O^2 / n + sigma_F^2)
~~~

Thus an objective channel can be averaged down, but it cannot eliminate noise
from independent self, informant or functional channels.

## Monte Carlo cross-check

Each repeat count is checked with a deterministic 20,000-sample Monte Carlo
simulation against the closed-form RMSE equations.

The purpose is not to estimate human measurement error. It is to verify the
qualitative control result:

~~~text
Full Rank != Zero Error
More Objective Trials != Infinite Recovery
Reporter / Function Noise Becomes The Residual Floor
~~~

## Decision rule

The synthetic practical knee is the first repeat budget immediately before a
further 4x increase yields less than a 5% relative reduction in the average
RMSE of A/B/E.

This uses the same finite-resource logic as other DCS / Finite RAM pressure-knee
experiments: once one channel is no longer the dominant error source, spending
more budget on that channel is friction rather than progress.

## Next question

If repeated objective measurements saturate, should the next evidence budget go
to:

- repeated self report;
- repeated informant report;
- a second independent informant;
- repeated functional observation;
- temporal change rather than same-visit replication?

SIM-040 should compare those evidence-allocation choices without assuming that
all channels have the same bias structure.
