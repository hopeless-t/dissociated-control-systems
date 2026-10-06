# Cancer Latent-State Digital Twin v0.13 — stochastic acquisition / redundancy / static-vs-adaptive safety

Date: 2026-10-06
Status: simulation-stage optimization / falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_12_DEADLINE_AWARE_ACQUISITION_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/observation_policy.py`
Known-answer tests: `tests/test_observation_policy.py`

## Meta-meta target

v0.11 showed that adaptive acquisition can reduce expected burden.
v0.12 showed that decision value depends on timeliness.

v0.13 attacks a stronger assumption:

```text
Adaptive Sequential Acquisition Is Always Safer Than A Static Panel
```

The attack adds:

- stochastic turnaround time;
- assay failure / no-result events;
- patient-specific burden ceilings;
- parallel execution for predeclared panels;
- hidden model shift that corrupts a highly valued observation bundle.

All values and channels below are synthetic.

## Synthetic observation world

A binary competing-world generator was used with:

- weak baseline evidence;
- complementary low-burden pair `A+B`;
- medium channel `C`;
- strong but costly channel `D`;
- weak independent channels `E` and `F`.

Illustrative burden / delay / failure surfaces:

```text
A+B   burden 2   delay 2 or 4   failure ~8%
C     burden 2   delay 1 or 3   failure ~5%
D     burden 6   delay 3 or 6   failure ~12%
E/F   burden 1   delay 1 or 2   failure ~4%
```

Patient-specific burden ceilings were generated from an abstract host-reserve variable.

The ceiling is a research constraint only; it does not represent a validated clinical tolerance score.

## Nominal sequential-adaptive vs parallel-static result

A 20,000-patient synthetic evaluation compared:

1. sequential adaptive acquisition that waits for each result before choosing the next observation;
2. a predeclared parallel static panel launched simultaneously.

A moderate parallel panel `A+B+C+E+F` incurred higher burden but all component observations could proceed concurrently.

Approximate result:

```text
sequential adaptive
    overall error              ~17.1%
    high-confidence error      ~4.2%
    mean burden                ~3.95

parallel static moderate panel
    overall error              ~14.7%
    high-confidence error      ~3.0%
    mean burden                6.0
```

The static panel was not preferable on burden, but it was safer on this stochastic deadline surface.

The reason is structural:

```text
sequential adaptation pays waiting time serially
parallel static acquisition pays burden in parallel
```

Therefore:

```text
Adaptive != Automatically Deadline Efficient
Static != Automatically Wasteful
```

## Parallelism correction

The observation scheduler needs two resource dimensions:

```text
patient burden
calendar occupancy / critical-path delay
```

For a panel `Q`:

```text
SequentialCompletion(Q) = sum delay(q)
ParallelCompletion(Q)   = max delay(q)
```

under the simplest deterministic independence model.

The repository now locks this distinction as a known-answer test.

## Hidden model-shift attack

A second attack corrupted the previously valuable `A+B` relationship in a hidden 12% subgroup while leaving the adaptive policy trained on the nominal relationship.

This is a deliberately adversarial model-misspecification surface.

Among synthetic patients with sufficient burden ceiling for a larger redundant panel:

```text
adaptive policy
    overall error              ~20.6%
    high-confidence error      ~10.1%
    mean burden                ~4.05

parallel panel excluding A+B dependence
    overall error              ~16.3%
    high-confidence error      ~3.1%
    burden                     10.0
```

Again, the static panel is more burdensome.

But it exposes an important counterexample:

```text
An adaptive policy can concentrate measurement on the observation family it believes is most informative.
If that family is misspecified, adaptation can amplify model error rather than diversify it.
```

## New invariant — adaptability vs redundancy

The acquisition problem now has a genuine trade-off:

```text
Adaptability
    reduces expected unnecessary measurement

Redundancy / diversity
    can reduce fragility to observation-family misspecification
```

Therefore the goal is not maximal adaptation.

The goal is:

```text
minimum expected burden
subject to
    sufficient identifiability
    deadline feasibility
    model-support robustness
    declared redundancy floor when model risk is material
```

## Sentinel-observation concept

A candidate protection is to require a small amount of observation diversity before permitting a high-confidence stop.

Conceptually:

```text
adaptive primary path
    + one orthogonal sentinel channel
```

The sentinel is not necessarily strong enough to decide the case by itself.
Its purpose is to challenge the dominant measurement family and detect disagreement.

This should be tested as a policy family, not assumed safe.

Candidate condition:

```text
HighConfidenceAllowed
    only if
        posterior threshold met
        AND semantic support passes
        AND model support passes
        AND diversity / sentinel requirement passes
```

## Failure / no-result semantics

An ordered observation can fail, return no result, or require re-acquisition.

Therefore acquisition value should include at least:

```text
P(result available)
P(result available before deadline)
expected re-acquisition burden
expected critical-path delay
```

The repository primitive now records a synthetic `success_probability` and exposes a minimal expected-successful-value helper.

Important limitation:

```text
Expected value = raw information * success probability
```

is only a toy expectation.

It is invalid when assay failure is informative or state-dependent. In that case missingness itself must enter the generative model.

## Patient-specific burden ceiling

A panel that is globally optimal can be infeasible for an individual patient.

The scheduler must therefore enforce:

```text
CumulativeBurden <= PatientSpecificCeiling
```

before optimization, not as an after-the-fact penalty.

This produces another explicit state:

```text
IDENTIFIABILITY_TARGET_INFEASIBLE_UNDER_BURDEN_CEILING
```

when no admissible panel can reach the declared ambiguity target.

The model must return unresolved rather than silently exceed the ceiling.

## Static vs adaptive policy taxonomy

The branch now distinguishes at least four acquisition modes:

```text
1. static serial
2. static parallel
3. adaptive serial
4. adaptive parallel / staged-batch
```

The fourth mode may be the most interesting next candidate:

```text
small parallel starter bundle
    -> posterior update
    -> adaptive second-stage bundle only if needed
```

This can preserve some redundancy and deadline robustness without paying the full-panel burden for everyone.

## New optimization form

For policy `pi`:

```text
pi* = argmin_pi ExpectedPatientBurden(pi)
```

subject to:

```text
DecisionAmbiguity(pi) <= epsilon
FalseConfidenceRate(pi) <= alpha
P(ResultByDeadline | pi) >= beta
ModelRiskFragility(pi) <= gamma
CumulativeBurden(pi, patient) <= ceiling(patient)
SemanticSupport = PASS
```

The model-risk term is intentionally explicit. A policy with excellent nominal information efficiency can be rejected if it is too concentrated on one fragile measurement family.

## Research-design implication

The emerging acquisition architecture is no longer purely sequential.

Candidate form:

```text
Stage 0: validate semantics / support / burden ceiling / decision horizon
Stage 1: acquire a small nuisance-diverse parallel starter set
Stage 2: update competing-world posterior
Stage 3: if ambiguity resolved -> STOP
Stage 4: otherwise select adaptive singleton or bundle actions
Stage 5: enforce deadline, failure-risk and burden constraints
Stage 6: retain an explicit unresolved state when constraints cannot be jointly satisfied
```

## Literature alignment

Recent oncology workflow studies reinforce that turnaround time and complementary test surfaces matter in real decision pathways, while not validating this synthetic policy model.

Examples to qualify separately:

- PMID 42475778 (2026): previsit liquid biopsy workflow in NSCLC reported different turnaround times for commercial vs institutional testing and emphasized complementary plasma/tissue profiling.
- PMID 40570258 (2025): prospective metastatic NSCLC study reported materially shorter liquid-biopsy turnaround than tissue NGS while tissue and plasma retained complementary yield.
- PMID 41590362 (2026): a real-world implementation study showed that workflow/laboratory batching can make nominally low-burden liquid biopsy operationally slow, demonstrating that modality alone does not determine decision timeliness.

These sources support treating turnaround and workflow as first-class variables; they do not validate the synthetic burden values or policy rankings above.

## v0.13 convergence update

The policy theory is now:

```text
Efficient Observation Policy
!=
Always Sequential
!=
Always Adaptive
!=
Always Minimal-Burden Per Step
```

Instead:

```text
Efficient Observation Policy
=
Patient-Specific Constraint Handling
+ Parallelism Awareness
+ Conditional Information Value
+ Complementarity Search
+ Reliability / Failure Modeling
+ Model-Risk Diversification
+ Deadline Awareness
+ Explicit Stop / Unresolved States
```

## Next falsifiers

1. staged-batch policy: small parallel starter bundle followed by adaptation;
2. stochastic turnaround distributions rather than two-point delays;
3. informative missingness / state-dependent assay failure;
4. re-acquisition and redraw loops;
5. correlated laboratory failure across channels;
6. sentinel-observation value under multiple misspecification families;
7. optimize redundancy floor versus patient burden;
8. compare expected burden and worst-case regret, not only mean performance;
9. test robust / minimax acquisition against Bayesian expected-value acquisition;
10. preserve treatment optimization outside this measurement-policy layer.

## Claim boundary

All channels, delays, failures, burden ceilings, performance values and misspecification families in this note are synthetic research objects. They do not rank real cancer tests, define clinical thresholds, recommend procedures, or guide treatment.
