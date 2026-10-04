# CGD-SIM-052 — Common-mode failure attack on the context watchdog

> Status: SYNTHETIC OBSERVABILITY ATTACK  
> Clinical authority: NONE

SIM-051 showed that an independent disagreement watchdog can revoke stale
context authority at reliability transitions while reducing full
requalification work.

SIM-052 attacks the word **independent**.

## Common-mode construction

Both the primary context channel and watchdog receive the same hidden bias:

~~~text
primary  = environment + B_common + eps_primary
watchdog = environment + B_common + eps_watchdog
~~~

The disagreement statistic becomes:

~~~text
primary - watchdog = eps_primary - eps_watchdog
~~~

The common-mode term cancels exactly. Pairwise agreement therefore contains no
information about `B_common`.

The frozen bias trajectory is:

~~~text
epoch 0:      B_common = 0.00
epoch 1..6:   B_common = +0.08
epoch 7..9:   B_common = 0.00
~~~

Independent per-channel noise remains small at `0.01`.

## Why route quality changes

Context normalization subtracts the primary context estimate from the
functional innovation. A shared bias therefore enters the corrected signal as
an unobserved offset even though the two context channels continue agreeing.

The raw functional route is unaffected by the hidden context bias.

Each epoch still has a full pilot qualification available as a positive
control, so the experiment can distinguish:

~~~text
watchdog failed to request requalification
!=
no better route existed
~~~

## Policies

The attacked policy is the SIM-051 pairwise watchdog with:

~~~text
watchdog delta threshold = 0.03
hard maximum authority age = 6 epochs
~~~

A full every-epoch qualification is retained as the control.

## Frozen hypotheses

- the pairwise watchdog should emit no change trigger when shared bias appears;
- normalization authority should become stale while watchdog disagreement stays
  small;
- hard expiry should eventually bound the persistence of the stale grant but
  should not count as successful detection;
- after common bias disappears, the same pairwise blindness can keep the
  fallback route stale until another explicit qualification;
- every-epoch full qualification should continue following the held-out winner.

## New invariants

~~~text
Primary And Watchdog Agreement != Joint Correctness
Pairwise Disagreement Cannot Identify Shared Bias
Redundancy Without Independence Can Manufacture False Confidence
Hard Expiry Bounds Persistence But Does Not Detect The Failure
~~~

## Claim ceiling

The common bias, channel noise, route model, epoch duration and thresholds are
synthetic. The result is an observability argument about shared-error modes.
It does not estimate the reliability of any real sensor, caregiver report,
digital IADL, environment monitor or clinical assessment.

A PASS here means SIM-051 is correctly limited: pairwise redundancy can help
against independent failures but cannot certify absence of common-mode error.
