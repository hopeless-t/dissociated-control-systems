# CGD-SIM-001 — Cognitive Graceful Degradation synthetic simulation

> Status: SYNTHETIC WORKING MODEL  
> Biological interpretation: UNVALIDATED  
> Clinical authority: NONE

## Question

Can the existing DCS distinction between latent capability, expressed
capability, observation, and intervention represent a two-track response to a
progressively degrading latent capability?

The two tracks are:

1. fast-loop compensation: preserve task function through an alternate path;
2. slow-loop modification: change the declared latent capability decline rate.

This is a mathematical control-model experiment, not a treatment model.

## Frozen variables

~~~text
c_t   latent capability
a_t   self-estimated capability
m_t   = a_t - c_t                 metacognitive gap
r_t   compensation strength
p_t   functional performance
d     latent capability decline rate
k     objective-feedback gain
q     fractional decline-rate reduction
lambda compensation cost
~~~

All state-like variables are bounded to [0,1].

## Dynamics

Without a slow-loop intervention:

~~~text
c_(t+1) = c_t - d
a_(t+1) = a_t + k(c_t - a_t)
~~~

Therefore:

~~~text
m_(t+1) = (1-k)m_t + d
~~~

When the trajectory stays away from the [0,1] boundaries and k > 0, the
stationary gap is:

~~~text
m* = d / k
~~~

The synthetic slow-loop arm changes only the declared decline rate:

~~~text
d_eff = d(1-q)
~~~

No biological mechanism is implied by q.

## Fast-loop compensation

Assume:

~~~text
p = c + (1-c)r
J = (1-p)^2 + lambda r^2
~~~

The known-answer optimum is:

~~~text
r* = (1-c)^2 / ((1-c)^2 + lambda)
~~~

This makes the first simulation deterministic and analytically checkable.

## Compensation-induced observability cost

If assisted performance is observed as:

~~~text
p_obs = r + (1-r)c + epsilon
~~~

and inverted to estimate latent capability:

~~~text
c_hat = (p_obs-r)/(1-r)
~~~

then observation-noise variance is amplified by:

~~~text
A_obs = 1/(1-r)^2
~~~

Thus stronger compensation can preserve observable function while making
latent capability harder to infer from that same assisted behavior.

This is a formal observability result under the declared equation, not evidence
about a person's brain.

## Frozen first run

GitHub Actions compares four arms using:

~~~text
steps = 100
initial capability = 1.0
initial self estimate = 1.0
d = 0.005
k = 0.2
lambda = 0.2
q = 0.5 in slow-loop arms
~~~

Arms:

~~~text
baseline
compensation_only
decline_reduction_only
dual_track
~~~

## Acceptance checks

CGD-SIM-001 is useful only if:

1. the metacognitive-gap recurrence approaches the analytic known answer;
2. compensation never decreases functional performance under the frozen model;
3. unassisted observability amplification equals 1;
4. assisted observability amplification exceeds 1 when r > 0;
5. the dual-track arm preserves more mean function and more final latent
   capability than the frozen baseline;
6. invalid inputs fail closed.

## Claim ceiling

A passing Actions run establishes only that the code reproduces consequences of
the frozen equations.

It does not establish:

- that dementia follows these equations;
- that a measured self-report directly equals a_t;
- that any real treatment reduces decline by q;
- that stronger external assistance is always beneficial;
- that functional success proves preserved latent cognition;
- any diagnosis, prognosis, or treatment recommendation.
