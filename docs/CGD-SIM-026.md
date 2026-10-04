# CGD-SIM-026 — Adaptive evidence allocation

> Status: SYNTHETIC POST-CONVERGENCE RESOURCE-ALLOCATION TEST  
> Clinical authority: NONE

SIM-025 used equal repeat budgets across all four fault dimensions. That is a
useful baseline but it can waste evidence on dimensions that are already easy
to classify.

SIM-026 keeps the same causal probe, noise model, likelihood model, and 0.90
exact-state contract. The only change is allocation policy.

For each dimension:

~~~text
acquire evidence
update posterior
if posterior >= 0.99 or <= 0.01:
    stop probing this dimension
else:
    continue until the current hard cap
~~~

Hard caps per dimension:

~~~text
5, 8, 13, 21, 34
~~~

The same evidence trace is reused across caps so the frontier measures budget
effects rather than different random draws.

## Question

Can the apparent failure at noise >= 0.020 be explained by equal-allocation
waste, or does it persist after adaptive allocation?

## Decision rule

If a large adaptive cap still cannot reach the 0.90 exact-state contract, the
next iteration should redesign the probe channel rather than continue blind
repetition.

Synthetic engineering result only; no clinical authority.
