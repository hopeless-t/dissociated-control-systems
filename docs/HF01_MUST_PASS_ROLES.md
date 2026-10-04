# HF01 Must-Pass Roles

The phrase "must pass" is stronger than "useful checkpoint".

HF01 therefore distinguishes:

~~~text
checkpoint instance
    a concrete slide, panel, assay label, dialog, or code node

checkpoint role
    an invariant that must be enforced somewhere on every accepted path
~~~

Two different slides can implement the same role.

Neither slide is sacred.

The role is.

## Dominator formulation

Let the projection system be a directed graph from:

~~~text
source = hypothesis / formal model
target = calibrated human-facing claim or decision
~~~

A concrete node dominates the target when every source-to-target path contains
that node.

More useful for HF01 is role domination:

> a semantic role dominates the target when every accepted path contains at
> least one node implementing that role.

This allows representation to adapt without allowing invariant bypass.

## Current mandatory role candidates

### Provenance

The path must expose what came from:

- source observation;
- public data;
- synthetic model;
- inference.

If omitted, evidence can be laundered into narrative.

### State/response typing

The path must say whether a quantity is:

- current state;
- state-separating coordinate;
- response to input;
- or reachability evidence.

If omitted, GSE178510-style mistakes recur.

### Uncertainty

The path must preserve:

- SUPPORTED;
- ASSUMED;
- UNKNOWN;
- FALSIFIED.

If omitted, explanatory smoothness can over-promote a claim.

### Reachability

The path must explicitly ask whether the available evidence establishes that the
target state is reachable under the declared actuator class.

If not, the answer remains UNKNOWN.

## Compression rule

Between must-pass roles:

~~~text
compress aggressively
~~~

At a must-pass role:

~~~text
do not bypass
~~~

If the user already understands the content, the checkpoint can be rendered as
a one-line badge rather than a full explanatory slide.

So adaptive explanation changes checkpoint *presentation cost*, not checkpoint
*existence*.

## Stronger optimization objective

The projection system should minimize:

~~~text
visible explanation cost
~~~

subject to:

~~~text
every accepted path traverses every required semantic role
no unsupported edge is promoted
user reconstruction remains correct
uncertainty remains calibrated
~~~

This is closer to compiler IR validation than to textbook exposition.

Many intermediate explanatory nodes are optimization hints.

Must-pass roles are correctness barriers.

## Current compact HF01 path

A minimal human-facing skeleton can therefore look like:

~~~text
[1] SOURCE / PROVENANCE
        ↓
[2] STATE vs RESPONSE
        ↓
[3] UNCERTAINTY / CLAIM CEILING
        ↓
[4] REACHABILITY or UNKNOWN
        ↓
    calibrated claim
~~~

Mechanistic and molecular detail can expand between these gates when needed.

The mandatory path stays short.

## Meta-meta conclusion

The goal is not to preserve intermediate detail.

It is to preserve the small set of semantic barriers whose removal allows a
known failure class to reach the endpoint.

Everything else is a candidate for adaptive compression.
