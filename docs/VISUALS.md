# Visuals

> **Visual contract:** Visualization != Evidence

This document defines how visual material may be used in Dissociated Control
Systems.

## Purpose

Visuals have three legitimate jobs here:

1. reduce comprehension cost;
2. expose model structure and ambiguity;
3. invite inspection and contribution.

They are not acceptance or truth authorities unless a future experiment
contract explicitly says otherwise.

## Current visual: Dissociated State Field

The optional browser demo under `web/` is a **conceptual projection**.

It maps four synthetic accessibility dimensions:

~~~text
motor
procedural
executive
memory
~~~

to four families of moving state particles.

The coarse observable is:

~~~text
complex_action =
    motor >= 0.5
    AND
    procedural >= 0.5
~~~

The visual intentionally lets executive and memory accessibility change while
the coarse observable remains unchanged.

That is the point being illustrated:

~~~text
same coarse observation
can remain compatible with
different richer subsystem states
~~~

## Mapping table

| Visual feature | Model-side meaning | Claim status |
| --- | --- | --- |
| Four particle families | Four bootstrap subsystem dimensions | Conceptual |
| Slider value | Synthetic accessibility value in [0,1] | Direct UI state |
| Flow speed / reach | Accessibility-weighted expression | Conceptual mapping |
| Convergence toward portal | Contribution to coarse observable | Conceptual mapping |
| Dissociation index | Formula from MATHEMATICAL_MODEL.md | Deterministic calculation |
| Observable badge | Frozen VAL-001 coarse predicate | Deterministic calculation |
| Noise / trails | Visual legibility and continuity | Decorative / explanatory |

Particle paths, colors, spatial positions, and apparent forces are **not**
biological measurements.

## Technology

The first implementation uses:

- `pmndrs/math` for seeded random and simplex-noise primitives;
- browser-standard Canvas2D for the public renderer;
- `pmndrs/math` for seeded random and simplex-noise trajectory primitives;
- ordinary HTML/CSS controls for inspectable interaction.

`gpucat` remains recorded as an experimental rendering reference, but VIS-001
uses Canvas2D as its canonical public backend after real-browser testing found a
blank WebGL field on the target Lubuntu/Chrome environment.

Pinned provenance is recorded under `external/`.

## Design requirements

Every repository visual should:

- identify whether it is conceptual, measured, simulated, or illustrative;
- keep the scientific claim ceiling visible;
- remain useful without animation where possible;
- avoid implying causal pathways that have not been measured;
- avoid fake precision;
- expose the inputs controlling the visual;
- preserve a text explanation in README/docs.

## Accessibility

Interactive visuals should prefer:

- keyboard-operable controls;
- visible labels;
- sufficient text contrast;
- a reduced-motion mode when the browser requests it;
- no information encoded by color alone.

## Recruitment surface

The visual is deliberately allowed to be attractive.

A public research repository benefits when a new visitor can understand the
question before reading every paper.

The permitted chain is:

~~~text
visual curiosity
  ↓
model comprehension
  ↓
source inspection
  ↓
contribution
~~~

The forbidden shortcut is:

~~~text
beautiful animation
  ↓
therefore the hypothesis is true
~~~

## Future VIS lanes

Candidate future visual work:

~~~text
VIS-001  Dissociated State Field          CURRENT
VIS-002  Observation-equivalence explorer
VIS-003  Hidden-state posterior explorer
VIS-004  Cross-domain correspondence map
~~~

Future visual IDs describe design work, not scientific experiments.
