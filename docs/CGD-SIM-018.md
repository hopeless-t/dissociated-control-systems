# CGD-SIM-018 — Multivariate cumulative-energy detector

> Status: SYNTHETIC POST-CONVERGENCE CONTROL TEST  
> Clinical authority: NONE

SIM-017 showed that longer observation alone was not enough.

The score still selected the **maximum single-channel deviation**, so a weak
shift spread across every channel could remain below the threshold until almost
the end of the sequence.

## New invariant

~~~text
Distributed Weak Shift != Max Single-Channel Deviation
~~~

SIM-018 changes the statistic rather than adding another controller.

For each sample and feature:

~~~text
z_j = (x_j - mean_clean_j) / std_clean_j
~~~

The detector computes multivariate standardized energy:

~~~text
e = mean_j(z_j^2)
~~~

and accumulates the departure of mean energy from the clean baseline across
the sequence.

A separate multivariate mean-vector score remains available for common-mode
drift. Explicit missingness still causes immediate OOD routing.

The sequence threshold is set strictly above the maximum score observed across
20 independent clean calibration sequences, then tested on 20 different clean
sequences.

Success requires:

~~~text
independent clean sequence false-alarm rate <= 0.10
noise inflation is detected
noise-shift error-exposure reduction > 0.50
~~~

Synthetic engineering result only; no clinical authority.
