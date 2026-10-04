# CGD-SIM-036 — Standardized current-state challenge

> Status: SYNTHETIC CURRENT-STATE OBSERVABILITY TEST  
> Clinical authority: NONE

SIM-035 established an information ceiling: even perfect knowledge of the
four-fault stratum cannot identify the rare current state with enough positive
predictive value for action authority.

SIM-036 adds a different information channel instead of improving fault
classification again.

## Synthetic challenge

A bounded standardized task is presented for a fixed number of trials.

The observable outputs are:

~~~text
objective task success rate
reported confidence with declared measurement noise
observed discrepancy =
    reported confidence - objective task success rate
~~~

The generator retains latent capability and latent self estimate only for
simulation and truth evaluation. The challenge does not emit them.

## Frozen trial counts

~~~text
8, 16, 32, 64, 128
~~~

This creates an evidence-budget axis analogous to the earlier causal-probe
frontier.

## Policy family

A positive current-state flag requires both:

~~~text
objective performance <= performance ceiling
observed discrepancy >= discrepancy floor
~~~

A frozen grid is evaluated on pilot data.

For each false-positive harm multiplier k, the pilot selects the grid point
maximizing:

~~~text
(TP - k * FP) / N
~~~

subject to at least three pilot true positives.

The selected policy is then evaluated on disjoint held-out seeds.

## Why this tests the original hypothesis

The original CGD framing separates:

~~~text
cause / failure class
from
current functional state
from
self-estimated state
~~~

SIM-036 asks whether standardized objective feedback plus self report can
recover information that cannot exist in the four-fault class label alone.

This is a synthetic observability test, not a cognitive test proposal or a
clinical validation.
