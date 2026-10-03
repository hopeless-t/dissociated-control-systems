# RQ-001 — AI-assisted retrieval dissociation

**Status:** OPEN RESEARCH  
**Authority:** NONE  
**Clinical authority:** NONE  
**Production-control authority:** NONE

## Question

Can a system show high performance while an external cognitive scaffold is
present, yet show substantially lower independent retrieval after that scaffold
is removed?

This is a narrower instance of the repository's existing distinction:

```text
Capability != Accessibility
Observable Behavior != Unique Internal State
```

For this lane we add:

```text
Joint-Context Performance != Independently Retrievable Knowledge
Assisted Success != Internalized State
Feedback Aid != Answer Substitution
```

The terms are operational labels for a synthetic model. They are not claims
about a unique biological memory mechanism.

## Motivation

The October 2026 essay "AI時代の勉強法(2026)" describes a practical loop:
learn with AI support, explain the material without looking, use the places
where explanation fails as a signal, ask the AI only about those gaps, then
explain again and request corrective feedback.

That workflow is interesting here because removing the scaffold acts as an
observation intervention. A successful answer while AI/context is present does
not identify whether the performance came from independently retrievable
knowledge, the external scaffold, or both.

Research on retrieval practice provides a separate empirical reason to measure
unaided reconstruction. A 2025 meta-analysis found a small overall advantage
of retrieval practice over elaborative conditions, with a substantially larger
advantage in comparisons where feedback was supplied. An RCT of an
AI-powered tutor also reported learning gains relative to in-class active
learning, while other experimental work has reported retention costs under
unrestricted ChatGPT use. These findings are heterogeneous; this repository
does not treat "AI use" as one intervention.

## Synthetic state

The first deterministic primitive is:

```text
k = internal_capability  in [0,1]
r = retrieval_access     in [0,1]
a = external_scaffold    in [0,1]

independent = k * r
assisted    = max(independent, a)
gap         = assisted - independent
```

The `max` composition is intentionally a toy assumption. It is chosen because
the known-answer test is transparent, not because it is asserted to be a
psychological law.

Two states can therefore have the same coarse assisted score:

```text
State A: k=1.0, r=0.2, a=0.9  -> assisted=0.9, independent=0.2
State B: k=0.9, r=1.0, a=0.9  -> assisted=0.9, independent=0.9
```

The assisted observation alone is non-identifying. Removing the scaffold
("context eviction") creates a second observation that separates the states.

## Candidate measurement loop

```text
INGEST
  -> ASSISTED EXPLANATION
  -> CONTEXT EVICTION
  -> FREE RECALL / RECONSTRUCTION
  -> GAP CAPTURE
  -> TARGETED FEEDBACK
  -> REPLAY
  -> ADVERSARIAL CHECK
  -> DELAYED RETRIEVAL
```

Candidate observables:

- assisted score before eviction;
- independent score immediately after eviction;
- `offloading_gap = assisted - independent`;
- error classes found during free recall;
- gain after targeted feedback;
- delayed independent retrieval after a declared interval;
- transfer to a differently phrased or structurally altered task.

## Falsifiable directions

**HYP-005 — Assisted/Independent Retrieval Dissociation.**

For at least some tasks and assistance policies, assisted performance can remain
high while independent retrieval is materially lower; an assisted score alone
therefore cannot identify independent knowledge accessibility.

Potential falsifiers include a task family where controlled assistance never
creates a reproducible assisted/independent gap, or where the gap disappears
under measurement controls showing that it was purely an instrumentation
artifact.

A stronger future hypothesis may compare answer-substitution assistance with
calibration-only feedback. It is intentionally not asserted yet.

## Experimental controls needed before human-learning claims

A later human-learning experiment would need, at minimum:

- pre-registered task and scoring rubric;
- matched baseline knowledge;
- separation of answer-providing and feedback-only conditions;
- fixed context-eviction procedure;
- held-out transfer items;
- delayed retrieval measurement;
- contamination logging;
- blinded or deterministic scoring where possible;
- multiple models/providers or a model-independent control if an AI effect is
  being claimed.

No human experiment is authorized by this note.

## Cross-project relationship

MVCA can use the same distinction for agent evaluation: success in a rich
joint context should not automatically be interpreted as durable Worker
capability. MVCA authority, routing, and production adoption remain separate
questions governed in that repository.

Likewise, a result here cannot grant MVCA mainline authority.

## Sources

- iwashi.co, "AI時代の勉強法(2026)", 2026-10-01:
  https://iwashi.co/2026/10/01/how-to-study-in-ai-era
- Gonçalves, Muniz, Jaeger, "Retrieval Practice Versus Elaborative Encoding:
  A Systematic and Meta-analytic Review", Educational Psychology Review (2025):
  https://doi.org/10.1007/s10648-025-10076-6
- Kestin et al., "AI tutoring outperforms in-class active learning", Scientific
  Reports (2025): https://doi.org/10.1038/s41598-025-97652-6
- "ChatGPT as a cognitive crutch: Evidence from a randomized controlled trial
  on knowledge retention" (2025):
  https://doi.org/10.1016/j.ssaho.2025.102287
