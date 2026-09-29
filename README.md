# dissociated-control-systems

A small, reproducible computational research lab for studying systems whose
**observable behavior can remain complex even when internal control subsystems
occupy different states**.

> **Core question:**  
> When a system appears globally "awake", "capable", "slow", "stuck", or
> "inactive", how much of that observation can actually be explained by
> different internal subsystems being active, suppressed, inaccessible, or
> unobserved at the same time?

## Status

**OPEN RESEARCH — repository bootstrap / Phase 0**

This repository is intentionally hypothesis-first.

It does **not** claim that sleep parasomnias, zolpidem effects, AI agents,
GPU pipelines, and computer memory systems share one biological or physical
mechanism.

Instead, it asks a narrower question:

> **Can the same mathematical language of partial observability, subsystem
> activation, gating, and state transitions usefully describe otherwise very
> different systems?**

The initial public research object is the abstraction, not a medical treatment
claim and not a production control architecture.

## Working thesis

Three distinctions motivate the lab:

~~~text
Capability != Accessibility
Global State != Uniform Subsystem State
Observable Behavior != Unique Internal State
~~~

A subsystem can retain capability while another process controls whether that
capability is expressed, observed, recorded, or integrated.

The repository calls this family of possibilities the **Dissociated Capability
Hypothesis**.

It remains a hypothesis until individual mechanisms are tested.

## At a glance

~~~mermaid
flowchart LR
    C["Latent capability<br/>C"] --> G["Access / control gate<br/>G(s,u)"]
    S["Subsystem state vector<br/>s(t)"] --> G
    U["Input / intervention<br/>u(t)"] --> G

    G --> E["Expressed capability<br/>E"]
    E --> O["Observation<br/>y(t)"]

    S --> T["State transition"]
    T --> S

    O --> I["Inference"]
    I -. "partial observability" .-> S
~~~

The diagram is a navigation aid, not an empirical result.

## Interactive conceptual projection

The repository includes a small browser visualization, **Dissociated State
Field**, designed as a comprehension and contribution surface rather than
scientific evidence.

**[Open the interactive field](https://hopeless-t.github.io/dissociated-control-systems/)**

It uses `pmndrs/math` for deterministic random/noise primitives and
`gpucat` for WebGL2 rendering. Four subsystem-accessibility controls change
how state trajectories converge toward the same coarse observable.

~~~text
Visualization != Evidence
Conceptual Projection != Biological Mechanism
Interaction != Experiment
~~~

See [docs/VISUALS.md](docs/VISUALS.md) for the visual contract and
[CONTRIBUTING.md](CONTRIBUTING.md) for ways to participate.

## Why this project exists

Several research areas contain examples where a single global label is a poor
description of the system.

In NREM parasomnias, neurophysiological work has reported combinations of
wake-like activity in motor/cingulate regions with sleep-like activity in
associative regions.

In disorders of consciousness, zolpidem has produced paradoxical improvement
in a small subset of patients, motivating circuit-level hypotheses in which
local inhibition and disinhibition change access to surviving functional
capacity.

In engineered systems, performance can also depend on scheduling, residency,
routing, observation, and control state rather than physical capacity alone.

These domains must not be collapsed into one explanation.

They are used here as **separate test beds for a shared formal question**:

> How do we distinguish missing capability from inaccessible capability?

## Scientific boundary

This repository does **not** currently claim to:

- explain consciousness;
- explain the full mechanism of sleepwalking or sleep-related eating;
- establish the mechanism of zolpidem-induced complex sleep behavior;
- recommend or test zolpidem or any other drug;
- use personal medical anecdotes as scientific evidence;
- infer that one control model applies unchanged across brains and computers;
- prove that a hidden-state model corresponds to a biological latent state;
- treat analogy as causality;
- turn a synthetic model into a clinical conclusion;
- turn a research finding into production authority for another project.

Medical and neuroscience claims must be traced to published sources.

No human drug administration, medication challenge, or intentional induction of
parasomnia is in scope.

## Initial hypotheses

| ID | Hypothesis | Current status |
| --- | --- | --- |
| HYP-001 | **Capability–Accessibility Separation:** retained capability and expressed capability can differ because of a gate or control state. | OPEN |
| HYP-002 | **Subsystem State Dissociation:** a useful global state may require a vector of subsystem states rather than one scalar label. | OPEN |
| HYP-003 | **Observability Gap:** multiple latent subsystem configurations can produce the same coarse external observation. | OPEN |
| HYP-004 | **Local Intervention / Global Transition:** a bounded change to one gate or coupling can move the whole system between qualitatively different observable regimes. | OPEN |

## Mathematical starting point

Let a system contain n subsystems.

~~~text
s_t = [s_1(t), ..., s_n(t)]       hidden / partially observed state
c   = [c_1, ..., c_n]             latent capability
g_i(s_t, u_t) in [0,1]            access / control gate
e_i(t) = c_i * g_i(s_t, u_t)      expressed capability
y_t = h(e_t) + noise              observation
~~~

State evolution is modeled as:

~~~text
p(s_{t+1} | s_t, u_t)
~~~

This deliberately supports multiple model families:

- finite-state machines;
- Hidden Markov Models;
- switching state-space models;
- coupled dynamical systems;
- Bayesian latent-state models.

See [docs/MATHEMATICAL_MODEL.md](docs/MATHEMATICAL_MODEL.md).

## VAL-001 — Latent-State Non-Identifiability

The first validation is deliberately synthetic.

Its purpose is **not** to model a brain.

It verifies that the research harness can represent two distinct internal
configurations that generate the same coarse observable behavior.

Example:

~~~text
State A
    motor execution      ON
    procedural sequence  ON
    executive monitor    ON
    memory encoding      ON

State B
    motor execution      ON
    procedural sequence  ON
    executive monitor    LOW
    memory encoding      LOW

Coarse observer:
    "complex action occurred"

=> same coarse observation
=> different internal state
~~~

A model that infers a unique global state from that observation alone should
fail this validation.

See [docs/VAL-001.md](docs/VAL-001.md) and
[specs/VAL-001.json](specs/VAL-001.json).

## Research architecture

~~~text
Question
  ↓
Literature / prior-art intake
  ↓
Frozen hypothesis or validation spec
  ↓
Model
  ↓
Synthetic or public-data calculation
  ↓
Observable
  ↓
Acceptance / falsification checks
  ↓
Evidence
  ↓
Claim + limitations
~~~

A successful program execution is not automatically a successful research
result.

~~~text
Plan != Result
Figure != Evidence
Analogy != Mechanism
Correlation != Causation
Latent-State Fit != Biological Ground Truth
Research Finding != External Execution Authority
~~~

## Research lanes

~~~text
RQ-xxx     open research question
HYP-xxx    explicit falsifiable hypothesis
VAL-xxx    model / harness / method validation
EXP-xxx    controlled experiment
BENCH-xxx  comparative benchmark
REF-xxx    named reference object
~~~

## Planned sequence

~~~mermaid
flowchart LR
    L0["LIT-001<br/>state dissociation + control lineage"] -->
    V1["VAL-001<br/>latent-state non-identifiability"] -->
    V2["VAL-002<br/>state recovery under partial observation"] -->
    E1["EXP-001<br/>coupled-subsystem transition model"] -->
    E2["EXP-002<br/>intervention sensitivity"] -->
    P1["PUBLIC-DATA-001<br/>qualified external dataset"] -->
    X["cross-domain comparison<br/>only after domain-local validation"]
~~~

Roadmap nodes describe intent, not completed results.

## Repository structure

This repository follows the reusable discipline extracted from
[topological-spin-lab](https://github.com/hopeless-t/topological-spin-lab)
and later Catfood Lab research repositories.

~~~text
dissociated-control-systems/
├── README.md
├── RESEARCH_CHARTER.md
├── LICENSE
├── pyproject.toml
├── specs/
│   └── VAL-001.json
├── src/
│   └── dissociated_control_systems/
│       ├── __init__.py
│       └── state_model.py
├── tests/
│   └── test_state_model.py
├── docs/
│   ├── REFERENCES.md
│   ├── LITERATURE_MAP.md
│   ├── MATHEMATICAL_MODEL.md
│   ├── VAL-001.md
│   └── VISUALS.md
├── external/
│   ├── gpucat.md
│   └── pmndrs-math.md
├── web/
│   ├── src/
│   └── package.json
├── CONTRIBUTING.md
└── .github/
    └── workflows/
        └── ci.yml
~~~

No empty-directory architecture theatre: new components are added only when a
real research contract needs them.

## Evidence and citation rules

The repository distinguishes:

~~~text
SOURCE
ESTABLISHED SOURCE OBSERVATION
MODEL ASSUMPTION
OUR INFERENCE
NUMERICAL RESULT
EXPERIMENT IMPACT
~~~

Primary papers are preferred for scientific claims.

Reviews are used to orient the field or clearly labeled as hypothesis/review
sources.

Reference software is cited separately from scientific evidence.

A cited implementation does not imply that its scientific assumptions have
been adopted.

See [docs/REFERENCES.md](docs/REFERENCES.md) and
[docs/LITERATURE_MAP.md](docs/LITERATURE_MAP.md).

## Reference software

Candidate tools are references, not mandatory dependencies:

- [Dynamax](https://github.com/probml/dynamax) — probabilistic state-space models in JAX;
- [hmmlearn](https://github.com/hmmlearn/hmmlearn) — Hidden Markov Models;
- [ssm](https://github.com/lindermanlab/ssm) — state-space / switching models;
- [MNE-Python](https://github.com/mne-tools/mne-python) — EEG/MEG analysis;
- [YASA](https://github.com/raphaelvallat/yasa) — sleep analysis utilities;
- [pmndrs/math](https://github.com/pmndrs/math) — lightweight, tree-shakeable
  vector / matrix / geometry / random / noise utilities for small calculations
  and exploratory tooling. See [external/pmndrs-math.md](external/pmndrs-math.md);
- [gpucat](https://github.com/isaac-mason/gpucat) — TypeScript-first WebGPU /
  WebGL2 renderer used by the optional interactive conceptual projection. See
  [external/gpucat.md](external/gpucat.md).

The bootstrap code intentionally uses only the Python standard library so that
VAL-001 remains inspectable and deterministic. pmndrs/math is recorded as an
optional tool reference, not a canonical runtime dependency.

## Public-repository rule

A canonical public claim must be reproducible from:

- public literature;
- public datasets with explicit provenance; or
- deterministic synthetic generators committed in this repository.

Private Catfood Lab observations may inspire a research question.

They cannot be the sole evidence for a public canonical claim.

## Relationship to other Catfood Lab research

This project may exchange hypotheses with repositories such as
finite-ram-lab, memory-attention-lab, or agent research.

Cross-domain transfer must follow:

~~~text
analogy
  ↓
formal correspondence candidate
  ↓
domain-local experiment
  ↓
independent evidence
  ↓
only then: transferable claim
~~~

A shared equation is not proof of a shared physical mechanism.

## License

MIT. See [LICENSE](LICENSE).

## Project principle

> **Do not ask only whether a system has capability. Ask whether the capability
> is accessible, integrated, observable, and remembered — and measure those
> questions separately.**
