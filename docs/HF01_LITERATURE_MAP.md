# HF01 Literature Map

> Purpose: map source-supported biological observations onto the synthetic
> HF01 state variables without promoting analogy into mechanism.

## Evidence table

| Claim candidate | Evidence type | HF01 relevance | Source |
|---|---|---|---|
| Bald scalp in male AGA can retain KRT15-high stem cells while CD200-high / CD34-positive progenitor populations are markedly reduced. | Human bald vs non-bald scalp; flow cytometry and functional follow-up. | Supports separating stem-cell presence from functional progenitor reserve `P`. | Garza et al., J Clin Invest (2011), DOI 10.1172/JCI44478, PMID 21206086 |
| Balding AGA dermal papilla shows increased nuclear AR localization and early microvascular regression; AR-mediated paracrine signaling, mainly TGF-beta, can induce endothelial apoptosis. | Human scalp + transcriptomics + cell/animal experiments. | Supports an androgen-linked disturbance channel and a vascular intermediate, not a blood-flow-only theory. | Deng et al., J Invest Dermatol (2022), DOI 10.1016/j.jid.2022.01.003, PMID 35033537 |
| Paired vertex and occipital follicles from the same men with AGA show broad transcriptomic differences involving HIF-1, WNT/beta-catenin and focal-adhesion pathways. | Paired human RNA-seq, n=10 donors, plus functional experiments. | Supports within-person reference modeling while warning that occipital tissue is not an identical healthy vertex. | Liu et al., Br J Dermatol (2022), DOI 10.1111/bjd.21783, PMID 35862273 |
| Chronic corticosterone exposure in mice prolongs HFSC quiescence via dermal-papilla suppression of Gas6; restoring Gas6 can overcome the inhibition. | Mouse stress/endocrine experiments. | Supplies a plausible stress-to-niche path for `Q -> R`; does not establish the same causal path in human AGA. | Choi et al., Nature (2021), DOI 10.1038/s41586-021-03417-2 |
| Human AGA follicles show early connective-tissue-sheath changes; experimentally increased CTS contraction activates PIEZO1-linked signaling, increases progenitor apoptosis, suppresses ORS/matrix proliferation, and impairs growth. | 2026 single-cell + spatial transcriptomics, ex vivo human follicles, humanized mouse models. | Provides a concrete candidate mechanism for slow structural/mechanical state `F` and hysteresis-like damage. | Nature Communications (2026), DOI 10.1038/s41467-026-70153-4 |
| Hair-diameter variability, vellus hairs and peripilar signs are common trichoscopic AGA findings. | 2024 systematic review, 34 studies. | Supports a non-invasive observation layer for `H` / miniaturization, while remaining indirect for molecular states. | Kuczara et al., J Clin Med (2024), DOI 10.3390/jcm13071962, PMID 38610726 |

## Source links

- https://pubmed.ncbi.nlm.nih.gov/21206086/
- https://pubmed.ncbi.nlm.nih.gov/35033537/
- https://pubmed.ncbi.nlm.nih.gov/35862273/
- https://www.nature.com/articles/s41586-021-03417-2
- https://www.nature.com/articles/s41467-026-70153-4
- https://pubmed.ncbi.nlm.nih.gov/38610726/

## Evidence-to-model discipline

The model contains variables that are more abstract than any single assay.

~~~text
A = androgen pressure
    candidate observations:
      AR localization / androgen pathway activity
    NOT:
      "serum DHT uniquely determines A"

Q = stress / neuroendocrine load
    candidate observations:
      systemic/context measures
    NOT:
      "subjective stress uniquely determines follicle stress biology"

R = regenerative competence
    candidate observations:
      WNT/GAS6/IGF-family and cycle-associated signatures
    NOT:
      one biomarker == R

P = functional progenitor reserve
    candidate observations:
      progenitor markers / functional assays
    NOT:
      ordinary photography

N = niche integrity
    candidate observations:
      stem/niche adhesion, ECM and local support signatures
    NOT:
      hair count alone

F = structural / mechanical lock
    candidate observations:
      connective-tissue mechanics, ECM, mechanotransduction candidates
    NOT:
      scalp "tightness" by subjective feel

H = coarse output
    candidate observations:
      diameter distribution, density, terminal/vellus mix, growth trajectory
~~~

## Competing model classes

HF01 must retain competing explanations rather than forcing every observation
into one degeneration story.

### M0 — output-only model

Hair output alone predicts future hair output.

Expected weakness: latent-state non-identifiability.

### M1 — androgen-dominant model

~~~text
A -> R/P -> H
~~~

Prediction: adding slow structural state does not materially improve held-out
trajectory prediction.

### M2 — stress/context modifier model

~~~text
Q -> R -> H
A -> R/P -> H
~~~

Prediction: context variables improve prediction, but do not necessarily create
irreversible lock.

### M3 — structural-hysteresis model

~~~text
A,Q -> R,P
P,R -> F
F -> R,P,N
R,P,N,F -> H
~~~

Prediction: path dependence exists; the same current `H` can have different
future recoverability depending on `P,N,F`.

### M4 — mixture / phenotype model

Different individuals are better described by different combinations of the
above. This is currently the most conservative population-level expectation.

## What the literature does NOT establish

The source set does not establish that:

- conscious visualization can directly up-regulate WNT or lower follicular DHT;
- behavioral intervention alone reverses established AGA;
- scalp blood flow is the single primary cause of AGA;
- a particular `F` threshold exists in humans;
- the synthetic HF01 coefficients have clinical meaning;
- the occipital scalp is a perfect saved copy of the former vertex state;
- a PowerPoint or explanatory model is itself a biological treatment.

Those remain testable research questions or rejected overclaims.
