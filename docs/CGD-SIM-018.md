# CGD-SIM-018 — Template-residual CUSUM

> Status: SYNTHETIC POST-CONVERGENCE CONTROL TEST  
> Clinical authority: NONE

SIM-017 accumulated evidence across time but still failed on weak variance
inflation. The failure biopsy suggested that the monitored variable itself was
wrong.

The global observation stream is a mixture of many legitimate latent fault
states. Its natural between-state variance can hide a small increase in
within-state observation noise.

SIM-018 first removes that nuisance structure.

For each sample:

~~~text
for every clean fault template h:
    E_h = mean_j ((x_j - mu_hj)^2 / var_hj)

residual_energy = min_h E_h
~~~

The minimum asks:

> How surprising is this observation even under the clean latent state that
> explains it best?

The residual energy is standardized against independent clean data and fed to
a one-sided CUSUM:

~~~text
C_t = max(0, C_(t-1) + z_t - kappa)
~~~

The detector's kappa and threshold are selected on separate calibration data
subject to a declared clean-sequence false-alarm target. Final performance is
measured on different clean and shifted seeds.

This generation therefore changes the monitored sufficient statistic rather
than adding another governance layer.

Synthetic engineering result only; no clinical authority.
