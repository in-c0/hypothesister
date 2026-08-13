# RQ-002 — Wet mechanics / swelling evidence seed

Status: **EVIDENCE MAP OPEN**

## Objective

Replace A01 v0.3's reduced `expansion_proxy` with source-grounded state variables linking calcium-crosslink state, swelling and wet mechanical integrity.

The immediate target is not a final constitutive law. It is to identify primary datasets that jointly constrain at least two of:

- crosslinking / preparation history;
- calcium state or concentration;
- swelling / volume change;
- modulus / strength / stress relaxation;
- time in water / salt / exchange medium.

## High-value primary evidence located

### Patel et al. 2017 — preparation history couples chemistry, morphology and mechanics

DOI: `10.1016/j.carbpol.2016.08.095`

Ionotropic-gelation residence time significantly altered particle size, porosity, density, mechanical strength and swelling. Surface and internal Ca²⁺ were measured separately using EDS, making this especially valuable for constraining the `prepare` stage and linking it to mechanical state.

### LeRoux, Guilak & Setton 1999 — ion exchange causes large wet-modulus loss

DOI: `10.1002/(SICI)1097-4636(199910)47:1<46::AID-JBM6>3.0.CO;2-N`

Calcium-alginate gels were tested in compression, equilibrium/dynamic shear and oscillatory shear as a function of alginate concentration and NaCl exposure. After 15 h in physiological NaCl, reported compressive, equilibrium shear and dynamic shear moduli decreased by approximately 63%, 84% and 90% relative to controls. This establishes that ionic exchange/environment can strongly reduce wet mechanical integrity.

### Kuo & Ma 2001 — composition controls gelation rate and compressive mechanics

DOI: `10.1016/S0142-9612(00)00201-5`

Controlled alginate gelation systems showed compressive modulus/strength increasing with alginate concentration, total calcium, molecular weight and guluronate content. Slower gelation produced more uniform and mechanically stronger gels. This supports treating preparation history and composition as constitutive inputs rather than using one universal modulus.

### Posbeyikian et al. 2021 — gel-front evolution links to rheological stabilization

DOI: `10.1016/j.carbpol.2021.118293`

Time-resolved optical video microscopy tracked Ca-alginate bead formation. Gel-front migration correlated with the storage-modulus plateau, while bead-volume shrinkage (syneresis) correlated with stabilization of shear strain and yield stress. This is close to the coupled preparation-state evidence needed by the virtual process twin.

### Bajpai & Sharma 2004 — swelling / Ca²⁺ release / dissolution are coupled

DOI: `10.1016/j.reactfunctpolym.2004.01.002`

Ca-alginate beads showed substantial water uptake followed by dissolution; Ca²⁺ release confirmed an ion-exchange mechanism and was reported as diffusion controlled. This is useful for tying the RQ-001 transport state to RQ-002 swelling/degradation mechanics.

## Initial interpretation

The literature supports the model architecture qualitatively:

`preparation / Ca²⁺ distribution -> network morphology -> swelling / ion exchange -> wet modulus / strength -> failure`

but the current evidence map is not yet sufficient to identify a source-matched quantitative constitutive law for the Tavakoli A1112 / 100 mM CaCl₂ system.

## Next extraction priority

1. Obtain quantitative time-series / tabulated values from Posbeyikian 2021 for gel-front migration, volume change and rheology.
2. Obtain Patel 2017 internal/surface Ca²⁺ vs residence-time and mechanical-strength/swelling values.
3. Extract LeRoux 1999 modulus-vs-NaCl-time/composition values to bound ion-exchange-induced mechanical weakening.
4. Determine whether these datasets can be nondimensionalized into a transferable relation between calcium-network state and modulus/swelling.

Only if those relations remain underdetermined should molecular/coarse-grained simulation or targeted physical testing be introduced.
