# RQ-002E — Ma 2025 spherical exchange benchmark

Primary source: Ma et al. 2025, DOI `10.1021/cbe.5c00017`.

The source models alginate microgel ion exchange as transport-limited spherical Fickian diffusion and reports interior diffusivities around `1.7e-11 m^2/s`. Crosslink degree approaches a plateau after about 10 min. The exact mean particle radius has not yet been recovered from the accessible source text, so it must not be fitted silently.

Using the analytical perfect-sink sphere solution only as a geometry-consistency calculation:

- if 90% of exchangeable Ca is removed by 10 min: equivalent radius ~237 um;
- 95% removed: ~202 um;
- 98% removed: ~173 um;
- 99% removed: ~157 um.

Thus a plausible benchmark radius band for near-plateau exchange is roughly `157–237 um` (diameter `315–475 um`) conditional on the stated 90–99% interpretation. This is consistent with the source's sub-mm micrographs but is not a measured radius.

The repository's `sphere_diffusion.py` stores the dimensionless spherical solution so future source geometry can be inserted without re-fitting diffusion physics.
