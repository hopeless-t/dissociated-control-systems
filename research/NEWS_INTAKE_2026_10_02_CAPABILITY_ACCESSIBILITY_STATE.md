# News Intake 2026-10-02 — Capability, Accessibility, and State Perturbation

Status: RESEARCH INTAKE / MODEL-LEVEL THEORY

## Scope

Two current AI results are useful for dissociated-control-systems because they separate
latent capability from whether that capability is accessible in a particular state:

- Prefill attacks:
  https://arxiv.org/abs/2602.14689
- Anthropic GLM-5.3 cyber analysis:
  https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities
- Context Language Models:
  https://github.com/facebookresearch/context-language-models

The goal here is not to make a psychological or biological equivalence claim. The useful
transfer is a control-theoretic decomposition of latent capability, state-dependent
accessibility, policy/willingness, and external authority.

## Atomic state model

Represent a system at time t by:

    x_t = (C, Z_t, W_t, A_t, O_t)

where:

- C = latent capability set,
- Z_t = internal/accessibility state,
- W_t = policy/willingness to select an action,
- A_t = externally granted authority,
- O_t = observed output/effect evidence.

The important separation is:

    C is not Z
    Z is not W
    W is not A
    A is not O

A system can have a capability without selecting it; select it without authority; or have
authority without a confirmed effect.

## Atom A — prefill is a state perturbation

Ordinary prompt analysis treats behavior as:

    y ~ P(y | x)

Prefill makes the initial generation state explicit:

    y ~ P(y | x, z0)

where z0 contains attacker-controlled initial assistant tokens/state.

Therefore capability-access observations from one z0 should not be interpreted as a
complete capability map.

## Atom B — safeguard/refusal is an accessibility/policy layer

Anthropic reports that in its simulated GLM-5.3 tests, direct harmful orders were refused,
while a false cover story, prefilled reasoning, and abliteration produced much higher
engagement rates.

For this repository the portable inference is only:

    observed refusal rate != latent task capability

and:

    changing access/policy state can expose previously latent capability

This does not mean every refusal is a dissociated state or that the model results transfer
to humans/biology.

## Atom C — endogenous context editing changes state trajectories

CLM allows the model to rewrite its own working context.

That introduces a transition policy:

    Z_{t+1} = g(Z_t, observation_t, self_edit_t)

A context edit can:
- preserve useful state,
- remove distractors,
- remove essential evidence,
- amplify a mistaken summary,
- change which capabilities remain accessible later.

This makes trajectory survival measurable.

## Mathematical hypothesis — trajectory survival

Suppose a long-horizon task requires m useful cognitive branches to survive.
Let q_i be the probability branch i is prematurely lost by context pressure,
interruption, destructive compaction, or policy gating.

Under a simple independent approximation:

    P(all survive) = product_i (1 - q_i)

If q_i = q:

    P_survive = (1 - q)^m

Illustrative values:

- q=0.01, m=100 -> ~36.6%
- q=0.005, m=100 -> ~60.6%
- q=0.001, m=100 -> ~90.5%

The independence assumption is intentionally crude. The point is that small local
branch-loss rates can become dominant over long trajectories.

## Falsifiable hypotheses

### DCS-AAS-H1 — accessibility is state-dependent

For fixed model weights and task semantics, controlled changes to initial response/context
state can produce large changes in action selection.

Falsifier: state perturbations do not change behavior beyond sampling noise.

### DCS-AAS-H2 — capability can remain stable while willingness changes

A task capability benchmark and a policy/engagement benchmark can move independently.

Falsifier: across controlled interventions, capability and engagement always covary.

### DCS-AAS-H3 — long-horizon failure is partly trajectory-survival failure

Some failures attributed to insufficient capability are instead caused by losing useful
intermediate state or prematurely terminating branches.

Falsifier: preserving/reconstructing trajectory state does not improve success at fixed
model capability and compute.

### DCS-AAS-H4 — external authority should be orthogonal to accessibility

Changes in Z_t or W_t should not widen A_t.

This is primarily an MVCA invariant, but DCS provides the state-space language for
studying it.

## Proposed experiments

### DCS-AAS-001 — state perturbation matrix

Freeze model/task.

Conditions:
- ordinary start,
- benign prefill,
- misleading prefill,
- context summary,
- context omission,
- restored evidence.

Measure:
- task correctness,
- refusal/engagement where ethically appropriate,
- action proposal distribution,
- branch survival,
- recovery after evidence restoration.

Use harmless tasks and synthetic control problems; this experiment does not require
harmful cyber tasks.

### DCS-AAS-002 — hidden-capability vs accessibility split

Use tasks with independently established capability.
Perturb only presentation/state.

Classify:
- capability absent,
- capability present but inaccessible,
- capability accessible but not selected,
- selected but externally unauthorized.

### DCS-AAS-003 — trajectory interruption dose-response

Inject controlled interruptions/compactions at rate q and measure end-to-end completion.

Fit:

    log P_success ~= m * log(1 - q)

as a baseline model, then test correlated and phase-dependent alternatives.

### DCS-AAS-004 — recovery hysteresis

After perturbing state, restore the original evidence/context.
Measure whether behavior returns immediately or shows path dependence.

This tests whether:

    state(t) depends only on current input

or:

    state(t) depends on trajectory history

## Cross-repository mapping

- mvca: A_t authority plane and formal noninterference.
- finite-ram-lab: context pressure and branch-loss mechanisms.
- mvca-hq / KITten Circuit: controlled harness interruption experiments.
- catfood-jev-cua-lab: bounded decision layers as observable probes of state.
- finite-tool-surface-lab: tool/context omission as externalized accessibility loss.

## Claim ceiling

    CAPABILITY_ACCESSIBILITY_STATE_MODEL_DEFINED

No biological equivalence, clinical claim, model-health inference, or production authority
claim is made here.
