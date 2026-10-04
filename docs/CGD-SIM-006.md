# CGD-SIM-006 — Diagnostic-window preserving repair scheduler

> Status: SYNTHETIC WORKING MODEL  
> Clinical authority: NONE

## Failure discovered by CGD-SIM-005

The active probe / repair / re-observe loop recovered two simultaneous faults
well, but a three-fault stress exposed a new harness failure.

A fault can be observable early and become unobservable later.

For the synthetic L0 decline fault, delaying repair while other components are
handled can drive latent capability to a boundary. Once the trajectory
saturates, the independent-reference drop signal shrinks and the original L0
fault can disappear from the current observation even though its causal effect
has already occurred.

This is a diagnostic-window problem:

~~~text
fault exists
  -> signature becomes observable
  -> repair scheduler defers it
  -> state saturates / trajectory changes
  -> signature disappears
  -> current-state-only harness forgets the evidence
~~~

## Meta improvement

Do not add another recursive reasoning layer.

Instead, preserve bounded evidence for a fault whose signature is known to be
perishable:

~~~text
m_L0(t+1) = m_L0(t) OR detected_L0(t)
~~~

The scheduler then uses:

1. current observer-bias evidence;
2. latched L0 evidence;
3. current L2 handoff evidence;
4. current L1 calibration evidence.

After each repair the system is re-observed. Only L0 evidence is latched in
this experiment; this avoids turning all transient anomalies into permanent
repair requests.

## Research implication

The harness now distinguishes:

~~~text
current state != complete causal history
~~~

and therefore:

~~~text
Re-observation != permission to discard earlier valid evidence
~~~

This mirrors the broader DCS/MVCA idea that durable state may be necessary
when transient transport or observation state can no longer reconstruct what
already happened.

## Claim ceiling

The scheduler is a synthetic fault-tolerance result. It does not define a
medical intervention order, a clinical diagnosis protocol, or a biological
model.
