# RQ-002A — Effective crosslink density -> wet modulus prior

Status: **CONSTITUTIVE CONTEXT PRIOR ESTABLISHED — swelling correction still missing**

## Primary anchor

Grassi et al. (2009), *Molecules* 14, 3003–3017. DOI: `10.3390/molecules14083003`.

The study mechanically characterized homogeneous calcium-alginate cylinders using 10% compression stress-relaxation tests at 25 °C and fitted the relaxation data with a generalized Maxwell model.

Source conditions:

- alginate G content: 65–75% (high-G relative to A01's A1112 family prior)
- gel geometry: height ~1.9 cm; diameter 1.5 cm
- crosslink medium: 0.05 M CaCl₂ + 0.4 M NaCl
- crosslink duration: 3 days to obtain homogeneous crosslinking
- no significant swelling/shrinking detected after crosslinking before mechanical testing
- mechanical test temperature: 25 °C
- 10% deformation selected within the reported linear viscoelastic region

## Quantitative observations

| alginate % w/v | Young modulus E | effective crosslink density rho_x | mesh size xi | lambda1 |
|---:|---:|---:|---:|---:|
| 0.5 | 2.162 kPa | 0.29 mol/m³ | 22.0 nm | 3.3 s |
| 1.0 | 8.158 kPa | 1.10 mol/m³ | 14.0 nm | 8.9 s |
| 2.5 | 21.294 kPa | 2.80 mol/m³ | 10.0 nm | 15.0 s |
| 3.8 | **47.587 kPa** | **6.40 mol/m³** | **7.9 nm** | **20.1 s** |
| 5.0 | source E value flagged | 6.90 mol/m³ | 7.7 nm | 22.5 s |

The 5% Young-modulus value is deliberately not used: the PMC-rendered table shows 511902 Pa, while its listed Maxwell spring constants sum to ~51101 Pa and the reported crosslink density is likewise consistent with ~51 kPa under the same Flory relation. We preserve the source ambiguity rather than silently correcting it.

## Constitutive relation

The paper states that, for gels crosslinked in solution that did not subsequently swell/shrink before the mechanical test, Flory theory relates Young's modulus `E` to network crosslink density `rho_x` through its Equation (3).

The reported table is numerically consistent with:

`E = 3 R T rho_x`

where `rho_x` is in mol/m³, `T` in kelvin and `E` in pascals.

For the 3.8% gel at ~298.15 K:

`3 * R * T * 6.4 mol/m³ ≈ 47.596 kPa`,

which agrees with the reported 47.587 kPa to much better than 1%.

## Why this matters for HYP-001

Our prior calcium work had a broad feed/total-Ca scale of roughly 15–81 mol/m³ for 4% A1112-like alginate. Grassi's 3.8% high-G gel gives a **mechanically effective crosslink-density** scale of ~6.4 mol/m³.

These quantities are not contradictory because they represent different things:

- feed/total/associated Ca²⁺ inventory;
- mechanically effective network crosslinks.

The virtual lab must therefore preserve an explicit mapping:

`calcium/junction state -> effective load-bearing crosslink density rho_x -> modulus E`

rather than equating total calcium with mechanical connectivity.

## Transfer limitations

The 3.8% concentration is close to A01's ~4% anchor, but several major differences prevent direct assignment of `rho_x = 6.4 mol/m³` to A01:

1. Grassi alginate is high-G (65–75%), whereas historical A1112 is much lower-G (~30–40%).
2. Grassi used 3 days of crosslinking, versus Tavakoli's 1–5 min.
3. Grassi used 50 mM CaCl₂ + 0.4 M NaCl, versus 100 mM CaCl₂ preparation and distilled-water use in Tavakoli.
4. The Flory relation is applied to gels that had not undergone further swelling/shrinking before mechanics; CleanCoin explicitly relies on hydration/swelling and de-crosslinking.
5. CleanCoin adds a cellulose/CNF reinforcement phase that can carry load independently of alginate crosslinks.

Therefore this is a **constitutive context prior and validation case**, not an A01 calibrated modulus.

## Independent weakening constraint

LeRoux, Guilak & Setton (1999), DOI `10.1002/(SICI)1097-4636(199910)47:1<46::AID-JBM6>3.0.CO;2-N`, measured Ca-alginate compressive/shear properties during physiological NaCl exposure. After 15 h, the abstract reports reductions of ~63% in compressive modulus, ~84% in equilibrium shear modulus and ~90% in dynamic shear modulus relative to controls.

This establishes that ion exchange can produce very large wet-mechanics losses, but a time-resolved quantitative extraction is still needed before it can become a weakening law.

## Next model step

Add a small source-backed mechanics mapping that converts **effective crosslink density** to an unswollen reference modulus, while keeping the mapping from simulated calcium state to `rho_x(t)` unresolved.

Then search/calibrate a swelling/ion-exchange correction:

`E(t) = E_ref(rho_x(t), T) * g(swelling_state, ionic_state, reinforcement)`.

This separates what the literature already constrains from what remains unknown, and avoids embedding the v0.3 `expansion_proxy` directly into modulus without evidence.
