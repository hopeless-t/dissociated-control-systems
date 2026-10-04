# CGD-OBS-003 — Preregistered Observational Analysis Contract

> Status: ANALYSIS FREEZE CANDIDATE  
> Human participant rows processed: NONE  
> Clinical authority: NONE

OBS-002 froze the signed observation variables. OBS-003 freezes the primary
analysis and negative controls before any authorized participant-level dataset
is inspected.

## Primary endpoint

~~~text
rho_primary = Spearman(D_SI, objective impairment)
~~~

Primary direction:

~~~text
rho_primary > 0
~~~

Higher positive self/informant discrepancy means the self channel reports less
impairment than the informant channel. The preregistered observational
hypothesis is that this direction should be associated with greater objective
impairment.

If a valid analysis instead gives a robust negative association, the result is
INCONSISTENT with the frozen projection. It must not be rescued after the fact
by switching to absolute discrepancy.

## Negative control

Break the dyadic relationship while preserving declared stratification:

~~~text
permute informant observations across participants
within frozen stratum / visit constraints
~~~

The exact permutation seed/count belongs to a later executable dataset
protocol, but the control family is frozen here.

The primary observed association must exceed the shuffled association
distribution at the declared operating point.

## Missingness

No complete-case result is interpreted without reporting:

~~~text
self channel coverage
informant channel coverage
objective channel coverage
complete-triad coverage
longitudinal-pair coverage
coverage by frozen population/group/time strata
~~~

Low coverage may make the result INCONCLUSIVE even when an effect estimate is
large.

## Secondary domains

Memory, executive, language, visuospatial, and other compatible instrument
domains are secondary unless a source-specific protocol freezes another primary
domain before access.

Secondary multiplicity is controlled using a preregistered FDR procedure.

## Longitudinal endpoint

~~~text
rho_longitudinal =
    Spearman(slope(D_SI), slope(objective impairment))
~~~

Cross-sectional and longitudinal findings remain separate claims.

## Decision vocabulary

~~~text
CONSISTENT
INCONSISTENT
INCONCLUSIVE
~~~

No p-value alone promotes a DCS mechanism claim.

## Falsification discipline

The DCS observational projection is weakened when:

- the primary signed effect is reliably opposite to the frozen direction;
- dyad permutation preserves the apparent effect;
- the association disappears under a preregistered compatible normalization;
- channel missingness is too severe to support the intended population claim;
- longitudinal discrepancy does not track longitudinal objective change when
  that endpoint has adequate coverage.

These outcomes are not harness failures. They are legitimate scientific
results.

## Claim ceiling

Even a CONSISTENT result means only:

> the frozen observational projection is consistent with the tested data under
> the frozen protocol.

It does not establish that the synthetic DCS L1 state is a biological
mechanism, and it does not establish diagnosis, prognosis, or treatment
authority.
