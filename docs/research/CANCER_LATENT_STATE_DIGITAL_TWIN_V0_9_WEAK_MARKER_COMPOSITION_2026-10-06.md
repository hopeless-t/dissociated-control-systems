# Cancer Latent-State Digital Twin v0.9 — weak-marker composition / nuisance diversity

Date: 2026-10-06
Status: simulation-stage falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_8_ACTIVE_OBSERVATION_2026-10-06.md`

## Meta-meta target

v0.8 established that a new observation must project onto the unresolved latent distinction.

v0.9 asks:

> can several weak observations compose into one useful discriminator, and when does that composition fail?

## Synthetic weak-marker campaign

The same hidden-future-phenotype world from v0.7/v0.8 was used.

Each synthetic candidate marker had only weak discrimination individually:

```text
hidden-world AUC ~0.64
```

The markers were not intended to represent any named assay.

### Independent weak markers

When marker noise was independently generated across channels, averaging / joint modeling progressively improved hidden-world discrimination:

```text
1 weak marker   hidden-world AUC ~0.64
2 weak markers  hidden-world AUC ~0.69
4 weak markers  hidden-world AUC ~0.76
8 weak markers  hidden-world AUC ~0.85
```

Future-outcome discrimination also improved from roughly:

```text
~0.86 -> ~0.90
```

across the same synthetic expansion.

The effect is modest per channel but cumulative when the errors are genuinely diverse.

## Correlated-nuisance attack

The experiment was repeated with marker noises sharing a strong common nuisance component (synthetic correlation ~0.8).

Results:

```text
2 correlated markers  hidden-world AUC ~0.64
4 correlated markers  hidden-world AUC ~0.65
8 correlated markers  hidden-world AUC ~0.66
```

The apparent panel size increased eightfold while effective discrimination barely improved.

This yields the invariant:

```text
Number Of Measurements != Effective Observation Rank
```

and:

```text
Shared Nuisance Can Make Many Sensors Behave Like One Sensor
```

## Conditional information, not raw modality count

For candidate channel `q_j`, the useful quantity is not only:

```text
I(M ; q_j)
```

but the incremental conditional information:

```text
I(M ; q_j | q_1, ..., q_(j-1), current evidence)
```

A marker can look informative alone yet contribute almost nothing after the existing panel is known.

The measurement-selection problem therefore becomes submodular-like rather than additive.

## Effective observation rank

Define the local sensitivity matrix of observations to latent distinctions:

```text
J_obs[i,j] = partial expected_observation_i / partial latent_dimension_j
```

A large number of channels with nearly collinear rows does not improve identifiability much.

The Twin should track an effective rank / diversity descriptor rather than a modality count.

Candidate qualitative rule:

```text
Panel Value
    grows with latent-axis coverage
    grows with independent error structure
    shrinks with conditional redundancy
    shrinks with shared nuisance
```

## Nuisance graph

Observation channels should carry a nuisance-dependency graph.

Example abstract structure:

```text
latent world M
   -> assay A
   -> assay B
   -> imaging C

shared pre-analytic nuisance P
   -> assay A
   -> assay B

scanner nuisance S
   -> imaging C
```

Then A and B are not independent confirmations merely because they have different names.

This is especially important for panels derived from the same specimen, same preprocessing pipeline, same sequencing chemistry, same normalization layer, or same latent surrogate.

## Observation objective update

v0.8 objective:

```text
information gain
+ model discrimination
+ counterfactual decision value
- burden
- delay
- redundancy
- assay uncertainty
```

v0.9 adds an explicit nuisance-diversity term:

```text
q* = argmax_Q [
    I(M ; Q | current evidence)
  + lambda * I(Theta ; Q | current evidence)
  + gamma * counterfactual_decision_value(Q)
  + eta * nuisance_diversity(Q)
  - mu * patient_burden(Q)
  - nu * delay_cost(Q)
  - xi * conditional_redundancy(Q)
  - psi * assay_uncertainty(Q)
]
```

`Q` may be a panel rather than one observation.

## Minimum-intervention consequence

This strengthens the branch principle:

```text
Minimum Intervention / Maximum Observability
```

because a smaller panel with orthogonal latent sensitivity and diverse nuisance structure can dominate a larger redundant panel.

The research target is therefore not maximal biomarker collection.

It is a **minimal sufficient separating set**.

Candidate definition:

```text
Q_min = argmin_Q burden(Q)
subject to:
    posterior ambiguity <= epsilon
    counterfactual decision ambiguity <= delta
    support contract satisfied
```

## Strong falsifier

The composition hypothesis should be weakened if independent weak channels fail to improve held-out model discrimination after explicit calibration and conditional-information accounting.

Likewise, apparent gains that disappear when shared nuisance is modeled should be classified as pseudo-replication rather than independent evidence.

## Next falsifiers

1. solve the minimal sufficient separating-set problem under synthetic cost budgets;
2. test three-way nuisance structures rather than one common correlation coefficient;
3. let nuisance dependencies drift over time;
4. distinguish biological correlation from technical nuisance correlation;
5. test panels where one high-burden highly-informative observation competes with several low-burden weak observations;
6. value-of-information stopping rule under patient-burden constraints;
7. identify public multimodal longitudinal cancer datasets suitable for a later domain-local qualification phase.

## Claim boundary

All markers and numerical values in this note are synthetic. The result supports an information-theoretic design principle only; it does not validate any specific biomarker panel, assay, diagnostic strategy, prognosis, or treatment decision.
