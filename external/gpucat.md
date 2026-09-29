# gpucat — external rendering reference

> Status: OPTIONAL VISUALIZATION DEPENDENCY  
> Scientific evidence: NO  
> Acceptance authority: NO

## Upstream

Repository:

https://github.com/isaac-mason/gpucat

Pinned reference commit:

~~~text
d739e5bed1597858a5c1d96f53641b965699cf32
~~~

License:

~~~text
MIT
Copyright © 2026 Isaac Mason
~~~

Upstream describes gpucat as a minimal TypeScript-first WebGPU and WebGL2
renderer with typed shader composition and explicit GPU-resource control.

## Role here

Dissociated Control Systems uses gpucat only in the optional browser visual
under `web/`.

The scientific Python harness does not depend on gpucat.

~~~text
Renderer != Model
Frame != Observation
Animation != Evidence
~~~

The first visual intentionally selects the WebGL2 backend to maximize browser
reach while preserving the same public interaction surface.

## Update rule

If the dependency is refreshed:

1. inspect upstream API / license changes;
2. record the new commit;
3. rebuild the visual in CI;
4. keep the visual claim boundary unchanged unless separately reviewed.
