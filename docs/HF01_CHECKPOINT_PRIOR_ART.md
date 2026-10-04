# HF01 Checkpoint Prior Art

> Purpose: orient the projection/checkpoint architecture against external human-factors and interpretable-AI ideas.
> These sources motivate design analogies. They do not validate HF01 biology.

## Forcing functions — human factors

AHRQ/PSNet describes forcing functions as design features that prevent an undesired action or permit an action only after another required action has occurred.

HF01 analogue:

~~~text
do not merely remind the reader to consider uncertainty

instead:

do not permit empirical claim emission until the required uncertainty
checkpoint has a valid proof-trace record
~~~

Source:

- AHRQ PSNet, Human Factors Engineering:
  https://psnet.ahrq.gov/primer/human-factors-engineering

AHRQ also describes forcing functions as higher-reliability strategies than relying only on education, reminders, or working harder.

- AHRQ, Implement the VTE Prevention Protocol:
  https://www.ahrq.gov/patient-safety/settings/hospital/vtguide/guide5.html

## Checklist design — necessary steps can still create burden

A 2024 BMJ Quality & Safety review emphasizes that checklists are widespread cognitive aids but are often designed or deployed poorly; merely having a checklist does not guarantee effectiveness.

HF01 implication:

~~~text
mandatory semantic barrier
!=
large mandatory checklist
~~~

The role should remain enforced while its visual/presentation cost is minimized.

Source:

- Alfred M, Barg-Walkow LH, Keebler JR, Chaparro A.
  Checking all the boxes: a checklist for when and how to use checklists effectively.
  BMJ Qual Saf. 2024. PMID 38697804.

## Concept bottlenecks — intermediate semantics need grounding

Concept Bottleneck Models expose human-readable intermediate concepts rather than mapping inputs directly to outputs.

Recent work also stresses that concept uncertainty must propagate, misleading or missing concept states can corrupt downstream inference, and interpretable concepts should be tied to inspectable evidence.

HF01 analogue:

~~~text
projection checkpoint
    must preserve
concept meaning + provenance + uncertainty
~~~

Relevant examples:

- ReCBM: uncertainty-gated relational reasoning for concept bottlenecks (2026), arXiv:2608.10004.
- Prototype-Grounded Concept Models for Verifiable Concept Alignment, ICML 2026, PMLR 306.

## Boundary

HF01 is not claiming that human comprehension is a Concept Bottleneck Model or that medical forcing functions prove this projection protocol is optimal.

The transferable engineering pattern is narrower:

> when a known failure must not cross a boundary, rely on structural constraints rather than hoping the operator remembers every rule.
