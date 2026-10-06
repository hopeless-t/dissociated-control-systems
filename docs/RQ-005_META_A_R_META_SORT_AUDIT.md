# RQ-005 META-A — R `meta` 5.5-0 input and forest sorting audit

## Question

Could the Bognár 2024 Figure 2 cross-binding pattern be explained by the
standard behavior of R package `meta` when constructing or sorting a generic
inverse-variance meta-analysis?

The paper reports using R package `meta` v5.5.0 for forest plots. The matching
upstream repository tag is `5.5-0`.

## Part A — `forest.meta()` sorting

In `meta` tag `5.5-0`, `forest.meta()` creates one ordering index:

~~~r
o <- order(subgroup.factor, sortvar)
~~~

and then applies the same index to the study-level fields, including:

~~~r
x$n.e      <- x$n.e[o]
x$n.c      <- x$n.c[o]
x$TE       <- x$TE[o]
x$seTE     <- x$seTE[o]
x$lower    <- x$lower[o]
x$upper    <- x$upper[o]
x$w.common <- x$w.common[o]
x$w.random <- x$w.random[o]
studlab    <- studlab[o]
~~~

When additional user columns are present, the underlying data frames are also
reordered with the same `o`:

~~~r
dataset1 <- dataset1[o, ]
dataset2 <- dataset2[o, ]
~~~

Upstream source:

- `guido-s/meta`, tag `5.5-0`, `R/forest.R`

### Consequence

A correctly constructed `meta` object containing aligned:

~~~text
studlab
TE / seTE
n.e / n.c
~~~

should preserve row identity under ordinary `sortvar` ordering.

Therefore the following explanation is strongly downgraded:

~~~text
STANDARD_FOREST_SORT_BUG:
  sortvar reordered labels/effects but left built-in patient counts behind
~~~

The direct source does not support that behavior for the built-in fields.

## Part B — `metagen()` input identity

The same package version exposes generic inverse-variance meta-analysis as:

~~~r
metagen(TE, seTE, studlab, ..., n.e = NULL, n.c = NULL, ...)
~~~

The implementation catches these vectors separately from the supplied data or
calling environment:

~~~text
TE
seTE
studlab
n.e
n.c
~~~

and validates vector length. In particular, non-null `n.e` and `n.c` are
checked against the number of effect estimates with `chklength(...)`.

That gate can establish:

~~~text
length(TE) == length(n.e) == length(n.c)
~~~

but vector length alone cannot establish:

~~~text
trial_id(TE[i]) == trial_id(n.e[i]) == trial_id(n.c[i])
~~~

The package documentation also demonstrates `n.e` as sample-size information
attached to a generic `metagen()` effect/se input. Generic inverse-variance
pooling is driven by the effect estimates and standard errors, not by the
sample-count metadata.

Upstream source:

- `guido-s/meta`, tag `5.5-0`, `R/metagen.R`

## Concrete failure class

This creates a specific *possible* failure class:

~~~text
correct TE / seTE / studlab vectors
+
equal-length n.e / n.c vectors from another row order, subset, or field

        ↓

length checks pass

        ↓

meta object contains internally misbound sample metadata

        ↓

forest.meta() faithfully applies one common sort index to the already-misbound
object

        ↓

pooled effect can remain correct while displayed counts / aggregate N have
incorrect evidence identity
~~~

This class matches the observed qualitative shape:

~~~text
Figure effect/weight arithmetic closes
while
population-count identity does not close
~~~

but it is **not** evidence that the Bognár analysis followed this exact path.
The original source table and analysis code are still required.

Synthetic method fixtures:

- `src/dissociated_control_systems/parallel_vector_identity.py`
- `tests/test_parallel_vector_identity.py`
- `src/dissociated_control_systems/meta_input_failure_fixture.py`
- `tests/test_meta_input_failure_fixture.py`

Known answers now enforce:

~~~text
Equal Vector Length != Evidence Identity
Correct Effect Pool != Correct Sample Metadata Binding
~~~

## What remains possible

Remaining worlds include:

~~~text
U1  n.e/n.c were already misbound when the meta object was constructed
U2  TE/studlab and count vectors came from different filtered data frames
U3  a manual join / cbind / vector assignment occurred before forest.meta()
U4  revision introduced a broader extraction-table column into the OS object
U5  event-count and population-count fields were confused before object creation
U6  a custom plotting/data-preparation step outside standard forest.meta()
U7  a documented endpoint-specific analysis subset explains some count changes
U8  another upstream mechanism not yet observed
~~~

The standard built-in forest sorting path is no longer a leading explanation.

## Stronger DCS invariants

~~~text
Correct Rendering Logic
!=
Correct Input Binding

Plot Sort Preserves Object Identity
!=
Object Identity Was Correct Before Plotting

Equal Vector Length
!=
Evidence Identity

Correct Effect Pool
!=
Correct Metadata Binding
~~~

The distinction matters because a renderer and statistical engine can faithfully
operate on a semantically corrupted internal state.

## Next falsification gate

Obtain the final supplementary/source extraction table and reconstruct the
exact inputs used to create the OS meta object:

~~~text
studlab vector
TE / seTE vectors
n.e / n.c vectors
subset/filter mask
sortvar
source row identifiers
field semantics
~~~

Then test identity *before* `metagen()` is called.

If those vectors are aligned before object creation, the upstream-binding worlds
are falsified and attention moves to any unobserved custom plotting or later
mutation step.

## Claim ceiling

This source audit identifies what standard `meta` 5.5-0 checks and sorts. It
does not establish that the authors' code used only that path, nor does it
establish a publication error without the original analysis artifacts.
