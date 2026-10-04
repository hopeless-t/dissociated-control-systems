# CGD-SIM-037 — Causal screen to current-state challenge cascade

> Status: SYNTHETIC TWO-STAGE OBSERVABILITY TEST  
> Clinical authority: NONE

SIM-035 showed that cause-class knowledge is insufficient for current rare-state
identification.

SIM-036 showed that a standardized objective challenge plus self report adds
within-stratum information but remains weak when applied directly to the whole
population.

SIM-037 composes them without collapsing their roles:

~~~text
Stage 1:
    bounded causal fault probe
    -> cheap candidate screen

Stage 2:
    standardized objective task
    + noisy self report
    -> current-state verification

Only Stage 1 positives pay the expensive Stage 2 challenge cost.
~~~

The current-state thresholds are selected on pilot data separately for the
one-stage and two-stage policies, then evaluated on disjoint held-out seeds.

## Key measurements

- rare-state sensitivity;
- specificity;
- PPV;
- positive-action expected margin for declared harm multiplier k;
- fraction of the population receiving the expensive current-state challenge.

## Boundary

This is a synthetic harness architecture experiment.

A positive synthetic expected margin would mean only that the staged
information architecture improved the declared simulated loss function. It
would not create clinical validity or authority.
