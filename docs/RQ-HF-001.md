# RQ-HF-001 — Hair-Follicle State Calibration and Recoverability

> Status: OPEN RESEARCH  
> Biological interpretation: PARTIAL / SOURCE-BOUND  
> Clinical authority: NONE  
> Human self-experiment authority: NONE

## Research question

Can age- and androgen-associated hair-follicle decline be usefully modeled as a
partially observed transition from a recoverable homeostatic state into a
hysteretic structural-lock state, and can the boundary of self-calibratable
control be detected before visible hair loss becomes severe?

The lane does **not** assume that conscious intention directly changes WNT,
DHT, PIEZO1, stem-cell abundance, or any other molecular variable.

Instead it tests the narrower control architecture:

~~~text
reference model
    ↓
observer
    ↓
state residual
    ↓
human / clinical controller
    ↓
autonomic + endocrine + behavioral + pharmacologic actuators
    ↓
follicle / niche / connective-tissue plant
    ↓
new observation
    ↓
model update
~~~

## Why DCS is relevant

The visible output "hair density" is a lossy observation. Similar output may be
compatible with different combinations of:

- androgen pressure;
- neuroendocrine stress load;
- regenerative signaling;
- progenitor-cell reserve;
- niche integrity;
- connective-tissue / mechanical lock.

Therefore:

~~~text
Hair output != unique follicle state
Normal appearance != guaranteed normal internal trajectory
Correct observation != guaranteed controllability
Awareness != direct molecular actuation
~~~

## Personal healthy counterfactual

Humans cannot load an earlier biological snapshot like a software image. HF01
therefore distinguishes three references:

1. population healthy reference;
2. within-person relatively spared occipital reference;
3. reconstructed personal counterfactual.

The occipital scalp is useful as a within-person comparator in male AGA because
paired vertex/occipital studies show molecular differences while sharing much of
the person's systemic environment. It is **not** assumed to be a perfect copy of
a healthy vertex.

~~~text
x*_vertex = T_occ_to_vertex(x_occipital, population priors, history)
residual  = x*_vertex - x_observed_vertex
~~~

The transformation T is an empirical object to be learned, not a hand-written
clinical truth.

## State model

The synthetic model committed in
`src/dissociated_control_systems/hair_follicle_model.py` uses:

~~~text
A = androgen pressure
Q = stress / neuroendocrine load
R = regenerative signaling competence
P = functional progenitor reserve
N = niche integrity
F = structural / mechanical lock
H = coarse hair output
~~~

All variables are normalized to [0, 1].

The model intentionally separates fast inputs from slow structure:

~~~text
fast:
    A, Q

medium:
    R

slow:
    P, H

very slow:
    N, F
~~~

This time-scale separation is a modeling hypothesis.

## Control channels

~~~text
u_behavioral
    primarily lowers Q in the synthetic model

u_antiandrogen
    primarily lowers A

u_regenerative
    increases regenerative/progenitor drive

u_structural
    reduces F and supports N
~~~

Names describe model roles, not treatment prescriptions.

## HF-VAL-001: synthetic hysteresis / reachability

The first executable question is deliberately non-clinical:

> Under the declared equations, can a slow positive-feedback structural state
> create a region in which reducing upstream disturbances is no longer enough
> to recover the healthy-output attractor?

Acceptance conditions:

1. all states remain bounded;
2. coarse output is non-identifying;
3. early-state output obeys a declared intervention ordering;
4. a late state fails to recover under upstream-only correction;
5. a structural actuator restores reachability in that same synthetic state;
6. the reachable region is nested when additional actuators are added;
7. the qualitative result survives bounded coefficient perturbation.

Current deterministic baseline:

~~~text
early state:
    combo > antiandrogen > behavioral >= none

late state:
    behavioral + antiandrogen -> remains locked
    behavioral + antiandrogen + structural -> escapes lock

initial structural-lock threshold for final H >= 0.50:
    behavioral + antiandrogen                 : 0.35
    behavioral + antiandrogen + regenerative : 0.80
    behavioral + antiandrogen + structural   : 1.00
~~~

These threshold numbers are properties of the synthetic coefficients only.

A fixed-seed 300-sample ±20% all-coefficient perturbation preserves the core
ordering/hysteresis acceptance rule in at least 94% of cases.

## What would falsify the useful version of the model?

The biological interpretation should be weakened or rejected if better data
show that:

- miniaturization is adequately predicted without a slow state;
- structural/mechanical variables do not add predictive power after androgen
  and cycle state are controlled;
- longitudinal output trajectories do not exhibit any measurable path
  dependence;
- within-person vertex/occipital comparison does not improve state estimation;
- adding richer probes does not reduce latent-state uncertainty;
- inferred "recoverability" does not predict response to independent,
  pre-specified interventions.

## Probe ladder

HF01 should not jump directly to invasive molecular measurement.

### Tier 0 — coarse longitudinal observer

- standardized photography;
- fixed-position trichoscopy;
- hair-diameter distribution;
- vellus/terminal fraction;
- follicular-unit occupancy.

### Tier 1 — cycle observer

- phototrichogram;
- growth rate;
- anagen/telogen estimate.

### Tier 2 — systemic/context observer

- sleep timing/regularity;
- HRV or other autonomic measures;
- validated stress measures;
- clinically indicated laboratory evaluation for differential diagnoses.

These signals are contextual covariates; they are not assumed to identify a
follicular molecular state.

### Tier 3 — research physiology

- scalp microvascular measurements;
- mechanical/elasticity measurements where validated;
- high-frequency imaging where appropriate.

### Tier 4 — molecular research

- paired follicle/scalp sampling;
- transcriptomics / single-cell / spatial assays;
- stem/progenitor markers;
- ECM/mechanical pathway assays.

Invasive tests require ordinary research/clinical governance.

## Meta-adaptive loop

~~~text
observe
  ↓
estimate posterior state
  ↓
compare with reconstructed reference
  ↓
select bounded intervention
  ↓
predict trajectory
  ↓
observe delayed response
  ↓
prediction error
  ↓
parameter update
  ↓
if residual structure persists:
    model-class update
~~~

The key rule is:

> Do not force the body to fit the model. Update the model when the body
> violates the prediction.

## QED boundary

HF01 may eventually prove statements **inside its declared mathematical model**.

It cannot derive a clinical theorem from synthetic dynamics.

Therefore the current strongest claim is:

> A DCS-compatible model exists in which visible output is non-identifying,
> recoverability shrinks as a slow structural state accumulates, and additional
> actuator classes expand the reachable set. Current human AGA literature
> supplies plausible biological candidates for several state variables, but
> does not yet validate the complete control model.

That is the boundary to attack next.
