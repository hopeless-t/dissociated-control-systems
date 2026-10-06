# HF01 Observability Contract

## Question

What probe set is sufficient to distinguish the synthetic HF01 latent state?

This document does **not** claim that a real clinical assay directly measures
the normalized state vector. It formalizes the information problem.

## State

~~~text
x = [A, Q, R, P, N, F, H]
~~~

A single visible hair-output measurement supplies one scalar for seven latent
dimensions.

Therefore a coarse observer is structurally underdetermined.

## Probe ladder result

The executable conceptual measurement matrix in
`hair_follicle_observer.py` gives:

~~~text
visible output only                        rank 1 / 7
Tier 0: output + trichoscopy + cycle       rank 3 / 7
Tier 0 + stress/context                    rank 4 / 7
Tier 0 + context + vascular proxy          rank 5 / 7
declared research probe set                rank 7 / 7
~~~

The numbers depend on the declared synthetic sensitivities; the durable result
is the discipline:

> Do not infer a 7-dimensional biological state from one or two correlated
> observables.

## Interpretation

### What non-invasive longitudinal observation can do

It can detect trajectory changes in the output/cycle space and may support early
warning.

### What it cannot currently do

It cannot uniquely establish:

- local androgen-pathway activity;
- functional progenitor reserve;
- niche integrity;
- mechanical lock.

Those require stronger priors or additional research measurements.

## Consequence for "normal model" feedback

Showing a person a reconstructed healthy cycle can improve understanding and
possibly alter controllable behavior/context variables, but the observer must
keep three layers separate:

~~~text
OBSERVED
INFERRED
UNKNOWN
~~~

A feedback UI must never render an inferred molecular state as a directly
measured fact.

## DCS implication

The first target is not "make the body recognize missing WNT."

The first target is:

~~~text
minimize posterior uncertainty
    before
choosing a control input
~~~

Only after the observer becomes informative enough should HF01 test whether
feedback-guided control changes a downstream trajectory.
