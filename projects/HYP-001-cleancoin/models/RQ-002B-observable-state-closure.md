# RQ-002B — Observable state closure

The anonymous v0.3 expansion proxy has been replaced by alginate-specific observable closures.

Swelling uses Davidovich-Pinhas & Bianco-Peled (2010), DOI `10.1016/j.carbpol.2009.10.036`: empirical `Q=A[Ca]^n` plus second-order swelling kinetics.

Mechanics uses Liu et al. (2016), DOI `10.1016/j.carbpol.2015.08.086`: `G_e=k*epsilon^1.5` above the gel point. Yuguchi et al. (2000), DOI `10.1016/S0022-2860(00)00556-1`, show that local chain association precedes formation of a continuous elastic network, so mechanics now has its own explicit connectivity threshold rather than sharing the swelling calcium axis.

## Corrected robustness screen

A 5,000-sample screen compared existing 60 s and 300 s preparation trajectories after a 60 s rinse at a 30 min horizon. It varied the swelling-state mapping, swelling rate, mechanical connectivity threshold, and connectivity scale.

Results:
- 100%: longer preparation was less swollen;
- 100%: longer preparation was mechanically stronger;
- median swelling-ratio separation: ~0.53; central 90% ~0.25–1.04;
- ~69.7%: short preparation fell below the sampled connectivity threshold while long preparation remained connected;
- where both remained connected, median modulus ratio was ~32.5. The very wide upper tail means near-threshold modulus ratios are not quantitative predictions.

This is a model-structure signal only. The priority unknown is now the mapping from local calcium-mediated junction/bundle state to sample-spanning connectivity.
