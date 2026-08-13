# RQ-002B — Observable state closure

v0.3's `expansion_proxy` is replaced for feed-forward analysis by source-backed alginate closures:

- swelling: Davidovich-Pinhas & Bianco-Peled (2010), DOI `10.1016/j.carbpol.2009.10.036` (`Q=A[Ca]^n`, second-order kinetics);
- mechanics: Liu et al. (2016), DOI `10.1016/j.carbpol.2015.08.086` (`G_e=k epsilon^1.5`).

The remaining explicit assumption is `bound junction fraction -> source-equivalent calcium`; this is a calibration variable, not a chemical identity.

## 5,000-sample exploratory screen

Using the existing 60 s vs 300 s preparation trajectories, 60 s rinse, and a 30 min horizon, the screen varied calcium floor/ceiling, junction-to-calcium exponent, swelling rate, and gel-point location over broad ranges.

At 30 min:

- 100% of samples had `Q_300s-prep < Q_60s-prep`;
- 100% had `G_300s-prep > G_60s-prep`;
- median swelling-ratio separation was about `0.53` (central 90% about `0.25–1.04`);
- median modulus ratio `G_300s/G_60s` was about `5.0` (central 90% about `2.2–22.2`).

This is a **model-structure signal only**. Absolute Q, modulus, lifetime, cyclic survival, and the junction-to-calcium mapping remain unvalidated.

Next target: bound the junction/network state -> effective gelling-calcium or rheologically effective crosslink-density relation from simultaneous structural+rheological primary data before escalating to higher-fidelity simulation.
