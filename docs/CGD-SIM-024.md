# CGD-SIM-024 — Causal-observability noise knee

> Status: SYNTHETIC POST-CONVERGENCE PRESSURE-KNEE TEST  
> Clinical authority: NONE

SIM-022 showed that paired causal probes can recover fault observability.
SIM-023 showed that sequential stopping reduces intervention count.

SIM-024 asks where this advantage breaks as the measurement channel becomes
noisier.

The same paired causal signals are evaluated under measurement-noise standard
deviations:

~~~text
0.0025, 0.005, 0.010, 0.020, 0.040, 0.080
~~~

At every noise level, the present/absent likelihood models are calibrated at
that same declared noise level. This isolates channel noise from model mismatch.

Three policies are compared:

1. one probe per fault dimension: exactly 4 total probes;
2. sequential likelihood-ratio stopping: 1–5 probes per dimension;
3. fixed five repeats per dimension: exactly 20 total probes.

The pressure knee is the first noise level where exact 16-state accuracy drops
below 0.90.

## Hypothesis

~~~text
Evidence Repetition Can Shift An Information Knee
    but
Evidence Repetition Cannot Remove The Knee
~~~

This provides a finite-RAM-style pressure frontier for causal observability.

Synthetic engineering result only; no clinical authority.
