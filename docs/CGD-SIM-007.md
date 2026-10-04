# CGD-SIM-007 — Cost-aware active diagnosis

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

## Question

After CGD-SIM-006, the harness can preserve perishable evidence and schedule
repairs. The next friction is observation itself.

A robust harness should not automatically acquire every possible probe. It
should ask:

> Which observation is worth acquiring next?

## Hypothesis space

The synthetic latent fault set is any of the 16 subsets of:

~~~text
L0 decline
L1 calibration failure
L2 handoff failure
observer bias
~~~

Each candidate probe has a declared symbolic cost:

~~~text
reference_drop          0.40
self_reference_gap      0.20
handoff_gap             0.15
observer_disagreement   0.25
~~~

These costs are not medical costs. They are harness friction units.

## Posterior update

For revealed probe value x_j and hypothesis h:

~~~text
p(h | x_j) proportional to p(x_j | h) p(h)
~~~

Each likelihood is a Gaussian fitted from synthetic known-answer data.

## Probe value

The harness uses a posterior-weighted discriminability score:

~~~text
B_j = sum_h p_h (mu_hj - mu_bar_j)^2
W_j = sum_h p_h sigma_hj^2

V(j | p) = log(1 + B_j / W_j) - alpha * cost_j
~~~

This is a practical signal-to-noise value proxy, not exact mutual information.

The highest-value probe is acquired, the posterior is updated, and the loop
continues until either:

1. posterior confidence crosses the stop threshold; or
2. no remaining probe has positive declared net value.

## Convergence relevance

This changes the optimization target from:

~~~text
maximize diagnostic accuracy
~~~

to:

~~~text
maximize useful diagnostic certainty subject to observation friction
~~~

The next experiment should tune the stop/cost parameters and compare the
best achievable utility against an oracle upper bound. That will provide a
candidate convergence criterion rather than another unbounded meta layer.

## Claim ceiling

This is a synthetic test-selection harness. It does not specify a medical
diagnostic workup or patient-facing test sequence.
