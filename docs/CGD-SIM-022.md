# CGD-SIM-022 — Causal intervention probes

> Status: SYNTHETIC POST-CONVERGENCE ACTIVE-OBSERVABILITY TEST  
> Clinical authority: NONE

SIM-021 showed that in the combined shifted regime:

- L0 remained recoverable above the 0.90 contract;
- L1, L2, and observer bias did not.

Continuing to reclassify the same corrupted observations would violate the
fixed-point lesson. SIM-022 therefore creates **new evidence** with a paired
intervention.

For a target fault dimension:

~~~text
same fault set
same random seed
same starting assumptions

arm A: no targeted repair
arm B: exactly one targeted repair

probe = paired response difference
~~~

The measured response uses synthetic observable control signals:

- L0: reduction in independent-reference decline;
- L1: reduction in self/reference calibration gap;
- L2: reduction in command/receipt handoff gap;
- observer: reduction in self/reference gap when redundant observation is used.

A small independent measurement noise term is added to the paired contrast.

Thresholds are trained across **all 16 fault subsets**, not merely isolated
single faults, then frozen for held-out seeds.

## Hypothesis

~~~text
Passive Observability Failure
    does not imply
Causal Observability Failure
~~~

This is purely a synthetic systems experiment. It does not recommend medical,
behavioral, or patient-facing diagnostic interventions.
