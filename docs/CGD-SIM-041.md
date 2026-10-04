# CGD-SIM-041 — Longitudinal observation freshness

> Status: SYNTHETIC LONGITUDINAL DRIFT TEST  
> Clinical authority: NONE

Public awareness/informant literature motivates a temporal warning for the CGD
external-observation lane: reporter calibration and reporting context should not
be assumed stationary forever.

SIM-041 therefore imports the DCS/Jev-Cua freshness rule into the four-channel
cognitive observation model.

## Question

After an objective state anchor is collected, how long can self/informant
change be used to propagate the current-state estimate if self-model bias and
informant bias drift over time?

## Synthetic model

At the anchor visit:

~~~text
O(0) = Z(0) + objective noise
~~~

Between anchors:

~~~text
S(t) = Z(t) - A(t) + self measurement noise
I(t) = Z(t) + B(t) + informant measurement noise
~~~

where A and B follow independent random walks in the frozen scenario.

The propagated estimate is:

~~~text
Z_hat(h) = O(0)
           + 0.5 * [(S(h)-S(0)) + (I(h)-I(0))]
~~~

The true Z trajectory itself is allowed to change. The estimation error comes
from anchor noise, endpoint measurement noise and accumulated reporter-bias
drift.

## Frozen unitless scenario

~~~text
self measurement noise std          = 0.05
informant measurement noise std     = 0.05
self-bias drift std / visit         = 0.04
informant-bias drift std / visit    = 0.04
objective-anchor noise std          = 0.03
state-estimate RMSE contract        = 0.10
~~~

These are engineering scenario values, not empirical estimates of any clinical
instrument or human population.

## Freshness lease

The experiment evaluates anchor ages:

~~~text
1, 2, 4, 8, 16, 32 visits
~~~

and defines a synthetic freshness lease as the last tested horizon whose
analytic state-estimate RMSE remains under the frozen 0.10 contract.

A deterministic 50,000-sample Monte Carlo run cross-checks the analytic error
formula.

## Interpretation

The intended result is not a recommended retest interval.

The structural lesson is:

~~~text
Historical Calibration != Current Calibration
Historical Objective Anchor != Permanent Ground Truth
Freshness Must Be Bound To Evidence
~~~

This matters because a longitudinal discrepancy model can otherwise treat an
old objective assessment as eternally current while self/informant observation
bias changes around it.

## External-evidence connection

Published MCI/AD studies report that self/informant discrepancy has longitudinal
associations with cognitive decline and biomarkers, while NACC work shows that
study-partner characteristics can affect informant-report properties.

Those findings justify testing nonstationarity. They do not calibrate the
synthetic drift parameters in SIM-041.

## Next step

If the freshness model behaves as expected, the next allocation problem is not
only **which channel** to measure, but **when to reacquire an independent
objective anchor**.

That creates a sequential scheduling problem with three costs:

- stale-evidence risk;
- measurement burden;
- missed state change.
