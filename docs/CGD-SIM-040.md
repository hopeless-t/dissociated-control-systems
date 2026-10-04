# CGD-SIM-040 — Four-channel evidence allocation

> Status: SYNTHETIC EVIDENCE-BUDGET OPTIMIZATION  
> Clinical authority: NONE

SIM-039 showed a measurement knee: after enough objective repetitions, the
remaining error is dominated by self-report, informant-report and
function-channel noise.

SIM-040 asks how a fixed total observation budget should be distributed across
all four channels in the same frozen unitless model.

## Loss

For averaged observations:

~~~text
Var(Z_hat) = sigma_O^2 / n_O
Var(A_hat) = sigma_O^2 / n_O + sigma_S^2 / n_S
Var(B_hat) = sigma_O^2 / n_O + sigma_I^2 / n_I
Var(E_hat) = sigma_O^2 / n_O + sigma_F^2 / n_F
~~~

The total state-estimation MSE trace is:

~~~text
L = 4*sigma_O^2/n_O
    + sigma_S^2/n_S
    + sigma_I^2/n_I
    + sigma_F^2/n_F
~~~

with every channel receiving at least one observation.

## Continuous optimum

Minimizing `sum c_j/n_j` under a fixed total budget gives:

~~~text
n_j proportional to sqrt(c_j)
~~~

Under the SIM-039 scenario:

~~~text
sigma_O = 0.20
sigma_S = sigma_I = sigma_F = 0.10
~~~

so the analytic ratio is:

~~~text
objective : self : informant : function
    4     :  1   :    1      :   1
~~~

## Exact integer validation

For total budgets:

~~~text
7, 14, 28, 56, 112
~~~

every positive integer allocation is exhaustively enumerated. The analytic
4:1:1:1 candidate is compared with:

- the exact exhaustive optimum;
- approximately equal allocation;
- an objective-pressure policy that leaves only one observation for every
  other channel.

## Interpretation boundary

The optimum is conditional on the frozen synthetic variances, independence,
equal per-observation cost and linear estimator.

It does not imply that a real assessment battery should use four objective
measures for every self/informant/function measure. Real instruments have
unequal burden, correlated error, systematic bias, fatigue, practice effects,
missingness and scale differences.

The structural lesson is narrower:

~~~text
More Measurement != Better Allocation
Evidence Budget Should Follow Marginal Information Value
~~~

A future externally validated model would need empirically estimated channel
error/cost structures before any allocation policy could be proposed.
