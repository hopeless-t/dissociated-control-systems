# CGD-SIM-043 — Repeated-test practice-effect robustness attack

> Status: SYNTHETIC MEASUREMENT-BIAS SENSITIVITY TEST  
> Clinical authority: NONE

SIM-039 and SIM-040 treated repeated objective measurements as conditionally iid
and unbiased. Public cognitive-testing literature makes that assumption unsafe
to export unchanged: repeated exposure can produce practice effects, including
in older adults and MCI samples.

SIM-043 therefore attacks the synthetic assumption before any external data are
fit.

## Frozen sensitivity model

For objective repeat `j`:

~~~text
O_j = Z + beta*(j-1) + eps_j
~~~

with:

~~~text
eps_j iid, zero mean, sigma = 0.20
~~~

The mean of `n` repeats has:

~~~text
bias = beta*(n-1)/2
variance = sigma^2/n
MSE = variance + bias^2
~~~

The model is intentionally simple and monotone. The beta values are not taken
from any published cognitive test and are not clinical estimates.

Sensitivity grid:

~~~text
beta = 0,
       0.00025,
       0.0005,
       0.001,
       0.002,
       0.005
~~~

For each beta, every integer repeat count from 1 through 256 is evaluated.

## Full-state loss

In the frozen four-channel reconstruction:

~~~text
Z_hat = O_bar
A_hat = O_bar - S
B_hat = I - O_bar
E_hat = F - O_bar
~~~

so objective error enters all four reconstructed states.

The total trace MSE is:

~~~text
4*MSE(O_bar)
+ sigma_S^2
+ sigma_I^2
+ sigma_F^2
~~~

with the non-objective channel variances frozen to the SIM-039 values.

## Hypothesis

When beta=0, more objective repetitions continue to reduce objective error.

When beta>0, the variance term falls with n while squared bias grows with n.
The result should be a finite optimum followed by worsening error.

~~~text
Variance Reduction != Error Reduction When Bias Accumulates
More Repeats Can Become Worse
~~~

## External-evidence motivation

Published work reports repeat-testing practice effects across cognitive measures,
including memory tests and longitudinal aging cohorts. This justifies a
robustness attack on the iid-unbiased model.

It does **not** justify assigning the synthetic beta values to any real test,
population, disease stage or retest interval.

## Consequence for the research loop

If SIM-043 passes, the previous evidence-allocation result must be interpreted
as conditional on a measurement model:

~~~text
Evidence Allocation
    requires
Measurement-Process Model
~~~

A future external model would need to account for practice effects, correlated
measurement error, alternate forms, retest interval and instrument-specific
properties before repeated objective measurements can be treated as simple
variance reduction.
