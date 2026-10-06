# Cancer-Survivor Latent-State Debugger — DCS cross-branch transfer

Date: 2026-10-06
Status: domain-local working hypothesis / observational-validation target
Scope: survivor watershed / hidden-state divergence / longitudinal robustness
Parent method: `VISUAL_LATENT_FAULT_DEBUGGER_2026-10-06.md`

## Transfer question

Can apparently similar clinical states hide materially different underlying trajectories because tumor biology, treatment response, immune/TME state, inflammatory/neuroendocrine state, behavior, and history combine into different latent worlds?

Core invariants:

```text
Current state != Complete causal history
Same observable status != Same latent risk state
Survival != Proof of one psychological or immune mechanism
```

This branch explicitly rejects "hope alone" as the causal explanation.

## Latent-state framing

Use an abstract state vector:

```text
x_t = (B, T, I, M, N, R, H, C)
```

where dimensions may represent tumor burden/biology, treatment effect, immune/TME state, metabolic/inflammatory state, neuroendocrine state, reserve, history, and contextual covariates.

These are modeling buckets, not asserted biological modules.

Observed clinical state:

```text
y_t = h(x_t, measurement_surface, history) + noise
```

Different latent states may therefore share the same coarse label such as response, stable disease, remission, or survivor status.

## Critical modification from the visual branch

Do **not** actively stress a patient merely to reveal a hidden state.

The perturbation framework must be observational or arise from clinically justified care / pre-existing longitudinal events.

Allowed research interpretation:

```text
existing treatment transition
natural longitudinal change
measurement timing
already-collected biomarker response
matched responder/non-responder trajectories
```

These can act as observed perturbations for system identification without creating a new harmful challenge.

## Passive perturbation signatures

For an observed transition `u_t`, define:

```text
Delta y / Delta u
```

only as a descriptive response signature.

Examples of questions:

- do two apparently similar baseline patients diverge after the same treatment class?
- do early molecular/biomarker responses precede later outcome divergence?
- does apparent short-term stability depend on one fragile control axis?
- are exceptional responders located in a different latent basin before outcome separation becomes visible?

## Longitudinal robustness

A direct analogue of robustness radius should be defined in observational terms:

```text
rho_surv(x) = distance in measured state-space to a clinically meaningful transition boundary
```

This is not a prescription for perturbation and not a patient-level risk score unless independently validated.

The useful distinction is:

```text
stable-looking + large margin
!=
stable-looking + small inferred margin
```

## Change-point / watershed model

Survivor and non-survivor trajectories may be better separated by change points or basin transitions than by one baseline scalar.

Candidate form:

```text
x_(t+1) = F_k(x_t, u_t) + process_noise
```

with regime `k` changing when a latent threshold is crossed.

The research target is not merely outcome prediction but localization of the divergence point:

```text
when did two superficially similar trajectories stop being dynamically equivalent?
```

## Competing causal worlds

For each apparent association, preserve at least these alternatives where applicable:

```text
A -> outcome
outcome trajectory -> A
common cause -> A and outcome
measurement/treatment selection -> apparent association
```

Psychological variables, immune variables, and behavior must therefore be tested against reverse causality and treatment-selection effects rather than promoted directly to causal mechanisms.

## Matched success/failure biopsy

The visual debugger's stress/rescue pair becomes a matched longitudinal comparison:

```text
similar coarse baseline
    -> different eventual outcome
    -> compare earliest reproducible divergence across independent channels
```

The strongest channels are those that separate the worlds before the coarse outcome label changes and replicate in held-out data.

## Posterior contraction

Let `E0` contain latent models compatible with the current coarse observation.

Sequential evidence updates:

```text
E_k = E_(k-1) intersect { models compatible with new longitudinal evidence }
```

Prefer measurements or analyses with expected information gain on the current competing worlds.

Candidate stopping rule:

```text
max expected information gain from available ethical/observational channels < epsilon
```

Remaining ambiguity must be reported rather than filled by a preferred story.

## Rare-event capture

Exceptional responders are information-rich but selection-prone.

Requirements:

- compare against matched non-exceptional trajectories;
- preserve treatment/burden/history covariates;
- use independent channels where possible;
- hold out blocks/cohorts for replication;
- separate post-hoc explanation from preregistered prediction.

## Strong falsifiers

Weaken the branch if:

- latent-state/change-point models do not improve held-out prediction or explanation over simpler baselines;
- apparent divergence disappears after treatment/history matching;
- candidate early markers fail independent replication;
- reverse-causality worlds explain the data equally well;
- exceptional-responder signatures are cohort-specific artifacts.

## Cross-branch transfer summary

The visual branch contributes:

```text
coarse normality -> equivalence class
orthogonal evidence -> posterior contraction
fragility -> distance to transition boundary
hidden coupling -> interaction structure
convergence -> information-gain saturation
```

The cancer-survivor branch modifies only one major rule:

> perturbation is observational / clinically justified, not an intentionally induced patient stress test.

## Claim boundary

This is a research formalism, not treatment advice, prognosis, or a claim that a named psychological/immune mechanism explains survival. Human conclusions require validated longitudinal datasets and independent replication.
