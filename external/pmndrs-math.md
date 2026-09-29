# pmndrs/math — external tool reference

> Status: OPTIONAL TOOL REFERENCE  
> Vendored source: NO  
> Canonical runtime dependency: NO  
> Scientific evidence: NO

## Upstream

Repository:

https://github.com/pmndrs/math

Pinned source-reference commit:

~~~text
98762395c1f34d7d594d31165e8005fd6915c431
~~~

Browser visual runtime package:

~~~text
math@0.1.0
~~~

The published package is used by the web build because the upstream source
repository intentionally does not commit its generated `dist/` artifacts.

License:

~~~text
MIT
Copyright © 2026 Isaac Mason
~~~

Upstream README at the pinned lineage describes `math` as:

- high-performance and allocation-conscious;
- tiny / tree-shakeable;
- portable across WebGL, WebGPU, Wasm and renderers;
- data-oriented, operating on caller-owned data.

Its public modules include vectors, quaternions, matrices, geometry, spatial
queries, seeded random generators, noise, easing/springs, colors, and inverse
kinematics.

## Why keep it in this lab

Dissociated Control Systems should prefer the smallest sufficient calculation
surface for exploratory work.

For lightweight tasks such as:

- vector / matrix transforms;
- bounded geometric calculations;
- deterministic seeded sampling;
- small simulation helpers;
- interpolation / remapping;
- quick geometry or spatial experiments;

`pmndrs/math` is a useful candidate because it can be consumed selectively
without pulling in a large scientific stack.

This is especially useful for browser-side visualizations or small TypeScript
research utilities.

The first concrete use in this repository is the optional
`web/` Dissociated State Field, where seeded random and simplex-noise
primitives shape deterministic visual trajectories. Rendering is delegated to
`gpucat`; the visualization is explicitly non-evidentiary.

## Boundary

~~~text
Useful calculator != validated scientific method
Convenient primitive != accepted research evidence
Reference tool != repository dependency
Pinned commit != frozen forever
~~~

A future experiment may use this library only if its experiment contract says
so and records the exact version / commit.

Numerically sensitive analyses, statistical inference, optimization, signal
processing, or domain-specific scientific calculations still require methods
appropriate to that experiment and independent validation where necessary.

## Install / skill entry points

Upstream currently documents:

~~~bash
npm install math
npx skills add pmndrs/math --skill math
~~~

These commands are recorded for provenance and convenience only. This
repository does not execute them automatically.

## Update rule

When the reference is intentionally refreshed:

1. inspect upstream changes;
2. record the new commit;
3. re-check license and scope;
4. update this file and the source registry together;
5. do not silently turn the reference into a mandatory dependency.
