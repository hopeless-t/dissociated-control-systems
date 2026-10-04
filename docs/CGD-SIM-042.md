# CGD-SIM-042 — Objective-anchor reacquisition scheduler

> Status: SYNTHETIC FRESHNESS / COST SCHEDULING TEST  
> Clinical authority: NONE

SIM-041 showed that, under one frozen longitudinal drift scenario, a historical
objective anchor eventually becomes too stale for the declared state-estimation
RMSE contract.

SIM-042 asks a different question:

> If independent objective re-observation has a cost, what interval minimizes
> estimation loss, and what happens when that unconstrained optimum violates the
> freshness contract?

## Frozen model

The observation and drift parameters are inherited from SIM-041:

~~~text
objective-anchor noise std          = 0.03
self measurement noise std          = 0.05
informant measurement noise std     = 0.05
self-bias drift std / visit         = 0.04
informant-bias drift std / visit    = 0.04
freshness RMSE contract             = 0.10
~~~

These are synthetic unitless scenario values, not empirical estimates.

## Periodic anchor schedule

For an objective-anchor interval `k`, the evidence age cycles through:

~~~text
0, 1, ..., k-1 visits
~~~

At age zero, current state is observed directly through the noisy objective
anchor. At positive age, the state estimate is propagated with the self and
informant change channels from SIM-041.

For every candidate interval the experiment computes:

- average state-estimation variance over the cycle;
- worst RMSE before the next anchor;
- anchor acquisition rate;
- whether the entire cycle remains inside the freshness contract.

Candidate intervals:

~~~text
1, 2, 4, 8, 16, 32, 64 visits
~~~

## Synthetic cost objective

For scenario anchor cost `c`:

~~~text
loss(k, c)
    = mean_state_variance(k)
      + c / k
~~~

Cost scenarios:

~~~text
0.001, 0.005, 0.010, 0.020, 0.040, 0.080, 0.160
~~~

The experiment reports two optima:

1. **unconstrained optimum** — minimum synthetic loss regardless of freshness;
2. **contract-constrained optimum** — minimum loss among intervals whose worst
   RMSE remains at or below 0.10.

## Hypothesis

At sufficiently high measurement cost, the unconstrained optimizer should
prefer a longer interval even after the evidence has become stale under the
frozen contract.

The contract must refuse that choice rather than reinterpret cost savings as
permission to use stale evidence.

~~~text
Cost Optimum != Safety-Admissible Optimum
Re-observation Cost != Retry / Staleness Permission
~~~

## DCS relationship

This imports the same separation used elsewhere in DCS/MVCA:

~~~text
optimization preference
    !=
authority
~~~

A scheduler may prefer an action economically while the evidence contract still
forbids it.

## Claim ceiling

This simulation does not produce:

- a human retest interval;
- a dementia-monitoring schedule;
- a recommendation for cognitive assessment frequency;
- a clinical safety threshold.

Real scheduling would require domain-local estimates of instrument reliability,
practice effects, reporter drift, disease/state dynamics, burden and risk.
