# HF01 Proof-Carrying Projection

The minimum-checkpoint model still allowed an implementation to *claim* that
all roles had been considered without proving the terminal claim actually
passed through them.

HF01 therefore adds a proof-carrying projection protocol.

## Core idea

Every terminal claim carries a compact trace:

~~~text
PROVENANCE
    ↓
STATE / RESPONSE TYPING
    ↓
UNCERTAINTY
    ↓
REACHABILITY
    ↓
terminal status
~~~

The trace is part of the claim artifact.

It is not optional explanatory metadata.

## Fail-closed semantics

Each checkpoint records:

~~~text
PASS
UNKNOWN
FAIL
~~~

Terminal propagation:

~~~text
any FAIL       -> FAIL
else any UNKNOWN -> UNKNOWN
else             PASS
~~~

A request to present the endpoint as an empirical claim is rejected unless all
required checks pass.

Therefore a fluent explanation cannot upgrade UNKNOWN into empirical fact.

## Why order matters

The roles are not merely a checklist.

For example, uncertainty must be evaluated *after* the quantity has been typed
as state/response and before reachability is asserted.

A trace containing all four roles in arbitrary order is not accepted.

This converts the checkpoint set into a protocol.

## Threat model

The protocol explicitly treats these as hostile shortcuts:

- a person mentally fills an omitted causal bridge;
- an LLM invents a plausible intermediate edge;
- a UI jumps directly from a state score to a recommendation;
- a mechanistic source is silently treated as a recovery guarantee.

The system cannot prevent a human from imagining a bridge.

It can prevent the official endpoint claim from acquiring authority without the
required trace.

## Compression property

Detailed explanation can still collapse.

The proof trace can remain four short badges:

~~~text
SOURCE: public-data + model inference
TYPE: state-separation, not response
CEILING: candidate / response UNKNOWN
REACHABILITY: UNKNOWN
~~~

That is enough to preserve the correctness barriers while hiding optional
detail.

## Current interpretation

The minimum viable explanation is not the shortest sentence.

It is the shortest sentence plus the smallest valid proof trace.
