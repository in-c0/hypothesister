# RQ-001B — A01 calcium stoichiometry and transport priors

Status: **CONTEXT PRIORS AVAILABLE — load-bearing calcium split remains unresolved**

This note constrains the order of magnitude of calcium inventory and transport parameters for A01 without converting context-specific measurements into false calibration.

## 1. Alginate composition prior for the anchor material family

The Tavakoli 2019 calcium-release anchor used Sigma low-viscosity sodium alginate A1112 at 4% w/w. Sigma does not certify M/G ratio lot-by-lot for A1112, but its historical product data report approximately:

- 60–70% mannuronate (M)
- 30–40% guluronate (G)
- historical M/G ≈ 1.56
- degree of polymerization ≈ 400–600
- molecular-weight range ≈ 30–100 kDa

Therefore the G fraction must be treated as a **broad product-family prior**, not an exact property of the Tavakoli lot.

### Approximate G-residue concentration at 4% alginate

For order-of-magnitude stoichiometry only, approximate 4% w/w aqueous alginate as 40 g/L and use ~198.1 g/mol for a sodium uronate repeat unit. This gives total uronate residues ≈ 202 mM.

Applying the historical A1112 G fraction gives:

- 30% G → ~60.6 mM G residues
- 40% G → ~80.8 mM G residues

The density approximation and unknown lot-specific composition are explicit uncertainty sources.

## 2. Calcium-to-guluronate regimes

Fang et al. (2007), DOI 10.1021/jp0689870, identified successive calcium-binding regimes in alginate. Hu et al. (2022), DOI 10.1016/j.carbpol.2022.119788, experimentally classified four Ca/G regimes:

- Ca/G < 0.25
- 0.25 < Ca/G < 0.55
- 0.55 < Ca/G < 1.0
- Ca/G > 1.0

The 2022 work reports that Ca-induced gelation was not observed below Ca/G = 0.25, gelation begins in the 0.25–0.55 regime, and higher regimes correspond to further junction-network development.

Combining these ratios with the approximate A1112 G concentration above yields **feed-equivalent stoichiometric scales**:

| Ca/G ratio | at 30% G | at 40% G |
|---|---:|---:|
| 0.25 | ~15.1 mM Ca | ~20.2 mM Ca |
| 0.55 | ~33.3 mM Ca | ~44.4 mM Ca |
| 1.0 | ~60.6 mM Ca | ~80.8 mM Ca |

These numbers constrain the relevant calcium order of magnitude to **tens of mol/m³** for a 4% low-G/moderate-G alginate formulation.

### Critical warning

These are **not measurements of load-bearing bound calcium**. Feed Ca/G, total elemental calcium, reversibly associated calcium, residual/adsorbed CaCl₂ and mechanically load-bearing junction calcium are distinct quantities. The v0.1 parameters `C_t0` and `C_s0` therefore remain uncalibrated.

The current exploratory total of 40 mol/m³ in `CalciumDesign` happens to lie inside this broad stoichiometric scale, but that numerical coincidence must not be interpreted as validation.

## 3. Water transport prior

Oroná, Zorrilla & Peralta (2024), DOI 10.1002/jsfa.13131, directly measured an effective water diffusion coefficient in calcium alginate:

- `D_eff,w = 2.256 × 10^-9 m²/s`
- measured using a diffusion cell at 37 °C
- alginate G fraction `F_G = 0.356`

This is a useful **context prior** for `D_w`, especially because its magnitude is close to the exploratory v0/v0.1 value of 2.0 × 10^-9 m²/s. It is not yet a room-temperature or formulation-specific calibration for CleanCoin.

## 4. Effective calcium transport prior

Thu et al. (2000), *Biopolymers*, modeled inhomogeneous calcium-alginate gel spheres using:

- calcium diffusion coefficient `D_Ca = 1 × 10^-9 m²/s`
- bead diameter 0.80 mm

The model was checked against an experimentally visible gel front moving at ~0.1 mm/min at 5 mM CaCl₂. The authors reported that the high effective diffusion value was consistent with the observed front propagation.

This supports **~10^-9 m²/s as an order-of-magnitude calcium-transport prior**, but it was inferred in an inward gelation problem. Outward transport during swelling/de-crosslinking may differ because pore structure, binding/rebinding, ionic composition and moving network geometry differ.

Therefore `D_Ca` should currently be represented as a broad context prior centered around ~1 × 10^-9 m²/s, not as a fixed dissolution coefficient.

## 5. Current prior box for A01 v0.1

| Quantity | Prior | Status |
|---|---:|---|
| `D_w` | 2.256e-9 m²/s point context measurement | CONTEXT_PRIOR |
| `D_Ca` | order 0.8–1.0e-9 m²/s | CONTEXT/MODEL_PRIOR |
| total calcium scale relevant to 4% A1112-like gelation | ~15–81 mol/m³ | STOICHIOMETRIC_PRIOR |
| `C_t0` | unresolved | UNSET |
| `C_s0` | unresolved | UNSET |
| temporary/strong split | unresolved | UNSET |
| `k_t` | unresolved | UNSET |
| `k_s` | unresolved | UNSET |

## 6. Consequence for the research gate

We can now stop treating `D_w`, `D_Ca`, and total calcium order-of-magnitude as unconstrained free parameters. The dominant blocker is narrower:

> **How does experimentally observable calcium loss map onto loss of temporary versus strong load-bearing junction populations under a source-matched geometry and medium?**

Until that mapping is bounded, a 10–30 minute predicted collapse time would still be model assumption rather than evidence.

## Primary sources

- Fang Y, Al-Assaf S, Phillips GO, et al. (2007). *Multiple Steps and Critical Behaviors of the Binding of Calcium to Alginate*. J Phys Chem B 111:2456–2462. DOI: 10.1021/jp0689870.
- Hu C, Lu W, Sun C, et al. (2022). *Gelation behavior and mechanism of alginate with calcium: Dependence on monovalent counterions*. Carbohydrate Polymers 294:119788. DOI: 10.1016/j.carbpol.2022.119788.
- Oroná JD, Zorrilla SE, Peralta JM (2024). *Assessment of calcium alginate gels as wall materials for encapsulation systems*. J Sci Food Agric 104:2458–2466. DOI: 10.1002/jsfa.13131.
- Thu B, Bruheim P, Espevik T, et al. (2000). *Inhomogeneous alginate gel spheres: an assessment of the polymer gradients by synchrotron radiation-induced x-ray emission, magnetic resonance microimaging, and mathematical modeling*. Biopolymers 53:60–71.
- Sigma-Aldrich A1112 technical product information: historical 60–70% M / 30–40% G; not lot-specific.
