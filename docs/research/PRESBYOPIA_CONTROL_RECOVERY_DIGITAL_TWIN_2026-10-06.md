# Presbyopia Control-Recovery Digital Twin

Date: 2026-10-06
Status: converged working hypothesis / research branch
Scope: DCS / presbyopia / accommodation / control-space recovery / Monte Carlo digital twin
Parent branch: `MUROFUSHI_MIZOGUCHI_CONTROL_BRANCH_2026-10-06.md`

## Research question

Can age-related loss of near vision be modeled not only as lens stiffening, but as a broader loss of *accessible control space* across optics, mechanics, neural control, sensory cues, and perceptual decoding?

The central DCS framing is:

> Presbyopia may contain both genuinely lost physical capability and capability that remains physically present but is no longer fully accessible through the learned controller.

This branch does **not** assume that training can reverse all presbyopia. It explicitly separates mechanical limits from control and perceptual compensation.

## Core system model

A useful first decomposition is:

```text
neural controller
    -> ciliary actuator
    -> sclera / choroid / zonular transmission
    -> crystalline lens deformation
    -> retinal image
    -> perceptual decoder
```

The original latent-state proposal was:

```text
(K_L, K_S, eta, F_C, w, G, tau)
```

where:

- `K_L`: effective crystalline-lens stiffness
- `K_S`: effective surrounding-structure stiffness (sclera/choroid/etc.)
- `eta`: force-transmission efficiency from actuator to lens deformation
- `F_C`: available ciliary actuator force
- `w`: sensory-cue weighting
- `G`: perceptual/decoder effectiveness
- `tau`: accommodation response time constant

### Identifiability correction

The first meta-loop exposed an important flaw: several variables cannot be uniquely recovered from accommodation output alone.

For example:

```text
H = F_C * eta
```

is directly relevant to output, but many different `(F_C, eta)` pairs produce the same `H`.

Likewise, without independent biomechanical measurements, `K_L` and `K_S` can collapse into a shared effective resistance term.

Therefore the first *observable* twin should use:

```text
x_obs = (K_eff, H, w_vec, G, delta, tau)
```

with:

```text
H = F_C * eta
w_vec = (w_blur, w_disparity, w_chromatic, w_proximity)
```

and:

- `K_eff`: effective mechanical resistance seen by the accommodation system
- `delta`: response latency before accommodation begins
- `tau`: convergence dynamics once the response has started

Only when additional measurements are available should the twin expand:

```text
K_eff -> (K_L, K_S)
H     -> (F_C, eta)
```

This prevents the model from claiming biologically specific explanations that are not identifiable from the data.

## Mechanical approximation

A minimal accommodation-capacity model is:

```text
A_mech ~ c * H / K_eff
```

or, before aggregation:

```text
A_mech ~ c * (F_C * eta) / R(K_L, K_S)
```

where `R` is an effective mechanical-resistance model.

Multiple candidate forms should be tested instead of fixing one representation:

```text
R1 = alpha*K_L + (1-alpha)*K_S
R2 = K_L^p * K_S^(1-p)
R3 = beta*K_L + (1-beta)*K_S
```

A result is more credible if its qualitative conclusion survives across plausible `R` families.

## Controller dynamics

For a stimulus frequency `f`, a minimal first-order controller/plant approximation is:

```text
T(f) = w_eff / sqrt(1 + (2*pi*f*tau)^2)
```

with a separate latency term `delta`.

Accommodation to demand `D` can then be approximated as:

```text
A(D,f) = min(D, A_mech) * T(f)
```

This model is deliberately simple. Its role is to expose assumptions and falsifiers, not to assert exact human-eye dynamics.

## Functional vision vs true accommodation

A critical distinction emerged from the Monte Carlo reasoning:

```text
Functional Visual Recovery != Accommodation Recovery
```

A perceptual decoder gain can improve task performance without changing mechanical accommodation capacity.

Let residual defocus be:

```text
e = D - A
```

and functional quality be modeled as:

```text
Q = exp(-(e / sigma(G))^2)
```

Increasing `G` can expand the usable visual range while leaving `A_mech` unchanged.

Therefore all experiments should maintain at least two separate endpoints:

1. **True accommodation endpoint**: objective optical/mechanical accommodation.
2. **Functional endpoint**: distance-specific usable visual performance.

A study that improves only the second must not be reported as mechanical reversal of presbyopia.

## Usable Visual Envelope (UVE)

Define UVE as the set of visual task states in which performance exceeds a required threshold.

A state may include:

```text
(distance, accommodation demand, target speed, contrast,
 spatial frequency, cue configuration, response latency)
```

The objective is not a single visual-acuity scalar, but expansion of the usable state-space volume.

Working objective:

```text
maximize UVE
```

subject to:

```text
risk <= bound
fatigue <= bound
objective accommodation claims require objective accommodation measurements
```

## Murofushi-Mizoguchi translation

The parent branch proposes that bounded perturbation can reveal latent control policies.

For vision, the direct translation should **not** be deliberate eye fatigue.

Instead:

> Temporarily weaken a dominant sensory cue or slightly perturb accommodation demand so that alternative residual control strategies become observable.

This is a safer form of constraint-induced exploration.

### Cue-space failure injection

Represent sensory weights as:

```text
w_vec = (
  w_blur,
  w_disparity,
  w_chromatic,
  w_proximity
)
```

Candidate perturbations include bounded experimental reduction or alteration of one cue while preserving the others.

Examples at the conceptual level:

```text
normal cues
  -> reduce blur cue reliability
  -> observe disparity/chromatic/proximity compensation
  -> restore cues
```

or:

```text
stable accommodation demand
  -> small stochastic demand perturbations
  -> measure adaptation and recovery
```

The purpose is system identification, not stress for its own sake.

## Progressive Control-Space Expansion

A Murofushi-style challenge schedule becomes:

```text
D_train = D_reliable + epsilon
```

where `epsilon` is small enough to remain inside a bounded, non-destructive exploration region.

The experiment adapts difficulty to keep the system near the edge of reliable control rather than repeatedly forcing failure.

Conceptually:

```text
measure current reliable envelope
    -> perturb slightly outside habitual policy
    -> observe whether a viable response exists
    -> consolidate successful response
    -> re-measure envelope
```

## Unlock -> Retrain hypothesis

The strongest converged hypothesis is a two-stage model.

### Stage A: Unlock

Increase the mechanically available state space by improving one or more of:

```text
K_eff down
H up
force-transmission efficiency up
mechanical freedom up
```

Potential research categories include lens-structure modification, hydration-state manipulation, surrounding-tissue compliance modification, or other validated non-destructive mechanical approaches.

### Stage B: Retrain

Once new physical freedom exists, the controller may still use an old policy learned under the previous constraint.

Therefore follow with controlled accommodation/cue training:

```text
mechanical freedom appears
    -> controller explores newly reachable states
    -> successful states are reinforced
    -> usable envelope expands
```

This predicts possible super-additive behavior when unlock and retraining are combined.

## Monte Carlo finding: qualitative convergence

A synthetic-twin Monte Carlo exploration was used as a hypothesis stress test, not as a clinical predictor.

Across multiple plausible mechanical-resistance formulations, the qualitative conclusions were stable:

- improving cue/controller use can produce large gains when residual mechanical capacity remains;
- increasing effective actuator/transmission capacity can expand true accommodation;
- reducing effective lens/mechanical resistance can expand true accommodation;
- reducing response delay/time constants improves dynamic performance more than static mechanical capacity;
- improving perceptual decoding can expand functional UVE without restoring true accommodation;
- `K_S` importance is more model-dependent than the other major terms;
- combined mechanical unlock + controller retraining can outperform either intervention alone when thresholds create nonlinear synergy.

These are model predictions requiring experimental validation.

## Stage-dependent prediction

The current branch predicts two broad regimes.

### Early / residual-capacity regime

```text
A_mech > small positive reserve
```

Prediction:

- cue perturbation and controller retraining should have more room to work;
- actuator/metabolic support may expose additional reserve;
- decoder training can improve functional vision even before mechanical change.

### Advanced mechanical-bound regime

```text
K_eff >> usable H
```

Prediction:

- controller training alone should saturate;
- perceptual compensation may still improve functional performance;
- true accommodation recovery requires some form of mechanical unlock or altered force transmission.

This stage-dependence is a major falsifiable prediction.

## Closed-loop experimental rig

Preferred non-invasive first-line research system:

```text
Eye tracking
    + objective photorefraction
    + tunable / varifocal optics
    + pupil / wavefront measurement when available
    + adaptive stimulus controller
```

The controller should choose the next perturbation using both treatment value and information value.

Candidate objective:

```text
u* = argmax_u [
  expected Delta_UVE
  + lambda * information_gain
  - mu * risk
  - nu * fatigue
]
```

This turns rehabilitation into simultaneous treatment and system identification.

## Meta-meta autonomous loop

```text
measure
  -> posterior over Digital Twin
  -> Monte Carlo candidate perturbations
  -> reject unsafe / low-information actions
  -> apply bounded cue or accommodation perturbation
  -> measure objective and functional response
  -> prediction-error biopsy
  -> update Twin
  -> revise model family if needed
  -> repeat
```

The loop should preserve competing models instead of prematurely collapsing to one biological explanation.

## Explicit non-goals / safety boundary

This research note is not a protocol for self-stimulation of the eye.

Do not infer that household electrical stimulation, heating/cooling, vibration, red-light devices, or other unsupervised interventions are appropriate simply because a model contains a corresponding control term.

Important negative result from the hypothesis exploration:

```text
mechanical stimulation != guaranteed softening
```

Mechanosensitive pathways may produce adverse remodeling or stiffening depending on stimulus type. Perturbation must therefore remain bounded and experimentally justified.

## Falsifiers

The branch should be weakened or rejected if controlled experiments show that:

1. cue perturbation does not reveal reproducible residual accommodation policies;
2. apparent training gains disappear when objective accommodation is measured;
3. unlock does not increase reachable mechanical state space;
4. unlock + retrain shows no advantage over either intervention alone;
5. model parameters cannot be identified even after adding independent measurements;
6. UVE gains are explained entirely by task familiarity or criterion shifts;
7. perturbation-induced gains require unsafe stimulus intensities;
8. simpler models predict the data equally well with fewer latent variables.

## Current convergence point

The branch currently favors the following abstraction:

> Presbyopia is not assumed to be a single-component lens-stiffness failure. It is treated as a loss of accessible visual control space produced by some combination of mechanical resistance, force transmission, control policy, cue weighting, temporal dynamics, and perceptual decoding.

The working strategy is:

```text
Identify
  -> Perturb safely
  -> Expose latent freedom
  -> Unlock when mechanically necessary
  -> Retrain newly available freedom
  -> Consolidate
  -> Re-measure objective accommodation and functional UVE separately
```

The Murofushi-Mizoguchi contribution is therefore not "train harder". It is:

> Use bounded constraints to reveal hidden degrees of freedom, then preserve the successful control solution with the cheapest safe path.

This is the current converged DCS hypothesis and should remain explicitly falsifiable.
