# HF01 Orthogonal Probe Roadmap

> Status: SOURCE-BOUND NEXT-EVIDENCE PLAN
> Clinical authority: NONE

## Why this roadmap exists

HF01 currently has two cross-sectional transcriptomic contexts supporting the
same frozen WNT/regeneration disease-state projection.

Those contexts are biologically different, but they share a projection root:

~~~text
HF01_GSE36169_AXES.json
~~~

Therefore another dataset scored only with the same axis improves context
replication without eliminating projection-family common-mode dependence.

The next high-information evidence should be orthogonal in measurement or
functional semantics.

## Candidate R-state orthogonal witness — Lu et al. 2016

Citation:

- Lu GQ et al.
- *An investigation of crosstalk between Wnt/beta-catenin and transforming
  growth factor-beta signaling in androgenetic alopecia.*
- Medicine (Baltimore). 2016;95(30):e4297.
- PMID 27472703; PMCID PMC5265840.

Human material:

- 15 male AGA patients;
- 15 frontal balding scalp specimens;
- 9 occipital non-balding specimens.

Orthogonal measurements included:

- beta-catenin immunofluorescence;
- beta-catenin Western blotting;
- nuclear accumulation/localization;
- active and total TGF-beta1 protein;
- Smad2/Akt phosphorylation;
- inhibitor perturbations in balding/non-balding DP cells.

Reported direction:

~~~text
balding DP:
    lower beta-catenin activity / nuclear signal
    higher TGF-beta pathway activity

TGF-beta inhibition in balding DP:
    Wnt10a / LEF1 increase
    beta-catenin nuclear accumulation increases

Wnt inhibition in non-balding DP:
    active TGF-beta1 increases
~~~

HF01 use:

This does not reuse the frozen transcript-axis scoring rule as the sole witness.
It supplies protein/localization and perturbation evidence tied to the same
mechanistic family.

Claim ceiling:

~~~text
orthogonal mechanism/state compatibility
!= validated R latent coordinate
!= recoverability
~~~

## Candidate P-state orthogonal witness — Bazid et al. 2026

Citation:

- Bazid H.A.S. et al.
- *Immunohistochemical Expression of Sox9 and CD34 in Androgenetic Alopecia
  Patients.*
- PMID 41629248.

Design reported by PubMed:

- 40 subjects total;
- male AGA and female pattern hair-loss groups plus site-/age-/sex-matched
  controls;
- scalp biopsy with immunohistochemical Sox9 and CD34 assessment.

Reported AGA pattern:

~~~text
CD34:
    present in all control biopsies
    reduced in frontal bald AGA tissue
    reduced frontal vs hairy occipital tissue within AGA patients

Sox9:
    preserved across frontal bald / occipital / control samples
~~~

HF01 use:

This is an orthogonal assay family for the existing hypothesis:

~~~text
stem-cell presence can persist while progenitor state is depleted
~~~

It therefore maps more naturally to P than to R.

## Candidate functional bridge — androgen/Wnt coculture

Citation:

- *Hair follicle stem cell differentiation is inhibited through cross-talk
  between Wnt/beta-catenin and androgen signalling in dermal papilla cells from
  patients with androgenetic alopecia.*
- PMID 22283397.

Functional readout includes DPC-induced HFSC differentiation and hair-specific
keratin expression, with Wnt activation restoring differentiation impaired by
androgen exposure.

HF01 use:

This is stronger than static expression for one narrow question:

~~~text
mechanistic state -> functional differentiation capacity
~~~

It remains a cell/coculture model and is not a human recoverability assay.

## Candidate ex-vivo actuator bridge — 2026 human AGA organ model

Citation:

- *Development and validation of a comprehensive in vitro organ model for
  androgenetic alopecia.*
- PMID 42237333.

Reported model behavior includes:

- DHT-associated inhibition of follicle growth;
- accelerated catagen entry;
- reduced matrix-cell proliferation;
- increased apoptosis;
- decreased beta-catenin and IGF-1;
- increased TGF-beta1, DKK1 and AR;
- partial reversal by minoxidil or androgen-receptor antagonism.

HF01 use:

This is a promising orthogonal system-identification bridge because it combines:

~~~text
known input
+ morphology / growth output
+ cell-state readouts
+ molecular readouts
~~~

It still does not establish in-vivo human longitudinal recoverability.

## Information-gain ranking

Current priority is not simply newest paper first.

### Priority A — orthogonal human state witness

Protein/localization or histologic assays that do not depend on the frozen
HF01 transcript score.

Goal:

~~~text
raise evidence topology robustness for R or P
~~~

### Priority B — functional state-to-output bridge

Human follicle / DPC-HFSC systems where a declared perturbation changes both an
internal probe and a functional output.

Goal:

~~~text
separate state compatibility from response susceptibility
~~~

### Priority C — another same-axis transcript dataset

Useful for context replication, but lower information gain for common-mode
projection dependence.

## Next formal test

HF01 should compare two assurance objects:

~~~text
A:
  GSE36169 + GSE93766
  shared transcript projection family

B:
  A + orthogonal protein/localization/functional witness
~~~

The desired improvement is not a higher narrative confidence score.

It is structural:

~~~text
fewer common-mode projection roots
more independent measurement families
better separation of state / response / function
~~~

No orthogonal source is promoted to a mandatory biomarker until its exact
claim, scope, measurement semantics, and failure modes are frozen.
