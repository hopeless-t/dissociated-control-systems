# HF01 Public-Data Result 001 — GSE36169

> Dataset: GSE36169  
> Design: 5 men with AGA, paired haired vs bald scalp  
> Platform: GPL96  
> Analysis status: PRE-REGISTERED AXES EXECUTED  
> Clinical authority: NONE

## Harness history

The first CI run failed while parsing the GEO platform annotation header.

That failure was treated as a harness fault, not a biological result. The parser
was repaired to tolerate GEO annotation preamble/BOM variants without changing
the frozen pathway-axis specification.

The repaired run passed and produced an immutable workflow artifact.

## Positive control

PTGDS was declared as a positive control because the dataset's original paper
reported elevated PTGDS/PGD2 in bald scalp. It is not counted as independent
validation.

~~~text
PTGDS:
mean bald-minus-haired log2 delta = +1.927634
direction consistency             = 5 / 5
~~~

The positive control therefore confirms that the download, sample pairing,
annotation and sign convention recover the dataset's known headline signal.

## Pre-registered axis results

| axis | available genes | mean signed log2 delta | positive pairs |
| --- | ---: | ---: | ---: |
| androgen/growth suppression | 6/7 | -0.058722 | 2/5 |
| WNT/regeneration loss | 4/6 | +0.727979 | 5/5 |
| vascular regression | 5/5 | -0.144918 | 2/5 |
| ECM/structural remodeling | 6/6 | +0.739120 | 5/5 |
| inflammatory activation | 2/5 | +0.371793 | 4/5 |
| hypoxia/oxidative response | 5/5 | +0.194802 | 4/5 |

## Model update

### Strongest compatibility signals

Two frozen axes aligned in all five paired subjects:

~~~text
WNT / regeneration loss
ECM / structural remodeling
~~~

This is compatible with the HF01 decision to model regenerative competence and
slow structural state separately.

### Important failed predictions

The frozen transcript-level androgen and vascular axes did **not** align with
their expected directions.

This is not repaired by changing the gene list after inspection.

Instead HF01 changes the interpretation boundary:

~~~text
androgen DRIVER STATE
    !=
whole-tissue androgen-pathway transcript abundance

vascular LOCAL STATE
    !=
whole-scalp endothelial transcript abundance
~~~

Known biological studies motivate activity/localization and cell-type-specific
mechanisms (for example AR nuclear localization / paracrine signaling), so a
whole-scalp expression panel is an inadequate direct probe of HF01 A.

The negative vascular result likewise warns against treating whole-scalp
vascular-marker RNA as a direct measurement of dermal-papilla microvasculature.

### Inflammation is provisional

Only 2/5 declared inflammatory genes were represented after annotation, so the
4/5 positive direction is insufficient for a strong axis claim.

## DCS lesson

The first human-data bridge reinforces the observability rule:

> A biologically meaningful hidden state can fail to appear in a coarse
> measurement channel even when the mechanism is real.

Therefore the observer model must distinguish:

~~~text
mechanism existence
measurement sensitivity
cell-type dilution
state variable
~~~

These are not interchangeable.

## Next test

Run the exact frozen axis definition on GSE90594:

- 14 AGA vertex samples;
- 14 healthy vertex controls;
- independent cohort;
- different platform (GPL17077);
- cross-person rather than within-person contrast.

Replication criterion is directional transfer, not identical effect magnitude.

The axes remain frozen from HF01_GSE36169_AXES.json.
