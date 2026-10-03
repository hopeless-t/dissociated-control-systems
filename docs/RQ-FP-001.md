# RQ-FP-001 — Fixed-point, convergence, and attractor observability

> Status: OPEN RESEARCH / deterministic synthetic probe added  
> Biological interpretation: UNVALIDATED  
> Clinical authority: NONE  
> Cross-domain transfer: FORMAL CORRESPONDENCE ONLY

## Trigger

Huang et al. (2026), *Towards Looped Models Done Right — Part II: Rethinking at
Fixed Points*, studies looped language models whose recurrent states approach
fixed points. The paper reports that, when training shapes sufficiently settled
states, some trajectory cost can be replaced by endpoint reuse: terminal KV
sharing, truncated backpropagation, distilled prefill, and fixed-point reuse in
RL.

Primary public sources:

- alphaXiv paper page: https://www.alphaxiv.org/abs/2610.looped-models-fixed-points
- official code / paper release: https://github.com/ifm-ai/xllm-loop
- paper PDF in the official repository:
  https://github.com/ifm-ai/xllm-loop/blob/main/papers/part2.pdf

The source is an AI-model result. It is **not** evidence that human control
systems use the same physical mechanism.

## Atomic decomposition

The useful transferable atoms are narrower than "brains are looped models":

| Source atom | Minimal mathematical object | DCS question |
|---|---|---|
| recurrent state | x_(t+1) = F(x_t, u) | what latent state is changing? |
| fixed point | x* = F(x*, u) | does repeated evolution settle? |
| finite-depth settling | ||x_(t+1)-x_t|| small | when is "stable" defensible? |
| contraction | perturbations shrink under repeated F | does the state return after disturbance? |
| heterogeneous convergence depth | tau_epsilon differs by token/state | do subsystems settle at different rates? |
| depth distribution | training exposes multiple recurrence depths | does exposure history reshape settling behavior? |
| orthogonal injection | remove state component parallel to input before injection | can intervention and autonomous state be measured separately? |
| terminal-state reuse | endpoint substitutes for some trajectory work only after settling | when is history compressible into sufficient state? |
| failure before convergence | endpoint/implicit shortcuts can fail when states still drift | when must trajectory history remain explicit? |

## DCS formal correspondence

DCS currently writes generic state evolution as:

~~~text
p(s_(t+1) | s_t, u_t)
~~~

For a deterministic local probe, use:

~~~text
s_(t+1) = F(s_t, u)
~~~

and define the following observables.

### Step norm

~~~text
delta_t = ||s_(t+1) - s_t||_2
~~~

Small delta is evidence of local settling only. It is not proof of a unique
global attractor.

### Fixed-point residual

~~~text
r_t = ||F(s_t, u) - s_t||_2
~~~

An exact fixed point has r_t = 0.

### Empirical contraction ratio

~~~text
kappa_t =
    ||s_(t+1) - s_t||
    -----------------
    ||s_t - s_(t-1)||
~~~

Repeated kappa_t < 1 in a controlled neighborhood is compatible with local
contraction. One observed decrease is insufficient.

### Convergence depth

~~~text
tau_epsilon =
    min t such that
    ||s_k - s*|| <= epsilon for every k >= t
~~~

This explicitly separates "first looks recovered" from "stays settled."

### Perturbation-return time

For a bounded perturbation p applied at time t0:

~~~text
T_return(epsilon) =
    min tau >= 0 such that
    ||s_(t0+tau) - s*|| <= epsilon
    and remains <= epsilon over the declared confirmation window
~~~

This is directly relevant to DCS recovery / hysteresis experiments.

## Orthogonal intervention decomposition

Let u be a non-zero intervention / conditioning direction and s the incoming
state. Define:

~~~text
proj_u(s) = (<s,u> / <u,u>) u

s_orth = s - proj_u(s)

inject_orth(s,u) = s_orth + u
~~~

Then:

~~~text
<inject_orth(s,u), u> / <u,u> = 1
~~~

independent of the incoming state's pre-existing component along u.

This is useful as a **measurement decomposition**: it creates a synthetic known
answer in which drive-parallel conditioning is held constant while orthogonal
state components remain free to vary.

It is not a claim that real human interventions can literally be orthogonalized
in a Euclidean latent space.

## New hypotheses

### FP-H1 — Settling-state observability

Two trajectories can emit the same coarse behavior while having different
fixed-point residuals or convergence depths.

Prediction: adding convergence observables can distinguish states that a coarse
behavior label cannot.

### FP-H2 — Heterogeneous subsystem convergence

Different subsystem coordinates can settle at different rates.

Prediction: one scalar "recovered" flag will lose information when
tau_epsilon differs materially across coordinates or subsystem projections.

### FP-H3 — Stable recovery is stronger than first success

A first successful observation after perturbation can occur before the latent
trajectory has returned to a stable neighborhood.

Prediction: confirmation-window criteria outperform one-sample recovery labels
when trajectories exhibit rebound or hysteresis.

### FP-H4 — Endpoint sufficiency is conditional

A terminal state can replace trajectory history only when an explicit
endpoint-sufficiency test passes.

Prediction: endpoint-only prediction error should fall as fixed-point residual
falls, but this relationship must be measured rather than assumed.

### FP-H5 — Exposure schedule can reshape state geometry

If training / practice / repeated control exposes a system to only one
termination depth, it may optimize the served endpoint without becoming stable
at intermediate depths.

Prediction: variable-depth practice can alter convergence-depth distribution,
but DCS requires domain-local evidence before transferring this AI result to
human skill learning.

## DCS-FP-001 deterministic known-answer probe

The repository adds `fixed_point.py` with a deliberately simple contraction:

~~~text
x_(t+1) = x* + a (x_t - x*)
0 <= a < 1
~~~

Known answers:

~~~text
step-size ratio = a
distance to x* shrinks geometrically
convergence depth can be computed exactly up to tolerance
fixed-point residual is zero at x*
~~~

The same module adds orthogonal injection with the exact drive-gain invariant
above.

These tests validate the **measurement harness only**. They do not validate a
biological attractor model.

## Next experiments earned by this intake

1. **DCS-FP-002 — observational aliasing under unequal convergence**
   - two trajectories share the same coarse output;
   - one is settled, one still drifts;
   - test whether convergence observables resolve the ambiguity.

2. **DCS-FP-003 — perturbation / rebound / hysteresis**
   - apply a bounded perturbation;
   - measure return time and overshoot;
   - compare first-success versus stable-confirmation recovery rules.

3. **DCS-FP-004 — multi-basin synthetic system**
   - create two attractors with an explicit basin boundary;
   - sweep bounded interventions;
   - estimate transition probability / boundary sensitivity.

4. **DCS-FP-005 — endpoint-sufficiency falsification**
   - compare full-trajectory and endpoint-only predictors;
   - record the residual level at which endpoint substitution stops being
     detectably harmful.

## Claim ceiling

This intake can establish:

~~~text
FIXED_POINT_MEASUREMENT_PRIMITIVES_DEFINED
ORTHOGONAL_INJECTION_KNOWN_ANSWER_VALIDATED
DCS_FIXED_POINT_RESEARCH_LANE_OPENED
~~~

It cannot establish:

~~~text
HUMAN_CONTROL_IS_A_FIXED_POINT_SYSTEM
PARASOMNIA_IS_AN_ATTRACTOR_TRANSITION
A_DRUG_RESHAPES_AN_ATTRACTOR_BASIN
AI_FIXED_POINT_RESULTS_TRANSFER_TO_BIOLOGY
~~~
