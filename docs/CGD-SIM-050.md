# CGD-SIM-050 — Context-authority freshness lease

> Status: SYNTHETIC AUTHORITY-FRESHNESS TEST  
> Clinical authority: NONE

SIM-049 established that context normalization should receive authority only
when a pilot qualification demonstrates incremental discrimination over the
raw functional route.

SIM-050 asks the next DCS question:

~~~text
Does a correct authority grant remain correct after the reliability regime changes?
~~~

The answer is not assumed.

## Frozen reliability trajectory

The context channel begins reliable, degrades immediately after its first
qualification, remains degraded for six epochs, and then recovers:

~~~text
epoch 0:      sigma_context = 0.01
epoch 1..6:   sigma_context = 0.08
epoch 7..9:   sigma_context = 0.01
~~~

The immediate post-qualification degradation is intentionally adversarial. It
stress-tests the maximum damage a stale authority grant can do before its next
scheduled requalification.

Each epoch uses the same SIM-049 qualification logic and a disjoint held-out
sample.

## Compared authority lifetimes

~~~text
static_once   qualify only at epoch 0
lease4        requalify every 4 epochs
lease2        requalify every 2 epochs
lease1        requalify every epoch
~~~

No policy is treated as a clinical cadence. `epoch` is only a synthetic time
unit.

## Metrics

For every epoch:

- selected evidence route;
- held-out best route;
- selected AUC;
- best available AUC;
- selection regret;
- whether the held authority is stale.

The frozen per-epoch contract is:

~~~text
selection regret <= 0.02
~~~

The experiment also reports mean regret, maximum regret, stale-authority epochs,
contract-violation epochs and qualification count.

## Hypothesis

A one-time grant should remain incorrectly attached to context normalization
through the degraded phase.

Shorter leases should reduce the time spent holding the wrong route, at the
cost of more qualification work.

A fresh qualification should also be able to restore context authority after
reliability recovers; revocation is not permanent punishment.

## New invariants

~~~text
Qualified Once != Qualified Forever
Authority Has Freshness
Reliability Regime Change Can Invalidate A Previously Correct Route
Expired Qualification -> Requalify Or Fail Back
Revocation != Permanent Disqualification
~~~

## Claim ceiling

The reliability changes, epoch duration, lease lengths, AUC gate and regret
contract are synthetic scenario parameters.

This simulation does not specify how often any real person, caregiver,
instrument, sensor, home context, cognitive test or clinical process should be
reassessed. It only tests the structural requirement that evidence-routing
authority needs a freshness contract when channel reliability can change.
