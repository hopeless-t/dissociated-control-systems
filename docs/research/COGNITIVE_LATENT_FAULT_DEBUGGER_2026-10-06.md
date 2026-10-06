# Cognitive Latent-Fault Debugger — DCS cross-branch transfer

Date: 2026-10-06
Status: domain-local working hypothesis / synthetic-validation target
Scope: cognitive decline / compensation / observability / latent reserve
Parent method: `VISUAL_LATENT_FAULT_DEBUGGER_2026-10-06.md`

## Transfer question

Can apparently preserved cognitive performance hide latent subsystem decline because compensation, scaffolding, task familiarity, or alternate routes keep coarse behavior above threshold?

This branch adopts the DCS invariant:

```text
Observed Normal != Internally Normal
Capability != Accessibility
Compensated Performance != Preserved Reserve
```

## Minimal model

Let:

```text
c_i      latent capability of subsystem i
g_i      accessibility / routing gate
r_i      compensatory reserve or alternate-route support
e_i      expressed capability
```

Bootstrap form:

```text
e_i = c_i * g_i
```

Observed task performance may be maintained by compensation:

```text
y = h(e, r, task, history) + noise
```

Therefore two people may emit the same coarse PASS while occupying different latent states.

## Latent-fault candidates

Examples of distinct internal worlds that can share the same baseline score:

```text
A: high c, high g, low compensation demand
B: moderate c, high g, compensation active
C: high c, low g, strong external/internal scaffolding
D: uneven subsystem state with task-specific alternate routing
```

A single familiar task cannot distinguish these worlds.

## Stress + rescue probes

The visual-debugger method transfers only as a measurement strategy, not as an instruction to induce harmful cognitive stress.

Candidate safe research probes are bounded task variations such as:

- novelty instead of overlearned material;
- divided-attention / dual-task variants within validated testing limits;
- delay / retention interval variation;
- context-switch cost;
- cue removal to test dependence on scaffolding;
- cue restoration or structured support as a rescue probe;
- counterfactual consistency / error awareness / confidence calibration.

Define stress sensitivity:

```text
S_j^- = [y(0) - y(-epsilon_j)] / epsilon
```

and rescue responsiveness:

```text
S_j^+ = [y(+epsilon_j) - y(0)] / epsilon
```

Interpretation candidate:

```text
large stress sensitivity + strong rescue response
    -> accessible reserve may remain but compensation margin is thin

large stress sensitivity + weak rescue response
    -> deeper capability loss is more plausible, but not proven
```

## Cognitive robustness radius

For a declared safe task-perturbation set `U_safe`:

```text
rho_cog(s) = inf { ||u|| : performance(s,u) < threshold }
```

A normal baseline with small `rho_cog` is a fragile-normal candidate.

This is not a diagnosis. It is a model feature for distinguishing apparent performance from reserve margin.

## Compensation observability loss

A central hypothesis is:

```text
better compensation can improve daily function while making latent decline harder to observe
```

Therefore the research architecture should maintain two endpoints:

1. functional floor / real-world performance;
2. latent-state evidence / reserve estimate.

Improving endpoint 1 must not automatically be interpreted as restoration of endpoint 2.

## Posterior-contraction loop

Let `E0` be the latent-state equivalence class compatible with baseline performance.

Each orthogonal safe probe adds a response signature:

```text
E_k = E_(k-1) intersect { s : h(s,u_k) matches observed response }
```

Probe selection objective:

```text
u* = argmax_u [
  information_gain
  + lambda * reserve_resolution
  - mu * burden
  - nu * risk
  - xi * redundancy
]
```

## Convergence rule

Stop the local debugger when all available validated low-risk probes satisfy:

```text
max information_gain < epsilon
```

or when additional probes do not increase the effective observation rank.

Remaining ambiguity is then structural non-identifiability, not evidence that one latent explanation is true.

## Strong falsifiers

Weaken this branch if:

- supposedly orthogonal probes produce no stable additional state information;
- stress/rescue asymmetry is explained by simple task familiarity or motivation;
- reserve estimates do not predict later functional fragility better than baseline scores;
- simpler observable-only models predict equally well;
- the required perturbation burden exceeds an ethically acceptable research envelope.

## Cross-branch consequence

This branch makes the earlier DCS-CGD idea more precise:

```text
compensation preserves function
        !=
latent decline absent
```

The intended output is not a single cognitive-health scalar but a fingerprint containing baseline performance, robustness radius, probe-sensitivity matrix, rescue responsiveness, history dependence, and posterior uncertainty.

## Claim boundary

Synthetic model support does not establish a biological mechanism or clinical diagnostic. Human validation requires independent, ethically approved domain-local studies.
