# Murofushi–Mizoguchi Control Branch

Date: 2026-10-06
Status: working research branch
Scope: DCS / human motor control / constraint-induced exploration

## Why this branch exists

This note records a DCS research line inspired by Koji Murofushi and Kazuhiro Mizoguchi, focusing not on extreme-training folklore itself but on a deeper control-system hypothesis:

> A local constraint or temporary degradation can expose alternative control policies that remain hidden when the dominant path has abundant capacity.

The branch is intentionally framed as a hypothesis-generation and cross-domain abstraction exercise. Biological claims require independent verification before being treated as established mechanisms.

## Core working hypothesis: fatigue as exploration pressure

A movement goal may be achievable through many different allocations of muscles, joints, timings, and motor units.

If a dominant contributor A normally carries most of the load,

```text
Goal
 ↓
A >>> B > C
```

then local fatigue or another controlled perturbation may reduce the usable capacity of A:

```text
Goal
 ↓
A degraded
 ↓
B / C / other coordination patterns become behaviorally relevant
```

The important hypothesis is not that fatigue literally creates a new neural wire on demand. A safer interpretation is:

- existing but low-priority coordination patterns can become more strongly recruited;
- motor-unit recruitment and timing can be redistributed;
- the controller is forced to search a different region of the available control space;
- repeated successful use may enlarge the practically usable policy repertoire.

In DCS language:

> fatigue is not necessarily the teacher; fatigue may be a search-space deformation mechanism.

## Failure-injection analogy

The branch maps naturally onto reliability engineering.

```text
healthy primary path
    ↓
success
```

reveals very little about hidden redundancy.

When the primary path is intentionally degraded:

```text
primary path degraded
    ↓
fallback / alternate coordination
    ↓
degraded but successful execution
```

the system reveals which alternate paths are actually usable.

This suggests a distinction:

```text
structural redundancy != usable redundancy
```

A body may possess multiple muscles and degrees of freedom capable of contributing to a task while the learned controller still relies heavily on one habitual solution.

## Cross-domain link: finite-ram-lab and Strata

The same pattern appears in finite-resource computing.

When RAM is abundant, the implementation can hide inefficient assumptions:

- everything resident;
- eager loading;
- duplication;
- unnecessary intermediate state;
- expensive representations preserved simply because resources permit them.

Under memory pressure those assumptions fail, exposing new options:

- cold state;
- streaming;
- recomputation;
- compression;
- offload;
- approximation;
- representation redesign.

Shared abstraction:

```text
Pressure
  -> constraint activation
  -> hidden redundancy / waste exposure
  -> alternative-policy search
  -> representation redesign
  -> cheaper viable solution
```

The same lens also resembles historical game development under severe RAM/CPU/storage constraints: the goal was not to reproduce an unconstrained implementation internally, but to preserve the player-visible outcome with a radically cheaper representation.

## Outcome equivalence over path equivalence

A second major principle emerged from the discussion:

> If the final observable result is equivalent, the internal derivation path does not need to match.

Let a reference implementation follow

```text
s0 -> s1 -> s2 -> ... -> s100 -> y
```

while an alternative implementation follows

```text
s0' -> s1' -> s2' -> y'
```

If the relevant semantics satisfy

```text
D(y', y) <= epsilon
```

then the shorter or cheaper path may be preferable even if its intermediate states differ completely.

A useful optimization statement is:

```text
minimize  PathCost(pi)
subject to Outcome(pi) ~= Outcome(target)
```

where PathCost can include:

- compute;
- RAM;
- storage;
- I/O;
- communication;
- latency;
- energy;
- number and cost of state transitions.

This yields the branch-level maxim:

> Preserve semantics, minimize transitions.

Working name:

**Outcome-Preserving Path Compression**

## Canonical-state interpretation

The stronger consequence is that intermediate state should not automatically be treated as essential state.

Instead of storing every implementation-specific step, seek the smallest state that is sufficient to reproduce the required outcome:

```text
large concrete state
    ↓
remove implementation-specific intermediates
    ↓
minimal sufficient / canonical state
    ↓
re-expand through the cheapest viable execution path
```

This connects directly to Canonical IR research:

- preserve outcome-relevant semantics;
- discard incidental representation;
- permit multiple execution policies;
- choose the lowest-cost valid projection for the current resource envelope.

## Tentative DCS principle

The Murofushi–Mizoguchi branch therefore currently centers on two coupled ideas.

### 1. Constraint-Induced Search

Controlled pressure can reveal alternative control policies, redundancy, and waste that abundant resources conceal.

### 2. Outcome-Preserving Path Compression

Once the invariant outcome is identified, the path is free to change. The preferred path is the cheapest one that remains within the required semantic tolerance.

Combined:

```text
apply bounded pressure
    ↓
observe what breaks
    ↓
discover alternate policies
    ↓
identify the actual outcome invariant
    ↓
remove unnecessary intermediate state
    ↓
compress toward the cheapest valid path
```

## Safety / falsification boundary

This branch must not be interpreted as endorsing extreme fatigue or injury-producing training. Excessive fatigue may impair learning, coordination, and tissue safety.

Research value lies in the abstract mechanism:

- bounded perturbation;
- alternative-policy discovery;
- recovery;
- consolidation;
- comparison against non-fatigued controls.

Possible falsifiers include:

- alternative recruitment appears only transiently and produces no durable control gain;
- fatigue reduces exploration quality more than it exposes useful alternatives;
- apparent alternate-path learning is explained entirely by compensation without retention;
- cheaper paths preserve coarse outcomes but destroy important hidden invariants.

## Next research questions

1. How much pressure is enough to expose a new policy without degrading learning quality?
2. Can the same effect be produced safely through mechanical constraints, altered task geometry, reduced degrees of freedom, or sensory perturbation instead of fatigue?
3. How should DCS define semantic outcome equivalence for biological movement?
4. Which intermediate states are implementation artifacts and which are true invariants?
5. Can the same formal model be instantiated across human motor control, finite-ram-lab, Strata, AI harnesses, and historical finite-resource game systems?
6. Can a pressure schedule be optimized automatically to maximize newly discovered viable policies per unit cost/risk?

## Current synthesis

The branch currently treats the Murofushi–Mizoguchi case as a biological entry point into a broader DCS idea:

> Abundance hides structure. Bounded pressure reveals structure. Once the invariant outcome is known, redesign the path freely and prefer the cheapest valid transition sequence.

## Derived branch: presbyopia / visual-control recovery

The visual-control extension has converged far enough to live in a dedicated note:

- [`PRESBYOPIA_CONTROL_RECOVERY_DIGITAL_TWIN_2026-10-06.md`](./PRESBYOPIA_CONTROL_RECOVERY_DIGITAL_TWIN_2026-10-06.md)

The key translation is that the Murofushi–Mizoguchi principle should **not** be implemented as deliberate eye fatigue. In the visual system, the safer analog is bounded sensory-cue perturbation and progressive control-space expansion: temporarily weaken a dominant cue, observe residual/alternate control, mechanically unlock only when necessary, then retrain newly reachable freedom.

That branch also formalizes an observable Digital Twin, identifiability limits, separate endpoints for true accommodation vs functional visual recovery, a Monte Carlo hypothesis stress test, and the `unlock -> retrain` prediction.
