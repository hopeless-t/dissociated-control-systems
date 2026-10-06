# Visual Latent Fault Debugger

Date: 2026-10-06
Status: converged working checkpoint / DCS visual-control branch
Parent: `PRESBYOPIA_CONTROL_RECOVERY_DIGITAL_TWIN_2026-10-06.md`
Related core formalism: `docs/MATHEMATICAL_MODEL.md`, `docs/VAL-001.md`

## Research question

Can a visual system that appears normal under a coarse observation still contain latent faults, exhausted reserve, hidden dependencies, or inaccessible capability that become visible only under bounded perturbation?

The central DCS claim tested here is:

```text
Observed Normal != Internally Normal
Observable Behavior != Unique Internal State
Capability != Accessibility
```

A normal visual-acuity score is treated as a coarse observation, not as proof that the internal visual-control state is healthy.

## Connection to DCS core model

DCS starts from:

```text
e_i(t) = c_i * g_i(s_t, u_t)
y_t = h(e_t) + epsilon_t
p(s_{t+1} | s_t, u_t)
```

where `c_i` is latent capability and `g_i` is accessibility / control gating.

For a coarse normal observation `y0`, define the latent-state equivalence class:

```text
E0 = { s : h(s, 0) = y0 }
```

A single normal output can therefore correspond to multiple internal states.

This is the visual-domain analogue of VAL-001.

## Visual Digital Twin checkpoint

The current observable twin is:

```text
x_obs = (K_eff, H, w_vec, G, delta, tau)
```

with:

```text
H = F_C * eta
w_vec = (w_blur, w_disparity, w_chromatic, w_proximity)
```

Additional measurements may later refine:

```text
K_eff -> (K_L, K_S)
H     -> (F_C, eta)
```

The visual-debugger extension adds runtime and robustness state rather than collapsing everything into one health score.

## Why apparently normal regions can hide faults

A task can fail to excite the parameter that is impaired.

Example minimal accommodation model:

```text
A_mech ~ c * H / K_eff
T(f) = w_eff / sqrt(1 + (2*pi*f*tau)^2)
A(D,f) = min(D, A_mech) * T(f)
```

If demand `D < A_mech`, two subjects with very different reserve can produce the same output.

If `f = 0`, dynamic terms such as `tau` are poorly observable.

If only final steady-state output is measured, response latency `delta` can disappear from the observation.

Therefore normal performance under one operating point can be an observability artifact.

## Robustness Radius

Define the minimum bounded perturbation required to push the system below a functional threshold:

```text
rho(s) = inf_{u in U_safe} { ||u|| : y(s,u) < theta }
```

Two systems can have the same baseline visual performance but very different `rho`.

Interpretation:

```text
high baseline + large rho  -> robust normal
high baseline + small rho  -> compensated / fragile normal candidate
```

The debugger must therefore estimate reserve and robustness, not only baseline performance.

## Perturbation-conditioned fragility

The existing DCS dissociation index remains useful as a descriptor, but synthetic stress testing rejects the stronger claim:

```text
D_visual high => fragility high
```

as a general rule.

Fragility depends on compensation topology.

A system that dynamically routes weight toward surviving channels can preserve a normal coarse output while becoming unusually sensitive to perturbation of those dominant channels.

Therefore:

```text
D_visual + compensation topology + perturbation response
```

is more informative than `D_visual` alone.

## Visual Fault Fingerprint

Do not replace a coarse VA score with another single scalar.

Maintain a structured fingerprint:

```text
F = (
  UVE,
  rho,
  D_visual,
  J,
  Gamma,
  Reserve,
  Posterior,
  H_history
)
```

where:

- `UVE`: usable visual envelope;
- `rho`: robustness radius;
- `D_visual`: descriptive subsystem non-uniformity;
- `J`: perturbation sensitivity matrix;
- `Gamma`: nonlinear / hidden coupling between perturbation channels;
- `Reserve`: inferred spare capacity;
- `Posterior`: current posterior over latent states;
- `H_history`: hysteresis / history dependence.

## Perturbation sensitivity matrix

Let input perturbations include conceptual channels such as:

```text
u = [
  focal demand,
  chromatic cue,
  disparity,
  contrast,
  spatial frequency,
  retinal micro-motion,
  luminance/pupil,
  blink/tear-film phase
]
```

and outputs include:

```text
y = [
  accommodation,
  vergence,
  pupil,
  distance-specific VA,
  CSF,
  fixation stability,
  other safe observables
]
```

Define local sensitivity:

```text
J_ij = partial y_i / partial u_j
```

Probe selection should maximize independent information, not merely the number of measurements.

A high-rank / information-rich probe set is preferable to many redundant probes along the same latent axis.

## Hidden coupling

For two perturbations `u_i` and `u_j`, define an interaction residual:

```text
Gamma_ij = Delta y(u_i, u_j) - Delta y(u_i) - Delta y(u_j)
```

`Gamma_ij != 0` indicates non-additive coupling or hidden dependency.

A system may tolerate either perturbation alone but fail when both are applied, revealing a masked dependency.

## Stress + Rescue probes

Failure injection alone cannot fully separate missing capability from inaccessible capability.

Under:

```text
e = c * g
```

states `(c=1.0, g=0.6)` and `(c=0.6, g=1.0)` can emit the same baseline output.

A stress probe asks how easily output degrades.

A rescue probe asks whether output can improve when access conditions become more favorable.

Conceptually:

```text
stress probe  -> bounded negative perturbation
rescue probe  -> bounded positive / accessibility-improving perturbation
```

Asymmetric response can help distinguish retained-but-inaccessible capability from genuinely limited capability.

## Active equivalence-class decomposition

For a probe set `U_k = {u1, ..., uk}`, define the response signature:

```text
R_Uk(s) = [h(s,u1), ..., h(s,uk)]
```

If two latent states remain identical under all response signatures, they are observationally equivalent under the current probe set.

The candidate latent set updates as:

```text
E_k = E_(k-1) intersect { s : h(s,u_k) = y_k }
```

In a probabilistic implementation, track posterior contraction:

```text
H(S | Y0)
  -> H(S | Y0,Y1)
  -> H(S | Y0,Y1,Y2)
  -> ...
```

The objective is not to force a unique biological explanation, but to reduce uncertainty as far as justified by safe observables.

## Orthogonal perturbation principle

Synthetic reasoning indicates that many variations of one probe family can be less informative than a smaller set of probes that excite different latent axes.

Preferred families include conceptual probes of:

```text
cue isolation
+ dynamic response
+ runtime optical state
+ combined bounded stress
```

rather than repeated measurements of the same dimension.

This is consistent with the DCS requirement to avoid inferring a unique hidden state from a single coarse observable.

## Runtime state

The debugger must track state that can change even when slow biological parameters are unchanged:

```text
x_runtime = (
  tonic accommodation,
  stimulus history / adaptation,
  tear-film state,
  pupil state,
  fixational retinal motion,
  cognitive/autonomic load
)
```

Consequences:

- repeated trials are stateful;
- washout / baseline recovery may be necessary between probes;
- blink phase and tear-film condition can masquerade as optical or accommodation change;
- near->far and far->near transitions should not be assumed symmetric;
- history dependence is itself an observable.

## Murofushi-Mizoguchi translation

The visual analogue is not deliberate eye fatigue.

The safer DCS translation is:

> apply a bounded, low-amplitude, sometimes unpredictable perturbation that weakens a dominant route just enough to reveal alternate residual control or reserve.

The purpose is exposure of latent degrees of freedom, not stress for its own sake.

## Adaptive probe selection

Choose the next probe using expected information gain and safety constraints:

```text
u* = argmax_u [
  I(S; Y_u | Y_history)
  + lambda * expected_Delta_UVE
  - mu * Risk(u)
  - nu * Fatigue(u)
  - xi * Redundancy(u, U_history)
]
```

This combines active system identification with bounded rehabilitation research.

## Convergence criterion

The debugger has reached a domain-local convergence point when additional safe probes no longer materially reduce latent-state uncertainty.

One stopping rule is:

```text
max_{u in U_safe} IG(u) < epsilon
```

for repeated rounds, together with no meaningful increase in the independent rank / span of the sensitivity matrix.

If convergence occurs while multiple latent states remain plausible, the result is not failure.

It is evidence of structural non-identifiability under the current sensor and perturbation set.

The correct next step is to add a genuinely new observable rather than forcing a unique explanation.

## Synthetic-loop findings retained at this checkpoint

The current synthetic stress tests support the following qualitative conclusions only:

1. normal baseline output can coexist with reduced reserve;
2. perturbation response contains information unavailable at baseline;
3. orthogonal probe families reduce latent ambiguity faster than redundant probe families;
4. a dissociation statistic alone does not generally predict fragility;
5. compensation topology matters;
6. pairwise perturbation can reveal hidden dependencies not visible under single probes;
7. stress + rescue asymmetry is useful for distinguishing inaccessible capability from limited capability;
8. information-gain saturation provides a principled stopping rule.

These are model-level findings, not clinical conclusions.

## Relation to DCS roadmap

This visual branch is a natural domain-local candidate for:

```text
VAL-001 -> latent-state non-identifiability
VAL-002 -> state recovery under partial observation
EXP-002 -> intervention / perturbation sensitivity
```

The visual system therefore functions as a concrete testbed for the repository's core question rather than as a separate analogy-only branch.

## Current convergence point

The branch currently converges on:

```text
Normal output
  -> define latent equivalence class
  -> apply safe orthogonal perturbations
  -> include stress + rescue probes
  -> estimate robustness / reserve / coupling
  -> contract posterior over latent states
  -> stop when safe information gain saturates
```

Canonical statement:

> A normal visual output is not the control group. It is an observation class that may contain robust, compensated, fragile, or partially inaccessible internal states. The debugger should decompose that class with bounded perturbations until additional safe observations no longer change the posterior materially.

## Safety / claim boundary

This note specifies a computational and experimental-design abstraction, not a self-treatment protocol.

Simulation support does not establish a human treatment effect.

Do not infer that electrical, thermal, mechanical, optical, or other interventions are safe for unsupervised ocular use merely because they appear as variables in a model.
