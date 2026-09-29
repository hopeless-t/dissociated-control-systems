# Contributing

Thank you for considering a contribution to Dissociated Control Systems.

This is an interdisciplinary research repository. You do not need to work in
every domain represented here.

## Start here

The project studies one narrow formal question:

> Can complex observable behavior be compatible with multiple internal
> subsystem states, and how can we measure the resulting accessibility and
> observability gaps?

Before contributing, keep these boundaries intact:

~~~text
Capability != Accessibility
Observable Behavior != Unique Internal State

Analogy != Mechanism
Visualization != Evidence
Model Fit != Biological Ground Truth
Research Finding != Clinical Advice
~~~

## What you can bring

### Neuroscience / sleep research

Useful contributions include:

- primary papers on NREM parasomnia, local sleep, arousal, memory, or motor
  control;
- public EEG / intracranial / imaging datasets with clear licenses;
- corrections to neurophysiological interpretation;
- proposals for measurable observables that do not overclaim hidden state.

Please distinguish direct measurement from interpretation.

### Mathematics / statistics / control

Useful contributions include:

- identifiability analysis;
- HMM / state-space / switching-model baselines;
- observability and controllability formulations;
- entropy / degeneracy measures;
- uncertainty quantification;
- counterexamples to current assumptions.

A more complicated model is not automatically a better contribution.

### AI / agent systems

Useful contributions include:

- controlled examples where worker, observer, memory, planner, or authority
  subsystems diverge;
- public reproducible fixtures;
- formal mappings that make domain-local predictions.

Do not treat an architectural analogy as evidence about brains.

### Systems / performance engineering

Useful contributions include:

- resource accessibility versus physical-capacity examples;
- scheduling, residency, queueing, or observation-state experiments;
- negative results showing where the abstraction fails.

### Visualization

Useful contributions include:

- clearer conceptual mappings;
- accessible interaction design;
- lightweight rendering;
- reduced-motion / keyboard accessibility;
- visuals that expose ambiguity without strengthening the scientific claim.

Read [docs/VISUALS.md](docs/VISUALS.md) before changing the interactive field.

## Contribution lanes

Use the repository's research lanes when proposing work:

~~~text
RQ-xxx     open research question
HYP-xxx    falsifiable hypothesis
VAL-xxx    model / harness / method validation
EXP-xxx    controlled experiment
BENCH-xxx  comparative benchmark
REF-xxx    named reference object
VIS-xxx    conceptual / explanatory visualization
~~~

## A good issue or pull request says

1. **Question** — what is being tested or clarified?
2. **Source** — which primary source, public dataset, or deterministic fixture
   motivates it?
3. **Observation** — what was actually measured or reported?
4. **Inference** — what is your interpretation?
5. **Falsifier** — what result would weaken the claim?
6. **Claim ceiling** — what must not be concluded?
7. **Reproduction** — how can another person rerun or inspect it?

Small, falsifiable contributions are preferred over broad speculative rewrites.

## Evidence

Canonical claims should be supportable from public inputs or deterministic
generators committed here.

Please do not submit private medical histories, identifying health records, or
personal medication anecdotes as repository evidence.

For neuroscience claims, prefer primary literature and include DOI / PubMed /
dataset identifiers where available.

For software dependencies, record repository, license, and pinned version or
commit when reproducibility depends on them.

## Code

Bootstrap Python code uses Python 3.12 and pytest.

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
~~~

The optional browser visual lives under `web/`.

~~~bash
cd web
npm install
npm run build
npm run dev
~~~

The browser visual must remain separable from the scientific Python harness.

## Safety

Do not propose human medication challenges, zolpidem rechallenge, intentional
parasomnia induction, or hazardous self-experimentation.

Clinical treatment decisions are outside this repository.

## Review principle

A contribution is welcome when it makes the research more inspectable,
falsifiable, reproducible, or understandable — including when it disproves a
working hypothesis.
