# CGD-SIM-027 — Controlled-input handoff challenge

> Status: SYNTHETIC POST-CONVERGENCE PROBE-REDESIGN TEST  
> Clinical authority: NONE

SIM-026 localized the high-noise failure. At noise 0.020 and a large adaptive
cap, L0, L1, and observer dimensions remained highly recoverable while L2
handoff accuracy stayed below the contract.

The previous L2 causal probe still depended on naturally occurring desired
compensation. That makes signal strength state-dependent.

SIM-027 adds a new bounded diagnostic interface:

~~~text
known unit command
    -> handoff channel
    -> observable receipt

paired arm:
known unit command
    -> redundant-handoff repair
    -> observable receipt

probe = repaired receipt - baseline receipt
~~~

The probe uses eight synthetic challenge pulses and never reads the latent
handoff reliability as an observation. It creates a controlled input and
measures the output response.

All other fault probes are unchanged.

## Question

Was the SIM-026 knee caused by an intrinsic information limit, or by a weak L2
probe whose input amplitude depended on the degraded controller state?

A moved knee supports the latter.

This is an in-silico systems probe. It is not a medical or patient-facing
intervention proposal.
