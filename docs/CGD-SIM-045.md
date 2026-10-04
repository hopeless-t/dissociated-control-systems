# CGD-SIM-045 — Independent functional-sentinel trigger frontier

> Status: SYNTHETIC INDEPENDENT-OBSERVATION TEST  
> Clinical authority: NONE

SIM-044 showed that self/informant disagreement change can be nearly useless as
a freshness trigger when self- and informant-bias drift are symmetric.

SIM-045 therefore tests a different architecture: add an independent current
function channel and trigger objective re-observation from its innovation.

## Synthetic sentinel

Let the propagated state estimate be wrong by `E`:

~~~text
predicted state = true current state + E
~~~

An independent function sentinel observes:

~~~text
sentinel = true current state + N
~~~

where `N` aggregates synthetic environment/scaffold variation and measurement
noise.

The available innovation is:

~~~text
sentinel - prediction = N - E
~~~

and the trigger score is its absolute magnitude.

## Target

The binary target is the top 10% of absolute propagated state errors under the
same equal-drift world used in SIM-044.

The baseline comparator is absolute self/informant disagreement change, which
should remain near chance.

## Nuisance pressure frontier

Frozen unitless sentinel nuisance standard deviations:

~~~text
0.00, 0.01, 0.02, 0.04, 0.08, 0.16
~~~

For each level the experiment reports AUROC for detecting the high-error state.
The first frozen nuisance level below AUROC 0.70 is reported as a pressure knee.

## External-evidence motivation

Performance-based measures of everyday function can provide information not
captured by self or collateral questionnaires alone. Published work has used
objective tasks involving medication management, financial skills and other
instrumental activities; more recent work also evaluates performance-based
functional measures in prodromal dementia research.

Digital IADL research offers another possible independent channel, including
ambient sensors and mobile/wearable observations, but systematic reviews report
substantial metric heterogeneity and limited longitudinal validation.

Therefore SIM-045 does not equate "digital" or "performance-based" with ground
truth.

~~~text
Independent Channel != Truth
Functional Sentinel != Disease Biomarker
~~~

## Hypothesis

A genuinely independent, sufficiently low-noise function channel should recover
freshness-trigger information that cannot exist in dyadic disagreement under
the symmetric-drift model.

As environment and measurement nuisance increase, that advantage should
collapse toward chance.

## Claim ceiling

No real IADL instrument, sensor or digital endpoint is assigned the synthetic
noise values or resulting AUROC values.

The experiment tests an observation architecture only:

~~~text
non-identifying dyad
    -> add independent function innovation
    -> audit its own pressure/noise frontier
    -> only then consider adaptive re-observation
~~~
