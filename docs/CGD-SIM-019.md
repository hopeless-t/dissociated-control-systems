# CGD-SIM-019 — Replicated OOD authority-plane audit

> Status: SYNTHETIC POST-CONVERGENCE REPLICATION  
> Clinical authority: NONE

The clean-world loop converged in SIM-013.

The fixed point then failed under OOD world-model shift in SIM-014.

SIM-015 through SIM-018 did not try to restore omniscience. They built a
fail-safe authority plane:

~~~text
detect world-model mismatch
-> lower normal execution authority
-> request external evidence / recalibration
~~~

SIM-019 freezes that plane and applies it unchanged to five independent shifted
test blocks.

The audit measures the fraction of wrong executions removed before the
authority gate closes.

Declared replicated OOD robustness:

~~~text
clean false-alarm blocks <= 10%
minimum noise-shift error-exposure reduction > 50%
mean common-bias reduction > 80%
mean combined-shift reduction > 80%
~~~

If this passes, the post-convergence result is not that the model became robust
to every world. It is that the **authority boundary around model failure**
became reproducible inside the declared OOD family.

Synthetic engineering result only; no clinical authority.
