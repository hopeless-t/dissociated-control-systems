# CGD-SIM-028 — Controlled calibration step-response

> Status: SYNTHETIC POST-CONVERGENCE PROBE-REDESIGN TEST  
> Clinical authority: NONE

SIM-027 replaced the weak L2 handoff probe with a known-command challenge.
That restored the 0.90 exact-state contract at noise 0.020 and 0.040. At noise
0.080, L2 remained perfect while L1 calibration became the dominant residual
failure.

SIM-028 applies the same systems principle to L1.

A known mismatch is created:

~~~text
trusted reference = 0.45
initial self estimate = 0.95
~~~

The synthetic feedback loop runs for a fixed number of steps. The observation
is the fraction of the original error that remains.

Healthy calibration contracts the known error quickly. L1 calibration failure
contracts it slowly.

The feedback gain is never returned directly as an observation.

## Question

Does a controlled step-response move the high-noise knee again?

If yes, the prior L1 limit was another probe-interface limit. If no, the
remaining uncertainty is more likely to require either more evidence or a
different latent decomposition.

This is an in-silico systems challenge only; it is not a clinical intervention.
