# CGD-SIM-033 — External Observation Lane Qualification

> Status: EVIDENCE-GOVERNANCE CONTRACT  
> Clinical authority: NONE  
> Real human data ingested: NONE

The post-convergence stopping rule says that further progress must eventually
come from external/domain-local evidence rather than stronger synthetic oracle
probes.

SIM-033 defines the gate **before** any human dataset is selected.

## Decisions

~~~text
ADMIT_OBSERVATIONAL_LANE
ADMIT_METHOD_ONLY
DEFER_REVALIDATE
REJECT_CANONICAL_EVIDENCE
~~~

### ADMIT_OBSERVATIONAL_LANE

Means only:

> this source shape is eligible to participate in a bounded DCS observational
> validation protocol.

It does **not** mean a clinical claim is established.

### ADMIT_METHOD_ONLY

A high-quality engineering/synthetic source can transfer methodology while
remaining ineligible to support a cognitive-domain empirical claim.

This is the formal destination for Finite RAM Lab, MVCA, Jev/Cua, Harness
Economics, and other cross-domain research unless domain-local evidence exists.

## Required bindings

~~~text
source identity or captured snapshot
provenance
measurement definition
population scope
freshness / revision
missingness semantics
deidentification or aggregation for human data
public or otherwise authorized access
claim scope
~~~

Unbound mutable web material is DEFER, not silently treated as current fact.

Anecdotal-only material and identifiable unauthorized human records are not
canonical evidence.

DCS-generated human intervention/challenge data are rejected by this lane; this
repository does not gain human-experiment authority by writing a protocol.

## Cross-research lineage

The contract composes:

- Jev/Cua external-material binding and freshness;
- Harness Component Economics UNKNOWN/provenance semantics;
- Memory Attention claim partitioning;
- Finite RAM hosted-evidence authority boundaries;
- DCS's existing analogy != mechanism rule.

## Compact boundary

~~~text
Engineering Reproducibility != Cognitive External Validity
Observational Admission != Treatment Authority
Synthetic Accuracy != Clinical Validity
~~~
