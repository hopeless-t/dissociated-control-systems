# CGD-OBS-001 — External Observational Source Intake

> Status: SOURCE QUALIFICATION / NO DATA INGESTION  
> Clinical authority: NONE  
> Participant-level human data processed: NONE

## Research question

The synthetic CGD lane repeatedly identified a signed discrepancy between
self-estimated and objective/independent state as an important control variable.

Before selecting any human dataset, ask:

> Is there domain-local observational evidence that self vs independent or
> informant assessment discrepancy is measurable and related to cognitive
> status/progression?

The answer from the literature is **yes as a research construct**, but that does
not validate the DCS synthetic state model.

## Candidate 1 — ADNI ECog

Official ADNI materials list Everyday Cognition (ECog) participant self-report
and study-partner report instruments across multiple ADNI phases.

Source:
https://adni.loni.usc.edu/data-samples/adni-data/clinical-assessments/

Published ADNI analyses have explicitly studied self/informant ECog discrepancy,
including longitudinal associations with objective cognitive decline and
Alzheimer-related markers.

Examples:

- PMID 32011757 — MCI under/over-estimation and AD pathology/prognosis.
- PMID 30278855 — longitudinal ECog discrepancy in MCI subtypes.
- PMID 40249614 — ADNI/eVAL self-study-partner discordance and MCI diagnosis.
- PMID 41380294 — multimodal neural correlates of cognitive awareness using
  subject/informant ECog discrepancy.

Disposition:

~~~text
published aggregate analyses -> ADMIT_LITERATURE_PRIOR
participant-level ADNI data  -> HOLD_ACCESS_OR_DUA
~~~

ADNI raw data is available to approved users through LONI/IDA under a Data Use
Agreement. The current DUA also places explicit restrictions/conditions around
AI-tool handling of ADNI participant-level data.

Therefore this repository does not download, copy, transform, or ingest ADNI
participant-level data in CGD-OBS-001.

## Candidate 2 — Brain Health Registry / eVAL

The Brain Health Registry describes de-identified data-sharing collaborations
for qualified investigators and notes that some third-party cognitive
assessment data require vendor approval.

Source:
https://www.brainhealthregistry.org/for-investigators/de-identified-data-sharing/

The eVAL cohort also appears as an external validation cohort in the published
self/study-partner discordance literature (PMID 40249614).

Disposition:

~~~text
published aggregate analysis -> ADMIT_LITERATURE_PRIOR
raw BHR/eVAL collaboration data -> HOLD_COLLABORATION_OR_VENDOR_APPROVAL
~~~

## Candidate 3 — independent MCI discrepancy literature

PMID 40857141 reports a longitudinal MCI cohort using self/informant subjective
memory complaint discrepancy and found that underreporting was associated with
progression and Alzheimer-related biomarker burden.

Disposition:

~~~text
peer-reviewed aggregate result -> ADMIT_LITERATURE_PRIOR
underlying participant data -> not qualified by this intake
~~~

## What transfers into DCS now

Domain-local literature supports studying at least:

~~~text
self report
independent / informant report
objective cognitive performance
longitudinal change
diagnostic/progression outcome
biomarker context
~~~

This is enough to strengthen the **research question**:

> Can discrepancy dynamics provide useful observation of metacognitive
> calibration under cognitive decline?

It is not enough to establish:

~~~text
DCS synthetic L1 == biological anosognosia
ECog discrepancy == latent capability
a DCS probe == a clinical diagnostic
association == mechanism
~~~

## Next qualified step

No participant-level dataset should be acquired through this chat unless its
access agreement, privacy rules, and AI-tool constraints are explicitly
compatible.

The next repo-local step can be performed without raw human data:

1. freeze an observational variable map from published instrument semantics;
2. define self/informant/objective discrepancy metrics without fitting them;
3. pre-register falsification and missingness rules;
4. only then evaluate whether an appropriately authorized dataset can execute
   that protocol.

## Compact boundary

~~~text
Literature Prior != Raw Dataset Access
Data Access != AI Processing Permission
Observational Association != Causal Mechanism
Self/Informant Discrepancy != DCS Latent State Ground Truth
~~~
