# CGD-SIM-046 — Selective adaptive objective re-anchor

> Status: SYNTHETIC SELECTIVE-OBSERVATION SCHEDULER  
> Clinical authority: NONE

SIM-041 established a simple age-only freshness boundary. SIM-044 showed that
self/informant disagreement is not generally a valid trigger for propagated
state-estimation error. SIM-045 showed that a sufficiently low-noise independent
functional innovation can recover trigger observability.

SIM-046 composes those findings into a scheduler.

## Selective contract

The scheduler is **not** allowed to reinterpret a stale dyadic estimate as
fresh merely because objective measurement is expensive.

Instead, extending beyond the simple age-only interval requires a current,
independent sentinel observation.

~~~text
historical objective anchor
    + self/informant change propagation
    + current independent functional sentinel
    -> accept propagated estimate OR reacquire objective anchor
~~~

A hard maximum anchor age of 16 visits remains in the synthetic scheduler.

## Frozen unitless dynamics

~~~text
state random-walk std / visit        = 0.03
self-bias drift std / visit          = 0.04
informant-bias drift std / visit     = 0.04
self measurement noise std           = 0.05
informant measurement noise std      = 0.05
objective-anchor noise std           = 0.03
functional-sentinel nuisance std     = 0.02 or 0.04
~~~

Synthetic objective-anchor cost:

~~~text
0.08
~~~

The values are engineering scenarios, not empirical cognitive-test or IADL
parameters.

## Policies

### fixed8

Reacquire objective state every eight visits.

### fixed16

Reacquire every sixteen visits. This is a deliberately stale-prone comparator.

### sentinel adaptive

Before the hard maximum age, reacquire when:

~~~text
|functional sentinel - propagated state estimate| >= threshold
~~~

### dyad adaptive

Matched adaptive comparator using:

~~~text
|current self/informant discrepancy
 - anchor self/informant discrepancy| >= threshold
~~~

SIM-044 predicts that this statistic is weak in the equal-drift world.

## Pilot / held-out separation

For each sentinel nuisance level:

1. generate frozen pilot trajectories;
2. sweep the same threshold grid for sentinel and dyad trigger families;
3. reject threshold policies whose **accepted stale estimates** have RMSE above
   0.085;
4. among survivors minimize:

~~~text
post-policy MSE + 0.08 * objective-anchor rate
~~~

5. freeze the selected threshold;
6. evaluate on disjoint held-out trajectories.

## Why accepted-stale RMSE is reported separately

An objective reacquisition visit has direct new evidence. The selective contract
therefore audits the visits where the scheduler chooses **not** to reacquire.

~~~text
accepted-stale RMSE
    = RMSE of propagated estimates the scheduler actually accepts
~~~

This distinguishes selective evidence quality from overall average error.

## Additional diagnostics

The experiment also reports:

- objective-anchor rate;
- stale-estimate coverage;
- fraction of adaptive triggers fired when pre-anchor absolute error was at or
  below a frozen 0.10 reference;
- synthetic total loss;
- gain versus fixed8 and matched dyad triggering.

The 0.10 reference is diagnostic only and is not a clinical safety threshold.

## Claim ceiling

A successful sentinel scheduler establishes only a synthetic architecture:

~~~text
independent current observation
    can conditionally extend historical evidence
~~~

It does not establish that any real performance-based IADL, sensor, digital
endpoint or cognitive task is sufficiently reliable to serve this role.

Real translation requires instrument-specific validity, longitudinal
reliability, environment/scaffold modeling, burden, practice-effect analysis,
rights/governance and risk/coverage evaluation.
