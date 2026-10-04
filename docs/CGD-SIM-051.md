# CGD-SIM-051 — Event-driven context-authority freshness watchdog

> Status: SYNTHETIC WATCHDOG / REVOCATION TEST  
> Clinical authority: NONE

SIM-050 showed that a previously correct context-normalization authority can
become stale immediately after qualification when channel reliability changes.
Requalifying every epoch preserved the frozen regret contract, but at the cost
of a full qualification every epoch.

SIM-051 separates two responsibilities:

~~~text
cheap freshness observation
!=
full evidence-route qualification
~~~

## Watchdog model

A second synthetic context channel observes the same environment state with
independent noise. The watchdog statistic is the RMS disagreement between the
primary context channel and the independent watchdog channel over 64 paired
samples.

~~~text
primary_context = environment + eps_primary
watchdog_context = environment + eps_watchdog
watchdog_score = RMS(primary_context - watchdog_context)
~~~

Frozen parameters:

~~~text
sigma_watchdog = 0.01
change threshold = 0.03
hard maximum authority age = 6 epochs
~~~

The primary channel follows the same adversarial SIM-050 reliability path:

~~~text
0.01 -> 0.08 -> 0.01
~~~

## Authority separation

The watchdog is deliberately not allowed to select `raw_function` or
`context_normalized` itself.

Its only powers are:

1. observe a reliability-regime change;
2. revoke the current authority grant;
3. request the existing SIM-049 full qualification gate.

The full gate alone chooses the new route.

~~~text
Watchdog != Router
Revocation Authority != Routing Authority
~~~

A hard maximum age remains in place so a watchdog that never fires cannot make
an authority grant immortal.

## Compared reference

The principal positive control is SIM-050 `lease1`, which performs a full
qualification every epoch and had zero stale-authority epochs in the frozen
trajectory.

The negative control remains `static_once`.

SIM-051 asks whether event-driven revocation can retain the lease1 regret
contract with fewer full qualifications.

## Metrics

- watchdog checks;
- change-triggered full qualifications;
- hard-expiry qualifications;
- full qualification count;
- stale-authority epochs;
- maximum selection regret;
- qualification reduction versus lease1.

## Hypothesis

For the frozen large reliability shifts, the independent disagreement watchdog
should trigger at degradation and recovery only.

Expected structural outcome:

~~~text
lease1:   10 full qualifications
watchdog:  3 full qualifications
            initial + degradation + recovery
~~~

while keeping zero stale-authority epochs.

## New invariants

~~~text
Freshness Check != Full Requalification
Cheap Independent Change Detection Can Revoke Stale Authority
Watchdog Has Revocation Authority, Not Routing Authority
No Trigger Forever Is Forbidden By Hard Expiry
~~~

## Claim ceiling

The independent watchdog is intentionally idealized. Real channels can share
bias, share sensors, share environment blind spots, drift together or fail in a
correlated way.

Therefore a PASS here would not establish that redundancy alone is sufficient.
The natural next attack is common-mode failure:

~~~text
Primary And Watchdog Agreement != Joint Correctness
~~~
