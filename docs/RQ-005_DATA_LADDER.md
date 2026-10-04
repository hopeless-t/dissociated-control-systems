# RQ-005 Data Ladder

## Goal

Prioritize datasets by how much they can discriminate the competing survivor
worlds, not by how emotionally compelling the cases are.

## Tier 1 — immediately computable public biological baseline\n\n### Current status\n\nA first real-data pilot has now been executed on a 1,897-row MB-only GitHub mirror. The current cBioPortal/Zenodo clinical object has 2,509 total rows, but 1,985 are canonical MB-prefixed METABRIC rows and 524 are MTS-prefixed records with a different sparse-field regime. The pilot is therefore explicitly non-canonical. See [RQ-005_METABRIC_PILOT.md](RQ-005_METABRIC_PILOT.md). Promotion requires rerunning the frozen pipeline on the 1,985-row MB subset and reconciling the 88-row delta; MTS must remain a separate provenance block.

### METABRIC / cBioPortal

Use within-cancer matching before any cross-cancer analysis.

The 2025 stage III TNBC long-term-survivor study used a public METABRIC
external-validation cohort of 111 stage III TNBC samples with matched molecular
and clinical data. The cBioPortal DataHub exposes the METABRIC study as
brca_metabric and supports dataset download or API slices.

Primary use in RQ-005:

~~~text
WB tumor-biology-first baseline
vs
WI immune / expression-associated alternative
~~~

This cohort does not test hope, stress, or agency.

It establishes how much survivor separation can be explained before those
layers are introduced.

## Tier 2 — exceptional responder multi-omics

### NCI Exceptional Responders Initiative

NCI profiled 111 exceptional responders across DNA, RNA, epigenetic, and tumor
microenvironment features. Plausible molecular explanations were found in
26/111 cases.

Program data are available through the Genomic Data Commons with controlled
access via dbGaP study phs001145 where required.

Primary use:

- rare-state census;
- residual-case biopsy after known molecular explanations;
- test whether unexplained cases cluster into additional molecular/TME regimes.

Important invariant:

~~~text
unexplained by current molecular analysis
!=
explained by psychology
~~~

## Tier 3 — large immune/TME survivor contrast

### Advanced ovarian HGSC LTS/MTS/STS cohort

The 2024 JCI study includes 374 LTS, 433 MTS, and 416 STS cases with extensive
immune-cell/TME scoring.

Individual patient data are not publicly downloadable because of privacy
restrictions; the authors state that collaborative analyses may be requested.

Primary use:

- immune/TME hypothesis calibration;
- study-level effect priors;
- independent target for later collaboration.

This is not the first executable dataset because the row-level data are not
public.

## Tier 4 — longitudinal psychosocial/immune trajectory templates

### Breast cancer 5-year stress/immunity cohort

113 women had repeated psychological and immune measurements over 12
assessments across five years.

Primary use:

- time-scale prior;
- change-point architecture;
- psychological/stress-to-immune temporal model design.

Current use is literature-level until row-level data availability is verified.

### GOG-218 ovarian QOL trajectory study

The published analysis compares 260 long-term survivors with 1115 short-term
survivors and shows baseline plus longitudinal QOL differences.

Primary use:

- patient-reported-state candidate axis;
- reverse-causality tests;
- landmark/prospective validation design.

Current use is literature-level until a row-level data route is verified.

## Tier 5 — survivor narratives

Narrative interviews and exceptional-survivor testimony remain useful for
variable discovery:

~~~text
narrative
 -> candidate latent state / transition
 -> measurable proxy
 -> competing-model test
~~~

They are not used as endpoint evidence.

## Dataset selection objective

For candidate dataset d:

~~~text
VOI(d)
  =
  expected model-ranking information
  * temporal resolution
  * layer coverage
  * replication value
  / acquisition and preprocessing cost
~~~

The first executable baseline should maximize information about the strongest
non-psychological competitors.

Current priority after the first pilot:

~~~text
1. METABRIC canonical 1,985-row MB-only rerun + 88-row mirror-delta audit
2. NCI exceptional-responder rare-state analysis
3. longitudinal psychosocial/immune data if row-level access is found
4. restricted ovarian HGSC collaboration target
5. narratives as hypothesis generators
~~~

This ordering is deliberately hostile to the original hope hypothesis: the
psychological layer is introduced only after strong tumor-biology and treatment
competitors have been quantified.
