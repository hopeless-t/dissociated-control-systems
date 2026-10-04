# CGD-SIM-044 — Disagreement-trigger informativeness audit

> Status: SYNTHETIC SUFFICIENT-STATISTIC TEST  
> Clinical authority: NONE

The external-observation lane now has a freshness problem: historical objective
anchors become stale when self- and informant-report calibration drifts.

A tempting adaptive policy is:

~~~text
if self/informant disagreement changes sharply:
    reacquire an objective anchor
~~~

SIM-044 tests whether that trigger actually measures the state-estimation error
that matters in the frozen longitudinal model.

## Minimal algebra

Let bias changes since the last objective anchor be:

~~~text
delta_A = self-model / awareness-bias change
delta_B = informant-bias change
~~~

The change in self/informant disagreement is:

~~~text
D = delta_A + delta_B
~~~

The propagated current-state estimation error from averaging dyadic change is:

~~~text
E = (delta_B - delta_A) / 2
~~~

For independent zero-mean drift:

~~~text
Corr(D,E)
  = [Var(delta_B) - Var(delta_A)]
    / [Var(delta_A) + Var(delta_B)]
~~~

Thus, if the two reporter-bias drifts have equal variance:

~~~text
Corr(D,E) = 0
~~~

and because the declared drifts are jointly Gaussian, the signed variables are
independent.

## Monte Carlo audit

The experiment simulates 100,000 drift pairs per scenario and asks whether
`|D|` can identify the top 10% of absolute propagated state errors `|E|`.

Frozen unitless drift scenarios:

~~~text
sigma_A : sigma_B
0.04    : 0.04
0.04    : 0.08
0.04    : 0.16
0.08    : 0.04
~~~

Reported metrics:

- analytic and empirical signed correlation;
- correlation between absolute disagreement and absolute state error;
- AUROC of `|D|` for detecting the top-error state.

## Hypothesis

Under equal drift variance, disagreement should be essentially chance as a
freshness trigger even though disagreement may remain scientifically associated
with cognition or progression in external literature.

Under asymmetric drift variance, signal may emerge because the sum and
difference cease to be orthogonal.

## Research implication

~~~text
Clinically Associated Statistic != Freshness Sensor
Disagreement Signal != State-Estimate Error Signal
~~~

This is a direct recurrence of an earlier DCS lesson:

~~~text
Wrong Sufficient Statistic Can Be The Fault
~~~

An adaptive scheduler therefore cannot be justified merely by choosing an
available discrepancy variable. The trigger itself needs a target-specific
information audit.

## Claim ceiling

The drift variances are synthetic and are not estimates of self-awareness or
study-partner reliability in any population.

The experiment does not invalidate self/informant discrepancy as a research
measure. It tests only whether that discrepancy is a reliable trigger for one
specific state-estimation-error target under one declared model family.
