# Cancer Latent-State Digital Twin v0.16 — risk-sensitive observation policy and robust abstention

Date: 2026-10-06
Status: simulation-stage policy falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_15_INFORMATIVE_MISSINGNESS_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/observation_policy.py`
Known-answer tests: `tests/test_observation_policy.py`

## Meta-meta target

Earlier checkpoints showed that:

- expected-optimal and robust-optimal panels can differ;
- adaptive acquisition can be lower burden but fragile under model shift;
- static parallel redundancy can outperform serial adaptation under deadlines;
- informative missingness must be modeled explicitly.

v0.16 compares policy objectives directly:

```text
Bayesian expected value
minimax / worst-case value
CVaR / lower-tail value
staged robust-adaptive acquisition
```

The primary question is not which policy has the best average synthetic error.

It is:

> how much average performance and burden should be traded for lower worst-case error and lower false confidence across declared plausible model worlds?

## Synthetic world set

A private deterministic experiment used three declared abstract worlds:

```text
N       nominal observation world
FlipAB  two otherwise useful observation channels reverse their class relation
WeakD   a strong observation channel becomes weak
```

World prior used only for the Bayesian / tail-risk experiments:

```text
N       0.70
FlipAB  0.15
WeakD   0.15
```

The hidden outcome was binary only for policy stress testing.

Six abstract observations were assigned:

- distinct burden;
- distinct turnaround time;
- distinct success probability;
- world-dependent likelihoods.

No channel represents a real clinical assay.

Patient-specific burden ceilings were sampled from three synthetic levels.
Turnaround time was stochastic around each declared mean.
A hard synthetic decision deadline was imposed.

## Static policy comparison

Approximate evaluation from 12,000 synthetic patients per policy:

```text
policy            mean error   mean burden   deadline-late   worst-world error
Bayesian static      22.1%        6.09          20.4%            35.9%
Minimax static       26.9%        5.19           6.3%            31.5%
CVaR static          21.5%        6.10          20.7%            35.4%
```

The numbers are specific to this toy world set.

The important pattern is that minimax sacrificed average performance while reducing both deadline exposure and the worst declared world.

The CVaR setting used in this attack was still relatively close to expected-value behavior because only a minority of prior mass occupied the adverse worlds.

Therefore:

```text
Risk Objective Choice Is Itself A Model Assumption
```

## Sequential policy comparison

Approximate synthetic results:

```text
policy                 mean error   mean burden   deadline-late   worst-world error
Bayesian adaptive         28.0%        4.04          20.2%            43.6%
Minimax adaptive          31.2%        3.38           5.1%            31.7%
CVaR adaptive             31.4%        3.38           5.1%            32.2%
Staged minimax            30.8%        3.41           1.6%            31.1%
```

In this surface the Bayesian adaptive policy used less average burden than the static Bayesian policy, but became especially fragile in the `FlipAB` world.

The risk-sensitive sequential policies made fewer aggressive high-confidence commitments and preserved a narrower worst-world error band.

## Robust safety can appear as abstention

A key failure of naive evaluation is to count abstention as if it were ordinary predictive failure.

When a robust confidence condition was imposed across all still-plausible worlds, many patients could not reach the declared high-confidence threshold within the burden/deadline envelope.

This is expected behavior.

```text
one plausible world unresolved
    -> robust high confidence unavailable
```

Repository primitive:

```text
worst_case_confidence(world_confidences)
```

returns the minimum confidence over explicitly supplied plausible worlds.

Known-answer example:

```text
world confidences = [0.97, 0.95, 0.61]
robust confidence = 0.61
```

The first two worlds do not erase the third.

New invariant:

```text
High Mean Confidence != Robust Confidence
Robust Safety Can Manifest As Abstention
```

## Tail-risk objective

The repository now includes an exact small-panel lower-tail selector:

```text
cvar_best_panel(...)
```

Higher value is assumed better.

For synthetic world utilities `V_j(Q)`, lower-tail utility is approximately:

```text
CVaR_lower_alpha(Q)
    = mean utility over the worst alpha probability mass
```

A known-answer test constructs:

```text
fragile panel:
    common world   +10
    rare bad world  -5
    rare good world +9

robust panel:
    all worlds       +6
```

The fragile panel has attractive nominal / mean behavior, but a sufficiently tail-sensitive objective selects the robust panel.

This locks the distinction:

```text
Expected-Optimal != Tail-Risk-Optimal != Minimax-Optimal
```

## Oracle regret perspective

For a fixed synthetic burden budget, each true world had a different oracle observation panel.

Examples from the same declared model surface:

```text
N oracle       -> A+B+C+D
FlipAB oracle  -> C+D+E
WeakD oracle   -> A+B+C+E+F
```

No single panel is simultaneously the world-specific oracle.

Therefore observation-policy evaluation should report regret by world rather than only aggregate error.

Candidate quantity:

```text
Regret_pi(w)
    = Loss_pi(w) - Loss_oracle(w)
```

and robust policy design should track:

```text
max_w Regret_pi(w)
```

alongside average burden and coverage.

## Policy output must separate prediction from permission

The emerging contract is:

```text
posterior prediction
policy objective
world-support set
robust confidence
coverage / abstention state
burden spent
calendar time spent
unresolved model worlds
```

A policy may have a numerically sharp posterior while lacking permission to emit a robust high-confidence conclusion.

## Updated acquisition objective

A generic research objective is now better written as a constrained multi-risk problem rather than one scalar information score:

```text
minimize:
    ExpectedBurden

subject to:
    ExpectedLoss <= epsilon_mean
    WorstWorldLoss <= epsilon_worst
    TailRisk_alpha <= epsilon_tail
    FalseConfidenceRate <= alpha_fc
    ResultArrival <= DecisionDeadline
    SemanticSupport = PASS
```

If the constraint set is infeasible:

```text
ROBUST_RESOLUTION_INFEASIBLE
```

or a typed unresolved state is preferable to relaxing constraints silently.

## Important correction to staged robust-adaptive intuition

A small robust starter panel followed by adaptation remains promising, but v0.16 does **not** establish it as universally optimal.

The synthetic tests show that:

- a robust starter can reduce late acquisition;
- myopic adaptation can still inherit model-form fragility;
- minimax adaptation can become too conservative to resolve within the available budget;
- a static redundant panel can still be safer in some deadline/model-shift regimes.

Therefore staged acquisition itself remains an object to falsify, not a final answer.

## Next falsifiers

1. explicit decision-deferral cost: act now versus wait for a stronger observation;
2. CVaR level sweep rather than one alpha;
3. distributionally robust optimization where world probabilities are uncertain;
4. world-set expansion / adversarial world generation;
5. dynamic programming for finite-horizon robust acquisition;
6. regret-based stopping rather than confidence-only stopping;
7. evaluate whether abstention is calibrated to actual downstream decision harm;
8. model patient-specific deadline as well as patient-specific burden ceiling;
9. test robust policy under informative missingness and correlated technical failures simultaneously;
10. move toward public-data qualification only after policy-risk architecture stabilizes.

## Claim boundary

All worlds, channels, probabilities, burdens, deadlines, errors and policy comparisons are synthetic. They do not estimate clinical test performance, prognosis, treatment benefit, or appropriate cancer monitoring strategy.
