# HF01 Minimum Sufficient Checkpoints

## Direction

The projection ladder should not preserve every intermediate step.

It should preserve only the checkpoints whose removal allows a declared
catastrophic error to pass undetected.

This changes the design objective from:

~~~text
show enough intermediate steps
~~~

to:

~~~text
retain the smallest checkpoint set that preserves all non-negotiable invariants
~~~

## Set-cover formulation

Let the catastrophic failure universe be:

~~~text
F = {f1, f2, ..., fm}
~~~

and each checkpoint c_i cover the subset S_i of failures it can detect or
block.

Find:

~~~text
C* = argmin |C|
subject to
union(S_i for c_i in C) = F
~~~

This is the minimum sufficient checkpoint set.

For the small contracts used in HF01, the repository uses an exact exhaustive
solver rather than a heuristic.

## Mandatory vs interchangeable

An important distinction:

~~~text
mandatory checkpoint:
    appears in every minimum sufficient solution

interchangeable checkpoint:
    one member of an alternative set is required, but no single member is
    individually mandatory
~~~

Therefore the UI should not keep two equivalent checks merely because both are
useful.

## Counterfactual deletion rule

For every checkpoint:

~~~text
remove checkpoint
re-run declared failure coverage
observe newly exposed failures
~~~

If deletion exposes no required failure, the checkpoint is a compression
candidate.

If deletion exposes a required failure, the checkpoint has structural value.

This is the explanation equivalent of an ablation test.

## Current HF01 catastrophic classes

The first frozen failure universe is deliberately small:

### C0 — provenance loss

The reader can no longer distinguish source observation from model inference.

### C1 — state/response confusion

A disease-separating coordinate is mistaken for an intervention-response
coordinate.

### C2 — uncertainty laundering

An UNKNOWN/ASSUMED bridge is presented as grounded fact.

### C3 — reachability overclaim

A current state or early response is treated as proof that the target state is
reachable.

These correspond directly to failures already observed during HF01.

## Candidate irreducible checkpoint roles

The current human-facing flow should therefore preserve functionally:

~~~text
1. Provenance checkpoint
   What was actually measured / sourced?

2. State-vs-response checkpoint
   Does this observation describe current state, response to input, or both?

3. Uncertainty checkpoint
   Which bridge is SUPPORTED / ASSUMED / UNKNOWN / FALSIFIED?

4. Reachability checkpoint
   Does the evidence establish reachability, or must the answer remain UNKNOWN?
~~~

The exact UI element implementing each role is replaceable.

The role is what matters.

## What gets removed

Examples of content that should disappear from the mandatory path when ablation
shows no loss of invariant coverage:

- repeated definitions;
- decorative pathway detail;
- mechanistic trivia that does not change a decision;
- two visualizations that guard the same failure;
- explanatory stages that the user already reconstructs correctly.

Such material may remain expandable, but it should not occupy the compulsory
path.

## Relation to projection density

HF-SIM-004 asks how much explanatory subdivision minimizes friction.

HF-SIM-007 adds a harder constraint:

~~~text
never compress past an invariant-bearing checkpoint
~~~

So the new optimization is:

~~~text
minimize exposed explanation cost

subject to:
    all declared catastrophic failures remain covered
    claim ceiling remains correct
    reconstruction error remains below threshold
    uncertainty is preserved
~~~

Projection density is therefore adaptive between mandatory checkpoints.

## Human interpretation

A useful interface should feel shorter over time.

As the person learns an edge and repeatedly reconstructs it correctly, the
system can collapse that explanatory region.

But it must not collapse a non-negotiable checkpoint merely because the user is
confident.

Confidence is not coverage.

## Current fixed-point statement

The target is no longer a long explanatory ladder.

It is:

> a sparse path through a richer latent projection graph, retaining only the
> checkpoints whose absence would permit a known class of epistemic or control
> failure.

This is closer to a proof skeleton than to a textbook chapter.
