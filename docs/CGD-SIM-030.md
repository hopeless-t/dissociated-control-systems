# CGD-SIM-030 — Durable probe transaction

> Status: SYNTHETIC CONTROL / RECOVERY TEST  
> Clinical authority: NONE

SIM-029 defines whether a probe is qualified for the synthetic research lane.
SIM-030 defines what happens once a qualified probe is actually attempted.

The model imports two adjacent research patterns:

- Finite RAM Lab: accepted-result correctness and
  predict -> normalize -> verify -> execute -> commit;
- MVCA: stable operation identity, Attempt != Operation,
  Re-observation != Re-execution, UNKNOWN != retry permission.

## Probe transaction

~~~text
probe_operation_id
    stable across delivery/reobservation attempts

probe_attempt_id
    one physical attempt to deliver or observe the operation
~~~

The synthetic ledger distinguishes:

~~~text
CREATED
ADMITTED
STATE_VERIFIED
DISPATCHED
OBSERVED
ACCEPTED
DEFER
INVALIDATED
UNKNOWN
~~~

Only ACCEPTED is allowed to carry a positive or negative diagnostic result.

Therefore:

~~~text
INVALIDATED != negative
missing measurement != negative
transport ambiguity != negative
transport ambiguity != permission to replay the probe
~~~

## Fault injections

The frozen scenarios include:

- stale evidence before dispatch;
- state invalidation during the probe;
- missing measurement;
- response loss after dispatch but before durable receipt;
- response loss after durable commit;
- duplicate physical delivery attempts;
- unqualified probe.

The transaction contract is compared against a naive retry baseline for
response-loss cases.

## Success objective

The primary engineering target is:

~~~text
P(result correct | transaction emits ACCEPTED)
~~~

not:

~~~text
P(first attempt always completes)
~~~

A fail-closed INVALIDATED/DEFER/UNKNOWN outcome is preferable to emitting a
diagnostic conclusion from an unverified transaction.

This remains a synthetic control-model result and grants no external execution
or clinical authority.
