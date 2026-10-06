# Cancer Latent-State Digital Twin v0.8 — active observation / model discrimination

Date: 2026-10-06
Status: simulation-stage falsification checkpoint / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_7_SUPPORT_AND_MODEL_MISSPECIFICATION_2026-10-06.md`

## Meta-meta target

v0.7 established a practical no-go:

> if two future worlds are observationally equivalent over every currently available channel, no inference algorithm can distinguish them before divergence.

v0.8 asks the next useful question:

> what kind of new observation actually breaks that equivalence class?

The target is not "more data" in the abstract.

It is **model-discriminating data**.

## Recalibration != new discrimination

The hidden-future-phenotype family from v0.7 was reused.

The original nominal-family predictor had approximately:

```text
AUC                    ~0.854
high-confidence error  ~15.8%
```

When labels from the shifted family were made available and the old score was recalibrated on that new family, patient-level confidence became substantially safer:

```text
AUC                    ~0.855
high-confidence coverage ~26%
high-confidence error    ~4.3%
```

The ranking AUC did not materially improve.

Interpretation:

```text
Recalibration Can Repair Probability Semantics
Recalibration Cannot Create Missing State Information
```

This distinction matters for post-deployment updating.

A newly calibrated model may become less overconfident while remaining unable to distinguish the causal worlds that matter.

## Redundant-observation attack

Four additional synthetic measurements were generated as noisy repeats of already-observed day-60 channels:

- imaging;
- ctDNA;
- resistance proxy;
- coarse immune score.

After shifted-family recalibration, each redundant measurement left held-out discrimination essentially unchanged:

```text
no additional channel       AUC ~0.855
repeat imaging              AUC ~0.855
repeat ctDNA                AUC ~0.855
repeat resistance proxy     AUC ~0.855
repeat coarse immune        AUC ~0.855
```

The exact synthetic decimals are not important.

The structural result is:

```text
More Samples Along The Same Observable Axis
    !=
More Latent-State Identifiability
```

Repeated measurements can reduce noise when noise is the problem.

They cannot resolve a structural equivalence class when the relevant hidden variable does not project onto that measurement axis.

## Orthogonal-marker campaign

A deliberately abstract new measurement was introduced:

```text
m = hidden_phenotype + noise
```

This is **not** a proposed clinical biomarker.

It represents any future measurement that is independently informative about the hidden aggressive world that existing channels cannot distinguish.

The marker was tested at several synthetic signal-to-noise levels.

Approximate held-out results after shifted-family training / recalibration:

```text
marker discrimination       future-outcome AUC
(hidden-world AUC)

~0.63                       ~0.862
~0.77                       ~0.880
~0.83                       ~0.893
~0.92                       ~0.916
~0.98                       ~0.939
~0.998                      ~0.955
~1.00                       ~0.968
```

The relationship was monotonic on this synthetic surface: as the new measurement better separated the competing hidden worlds, future-outcome discrimination recovered.

## Core principle — observational orthogonality

Define competing model worlds `M_a` and `M_b` that currently satisfy approximately:

```text
p(z_current | M_a) ~= p(z_current | M_b)
```

A useful next measurement `q` should maximize a separation quantity such as:

```text
D_q(M_a, M_b)
=
Divergence[
    p(q | M_a),
    p(q | M_b)
]
```

where the divergence can be KL, Jensen-Shannon, expected Bayes-factor separation, mutual information, or another qualified measure.

A repeated measurement with:

```text
D_q ~= 0
```

cannot break the equivalence class no matter how technically precise it is.

Thus:

```text
Precision != Orthogonality
More Precision On A Non-Discriminating Axis != State Recovery
```

## Active observation objective

The next-observation policy is refined to:

```text
q* = argmax_q [
    I(M ; q | current evidence)
  + lambda * I(Theta ; q | current evidence)
  + gamma * counterfactual_decision_value(q)
  - mu * patient_burden(q)
  - nu * delay_cost(q)
  - xi * redundancy(q)
  - psi * assay_uncertainty(q)
]
```

where:

- `M` is the competing model-family / mechanistic-world index;
- `Theta` is the transition-law parameter set;
- `patient_burden` explicitly penalizes invasive or burdensome measurements;
- `delay_cost` penalizes information that arrives too late to matter;
- `redundancy` penalizes measurements that mostly repeat existing axes.

## Minimum-intervention consequence

This creates a direct bridge to the branch North Star:

```text
Minimum Intervention / Maximum Observability
```

A theoretically good measurement is not the one that returns the largest data object.

It is the smallest / safest measurement that most strongly partitions the currently plausible future worlds.

The objective should therefore compare:

```text
information gained per unit burden
```

rather than information alone.

## Negative evidence

Repeated negative results can be informative only if the observation channel has known sensitivity to the competing hidden world.

If:

```text
P(negative | aggressive world)
```

is almost the same as:

```text
P(negative | controlled world)
```

then repeated negatives should not collapse the aggressive-world posterior.

Conversely, if a validated orthogonal marker has high sensitivity under the aggressive world, repeated qualified negatives can reduce its posterior probability.

Thus:

```text
Negative Result != Negative Evidence By Default
```

The likelihood model determines whether absence is informative.

## Recalibration / re-identification split

Future deployment should distinguish two update modes.

### Mode A — recalibration

Use when ranking / latent discrimination remains valid but predicted probabilities drift.

Target:

```text
P(Y | score)
```

### Mode B — re-identification

Use when new evidence shows the old observation surface cannot distinguish relevant worlds.

Target:

```text
new observation channel
or
new transition model
or
broader model family
```

Recalibration must not be presented as mechanism recovery.

## Measurement qualification contract

A candidate new observation should earn adoption only if it demonstrates, on held-out synthetic and later empirical data:

1. incremental model-family discrimination beyond existing channels;
2. incremental transition-law identification;
3. stable assay semantics / calibration lineage;
4. acceptable patient burden;
5. useful acquisition time;
6. robustness to censoring / missingness;
7. benefit that survives external / regime-held-out validation.

## Practical simulator output

Instead of recommending a measurement by name, the simulation should emit a ranked **measurement-property request**:

```text
Current unresolved ambiguity:
    resistant future-growth law vs controlled law

Needed observation property:
    channel correlated with resistant intrinsic growth / phenotype
    conditional on existing imaging + ctDNA + current clone proxy

Required timing:
    before decision horizon

Desired burden:
    lowest feasible

If unavailable:
    retain TRANSITION_UNRESOLVED
```

This keeps the Twin from inventing a biomarker merely because the mathematical model wants one.

## v0.8 convergence update

The research loop has shifted from:

```text
predict outcome better
```

to:

```text
1. enumerate competing latent worlds;
2. identify which worlds matter for counterfactual decisions;
3. find the smallest observation that separates those worlds;
4. if no such qualified observation exists, preserve uncertainty.
```

The strongest new invariant is:

```text
Data Volume != Identifiability
Orthogonal Information -> Equivalence-Class Contraction
```

## Next falsifiers

1. optimize observation choice under explicit synthetic burden budgets;
2. allow multiple weak orthogonal measurements and test whether they compose;
3. test correlated orthogonal markers that appear independent but share one nuisance cause;
4. active measurement selection under uncertain future intervention paths;
5. value-of-information stopping rule: when is another measurement not worth its burden/delay?;
6. model-family discrimination using real public longitudinal oncology datasets when a qualified dataset is identified;
7. require pre-registered candidate observation properties before looking at outcome labels;
8. distinguish biomarkers of current burden from biomarkers of transition-law parameters.

## Claim boundary

The abstract orthogonal marker in this note is synthetic. It is not a proposed assay, biomarker, diagnostic, prognosis, or treatment recommendation. The numerical results demonstrate an identifiability principle only.
