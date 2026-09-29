# gpucat — external rendering reference

> Status: OPTIONAL / EXPERIMENTAL VISUALIZATION REFERENCE  
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

Dissociated Control Systems evaluated gpucat for the optional browser visual.

A real-browser deployment on the target Lubuntu/Chrome environment produced a
blank WebGL field even though the TypeScript/Vite build and deployment passed.
VIS-001 therefore uses Canvas2D as its canonical public renderer.

gpucat remains a useful experimental rendering reference for future work. The
scientific Python harness and current public visual do not depend on it.

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
