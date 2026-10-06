# RQ-005 Temporal evidence contract

## Problem

Survivor research is unusually vulnerable to future-information leakage.
Variables that become visible only after a patient has already survived,
responded, or recurred can appear strongly predictive when retrospectively
inserted into an earlier model.

Examples:

- CR/NED status learned months after therapy starts;
- recurrence-site biology measured only after recurrence;
- a survivor narrative collected years after treatment;
- treatment duration that is itself partly determined by remaining alive and
  progression-free.

## Invariant

~~~text
Observed Later != Known Earlier
Association With Survival != Valid Baseline Predictor
Survivor Narrative Collected Later != Evidence Of Earlier Causal State
~~~

Implementation:

- `src/dissociated_control_systems/temporal_evidence.py`
- `tests/test_temporal_evidence.py`

The known-answer gate rejects any feature whose observation time is after the
prediction landmark.

## Landmark rule

For prediction origin L:

~~~text
feature j is eligible only if
  observation_time_j <= L
~~~

A later observation can become eligible only by explicitly moving the landmark
forward and changing the estimand.

Example:

~~~text
diagnosis landmark = month 0
  baseline NPI                       allowed
  CR/NED measured at month 12        future / forbidden

month-12 landmark among eligible survivors
  baseline NPI                       allowed
  CR/NED measured at month 12        allowed
~~~

The second model answers a different question and uses a different risk set.

## Multi-state consequence

RQ-005 therefore separates observation windows for:

~~~text
transition 0 -> 1: diagnosis to recurrence
  use information available before the chosen recurrence-risk landmark

transition 1 -> 2: recurrence to cancer death/censor
  reset time origin at recurrence or a declared post-recurrence landmark
  use only information available by that origin
~~~

## Narrative consequence

Survivor testimony remains valuable for discovering candidate variables.

But when collected after long survival it cannot be treated as direct evidence
that the described psychological state preceded tumor or immune divergence.
The candidate must be reconstructed from contemporaneous records or tested
prospectively/longitudinally.

## Claim ceiling

The temporal gate prevents one class of leakage. It does not by itself solve
confounding, informative censoring, measurement error, or causal
identifiability.
