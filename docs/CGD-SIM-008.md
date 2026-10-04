# CGD-SIM-008 — Information frontier and local convergence

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

## Why this experiment exists

An unbounded self-improvement loop needs a stopping rule.

"Perfect accuracy" is the wrong reference because the observation model itself
contains overlap and noise. A fair ceiling is therefore:

~~~text
accuracy when all four available probes are observed
~~~

No policy using only the same four probes can obtain more raw observational
information than that ceiling.

## Candidate generations

The experiment compares:

1. all probes;
2. optimized SNR-value adaptive selection;
3. optimized entropy-value adaptive selection.

Both adaptive families grid-search:

~~~text
confidence threshold in {0.65, 0.75, 0.85, 0.90, 0.95, 0.98}
cost weight          in {0.0, 0.2, 0.5, 1.0, 2.0}
~~~

Optimization occurs on a separate validation seed range and is then frozen for
the held-out test range.

## Utility

~~~text
U = 0.70 * exact_recovery
  + 0.30 * repair_coverage
  - 0.20 * extra_repairs
  - 0.12 * probe_cost
~~~

The coefficients are declared synthetic trade-off weights.

## Local convergence criterion

The current policy family is locally saturated if both conditions hold:

~~~text
abs(U_new - U_previous) < 0.005
all_probe_accuracy - best_adaptive_accuracy < 0.015
~~~

This does not claim a global optimum.

It means only that:

- a materially different next-probe selector no longer buys meaningful utility;
- the adaptive policy is already close to the information ceiling exposed by
  the current observation architecture.

If the criterion fails, the next improvement should change the observation
architecture, hypothesis representation, or temporal model rather than add a
gratuitous meta layer.

## Claim ceiling

Synthetic convergence only. No clinical diagnostic limit, medical stopping
rule, or biological optimum is claimed.
