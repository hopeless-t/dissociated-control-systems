# CGD-SIM-015 — OOD detection and authority routing

> Status: SYNTHETIC POST-CONVERGENCE CONTROL TEST  
> Clinical authority: NONE

SIM-014 showed that the clean-world fixed point can fail catastrophically when
the observation world shifts.

The next question is not initially:

> Can the same classifier be made omniscient?

It is:

> Can the harness notice that its world model no longer applies and stop
> treating an ordinary prediction as authorized execution?

## Detector

The detector is deliberately trained on **clean data only**.

For each base probe:

~~~text
z_j = abs(x_j - mean_clean_j) / std_clean_j
OOD score = max_j z_j
~~~

The threshold is selected from a high quantile of clean validation scores.

Explicit missingness is treated separately:

~~~text
Missing Observation != Observation At Mean
~~~

If a probe is missing, mean imputation may still be used by the frozen
classifier, but the authority layer retains a missingness marker and considers
the case out-of-distribution.

## Authority gate

~~~text
if OOD score <= threshold:
    normal classifier authority may continue
else:
    normal-path execution is not authorized
    route to external evidence / review / recalibration
~~~

The experiment reports:

- forced accuracy if the old model is always used;
- OOD flag rate;
- remaining execution coverage;
- accuracy on the accepted subset;
- total-rate of wrong decisions that still escaped the gate.

The gate is declared effective if:

~~~text
clean false-alarm rate < 0.03
and
combined-shift executed-error exposure reduction > 0.50
~~~

This does not claim that abstention solves the underlying problem. It tests
whether a failing world model can degrade explicitly instead of silently.

Synthetic engineering result only; no clinical authority.
