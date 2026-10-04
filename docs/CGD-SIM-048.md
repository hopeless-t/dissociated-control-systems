# CGD-SIM-048 — Context-bound adaptive re-anchor

> Status: SYNTHETIC LONGITUDINAL CONTEXT-BINDING TEST  
> Clinical authority: NONE

SIM-046 showed that a low-noise independent functional sentinel can selectively
extend historical objective evidence while preserving an accepted-stale RMSE
contract.

SIM-047 showed a confounding failure: functional change can come from
`environment/scaffold` rather than from the current cognitive/functional state
being estimated.

SIM-048 combines those results in a longitudinal scheduler.

## Environment state

The synthetic environment is piecewise persistent.

At each visit an event occurs with frozen probability:

~~~text
0%, 2%, 5%, 10%
~~~

When an event occurs, environment/scaffold state jumps to either `+0.12` or
`-0.12` and remains there until another event changes it.

The functional observation is:

~~~text
F(t) = Z(t) + E(t) + eps_F
~~~

and an independent context channel is:

~~~text
C(t) = E(t) + eps_C
~~~

with frozen unitless scenario noise:

~~~text
sigma_F = 0.02
sigma_C = 0.01
~~~

These are not empirical IADL or home-context estimates.

## Compared policies

### fixed8 / fixed16

Age-only objective reacquisition baselines from the earlier freshness work.

### raw functional adaptive

~~~text
score_raw = |F(t) - propagated_Z_hat(t)|
~~~

This score sees current-state error and environment/scaffold change together.

### context-normalized adaptive

~~~text
score_context = |F(t) - C(t) - propagated_Z_hat(t)|
~~~

The context channel is noisy and therefore does not reveal environment state
perfectly.

## Pilot / held-out contract

For raw and normalized trigger families independently:

1. sweep a frozen threshold grid on pilot trajectories;
2. reject any threshold whose accepted-stale RMSE exceeds 0.085;
3. among surviving thresholds minimize:

~~~text
post-policy state MSE + 0.08*objective-anchor rate
~~~

4. freeze the selected threshold;
5. evaluate it on disjoint held-out trajectories.

Reported diagnostics include:

- overall RMSE;
- accepted-stale RMSE and coverage;
- objective-anchor rate;
- low-state-error trigger fraction;
- fraction of adaptive triggers occurring while environment state is shifted;
- synthetic total loss.

## Hypothesis

As persistent environment/scaffold shifts become more common, the raw
functional trigger should repeatedly reacquire objective state even when the
cognitive-state estimate itself is acceptable.

Context normalization should preserve more of the SIM-046 selective-scheduling
benefit.

~~~text
Functional Change != Cognitive-State Change
Observation Context Is Part Of Evidence Identity
Context-Bound Observation > Unbound Observation Under Confounding
~~~

## Claim ceiling

The simulation does not establish that a real functional task, digital IADL,
sensor, caregiver context measure or support-state variable can remove
confounding this cleanly.

Real translation would require empirical validation of both the functional
measurement and the context representation. The context channel can itself be
biased, incomplete or stale and therefore requires its own evidence contract.
