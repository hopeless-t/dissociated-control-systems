# Cancer Latent-State Digital Twin v0.14 — robust / minimax observation acquisition

Date: 2026-10-06
Status: simulation-stage optimization / falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_13_STOCHASTIC_ACQUISITION_AND_REDUNDANCY_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/observation_policy.py`
Known-answer tests: `tests/test_observation_policy.py`

## Meta-meta target

v0.13 exposed a conflict:

```text
expected-information-efficient policy
    can be fragile to model-family misspecification
```

v0.14 asks:

> If several future-generating worlds remain plausible, should the acquisition policy optimize expected nominal performance, or protect against the worst declared world?

This note introduces a small exact minimax-style panel selector for synthetic research.

## Synthetic robust-panel campaign

The v0.13 observation world was reused with candidate action families:

```text
A+B   complementary but model-fragile pair
C     medium independent channel
D     strong expensive channel
E/F   weak independent channels
```

All non-empty panels with total synthetic burden <= 8 were enumerated.

Each panel was evaluated in two declared worlds:

```text
World N — nominal A+B relationship
World S — A+B relationship reversed by model-family shift
```

The second world is deliberately adversarial. It is not a biological claim.

## Nominal-optimal panel

Optimizing only World N selected approximately:

```text
A+B+C+E+F
burden ~6
nominal error ~15.6%
shifted-world error ~42.8%
worst-case error ~42.8%
```

This is an important failure mode:

```text
Excellent Nominal Panel != Robust Panel
```

The panel concentrated heavily on the observation family that the nominal model believed was most informative.

## Robust / minimax panel

Choosing the panel with the best worst-case performance across the two declared worlds selected approximately:

```text
C+D
burden 8
nominal error ~20.1%
shifted-world error ~20.2%
worst-case error ~20.2%
```

The robust panel deliberately sacrificed nominal efficiency to reduce model-shift fragility.

This is not evidence that a real clinical panel should be chosen by minimax error. It is a mathematical counterexample showing that expected-optimal and robust-optimal acquisition can diverge sharply.

## New invariant

```text
Expected-Optimal Observation Policy != Robust-Optimal Observation Policy
```

and:

```text
A High-Information Channel Can Be A Single Point Of Epistemic Failure
```

when the information model for that channel is itself uncertain.

## Robustness requires declared worlds

Minimax protection is only as good as the alternative worlds included.

The repository primitive therefore requires an explicit set of world-specific value functions.

```text
robust_best_panel(Q, {V_1, ..., V_k}, budget)
```

optimizes:

```text
max_Q min_j V_j(Q)
```

under the burden budget.

But:

```text
World Omitted From Robust Set
    -> No Robustness Guarantee Against That World
```

This prevents the word "robust" from being treated as a universal safety certificate.

## Expected-value vs worst-case frontier

The Twin should not collapse the trade-off to one hidden coefficient.

Candidate report:

```text
Panel P1
    nominal expected value: high
    worst-case declared-world value: low
    burden: low

Panel P2
    nominal expected value: medium
    worst-case declared-world value: medium-high
    burden: higher
```

This is a policy frontier, not a single universal winner.

## When robust acquisition is most relevant

Robust optimization becomes more attractive when:

- model-family posterior remains broad;
- one assay family dominates the nominal information gain;
- model misspecification has large consequence;
- independent observation families exist;
- patient burden ceiling still permits diversification.

Expected-value optimization becomes more attractive when:

- model support is strong;
- alternative worlds have very low posterior mass;
- additional redundancy is materially burdensome;
- delay from robust diversification would exceed the decision horizon.

These are theoretical conditions, not clinical thresholds.

## Posterior-weighted robustification

Pure worst-case minimax can be overly conservative if an extreme world is technically possible but poorly supported.

A future policy family should compare:

```text
Bayesian expected value
CVaR / tail-risk value
minimax worst-case value
distributionally robust value
```

rather than assuming one universal risk functional.

Candidate generic objective:

```text
PolicyScore(Q)
    = ExpectedValue(Q)
      - lambda * TailRisk(Q)
      - mu * Burden(Q)
      - nu * Delay(Q)
```

with `lambda` declared externally rather than silently learned from the same outcomes being evaluated.

## Interaction with adaptive acquisition

The strongest emerging candidate is not pure static minimax.

It is a robust staged policy:

```text
small nuisance-diverse starter bundle
    -> update model-family posterior
    -> if one world dominates, adapt efficiently
    -> if model ambiguity remains broad, preserve redundancy / robust acquisition
```

This avoids paying the worst-case panel cost for every patient while preventing early over-concentration on one fragile measurement family.

The staged policy remains unvalidated and is a next falsifier.

## Support taxonomy update

The policy layer now distinguishes:

```text
SUPPORTED_FOR_EXPECTED_VALUE_POLICY
SUPPORTED_FOR_ROBUST_POLICY
MODEL_WORLD_SET_INCOMPLETE
BURDEN_CEILING_LIMITS_ROBUSTNESS
DEADLINE_LIMITS_ROBUSTNESS
TRANSITION_UNRESOLVED
```

A patient can therefore have enough evidence for an efficient nominal forecast while still lacking enough model-family support for a robust forecast.

## Relation to DCS core

This result is a direct extension of:

```text
Observable Behavior != Unique Internal State
```

into policy space:

```text
One Good-Fitting Model != Unique Generating World
One Nominally Optimal Probe != Safe Probe Under Model Ambiguity
```

The acquisition policy must therefore reason over competing worlds, not only over parameter uncertainty inside one world.

## v0.14 convergence update

The observation-policy stack is now:

```text
1. canonical observation semantics
2. model / transition support
3. patient-specific burden ceiling
4. decision horizon
5. candidate singleton + bundle generation
6. complementarity / nuisance-diversity analysis
7. stochastic success / turnaround handling
8. expected-value vs robust-world policy comparison
9. explicit stop / unresolved state
```

The new design principle is:

> Optimize measurement efficiency only after declaring which model worlds the policy is expected to remain safe across.

## Next falsifiers

1. robust staged-batch acquisition;
2. Bayesian-model-average vs minimax vs CVaR policy comparison;
3. posterior misspecification where the true world receives tiny prior mass;
4. hidden world absent from the candidate set entirely;
5. informative missingness and correlated assay failure;
6. redraw / re-acquisition loops;
7. worst-case regret rather than classification error alone;
8. patient-specific burden ceiling interacting with robust diversification;
9. delay-sensitive robust acquisition;
10. static-panel safety under asynchronous laboratory workflows.

## Claim boundary

All channels, alternative worlds, errors, burdens and policy rankings are synthetic. This checkpoint does not recommend a real test panel, diagnostic workflow, monitoring schedule, or treatment action.
