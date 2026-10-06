# Cancer Latent-State Digital Twin v0.18 — multi-step value of information / belief routing

Date: 2026-10-06
Status: simulation-stage belief-policy falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_17_VALUE_OF_WAITING_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/belief_policy.py`
Known-answer tests: `tests/test_belief_policy.py`

## Meta-meta target

v0.17 merged stopping, waiting, and observation acquisition into one finite-horizon measurement-policy problem.

v0.18 attacks a deeper assumption:

```text
If an observation does not immediately reduce outcome uncertainty,
it has no value.
```

That assumption is false when an observation identifies **which model-world / route** should govern the next measurement.

## Exact finite-state counterexample

A four-state synthetic hidden space was used:

```text
(y=0, world=L)
(y=1, world=L)
(y=0, world=R)
(y=1, world=R)
```

with uniform prior.

The final decision concerns only `y`.
The latent world determines which specialist observation is informative.

Candidate observations:

```text
Scout S
    identifies world L versus R with 90% accuracy
    carries zero direct information about y
    burden 0.5

Specialist L
    95% accurate for y in world L
    random in world R
    burden 2.0

Specialist R
    95% accurate for y in world R
    random in world L
    burden 2.0

General G
    75% accurate for y in both worlds
    burden 2.5
```

The total burden of:

```text
Scout + routed specialist
```

is therefore the same as the direct general observation in this toy example.

No symbol corresponds to a real cancer assay.

## Immediate value of the scout

Before observing:

```text
Bayes outcome-classification loss = 0.50
```

After observing Scout alone:

```text
expected outcome-classification loss = 0.50
```

Exactly unchanged.

Formally:

```text
I(Y ; Scout) = 0
```

in the declared construction.

A myopic policy scoring only immediate reduction in outcome uncertainty therefore assigns the scout zero value.

## Multi-step value

Direct General observation:

```text
expected final classification loss = 0.25
```

Two-stage policy:

```text
Scout
 -> posterior over model-world
 -> choose Specialist L or Specialist R
 -> final outcome decision
```

has exact expected final loss:

```text
0.095
```

at the same declared total burden 2.5.

Therefore:

```text
ImmediateOutcomeVOI(Scout) = 0
but
MultiStepDecisionVOI(Scout) > 0
```

New invariant:

```text
Zero Immediate Outcome Information != Zero Decision Value
```

## Why the scout helps

The scout changes:

```text
p(model_world | evidence)
```

without changing:

```text
p(outcome | evidence)
```

immediately.

For a positive scout result in the known-answer case:

```text
P(world=R | Scout=1) = 0.90
P(y=1 | Scout=1)     = 0.50
```

Thus the observation is valuable as a **routing measurement**.

It tells the debugger which next observation is likely to be informative.

## Cancer-Twin interpretation

The methodological analogue is not a claim that a real assay has this structure.

It is the possibility that some measurement may primarily identify:

```text
clone regime
sensor/shedding regime
immune/TME regime
model family
assay-support regime
```

rather than directly predict the clinical endpoint.

Such an observation may still have large downstream value because it changes which subsequent observation should be acquired or trusted.

Therefore an observation-policy engine should not rank candidate measurements solely by:

```text
I(Y ; q | evidence)
```

It may need to evaluate:

```text
I(M ; q | evidence)
```

and especially the downstream routed value:

```text
E[
    optimal future decision value
    after q
]
```

where `M` denotes competing model worlds.

## One-step VOI can be structurally myopic

The counterexample is stronger than ordinary complementarity.

In v0.11:

```text
A and B were individually weak but jointly informative.
```

Here:

```text
Scout is not outcome-informative even jointly with the final decision by itself.
Its value comes from changing the action policy for the next observation.
```

This is **policy-mediated information value**.

## Belief-state formulation

The natural state for the measurement controller is the posterior belief:

```text
b_t = p(x_t, model_world, sensor_state | evidence_t)
```

An observation action changes the belief:

```text
b_(t+1) = BayesUpdate(b_t, q_t, result_t)
```

and the next acquisition can depend on the new belief.

The correct finite-horizon objective is therefore closer to:

```text
V_t(b)
    = min over actions a [
        immediate_cost(a)
        + E_result V_(t+1)(BayesUpdate(b,a,result))
      ]
```

with terminal loss based on the declared decision problem.

This is the standard shape of a small POMDP / belief-state dynamic program, applied here only to **measurement actions**.

Treatment optimization remains outside scope.

## Repository primitive

`belief_policy.py` now implements small exact synthetic helpers:

```text
normalize_belief
predictive_outcome_distribution
bayes_update
expected_terminal_loss_after_observation
expected_two_stage_loss
```

They are intentionally finite and dependency-free so that known-answer tests remain inspectable.

## Policy consequence

The acquisition engine now needs to distinguish at least three kinds of observation value:

```text
1. endpoint information
   directly reduces outcome uncertainty

2. model-discrimination information
   separates competing transition / sensor worlds

3. routing information
   changes which future observation has high value
```

A single scalar `immediate information gain` can miss categories 2 and 3.

## Scout-quality sweep

In the same toy construction, reducing scout accuracy weakens the two-stage policy smoothly.

Approximate exact losses:

```text
Scout accuracy 0.50 -> routed loss 0.275
0.55 -> 0.2525
0.60 -> 0.2300
0.65 -> 0.2075
0.70 -> 0.1850
0.75 -> 0.1625
0.80 -> 0.1400
0.85 -> 0.1175
0.90 -> 0.0950
```

The direct general observation remains at loss 0.25.

Thus the scout only becomes worthwhile once it is sufficiently informative about the routing world.

This creates a clean falsifiable threshold rather than a universal rule that routing measurements are always useful.

## New no-go for myopic acquisition

```text
Myopic Endpoint VOI Cannot Detect Pure Routing Value
```

If a measurement changes only the posterior over which future sensor/model is relevant, a policy that scores only immediate endpoint entropy reduction assigns it zero value by construction.

No calibration trick fixes that omission.
The action horizon itself must be extended.

## Updated Cancer Debugger architecture

The measurement controller now has the structure:

```text
belief over latent biology
+ belief over transition/model world
+ belief over sensor world
        ↓
finite-horizon acquisition planner
        ↓
STOP / WAIT / routing observation / endpoint observation / bundle
        ↓
Bayesian belief update
        ↓
re-plan
```

This is more general than a ranked test list.

## Next falsifiers

1. exact finite-horizon dynamic programming over the four-state known-answer model;
2. compare horizon-1, horizon-2, and horizon-3 policy regret;
3. add observation delay and stochastic failure to the routing counterexample;
4. add patient-specific burden ceilings so Scout+Specialist is not always feasible;
5. adversarially corrupt the Scout and test false routing;
6. add a third model world and approximate planning;
7. compare exact dynamic programming with beam search and rollout policies;
8. test whether robust/minimax planning over model worlds over-abstains;
9. keep endpoint prediction, model discrimination, and routing value separately reported;
10. only map synthetic observation roles onto real oncology measurements after external evidence qualification.

## Claim boundary

All hidden states, action costs, accuracies, losses and routing rules are synthetic. This result does not identify or recommend any real cancer test or monitoring sequence.
