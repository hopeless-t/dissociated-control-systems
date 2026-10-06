# HF01 Public-Data Result 002 — GSE93766

> Dataset: GSE93766  
> Contrast: BK0 vs NBK0  
> Material: immortalized balding vs non-balding human dermal-papilla aggregates
> co-cultured with NHEK  
> Analysis status: FROZEN-AXIS TRANSFER EXECUTED  
> Clinical authority: NONE

## Contrast calibration

Cuffdiff defines:

~~~text
log2(fold_change) = log2(value_2 / value_1)
~~~

The successful run reported:

~~~text
sample_1 = NBK0
sample_2 = BK0
~~~

Therefore the raw Cuffdiff direction is already:

~~~text
balding - non-balding
~~~

A deterministic known-answer test now freezes this orientation rule.

## Frozen-axis result

| axis | available | alignment | mean finite signed log2 FC | median finite signed log2 FC |
| --- | ---: | ---: | ---: | ---: |
| androgen/growth suppression | 7/7 | 5/7 | +1.180584 | +0.836220 |
| WNT/regeneration loss | 6/6 | 4/6 | +1.163161 | +0.328090 |
| vascular regression | 4/5 | 1/4 | -2.190883 | -1.493240 |
| ECM/structural remodeling | 6/6 | 5/6 | +0.881893 | +1.051513 |
| inflammatory activation | 4/5 | 2/4 | +0.959649 | +0.710748 |
| hypoxia/oxidative response | 5/5 | 1/5 | -0.495191 | -0.315810 |

The inflammatory mean is dominated by large positive CCL2 and IL6 effects while
two other genes oppose the declared direction, so it is classified as mixed.

## Cross-system comparison with GSE36169

GSE36169 was paired whole scalp from five men with AGA.

GSE93766 is an immortalized DP-cell aggregate model.

Despite those substantial differences, two axes retain the declared direction
in both systems:

~~~text
WNT / regeneration loss
ECM / structural remodeling
~~~

This is the strongest current public-data compatibility result.

## Non-replications are retained

### Vascular regression

The frozen vascular transcript axis fails in both current public-data runs.

This does not falsify published local microvascular regression mechanisms.
Instead, it falsifies the stronger measurement assumption:

~~~text
local DP microvascular regression
    ==
the declared bulk/DP-cell transcript panel
~~~

HF01 therefore removes that equivalence.

### Hypoxia / oxidative response

The axis is positive in GSE36169 but negative in GSE93766.

It is not promoted into a stable HF01 latent axis.

### Androgen axis

Whole scalp GSE36169 does not show the frozen transcript direction, while the
DP-cell model does.

This is compatible with androgen signaling being cell-type/context dependent
and with activity/localization being more informative than bulk transcript
abundance, but that interpretation remains a hypothesis rather than a rescued
validation.

## Model reduction

Public-data evidence currently favors:

~~~text
R = regenerative-state candidate
F* = structural-remodeling candidate
~~~

over a model in which every originally declared pathway is an equally reliable
observable state variable.

Important:

~~~text
F* structural remodeling
    !=
proven mechanical lock
    !=
proven biological hysteresis
~~~

Hysteresis remains a synthetic hypothesis requiring longitudinal evidence.

## Current strongest cross-data statement

> Across a paired human scalp dataset and a distinct dermal-papilla cell model,
> pre-registered WNT/regeneration-loss and ECM/structural-remodeling signatures
> both transfer in the declared disease-associated direction.

This is compatibility evidence, not proof of causality or recoverability.
