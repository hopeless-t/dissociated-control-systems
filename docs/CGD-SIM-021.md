# CGD-SIM-021 — Factorized partial-state recovery

> Status: SYNTHETIC POST-CONVERGENCE GRACEFUL-DEGRADATION TEST  
> Clinical authority: NONE

SIM-019 and SIM-020 could not restore exact 16-state fault classification in
the combined shifted regime, even with substantial verified shifted evidence.

That does not imply that every latent control dimension became unobservable.

SIM-021 changes the recovery target:

~~~text
one 16-class exact-state problem
    ->
four independently validated binary fault dimensions
~~~

The four dimensions are:

- L0 decline;
- L1 calibration;
- L2 handoff;
- observer bias.

Each binary classifier is trained on the same shifted calibration set and
selects its decision threshold using shifted validation only. A dimension is
eligible for partial authority restoration only when validation exact accuracy
is at least 0.90.

Held-out test data audits false restoration.

## Invariant

~~~text
Full-State Recovery != Useful Partial-State Recovery
~~~

A degraded controller should not require an all-or-nothing state estimate if
specific independently validated capabilities remain usable.

Synthetic engineering result only; no clinical authority.
