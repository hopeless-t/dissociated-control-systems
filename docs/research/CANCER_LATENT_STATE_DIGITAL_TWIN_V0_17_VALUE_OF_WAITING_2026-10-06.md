# Cancer Latent-State Digital Twin v0.17 — value of waiting / act-now versus measure-more

Date: 2026-10-06
Status: simulation-stage decision-timing falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_16_RISK_SENSITIVE_POLICY_AND_ABSTENTION_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/observation_policy.py`
Known-answer tests: `tests/test_observation_policy.py`

## Meta-meta target

v0.12 established:

```text
Information Gain != Decision Value
```

because an observation arriving after the useful decision horizon may not help the current decision.

v0.17 asks the stronger question:

> even if a result arrives in time, when is waiting for it worth the delay it introduces?

The candidate action set must include:

```text
ACT_NOW / stop observing
FAST_WEAK observation
MEDIUM observation
SLOW_STRONG observation
parallel observation bundle
```

The correct answer can change as the assumed cost of waiting changes.

## Synthetic setup

The same abstract three-world surface from v0.16 was reused.

Single/bundle expected synthetic classification losses from the declared prior included approximately:

```text
ACT_NOW       expected loss 0.5000   delay 0.0   burden 0
E             expected loss 0.3824   delay 0.8   burden 1
C             expected loss 0.3326   delay 1.5   burden 2
C+E           expected loss 0.3244   delay 1.5   burden 3
D             expected loss 0.1966   delay 3.0   burden 4
D+E           expected loss 0.1839   delay 3.0   burden 5
```

Worst-world loss differed materially for the strong `D` channel because it weakened in one declared world:

```text
D worst-world loss     ~0.415
D+E worst-world loss   ~0.397
C worst-world loss     ~0.333
E worst-world loss     ~0.382
```

No label represents a real assay or clinical action.

## Decision-adjusted loss

A deliberately simple synthetic accounting function was used:

```text
L_decision
    = prediction_loss
    + lambda_burden * burden
    + lambda_wait * delay
```

The repository now exposes this only as a falsifiable research primitive:

```text
decision_adjusted_loss(...)
```

The weights are not clinical constants. They are explicit assumptions that must be varied.

## Expected-value frontier

With a small burden penalty and increasing waiting penalty, the expected-value optimum changed qualitatively:

```text
very low waiting cost  -> D+E
moderate waiting cost  -> E
high waiting cost      -> ACT_NOW
```

Example synthetic sweep with burden weight 0.01:

```text
lambda_wait = 0.00  -> D+E
lambda_wait = 0.02  -> D+E
lambda_wait = 0.05  -> D+E
lambda_wait = 0.08  -> E
lambda_wait = 0.10  -> E
lambda_wait = 0.12  -> E
lambda_wait = 0.15  -> ACT_NOW
```

The specific transition points are toy-model artifacts.

The structural result is not.

```text
More Information Can Have Negative Net Decision Value
```

when acquisition delay and burden are sufficiently costly for the declared decision problem.

## Risk-objective dependence

The expected-value and worst-world objectives chose differently even when waiting cost was zero.

At zero synthetic waiting penalty:

```text
expected-value objective -> D+E
worst-world objective    -> C
```

The strong `D` observation performs very well in common worlds but poorly in the `WeakD` world.

Thus:

```text
ValueOfWaiting(q)
```

cannot be defined independently of the risk objective.

New invariant:

```text
Value Of Waiting Is Risk-Objective Dependent
```

## Wait / observe / act are one policy problem

Earlier checkpoints treated observation acquisition and stopping as separate questions.

v0.17 merges them conceptually.

At each step the policy should compare:

```text
1. stop now / preserve current uncertainty;
2. order a fast low-burden observation;
3. wait for a slower stronger observation;
4. launch a parallel bundle;
5. declare unresolved if no admissible action has positive net decision value.
```

Therefore the action set is not merely a set of measurements.

```text
A_t = {STOP, WAIT, OBSERVE(q), OBSERVE(bundle)}
```

Treatment choice remains outside this measurement-policy layer.

## Regret formulation

A useful simulation target is:

```text
Regret(a)
    = downstream loss under a
    - downstream loss under the world-specific oracle action
```

The policy can then minimize one of:

```text
ExpectedRegret
WorstCaseRegret
CVaR(Regret)
```

rather than optimizing information gain directly.

This naturally incorporates the possibility that `STOP` has lower regret than ordering another observation.

## Decision-deferral is itself an intervention on the workflow

A delay is not an empty period in the optimization.

It consumes:

```text
calendar time
operational capacity
opportunity to update
possibly patient burden from uncertainty / repeated visits
```

The exact downstream harm is domain- and question-specific and cannot be supplied by this synthetic model.

The methodological requirement is simply:

```text
delay cost must be declared rather than silently set to zero
```

## Known-answer test

The repository now locks a minimal inversion:

```text
slow-strong:
    prediction loss 0.10
    delay 5

fast-weak:
    prediction loss 0.20
    delay 1
```

With zero waiting penalty:

```text
slow-strong preferred
```

With waiting penalty 0.03 per synthetic time unit:

```text
fast-weak preferred
```

This proves only that acquisition preference can invert under waiting cost.

## Updated sequential debugger

The observation engine is now better described as:

```text
current evidence
 -> competing worlds
 -> semantic / model support
 -> patient burden ceiling
 -> decision horizon
 -> candidate STOP / WAIT / OBSERVE actions
 -> expected / tail / worst-case downstream loss
 -> choose admissible action
 -> posterior update or stop
```

This is a finite-horizon partially observed control problem over **measurement actions**, not treatment actions.

## Emerging mathematical object

The natural next abstraction is a small POMDP / belief-state control problem:

```text
belief_t = p(x_t, model_world, sensor_state | evidence_t)

action_t in {STOP, OBSERVE(q), OBSERVE(bundle), WAIT}

belief_(t+1) = BayesUpdate(belief_t, observation)

cost_t = burden + delay + unresolved-risk + false-confidence-risk
```

The branch does not yet claim that a full POMDP implementation is necessary or optimal.

It is the next model family to falsify against simpler policies.

## Next falsifiers

1. exact finite-horizon dynamic programming on a small belief-state grid;
2. compare one-step value-of-information with multi-step value-of-information;
3. test whether myopic STOP/OBSERVE choices have large long-horizon regret;
4. uncertain decision deadline rather than fixed deadline;
5. patient-specific waiting cost rather than one global value;
6. correlated assay failure that makes waiting for a bundle especially risky;
7. allow parallel launch followed by cancellation of now-redundant tests;
8. adversarially search for policies that are low burden but high regret;
9. keep treatment-selection utility outside scope until clinical evidence exists;
10. qualify real workflow data only after the synthetic policy architecture reaches a stable fixed point.

## Claim boundary

All losses, delays, burdens, weights, action labels and switching points are synthetic. This checkpoint does not advise when any real patient should wait, test, treat, defer, or stop monitoring.
