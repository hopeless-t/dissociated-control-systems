# Cancer Latent-State Digital Twin v0.2

Date: 2026-10-06
Status: simulation-stage working theory / falsifiable / not clinical authority
Parent: `CANCER_SURVIVOR_LATENT_STATE_DEBUGGER_2026-10-06.md`

## Objective

Develop the cancer-survivor branch into a simulation-complete theory before any clinical interpretation.

The central goal is not to explain survival with one favored mechanism. It is to determine whether superficially similar clinical states can be decomposed into distinct latent dynamical worlds early enough to improve observation and reduce unnecessary intervention.

Core rule:

```text
Observe aggressively; intervene conservatively.
```

In this branch, research perturbations should primarily be pre-existing treatment transitions, natural longitudinal changes, and already-collected measurements rather than intentionally induced patient stress.

## Three-layer architecture

### 1. Latent biological state

Use a minimal mechanistic state vector:

```text
x_t = (
  B_s,      # treatment-sensitive tumor burden
  B_r,      # resistant / escape-capable tumor burden
  E,        # effective anti-tumor immune activity
  M,        # suppressive / escape-supporting microenvironment pressure
  H         # host reserve / treatment tolerance state
)
```

The symbols are model variables, not claims that one biomarker maps one-to-one to each variable.

### 2. Observation state

Separate sensors from biology:

```text
z_t = (
  imaging,
  ctDNA,
  clonal / resistance signal,
  immune panel,
  routine host-state labs,
  clinical state
)
```

Critically, ctDNA requires nuisance observation parameters:

```text
ctDNA_t = phi_s * B_s + phi_r * B_r + assay_noise
```

where `phi_*` encode shedding / sampling / assay effects.

Therefore:

```text
ctDNA Value != Tumor Burden
ctDNA Negativity != Guaranteed Biological Absence
Sensor State != Biological State
```

### 3. Intervention / history input

```text
u_t = clinically justified treatment / treatment transition
```

The dynamics are conditioned on treatment history:

```text
x_(t+1) ~ F(x_t, u_t, theta) + process_noise
z_t     ~ H(x_t, phi) + observation_noise
```

Without `u_t`, treatment sensitivity and natural growth cannot generally be separated.

## Minimal mechanistic family

One useful bootstrap family is:

```text
dB_s/dt = growth_s - immune_kill_s - treatment_kill_s

dB_r/dt = growth_r - immune_kill_r - treatment_kill_r
            + treatment-associated selection / transition

dE/dt   = tumor-driven activation
            - decay
            - suppression by M
            + immunotherapy-dependent modulation

dM/dt   = tumor-driven suppressive pressure
            - clearance
            - treatment-dependent modulation

dH/dt   = recovery
            - treatment toxicity
            - disease burden cost
```

No single coefficient should be interpreted clinically until identified from domain-local data.

## Structural no-go results

These are theory-level constraints, not empirical guesses.

### No-go 1: imaging alone

If:

```text
imaging ~ B_s + B_r
```

then imaging alone cannot uniquely recover the resistant fraction.

Two states can satisfy:

```text
B_s + B_r = constant
```

while having very different future relapse dynamics.

### No-go 2: ctDNA alone

If:

```text
ctDNA = phi * B
```

then `B` and `phi` are structurally confounded without additional information.

For any positive scale `lambda`:

```text
B'   = lambda * B
phi' = phi / lambda
```

produces the same ctDNA observation.

Thus a ctDNA-only twin must not claim unique tumor burden unless shedding / assay state is independently constrained.

### No-go 3: one immune scalar

A single immune score can collapse distinct worlds such as:

```text
high effector + high suppressive pressure
low effector  + low suppressive pressure
```

into similar ratios.

Therefore immune observables should earn inclusion by information gain rather than being assumed useful because immune biology is important.

### No-go 4: survivor status does not identify cause

```text
Survivor -> inferred mechanism
```

is invalid without controlling for treatment history, baseline disease state, selection effects, reverse causality, and competing explanations.

## Latent basins

Do not force all trajectories into survivor / non-survivor binary labels.

Candidate dynamical regimes:

```text
CONTROLLED
DORMANT_OR_MRD
IMMUNE_CONTROLLED
TREATMENT_DEPENDENT_CONTROL
RESISTANT_ESCAPE
MIXED_OR_UNCERTAIN
```

The research task is to infer basin membership and transition risk, not merely final status.

## Change-point objective

For matched apparently similar trajectories, estimate:

```text
t* = earliest reproducible time at which posterior trajectory classes diverge
```

The key research question becomes:

> When did two superficially equivalent patients stop being dynamically equivalent, and which independent observation channel first revealed it?

## Simulation campaign 2026-10-06

A bounded synthetic experiment generated 30,000 virtual patients from nearly identical coarse baseline tumor burdens while varying:

- resistant fraction;
- immune-effector strength;
- suppressive pressure;
- host reserve;
- treatment sensitivity;
- mutation / selection parameters;
- ctDNA shedding;
- observation noise.

The simulation deliberately generated patients with the same visible starting state but different latent worlds.

Outcome label for this synthetic experiment only:

```text
controlled at day 180 <-> total modeled burden < 0.05
```

This threshold is a fixture, not a clinical cutoff.

### Matched early-imaging-response slice

A subset of 7,493 virtual patients was selected with nearly the same early imaging-response ratio:

```text
0.29 < imaging_day30 / imaging_day0 < 0.38
```

The endpoint remained nearly balanced:

```text
synthetic control rate ~47.4%
```

Thus similar early imaging response did not determine future trajectory.

### Single-early-surface discrimination

Illustrative held-out AUCs in the bounded synthetic fixture:

```text
imaging only                  ~0.713
ctDNA only                    ~0.607
resistance-clone proxy        ~0.700
imaging + resistance proxy    ~0.787
all measured channels         ~0.788
```

Interpretation:

- ctDNA is not automatically the best state estimator once shedding uncertainty is explicit;
- an orthogonal resistance/clonal channel can split worlds that imaging alone merges;
- adding every channel provides little benefit if the added channel is redundant or noisy.

These are model results only, not clinical performance estimates.

### Serial observation experiment

Using longitudinal observations at synthetic days 14, 30, and 60:

```text
serial imaging                ~0.895
serial ctDNA                  ~0.788
serial resistance proxy       ~0.740
serial imaging + resistance   ~0.908
all serial channels           ~0.911
```

The main result is structural rather than numerical:

```text
Longitudinal State Change > Single Snapshot
Orthogonal Channel > Redundant Channel
More Sensors != More Information By Default
```

### Negative result: immune score

In the current bootstrap model, a coarse immune-balance score added little or no predictive information after imaging.

This is intentionally preserved as a falsifier:

```text
Immune Biology Is Important
    !=
Any Immune Biomarker Improves The Twin
```

The immune branch must therefore test richer observables and independent validation rather than assume success.

## Literature consistency checks

Current external work supports important pieces without proving this model:

- ultrasensitive longitudinal ctDNA can provide early molecular-response information during checkpoint inhibition;
- longitudinal ctDNA can reveal resistant-clone dynamics and treatment-emergent alterations;
- ctDNA MRD remains limited by variable shedding, assay interpretation, timing, and false-negative / false-positive behavior;
- digital-twin oncology frameworks now explicitly support longitudinal re-calibration and uncertainty quantification;
- multiscale immune-surveillance simulations have already generated >100,000 virtual patient trajectories and recovered multiple control/escape regimes.

These observations justify the modeling direction but do not validate the specific DCS state variables or equations.

## Bayesian twin target

The operational inferential object should be a posterior ensemble:

```text
p(x_t, theta, phi | z_0:t, u_0:t)
```

not one fitted hidden state.

Maintain multiple plausible parameter sets / model families until data separate them.

## Sensor-selection objective

Candidate next observation channel `q` should be selected by expected information value, burden, and redundancy:

```text
q* = argmax_q [
  EIG(q)
  + lambda * early_divergence_value(q)
  - mu * patient_burden(q)
  - nu * assay_cost(q)
  - xi * redundancy(q)
]
```

This creates the intended clinical-facing principle:

```text
Minimum Additional Intervention
Maximum State Disambiguation
```

## Simulation acceptance stack

The theory should not be considered simulation-converged until it passes all of the following.

### A. Known-answer state recovery

Generate synthetic patients from known ground truth and require posterior recovery / calibrated uncertainty.

### B. Observation ablation

Remove each sensor in turn and quantify information loss.

A sensor that repeatedly contributes no independent information should be removed from the canonical minimum set.

### C. Nuisance stress

Sweep:

- ctDNA shedding;
- assay detection floor;
- sampling cadence;
- missing measurements;
- measurement error;
- imaging lag;
- immune-panel noise;
- treatment-history uncertainty.

Core claims must survive plausible nuisance ranges.

### D. Model-family stress

Repeat the same inference question under multiple families:

```text
ODE compartment model
switching state-space model
clone-evolution model
agent / multiscale surrogate
```

Keep only conclusions invariant across families or explicitly mark family dependence.

### E. Counterexample mining

Search deliberately for:

```text
same imaging, different future
same ctDNA, different true burden
ctDNA decline without durable control
stable imaging with resistant-clone expansion
molecular response with inflammatory / imaging discordance
apparent immune improvement caused by state-selection artifact
```

Each discovered counterexample becomes a permanent regression fixture.

### F. Calibration, not just discrimination

Require more than AUC.

Track:

```text
Brier score
calibration slope/intercept
posterior credible-interval coverage
negative log likelihood
change-point lead-time error
false-confidence rate
```

A confident wrong twin is worse than an explicit UNKNOWN.

### G. Held-out regime validation

Hold out whole trajectory regimes / parameter blocks, not only random patients.

This tests extrapolation rather than interpolation memorization.

## Simulation convergence rule

Call the current theory simulation-converged only when:

1. major qualitative conclusions survive plausible model families;
2. posterior coverage remains calibrated under nuisance sweeps;
3. no bounded counterexample invalidates the core invariants;
4. added sensor channels produce negligible expected information gain;
5. remaining ambiguity is explicitly classified as structural non-identifiability;
6. the model correctly returns `UNKNOWN` when evidence cannot distinguish candidate worlds.

Formally:

```text
max_q EIG(q) < epsilon
AND
core invariants stable across model family / nuisance ensemble
AND
false-confidence rate <= declared bound
```

## Current theoretical fixed point

The branch currently favors this abstraction:

```text
Cancer Survivor Research
    != search for one survivor trait

Cancer Survivor Research
    = infer latent dynamical basins from longitudinal multi-channel evidence,
      locate the earliest reproducible divergence,
      identify the minimum observation set that distinguishes the basins,
      and preserve uncertainty when states remain observationally equivalent.
```

The most important cross-domain lesson from the visual debugger remains:

```text
Coarse Normality / Stability = Equivalence Class, Not Unique State
```

For oncology, the practical translation is:

> Treat imaging status, ctDNA status, and survivor labels as observations emitted by a hidden dynamical system. Never promote any one observation directly into the hidden state itself.

## Clinical boundary

This note is not treatment guidance, prognosis, or a patient-testing protocol. Simulation performance does not authorize treatment escalation, de-escalation, or replacement of established clinical assessment. Clinical utility must be demonstrated separately by prospective domain-specific trials.
