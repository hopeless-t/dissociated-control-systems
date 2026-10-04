# CGD-EXT-001 — External observation and data-rights admission

> Status: PUBLIC EVIDENCE / SCHEMA INTAKE  
> Clinical authority: NONE  
> Participant-level external data ingested here: NONE

## Why this lane exists

SIM-035 through SIM-037 reached a local information boundary:

~~~text
cause / fault class
    !=
current functional state
    !=
action authority
~~~

The next justified move is therefore not a stronger synthetic oracle. It is to
ask which externally measured variables can observe current function and
self/objective divergence.

Before scientific utility, however, data-handling authority must be checked.

~~~text
Scientific Relevance != Data-Handling Permission
~~~

## Candidate external sources

### ADNI public documentation and published aggregate literature

Public ADNI documentation shows that the study contains complementary channels
needed by the CGD model:

- participant ECog self-report;
- study-partner ECog report;
- Functional Assessment Questionnaire (FAQ);
- Clinical Dementia Rating (CDR);
- objective cognitive measures including MMSE, MoCA, AVLT and Trails;
- repeated/longitudinal collection across study phases.

These public schemas are admissible for designing a variable map.

Published ADNI analyses also establish that participant/study-partner
**discordance is scientifically nontrivial**, including:

- PMID 32011757: MCI participants who underestimated their decline had poorer
  memory, smaller hippocampal volume, greater AD pathology and greater
  longitudinal deterioration than overestimators;
- PMID 40249614: self/study-partner ECog discordance contributed to a model that
  distinguished cognitively unimpaired versus MCI participants with high
  specificity in an external validation cohort;
- PMID 40857141: underreporting of memory deficits in MCI was associated with
  greater biomarker burden and increased longitudinal conversion risk;
- PMID 41380294: longitudinal and cross-sectional ECog awareness discrepancy was
  related to multimodal AD biomarkers in ADNI.

These publications support the *measurement question*. They do not make an
ECog discrepancy score a diagnosis or intervention gate.

### ADNI participant-level data

The current public ADNI Data Use Agreement explicitly restricts use of ADNI
participant-level data with AI tools where data containment is not guaranteed.

Therefore this repository records:

~~~text
ADNI participant-level data
    -> NO_INGEST in this ChatGPT execution path
~~~

No workaround, copy, export or indirect ingestion is authorized by CGD-EXT-001.

### NACC

Public NACC UDS documentation supports a longitudinal functional/cognitive lane,
including informant-based FAQ. Participant-level data require a data request.
This repository has not established source-specific AI-use permission, so:

~~~text
NACC public schema -> ADMIT_SCHEMA_ONLY
NACC participant data -> DEFER_RIGHTS_REVIEW
~~~

Importantly, PMID 31964443 found that NACC FAQ ratings in MCI varied with
informant characteristics such as cohabitation and relationship even after
adjustment for participant cognition and other covariates.

Therefore:

~~~text
Informant Report != Ground Truth
~~~

### Brain Health Registry

Public BHR documentation describes longitudinal online questionnaires,
participant/study-partner reporting and cognitive assessments. Data sharing is
controlled by a DUA and some cognitive data can require third-party vendor
approval.

~~~text
BHR public schema -> ADMIT_SCHEMA_ONLY
BHR participant data -> DEFER_RIGHTS_REVIEW
~~~

## Compensation / rerouting evidence

The external observation lane must remain separate from the Track A
compensation lane.

Published prospective-memory intervention work is useful here because it shows
that function can improve without implying disease modification:

- PMID 34786698: a randomized trial in older adults with MCI or mild dementia
  tested smartphone reminder/voice-recorder strategies for off-loading
  prospective intentions;
- PMID 19332424: cognitive rehabilitation in amnestic MCI improved objective
  prospective-memory performance and strategy use, while self-appraisal of
  everyday memory did not show a corresponding intervention effect.

The second result is especially relevant to DCS because it separates:

~~~text
objective functional improvement
    from
self-appraisal change
~~~

Thus:

~~~text
Compensation != Disease Modification
Functional Improvement != Awareness Calibration
~~~

## Admission result

CGD-EXT-001 admits only:

1. public metadata/schema;
2. public aggregate literature;
3. mathematical modeling derived from those public materials.

It does not admit controlled participant-level ADNI, NACC or BHR data into this
execution environment.

## Next experiment

Use the public evidence to test a structural question before any data request:

> Are self-report and informant-report alone sufficient to identify current
> impairment and reporter bias, or is an independent objective channel
> mathematically required?

This becomes SIM-038.
