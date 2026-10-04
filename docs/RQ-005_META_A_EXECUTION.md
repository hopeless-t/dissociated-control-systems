# RQ-005 META-A execution contract

## Goal

Reproduce the 2026 Asakawa-Haas et al. primary psychosocial-survival
meta-analysis from the authors' frozen public artifacts before performing any
DCS-specific reanalysis.

This document separates four states:

~~~text
ARTIFACT DISCOVERED
ARTIFACT VERIFIED
AUTHOR RESULT REPRODUCED
DCS REANALYSIS PERFORMED
~~~

They are not interchangeable.

## Frozen upstream identity

Manifest:

- `specs/RQ-005-META-A-OSF-MANIFEST.json`

The manifest records OSF file IDs, GUIDs, exact sizes, and SHA256 digests for
selected S2/S3 upstream assets.

The current ChatGPT execution environment could enumerate the OSF API but could
not retrieve binary files because outbound DNS/download access is unavailable.
That infrastructure limitation is not an upstream data-access failure.

Current status:

~~~text
artifact discovery:       PASS
artifact identity freeze: PASS
artifact byte download:   NOT EXECUTED IN THIS ENVIRONMENT
author result reproduced: NOT YET
DCS reanalysis:           NOT YET
~~~

## Stage 0 — acquire without transformation

Download the original OSF artifacts by GUID/file ID into a dedicated immutable
input directory.

Do not:

- resave XLSX files;
- normalize line endings in R code;
- rename and overwrite upstream files in place;
- convert spreadsheets before the raw artifact hash is recorded.

## Stage 1 — verify exact bytes

Run:

~~~text
python analysis/rq005_verify_meta_artifacts.py \
  specs/RQ-005-META-A-OSF-MANIFEST.json \
  /path/to/raw-osf-artifacts \
  --output /path/to/verification.json
~~~

The verifier checks:

- every frozen file exists;
- byte size matches;
- SHA256 matches;
- manifest names are unique;
- malformed manifest entries fail closed.

Implementation:

- `src/dissociated_control_systems/artifact_verification.py`
- `tests/test_artifact_verification.py`
- `analysis/rq005_verify_meta_artifacts.py`

Promotion condition:

~~~text
ALL_ARTIFACTS_VERIFIED
~~~

Anything else stops execution.

## Stage 2 — reproduce the authors' primary analysis unchanged

Use the authors' published analysis environment as closely as practical.
The article reports R 4.3.0 and Metafor 4.0.0 for the primary analysis.

Record at minimum:

~~~text
R version
sessionInfo()
package versions
OS / architecture
upstream artifact hashes
command / entry script
stdout/stderr
exit status
produced summary statistics
~~~

The first target is reproduction of the reported primary synthesis, not a DCS
alternative model.

Expected paper-level targets to compare against include:

~~~text
32 RCTs
5,704 participants
overall survival HR approximately 0.80
95% CI approximately 0.71-0.90
I^2 approximately 48%
95% prediction interval approximately 0.49-1.29
~~~

These numbers are comparison targets from the publication. They must not be
written into a generated result as if they had been independently reproduced.

## Stage 3 — construct the trial identity ledger

Before changing any pooling rule, build:

- `specs/RQ-005-META-A-TRIAL-LEDGER.schema.json`

and validate the semantic identity mapping with:

- `src/dissociated_control_systems/trial_ledger.py`
- `tests/test_trial_ledger.py`

Required invariant:

~~~text
Publication != Trial
Follow-Up Paper != New Randomization
~~~

A stable `trial_id` must map to one randomized population. Primary,
long-term-survival, recurrence, and mediator papers may all map to the same
trial without becoming independent statistical units.

## Stage 4 — reconcile 2024 vs 2026 syntheses

Only after Stage 2 succeeds:

1. reconstruct which trials/publications enter each review;
2. harmonize effect metrics where defensible;
3. identify duplicate or updated publications;
4. compare endpoint hierarchy;
5. compare disease-stage scope;
6. compare follow-up rules;
7. perform leave-one-trial-out influence checks;
8. reproduce defensible multiverse specifications;
9. test moderator interactions without treating exploratory significance as a
   biological mechanism.

## Stage 5 — DCS-specific mechanistic bridge

Only after quantitative synthesis is reconciled should META-A inform RQ-005
mechanism priors.

The bridge remains:

~~~text
randomized intervention
 -> measured psychological / behavioral state
 -> measured neuroendocrine / immune state
 -> transition-specific cancer outcome
~~~

A pooled survival HR does not identify the active mediator.

## Failure taxonomy

Execution failures must be typed rather than repaired silently:

~~~text
ARTIFACT_MISSING
ARTIFACT_HASH_MISMATCH
UPSTREAM_RUNTIME_MISMATCH
DEPENDENCY_FAILURE
AUTHOR_RESULT_NOT_REPRODUCED
TRIAL_IDENTITY_AMBIGUOUS
EFFECT_METRIC_NONCOMPARABLE
POST_RANDOMIZATION_SELECTION_RISK
MODERATOR_UNDERPOWERED
MECHANISM_NONIDENTIFIABLE
~~~

The failure specimen is preserved before changing code/specifications.

## Meta-loop rule

~~~text
First reproduce.
Then explain discrepancies.
Then vary one justified assumption at a time.
Never optimize the specification for the preferred cancer-survival story.
~~~

## Claim ceiling

Until the upstream assets pass byte verification and the authors' reported
primary result is reproduced, META-A remains an executable research contract,
not an independent replication.
