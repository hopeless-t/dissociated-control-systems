# RQ-005 Next-observation plan for rare survivor residuals

## Trigger

The first METABRIC pilot produced a clinically high-risk residual class:
patients with high NPI / nodal burden who nevertheless crossed the 10-year
survival horizon.

Within NPI >= 5.5, LTS and STS have nearly identical mean NPI:

~~~text
LTS 6.061
STS 6.079
~~~

Yet the endpoint trajectories remain very different.

The highest-value next question is therefore no longer:

> Is the baseline tumor clinically high risk?

It is:

> What hidden state distinguishes high-risk tumors that are controlled for a
> long time from apparently similar high-risk tumors that kill early?

## Trajectory typing before mechanism typing

The LTS endpoint must first be split into at least:

~~~text
S0  no recorded recurrence
S1  late recurrence (>60 months)
S2  early recurrence (<=60 months) + prolonged post-recurrence control
~~~

Mechanism discovery must compare like trajectory with like trajectory where
possible.

## Two frozen S2 sentinels

The pilot contains two especially high-information examples:

~~~text
MB-5566
  NPI 6.064
  14 positive nodes
  Basal / IntClust 10
  recurrence at 20.23 months
  alive at 234.4 months
  observed post-recurrence interval >214 months

MB-4348
  NPI 6.08
  4 positive nodes
  HER2-like / IntClust 5
  recurrence at 44.9 months
  died of disease at 226.2 months
  observed post-recurrence interval >181 months
~~~

Both rows were independently re-observed in the current 2026 Zenodo clinical
snapshot.

## External constraint

Recent breast-cancer recurrence literature reports that early recurrence
usually predicts short post-recurrence survival, with strong dependence on
molecular subtype and recurrence site.

A 2026 young-breast-cancer cohort reported median post-recurrence survival
around 22 months for HER2-overexpressing disease and 26 months for TNBC after
early recurrence.

Cross-cohort numeric comparison is **not** used as an effect estimate because
age, era, therapy, recurrence site, and ascertainment differ.

The literature is used only to justify high value-of-information for these
extreme residual trajectories.

Reference:
https://pmc.ncbi.nlm.nih.gov/articles/PMC13090497/

A 2025 metastatic-breast-cancer exceptional-responder cohort also reports that
complete response / no-evidence-of-disease state is strongly enriched among
durable responders.

Reference:
https://pubmed.ncbi.nlm.nih.gov/39987798/

## Observation ladder

Rank candidate observations by expected ability to discriminate competing
worlds.

### O1 — recurrence topology and burden

Acquire if possible:

- first recurrence site;
- locoregional vs bone-only vs visceral vs brain;
- metastatic lesion count;
- oligometastatic vs polymetastatic state;
- radiologic CR/PR/SD/PD trajectory;
- no-evidence-of-disease intervals.

Why first:

recurrence site and achieved response state can explain large post-recurrence
survival differences without invoking a new upstream mechanism.

### O2 — treatment sequence and effective exposure

Acquire:

- exact systemic agents;
- line number;
- start/stop dates;
- dose intensity / interruptions;
- local treatment of metastases;
- endocrine / HER2-targeted exposure where historically available.

Invariant:

~~~text
recorded treatment category
!=
effective treatment trajectory
~~~

### O3 — paired primary / recurrence biology

Acquire when available:

- ER / PR / HER2 at recurrence;
- proliferation / grade;
- genomic evolution;
- copy-number state;
- acquired resistance alterations.

A primary tumor state may not represent the recurrent controller state.

### O4 — immune / TME state

Prioritize:

- CD8 / Treg / B-cell architecture;
- exhaustion markers;
- myeloid suppression;
- stromal / fibrosis state;
- spatial immune organization.

This tests whether the residual is better explained by host-tumor control state
than by primary tumor burden.

### O5 — dormancy / reactivation state

Metastatic dormancy is a mechanistically plausible separate axis from primary
tumor aggressiveness.

Candidate literature includes recent work on cancer-cell-intrinsic and
niche/immune regulation of dormancy and reawakening.

This is a hypothesis layer, not yet a patient-level explanation for the pilot
sentinels.

### O6 — systemic neuroendocrine / inflammatory state

Only after O1-O5 are controlled:

- inflammatory markers;
- longitudinal cortisol/autonomic proxies where available;
- sleep/activity;
- metabolic/systemic state.

### O7 — psychological / agency state

Narrative and psychometric variables remain legitimate candidate observations,
but they are deliberately late in the ladder.

They move upward only if they add prospective information beyond O1-O6 and
precede downstream divergence.

## Value-of-information rule

For observation q:

~~~text
VOI(q)
  =
  expected reduction in competing-world uncertainty
  * temporal relevance
  * independent-observer value
  / acquisition cost
~~~

The next observation is chosen by VOI, not by how well it supports the current
story.

## Meta-loop stop condition

Stop adding mechanistic layers when:

1. held-out model ranking stabilizes;
2. new observations no longer materially reduce residual uncertainty;
3. rare residual classes replicate independently or remain irreducibly
   heterogeneous;
4. remaining uncertainty is dominated by unavailable historical measurements.

At that point the correct output may be UNKNOWN rather than a single survivor
mechanism.
