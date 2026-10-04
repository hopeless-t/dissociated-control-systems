# RQ-005 META-A — R `meta` 5.5-0 forest sorting audit

## Question

Could the Bognár 2024 Figure 2 cross-binding pattern be explained by the
standard behavior of `meta::forest()` when the forest plot is sorted by effect?

The paper reports using R package `meta` v5.5.0 for forest plots. The matching
upstream repository tag is `5.5-0`.

## Direct source observation

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

## Consequence

A correctly constructed `meta` object containing aligned:

~~~text
studlab
TE / seTE
n.e / n.c
~~~

should preserve row identity under ordinary `sortvar` ordering.

Therefore the following explanation is downgraded:

~~~text
STANDARD_FOREST_SORT_BUG:
  sortvar reordered labels/effects but left patient counts behind
~~~

The direct source does not support that behavior for the built-in fields.

## What remains possible

The source audit does **not** prove which upstream step failed. Remaining worlds
include:

~~~text
U1  n.e/n.c were already misbound when the meta object was constructed
U2  TE/studlab and count vectors came from different filtered data frames
U3  a manual join / cbind / vector assignment occurred before forest.meta()
U4  revision introduced a broader extraction-table column into the OS object
U5  event-count and population-count fields were confused before object creation
U6  a custom plotting/data-preparation step outside standard forest.meta()
U7  another upstream mechanism not yet observed
~~~

## Stronger DCS invariant

~~~text
Correct Rendering Logic
!=
Correct Input Binding

Plot Sort Preserves Object Identity
!=
Object Identity Was Correct Before Plotting
~~~

The distinction matters because a renderer can faithfully display a corrupted
internal state.

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
~~~

If those vectors are aligned before object creation, the upstream-binding worlds
are falsified and attention moves to any unobserved custom plotting step.

## Claim ceiling

This source audit identifies what the standard `meta` 5.5-0 sorter does. It
does not establish that the authors' code used only that standard path, nor does
it establish a publication error without the original analysis artifacts.
