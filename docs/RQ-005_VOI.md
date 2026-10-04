# RQ-005 Evidence-grounded value of information

## Purpose

RQ-005 now has several competing explanations for durable survivor trajectories.
The next measurement should be selected by how much it is expected to reduce
uncertainty between those worlds, not by narrative appeal.

For declared worlds W and candidate observation Q:

~~~text
IG(Q) = H(W) - E_q[H(W | Q=q)]

VOI_per_cost(Q) = IG(Q) / cost(Q)
~~~

Implementation:

- `src/dissociated_control_systems/survivor_voi.py`
- `tests/test_survivor_voi.py`

## Critical evidence rule

The arithmetic can rank only likelihoods that already exist.

Therefore:

~~~text
VOI Calculator != Evidence Generator
P(observation | world) must not be invented to make a preferred world win.
~~~

Allowed likelihood sources:

1. held-out cohort estimates;
2. externally replicated observational estimates with compatible definitions;
3. randomized/interventional estimates where the estimand is appropriate;
4. an explicitly labelled synthetic known-answer fixture used only to validate
   the calculation.

If likelihoods are not identifiable from available evidence, the candidate
observation remains `VOI_UNKNOWN` rather than receiving an arbitrary score.

## Known-answer validation

The unit tests freeze basic information-theory behavior:

~~~text
uniform 4-world prior             -> 2 bits entropy
non-informative binary probe      -> 0 bits expected information gain
perfect 2-world discriminator     -> 1 bit expected information gain
same information, lower cost      -> higher information-per-cost
invalid likelihood normalization  -> fail closed
~~~

These tests validate the calculator, not the oncology model.

## Current qualitative ordering

The current literature constrains the ordering without yet supporting numeric
likelihoods for the METABRIC sentinels.

### Response depth / NED state

A 2025 metastatic breast-cancer exceptional-responder cohort identified 58
patients with responses lasting more than twice expected PFS. CR/NED was
observed in 69% and was associated with better outcome than partial response.

This makes response depth a high-value discriminator for the current
post-recurrence durable-control residuals.

Reference: PMID 39987798.

### Metastatic immune/TME and dormancy/niche

Current reviews describe metastatic dormancy and reactivation as dynamic,
context-dependent states shaped by cancer-cell-intrinsic programs together
with immune cells, stromal cells, extracellular matrix, and organ-specific
niches. Immune populations can either inhibit or promote metastatic
progression depending on stage and phenotype.

References:

- PMID 40628544
- PMID 39821034
- PMID 41855938
- PMID 42032160

This supports measuring metastatic site and TME/niche state, but it does not
establish that dormancy explains MB-5566, MB-4348, or any other pilot case.

## Current observation tiers

Until numeric observation likelihoods are learned, RQ-005 keeps a qualitative
VOI ladder:

~~~text
Tier A
  recurrence site/topology/burden
  radiologic response depth / CR / NED history
  exact treatment sequence and local metastatic treatment

Tier B
  paired primary-vs-recurrence biology
  recurrent-tumor genomic/evolutionary state
  metastatic immune/TME architecture

Tier C
  dormancy/reactivation biomarkers when a validated human measurement exists
  systemic inflammatory/neuroendocrine trajectory

Tier D
  psychological/agency state and survivor narrative variables
~~~

Tier D is not considered unimportant. It is placed later because a measured
psychological difference is difficult to interpret causally until major
post-recurrence tumor, treatment, response, and TME competitors are observed.

## Promotion rule

A candidate observation can move upward when it demonstrates conditional
information beyond the layers above it:

~~~text
I(Q ; future transition | existing state) > 0
~~~

and reproduces in held-out data.

A variable can therefore rise or fall in the hierarchy as evidence arrives.
The hierarchy is an adaptive observation policy, not a permanent biological
ranking.

## Stop rule

If repeated new observations add little expected information and model ranking
stabilizes, stop adding layers.

If the remaining candidate likelihoods cannot be identified from historical
data, return:

~~~text
MECHANISM_NONIDENTIFIABLE_WITH_AVAILABLE_OBSERVATIONS
~~~

rather than filling the gap with a survivor story.
