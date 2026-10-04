# CGD-SIM-016 — Window-level regime-shift detection

> Status: SYNTHETIC POST-CONVERGENCE CONTROL TEST  
> Clinical authority: NONE

SIM-015 exposed a precise weakness:

- explicit missingness was easy to route away from normal authority;
- common-mode bias and variance inflation could destroy classifier accuracy
  while individual observations still looked locally plausible.

That means per-sample OOD detection is insufficient.

## New invariant

~~~text
Plausible Individual Observation != Stable Population Regime
~~~

SIM-016 therefore monitors windows of observations instead of only individual
samples.

For each clean-calibrated window it measures:

- feature-mean drift, scaled by the sampling error of the mean;
- feature-variance drift;
- selected cross-feature correlation drift;
- explicit missingness.

The threshold is calibrated only from independent clean windows.

If a whole window is out-of-regime, normal execution authority is lowered for
that window and the system requests new evidence/recalibration.

The gate is considered effective when:

~~~text
clean window false-alarm rate < 0.05
and
minimum error-exposure reduction across
  {common-mode bias, noise inflation, combined shift}
> 0.50
~~~

This is still not a cure for model drift. It is a fail-safe transition from
silent wrong execution to explicit regime uncertainty.

Synthetic engineering result only; no clinical authority.
