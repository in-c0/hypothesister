# RQ-001D — Crosslink duration must map to network state

Status: **MODEL-STRUCTURE REQUIREMENT ESTABLISHED**

## Why this sub-question exists

Tavakoli et al. (2019) used the same nominal 4% alginate / 100 mM CaCl₂ formulation but changed crosslink duration from 1 min to 5 min. The normalized swelling-stage calcium-release curves differ strongly:

- 1-min crosslink apparent normalized release rate: ~7.24e-4 s^-1
- 5-min crosslink apparent normalized release rate: ~2.66e-4 s^-1
- ratio: ~2.72×

The 5-min system also develops a distinct 240–360 min equilibrium plateau before later degradation.

## Structural consequence for A01 v0.1

In the current reduced model, if strong-junction degradation is inactive and two samples share:

- geometry,
- `D_w`,
- `D_Ca`, and
- temporary-junction dissociation rate `k_t`,

then changing only `C_t0` (the amount of temporary Ca²⁺) primarily rescales the release amplitude. It cannot explain the observed ~2.7× change in the **normalized release shape**.

Therefore a preparation model in which crosslink duration changes calcium inventory only is structurally inadequate.

At least one of the following must be crosslink-state dependent:

1. accessible temporary-junction fraction;
2. effective temporary-junction dissociation kinetics;
3. effective water/Ca²⁺ transport through the network;
4. pore/mesh geometry and diffusion length;
5. topology / distribution of temporary versus chelate junctions;
6. swelling-coupled transport and connectivity.

## Independent primary support

Patel et al. (2017), DOI `10.1016/j.carbpol.2016.08.095`, directly studied ionotropic-gelation residence time (IGRT) in calcium-alginate particles and measured surface and internal Ca²⁺ separately by EDS.

Their results establish that IGRT changes more than total calcium:

- particle size, porosity, density, mechanical strength and swelling were significantly affected;
- internal Ca²⁺ concentration increased with residence time until a plateau around 4 h;
- surface Ca²⁺ distribution changed little after ~30 min;
- the authors interpret alginate crosslinking as diffusion-driven;
- longer residence time therefore creates a spatially and mechanically different network state, not merely a scalar increase in Ca²⁺.

This evidence strongly supports representing **preparation history as a state-generating process**.

## Updated model architecture

Instead of:

`crosslink_time -> total_Ca -> release`

use:

`crosslink_time + bath_Ca + geometry + alginate composition`

`        -> preparation / gelation transport model`

`        -> spatial network state at t = 0 of washing`

`        -> swelling / de-crosslinking model`

The preparation-state output should eventually include fields such as:

- `C_temp(x, 0)`
- `C_strong(x, 0)`
- `mesh_size(x, 0)` or a defensible proxy
- porosity / water fraction
- effective `D_w(x)` and `D_Ca(x)` or constitutive relations tying them to state
- initial residual stress / syneresis state if sensitivity warrants it

## Consequence

The next A01 virtual-lab version should become a **two-stage simulation**:

1. `prepare`: simulate Ca²⁺ ingress / junction formation for a specified crosslink duration;
2. `use`: switch boundary conditions to water and simulate Ca²⁺ egress, swelling, junction loss and later mechanics.

That architecture has an important scientific advantage: the observed 1-min versus 5-min Tavakoli curves become a direct test of whether the same underlying physics can predict different material lifecycles from preparation history alone.

## Gate

Do not introduce an arbitrary empirical `crosslink_duration_factor` merely to fit both curves. The duration dependence should emerge from transport + network-state evolution as far as the available evidence permits.
