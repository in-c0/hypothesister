# RQ-002D — Transport-length gate

A 2025 primary ion-exchange study (DOI `10.1021/cbe.5c00017`) fitted effective interior Ca transport coefficients of `1.69–1.76e-11 m^2/s` in 5 wt% alginate microgels during Mg exchange. Crosslink degree decreased with exchange time and plateaued after about 10 min in that source geometry.

Using the diffusion scale `t ~ L^2/D` with `D = 1.7e-11 m^2/s`:

| characteristic path L | diffusion scale |
|---:|---:|
| 50 um | 2.45 min |
| 100 um | 9.8 min |
| 150 um | 22.1 min |
| 250 um | 61.3 min |
| 500 um | 4.08 h |
| 1 mm | 16.3 h |

For a 20 min target, `sqrt(D*t)` is about `143 um`.

## Consequence

Passive ion-exchange timing on the desired 10–30 min scale is plausible only if the relevant transport distance is roughly hundreds of micrometres or less under a diffusion coefficient of this order. A dense millimetre-scale alginate body is therefore a poor A01 geometry.

A01 should prioritize porous architectures with thin alginate walls/struts or short diffusion paths. A01B/internal-trigger concepts remain useful alternatives if a thicker load-bearing geometry is required.

This is a scaling constraint, not a lifetime prediction: the source uses 5 wt% alginate microgels, Mg exchange, and source-specific geometry/boundary conditions.
