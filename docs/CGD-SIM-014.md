# CGD-SIM-014 — OOD world-model shift challenge

> Status: SYNTHETIC POST-CONVERGENCE CHALLENGE  
> Clinical authority: NONE

CGD-SIM-013 established a local fixed point only inside the original synthetic
world. The stopping rule explicitly said that the next productive move must
change the world model or acquire new independent evidence.

SIM-014 does exactly that.

The clean-world classifier and parameters are frozen, then tested under four
out-of-distribution conditions:

1. **common-mode bias** — correlated drift enters multiple observation channels;
2. **noise inflation** — every base probe receives additional stochastic noise;
3. **probe dropout** — selected observations are replaced by clean-training means;
4. **combined shift** — bias, noise and dropout occur together.

The test then asks two separate questions.

### A. Does the old fixed point survive the changed world?

~~~text
robust fixed point := worst OOD accuracy drop < 0.03
~~~

### B. If it breaks, does genuinely new shifted evidence help?

A small calibration set from the shifted world is appended to the original
clean training set. Model/ensemble parameters are reselected on a separate
shifted validation set and evaluated on a fresh shifted test set.

~~~text
external evidence has material value := adapted accuracy - frozen accuracy > 0.01
~~~

This is the important post-convergence distinction:

~~~text
same information + more recursion
    !=
new information + adaptation
~~~

If the former has saturated but the latter helps, the fixed point was correctly
identified as epistemic rather than absolute.

All results remain synthetic engineering results with no clinical authority.
