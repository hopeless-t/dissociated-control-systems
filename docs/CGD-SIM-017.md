# CGD-SIM-017 — Sequential weak-shift accumulation

> Status: SYNTHETIC POST-CONVERGENCE CONTROL TEST  
> Clinical authority: NONE

SIM-016 localized the remaining OOD-routing failure:

- large common-mode bias was detected;
- explicit missingness was detected;
- combined shift was detected;
- mild persistent noise inflation was mostly missed by isolated 64-sample
  windows.

The remaining hypothesis is temporal accumulation.

## New invariant

~~~text
Weak Persistent Shift != Benign Local Noise
~~~

SIM-017 evaluates the observation stream at regular checkpoints. Each
checkpoint uses all evidence accumulated so far to score mean and variance
departure from the clean reference regime.

The detector threshold is calibrated from the **maximum score over entire clean
sequences**, not from individual checkpoints. This makes the false-alarm unit
the sequence rather than one look.

Once the threshold is crossed:

~~~text
normal execution authority -> disabled
external evidence / review / recalibration -> required
~~~

The experiment reports detection latency as a sample index and translates that
latency into the fraction of wrong executions that escaped before the gate
closed.

The weak-noise gate is considered effective when:

~~~text
independent clean sequence false-alarm rate <= 0.10
noise shift is detected
noise error-exposure reduction > 0.50
~~~

Synthetic engineering result only; no clinical authority.
