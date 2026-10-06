# Cancer Latent-State Digital Twin v0.3 — adversarial checkpoint

Date: 2026-10-06
Status: simulation-stage working theory / adversarially stress-tested / not clinical authority
Parent: `CANCER_LATENT_STATE_DIGITAL_TWIN_V0_2_2026-10-06.md`
Implementation primitive: `src/dissociated_control_systems/cancer_twin.py`
Known-answer tests: `tests/test_cancer_twin.py`

## Meta-meta question

Can a cancer latent-state Twin be made to fail confidently even when apparently useful longitudinal observations are available?

The v0.3 loop treats high-confidence wrong predictions as the primary research object.

```text
Good average discrimination != safe latent-state inference
High-confidence error -> failure biopsy -> model-family revision
```

## Core revision: state != transition law != observation law

v0.2 separated latent biology from observation nuisance state.

v0.3 adds an equally important third object:

```text
x_t      latent biological state
Theta    transition law / patient-specific dynamics
Phi      observation law / sensor nuisance state
```

General form:

```text
x_(t+1) ~ F(x_t, u_t, Theta) + process_noise
z_t     ~ H(x_t, Phi) + observation_noise
```

A patient may share the same current state and sensor outputs with another patient while having a different `Theta`, and therefore a different future.

This creates a new invariant:

```text
Same Current State != Same Future Dynamics
State Estimation != Transition-Kernel Identification
```

## Structural counterexamples now locked in code

### Imaging equivalence

```text
(B_s, B_r) = (0.9, 0.1)
(B_s, B_r) = (0.1, 0.9)
```

Both have the same total burden but different resistant fraction.

### ctDNA burden/shedding equivalence

```text
signal = phi_s * B_s + phi_r * B_r
```

Different burden/shedding combinations can emit the same ctDNA value.

### Transition-law equivalence at one time point

Two synthetic patients can have exactly the same `x_t` and exactly the same imaging/ctDNA while differing in resistant growth and resistant treatment sensitivity.

After the same treatment-history input, their futures diverge.

The repository tests treat these as known-answer non-identifiability cases.

## Adversarial campaign A

A private analysis run generated 80,000 synthetic patients with nearly matched baseline tumor burden and variation in:

- sensitive / resistant fraction;
- resistant growth rate;
- treatment sensitivity of both compartments;
- immune activity and suppressive pressure;
- host reserve;
- treatment-associated selection;
- ctDNA shedding of both compartments;
- resistance-signal detectability;
- imaging / ctDNA / immune observation noise.

A deliberately difficult apparent-response cohort was selected by day-30 imaging ratio:

```text
0.32 < imaging_30 / imaging_0 < 0.42
```

Cohort size: 20,484 synthetic patients.
Synthetic future-escape prevalence: ~36.2%.

The values below are synthetic held-out discrimination metrics, not clinical performance estimates.

### Single / day-30 observations

```text
imaging day30 only       AUC ~0.524
ctDNA day30 only         AUC ~0.562
coarse immune day30      AUC ~0.496
resistance signal day30  AUC ~0.855
all day30 channels       AUC ~0.860
```

The apparent-response selection intentionally removes much of the information from the day-30 imaging scalar.

### Serial observations

```text
serial imaging           AUC ~0.920
serial ctDNA             AUC ~0.761
serial resistance        AUC ~0.882
serial multi-channel     AUC ~0.957
```

The qualitative result is:

```text
Longitudinal Dynamics > One Snapshot
Orthogonal Channel > Redundant Channel
More Sensors != Automatically More Information
```

## High-confidence failure biopsy

The important cases were synthetic patients that truly escaped but were assigned low escape probability by the day-30 multi-channel model.

Compared with confidently controlled true negatives, the strongest latent differences were not primarily current tumor size.

The largest standardized differences were approximately:

```text
resistant intrinsic growth rate      +1.86 SD
resistant treatment sensitivity      -0.93 SD
resistant fraction at day30          +0.95 SD
resistance-sensor detectability       lower
```

After adding serial observations, the dominant hidden variable remained resistant intrinsic growth (~+1.83 SD), with low resistance-sensor detectability and lower resistant treatment sensitivity also remaining important.

Interpretation:

> A rich snapshot can still fail when the important hidden variable is a transition parameter rather than a state variable.

This motivates explicit posterior inference over `Theta`, not only `x_t`.

## Adversarial campaign B — model-family swap

To test whether the result was an artifact of one ODE family, a second synthetic family generated 45,000 patients using:

- logistic tumor growth;
- a carrying-capacity term;
- immune exhaustion at higher burden;
- independently sampled observation nuisance parameters.

An analogous day-30 apparent-response cohort contained 12,694 patients.

Synthetic held-out results again favored longitudinal and resistance-aware observations:

```text
imaging day30 only       AUC ~0.513
ctDNA day30 only         AUC ~0.564
coarse immune day30      AUC ~0.495
resistance day30         AUC ~0.819
all day30 channels       AUC ~0.824
serial imaging           AUC ~0.891
serial ctDNA             AUC ~0.743
serial resistance        AUC ~0.862
serial multi-channel     AUC ~0.949
```

Thus the central ranking survived a substantial model-family change.

This is still synthetic support, not human validation.

## Observation-time frontier

In campaign A, using the same multi-channel observation concept at progressively later times produced approximately:

```text
day14 panel  AUC ~0.822
day30 panel  AUC ~0.861
day60 panel  AUC ~0.928
```

Therefore the objective cannot be prediction accuracy alone.

Waiting longer reveals dynamics but can reduce decision value.

Candidate observation objective:

```text
q* = argmax_q [
    expected_information_gain(q)
  + lambda * decision_value(q)
  - mu * observation_burden(q)
  - nu * delay_cost(q)
  - xi * redundancy(q)
]
```

The `delay_cost` term is new in v0.3.

## New adversarial classes

The Twin should explicitly generate and search for at least these classes:

### A. Sensor-silent escape

```text
low shedding / low assay detectability
+ growing resistant compartment
```

### B. Radiographically quiet clonal escape

```text
total burden stable or falling
+ resistant fraction rising
```

### C. Transition-kernel trap

```text
current state looks controlled
+ resistant growth high
+ resistant treatment sensitivity low
```

### D. Compensated immune appearance

```text
high effector signal
+ high suppressive pressure
```

A one-dimensional immune score may collapse this pair.

### E. Treatment-dependent fragile control

```text
low current burden
+ negative drift only while treatment input remains present
```

This state must not be confused with self-sustaining control.

### F. History aliasing

```text
same current state
+ different prior treatment / selection history
-> different hidden clone composition / transition law
```

## Transition-kernel posterior

The Twin target becomes:

```text
p(x_t, Theta, Phi | z_(0:t), u_(0:t))
```

rather than only:

```text
p(x_t | z_(0:t))
```

Important quantities include posterior distributions over:

- resistant net growth under each clinically relevant treatment state;
- resistant treatment sensitivity;
- clone-transition / selection parameters;
- immune activation and suppression dynamics;
- observation shedding/detectability parameters.

## Fragile control

Define a treatment-conditioned local drift margin rather than only current burden.

For a resistant compartment:

```text
m_r(u) =
    treatment_kill_r(u)
  + immune_kill_r
  - intrinsic_growth_r
```

Candidate interpretation:

```text
m_r >> 0    robust local control under declared input
m_r ~ 0     fragile boundary
m_r < 0     local escape tendency
```

This is a synthetic model descriptor, not a validated clinical score.

A patient can therefore satisfy:

```text
current burden low
AND
m_r approximately 0
```

and still be a fragile-normal state.

## Information policy correction

A biologically interesting measurement is not automatically an informative measurement.

In both synthetic families, a coarse immune scalar added little discriminative information in the selected apparent-response cohort.

Therefore:

```text
Biological Importance != Observation Information Gain
```

Immune channels should be decomposed or rejected according to whether they reduce posterior uncertainty and survive held-out validation.

## External evidence alignment

This synthetic architecture is directionally compatible with current oncology research showing that:

- longitudinal ctDNA can expose resistant-clone dynamics across treatment;
- resistance mutations can become detectable during radiographic stability;
- ctDNA interpretation is limited by heterogeneous shedding and technical/biological false negatives;
- liquid-blood immune measurements are complementary to, not complete substitutes for, the tumor immune microenvironment;
- cancer digital twins require verification, validation, uncertainty quantification, and repeated recalibration.

These literature correspondences do not validate this particular synthetic model.

Relevant public references for later qualification include:

- PMID 39992716 — longitudinal ctDNA and metastatic prostate cancer clonal evolution;
- Nature 2025, doi:10.1038/s41586-025-09580-0 — CloneSeq-SV longitudinal ovarian cancer clone tracking;
- PMID 42528143 — acquired KRAS resistance detected during radiographic stability;
- PMID 42795008 — NSCLC ctDNA MRD biology, low-shedding and false-negative limitations;
- Nature Reviews Genetics 2026, doi:10.1038/s41576-026-00974-y — liquid biopsy advances and limitations;
- PMID 42116079 — TumorTwin framework;
- PMID 39825103 — VVUQ for precision-medicine digital twins;
- PMID 39627216 — >100,000 virtual trajectories in a multiscale immune-surveillance model.

## v0.3 falsification program

The next loop should attack:

1. treatment-history missingness;
2. irregular sampling intervals;
3. sensor drift / platform changes;
4. clone below detection followed by expansion;
5. correlated observation errors;
6. model misspecification where no candidate `F` family is correct;
7. domain shift in which an entire parameter regime is held out;
8. false-confidence calibration under all of the above.

Primary safety metric for the simulation stage:

```text
FalseConfidenceRate =
P(model confidence > threshold AND prediction wrong)
```

A high AUC with unacceptable FalseConfidenceRate is a failed Twin.

## v0.3 convergence statement

The current synthetic evidence supports a stronger architecture than v0.2:

```text
Latent-state debugging alone is insufficient.
A credible cancer Twin must jointly debug:

1. biological state x;
2. patient-specific transition law Theta;
3. observation law Phi;
4. intervention/history input u.
```

The practical research principle remains:

```text
Observe aggressively; intervene conservatively.
```

But the observation target is now not just "what state is the cancer in?"

It is:

> Which latent state, transition law, and sensor law remain compatible with the full longitudinal history, and what smallest additional observation most efficiently separates the remaining worlds before the decision loses value?

## Claim boundary

All numerical results above are synthetic stress-test observations. They are not clinical sensitivity/specificity estimates, prognostic tools, treatment rules, or evidence for changing patient care.
