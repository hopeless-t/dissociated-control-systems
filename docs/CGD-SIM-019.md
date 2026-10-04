# CGD-SIM-019 — Quarantine, recalibrate, validate, restore

> Status: SYNTHETIC POST-CONVERGENCE AUTHORITY TEST  
> Clinical authority: NONE

SIM-018 can detect the declared OOD shifts quickly and fail closed. Detection is
not the end of the control problem.

The next question is:

> Under what evidence contract may normal authority return?

## Lifecycle

~~~text
world-model mismatch
    -> quarantine
    -> collect verified evidence from the new regime
    -> fit a regime-specific candidate
    -> validate on independent shifted evidence
    -> restore authority only if validation >= declared threshold
~~~

The experiment freezes the original clean model, creates an independent
combined-shift validation set and a separate combined-shift test set, and then
varies the amount of verified shifted calibration evidence.

Calibration sizes:

~~~text
5, 10, 20, 40, 80, 160 samples per latent hypothesis
~~~

The candidate model is trained on shifted evidence only. This intentionally
tests whether a genuinely changed world should get its own model instead of
being diluted into the clean-world model.

Authority restoration threshold:

~~~text
shifted validation exact accuracy >= 0.90
~~~

The held-out test set is never used to decide restoration. It exists only to
audit whether the validation gate caused false restoration.

## Invariant

~~~text
Successful OOD Detection != Permission To Resume
~~~

Resumption requires independent evidence that the candidate model works in the
new regime.

Synthetic engineering result only; no clinical authority.
