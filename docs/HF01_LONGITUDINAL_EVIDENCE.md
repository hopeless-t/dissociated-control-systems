# HF01 Longitudinal / Intervention-Linked Evidence

> Status: SOURCE-BOUND DESIGN INPUT
> Clinical authority: NONE
> Medication/self-experiment authority: NONE

## Why this evidence class matters

Cross-sectional public data can show that two tissues occupy different states.
It cannot establish temporal precedence.

~~~text
baseline state x0
    ↓
known input u
    ↓
early hidden-state response Δz(t1)
    ↓
later hair-output response ΔH(t2)
    where t1 < t2
~~~

The input is treated here as a system-identification perturbation in published data, not as a treatment recommendation.

## Human evidence candidate 1 — Tang et al. 2003

- Tang L et al. J Am Acad Dermatol. 2003;49(2):229-233.
- PMID 12894070; DOI 10.1067/S0190-9622(03)00777-1.
- 9 men with AGA.
- Balding and occipital biopsies before and after 4 months of finasteride.
- Dermal papillae were microdissected and growth-factor/cytokine mRNA measured.
- Treatment continued for 1 year; month-12 efficacy was graded from photography.

Reported IGF-1 / outcome pattern:

~~~text
IGF-1 increased at month 4: 4/9
    -> 3 moderate improvement at month 12
    -> 1 unchanged

IGF-1 decreased at month 4: 3/9
    -> 3 clinical worsening at month 12

no noticeable IGF-1 change: 2/9
    -> slight improvement or unchanged
~~~

HF01 treats dermal-papilla IGF-1 change as a candidate early regenerative-state probe, not as the full latent R state.
The important feature is temporal ordering: early molecular response precedes later visible response.

Limitations: n=9, uncontrolled, association only, insufficient to validate recoverability.

## Human evidence candidate 2 — Mirmirani et al. 2015

- Mirmirani P et al. Br J Dermatol. 2015;172(6):1555-1561.
- PMID 25204361; DOI 10.1111/bjd.13399.
- Placebo-controlled, double-blinded prospective pilot.
- 16 men aged 18-49 with Hamilton-Norwood IV-V thinning.
- 5% topical minoxidil foam or placebo for 8 weeks.
- Baseline/final stereotactic photographs plus before/after scalp biopsies and microarray.

This supports feasibility of measuring a declared input, molecular response, and hair-output response in the same prospective design.

## HF01 longitudinal state contract

Let:

~~~text
H0          baseline visible output
z0          baseline internal/proxy measurement
u           bounded external input
Δz_early    early internal-state response
ΔH_late     later visible-output response
~~~

The core question is whether Δz_early adds predictive information about ΔH_late beyond H0 and baseline covariates.

### Null observer M0

~~~text
ΔH_late ~ H0 + baseline covariates
~~~

### Dynamic observer M1

~~~text
ΔH_late ~ H0 + baseline covariates + Δz_early
~~~

HF01 must compare M1 with M0 out of sample. In-sample correlation is insufficient.

## Pre-registered acceptance direction

A longitudinal state probe becomes a serious HF01 candidate only if:

1. the probe is measured before the late output;
2. the input/intervention is explicitly recorded;
3. adding the early response improves held-out prediction over baseline-output observation;
4. the direction transfers to at least one independent intervention-linked dataset;
5. subject-level grouping prevents leakage;
6. uncertainty and sensitivity analysis are reported.

## Stronger future model

~~~text
ΔR_early
ΔF*_early
ΔP_early
...
       ↓
posterior recoverability
       ↓
ΔH_late
~~~

The eventual target is rho(t) = P(reach healthy-output region | current state, declared actuator class).
No current human dataset identified by HF01 is sufficient to estimate this reliably.

## Implication for normal-model awareness

The awareness hypothesis splits into two separately falsifiable steps:

~~~text
Step A:
normal-reference feedback
    -> measurable early physiological / behavioral state response

Step B:
early state response
    -> later follicle-output response
~~~

Step B must be demonstrated before any claim that presentation of a normal model helps restore hair biology.
This prevents subjective understanding itself from being used as evidence of biological recovery.
