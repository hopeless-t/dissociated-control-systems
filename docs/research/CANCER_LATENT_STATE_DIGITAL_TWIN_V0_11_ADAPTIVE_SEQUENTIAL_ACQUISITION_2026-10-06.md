# Cancer Latent-State Digital Twin v0.11 — adaptive sequential observation acquisition

Date: 2026-10-06
Status: simulation-stage optimization / falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_10_MINIMAL_SEPARATING_SET_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/observation_policy.py`
Known-answer tests: `tests/test_observation_policy.py`

## Meta-meta target

v0.10 showed that the right target is:

```text
minimum measurement burden
subject to sufficient decision-relevant identifiability
```

v0.11 asks two harder questions:

1. Can patient-specific sequential acquisition reduce expected burden compared with ordering a full panel for everyone?
2. Can greedy information-per-burden fail when observations are complementary rather than additive?

## Synthetic adaptive-acquisition campaign

A private deterministic analysis generated 60,000 synthetic patients from a binary competing-world model.

The model deliberately included:

- a weak baseline observation;
- two low-burden observations `A` and `B` whose **marginals are individually uninformative**;
- opposite class-conditional correlation between `A` and `B`, making the pair jointly highly informative;
- one medium observation;
- one strong expensive observation;
- two weak independent observations.

The hidden-pair construction is important because it creates a direct counterexample to myopic single-observation selection.

No synthetic channel corresponds to a real biomarker or procedure.

## Static reference values

On a 15,000-patient evaluation subset:

```text
baseline only            AUC ~0.613
A+B pair                 AUC ~0.942
medium C only            AUC ~0.714
strong D only            AUC ~0.924
weak E+F                 AUC ~0.669
A+B+C                    AUC ~0.952
```

The striking result is:

```text
A alone -> approximately no class information
B alone -> approximately no class information
A+B     -> strong information
```

This is a pure observation-interaction effect.

## Pair-aware adaptive policy

A synthetic sequential policy started with the baseline observation and stopped once the posterior crossed a declared confidence band.

At each unresolved step it selected the candidate action with highest expected information gain per burden. Importantly, `A+B` was allowed to appear as a **bundle action** rather than only as two separate singleton actions.

Approximate evaluation:

```text
AUC                         ~0.983
overall error               ~5.4%
posterior-confidence coverage ~87.8%
error within confident set  ~2.2%
average added burden        ~5.14
median added burden         2.0
```

The full static panel cost was 13 burden units for every patient.

Full-panel reference:

```text
AUC                         ~0.988
overall error               ~5.1%
error within confident set  ~1.1%
average burden              13.0
```

Thus, in this declared toy surface, adaptive acquisition retained most of the full-panel discrimination while reducing mean burden by roughly 60%.

These numbers are synthetic only.

## Naive singleton-greedy policy

A second policy could only inspect one candidate observation at a time.

Because `A` and `B` have essentially zero individual marginal information, the singleton-greedy policy never discovers that measuring the pair is valuable.

Approximate evaluation:

```text
AUC                         ~0.970
overall error               ~6.3%
error within confident set  ~3.3%
average added burden        ~8.52
median added burden         6.0
```

Therefore the naive greedy policy was both:

- more burdensome than the pair-aware adaptive policy; and
- less accurate in this synthetic surface.

## Formal counterexample to greedy selection

The repository now locks a simpler known-answer set-function example.

Let three observations have equal burden:

```text
V(A)   = 0
V(B)   = 0
V(C)   = 4
V(A,B) = 10
```

with budget 2.

A marginal-gain greedy policy chooses `C` first and cannot recover the `A+B` synergy.

Exact subset search returns:

```text
A+B
```

This proves that:

```text
Greedy Information-Per-Burden Is Not Generally Safe Under Complementarity
```

The failure does not depend on oncology; it is a generic set-function property.

## Theory correction — observation value is set-conditional

v0.10 used a marginal quantity such as:

```text
Delta Information / Delta Burden
```

v0.11 replaces the naive interpretation with a conditional set value:

```text
V(q | Q_current)
```

and explicitly permits bundle actions:

```text
V({q_i, q_j} | Q_current)
```

The acquisition engine must therefore consider at least:

- singleton actions;
- selected low-order bundles;
- known mechanistic complements;
- nuisance-diverse combinations.

Full powerset search is exponential and may be infeasible for large candidate sets, so the simulation harness should compare practical approximations against exact small-panel optima.

## Sequential Cancer Debugger

The emerging loop is:

```text
current evidence
    -> enumerate competing latent worlds
    -> semantic + support validation
    -> identify unresolved decision-relevant distinctions
    -> score candidate observations AND candidate bundles
    -> choose lowest-burden high-value action
    -> observe
    -> contract posterior
    -> STOP if ambiguity target is met
    -> otherwise repeat
```

The key point is that **not every patient receives the same panel**.

Patients whose posterior resolves early should stop early.

Patients whose evidence lies near a decision boundary may justify additional observation.

## Safety / research implication

The phrase "minimum intervention" now has three nested requirements:

```text
1. do not measure without a declared unresolved question;
2. among adequate options, prefer lower burden;
3. do not let low burden justify an observation set that cannot separate the relevant worlds.
```

This is still a research-design principle, not a clinical recommendation.

## New optimization form

A sequential action can be written as:

```text
a_t* = argmax_a [
    ExpectedDecisionAmbiguityReduction(a | evidence_t)
  + lambda * ModelFamilyDiscrimination(a | evidence_t)
  - mu * PatientBurden(a)
  - nu * DelayCost(a)
  - xi * NuisanceRedundancy(a)
]
```

where `a` may be a singleton observation or a qualified bundle.

A hard-constrained version remains preferable when a minimum identifiability target is known.

## New no-go

Do not assume adaptive greedy acquisition is automatically superior to a static panel.

If the value surface is strongly non-submodular because of complementarity, interaction, censoring, or shared nuisance structure, a myopic policy can spend **more** burden while obtaining **less** information.

Therefore adaptive acquisition itself needs adversarial validation.

## Next falsifiers

1. compare exact dynamic programming, singleton greedy, pair-aware greedy and beam search;
2. add observation delay and hard decision deadlines;
3. add assay failure / unavailable observations;
4. add patient-specific burden ceilings linked to host-reserve state;
5. test adaptive policies under correlated nuisance and missing observations;
6. test whether expected-information policies remain calibrated under model misspecification;
7. evaluate regret relative to exact small-panel optimum;
8. find conditions where a static predeclared panel is safer than adaptation;
9. keep treatment action distinct from measurement acquisition;
10. move to public-data qualification only after policy-level simulation stabilizes.

## Claim boundary

All channels, burdens, posterior thresholds and numerical results in this note are synthetic. They do not rank real cancer tests, recommend diagnostic procedures, or guide treatment. The result is a mathematical / research-design falsifier for observation policy only.
