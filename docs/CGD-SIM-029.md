# CGD-SIM-029 — Probe-admission contract

> Status: SYNTHETIC GOVERNANCE / BOUNDARY TEST  
> Clinical authority: NONE

SIM-027 and SIM-028 showed that controlled diagnostic challenges can move a
synthetic observability knee dramatically.

That creates a new failure mode:

> If the loop is rewarded only for diagnostic accuracy, it can keep inventing
> stronger probes until the probe leaks the answer or exceeds the intended
> intervention boundary.

SIM-029 changes the objective from maximum accuracy to useful information under
a frozen admission contract.

## Required separations

~~~text
Diagnostic Accuracy != Probe Admission
Probe Qualification != Execution Authority
Synthetic Admission != Human / Clinical Authorization
Historical Evidence != Current Qualified Evidence
Missing Observation != Mean Observation
Mismatch Localization != Root Cause Proof
~~~

A synthetic interventional probe must bind a known input, paired/isometric
control, bounded perturbation, reversible synthetic effect, observable output,
measurement provenance, environment identity, freshness, missingness semantics,
risk/coverage semantics, and explicit authority separation.

Direct latent-state access is rejected even when accuracy is perfect.

All interventional candidates remain external-HOLD. Any real-world translation
would require independent domain evidence, ethics/governance, and explicit
human authorization.

## Cross-research lineage

The contract borrows research-control patterns from Finite RAM Lab, Finite Tool
Surface Lab, Harness Component Economics, Jev/Cua Lab, MVCA, and Memory
Attention Lab. It does not infer shared physical mechanisms from those
engineering analogies.
