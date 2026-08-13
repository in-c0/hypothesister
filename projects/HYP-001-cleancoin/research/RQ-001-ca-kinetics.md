# RQ-001 — Ca²⁺ loss / ion-exchange kinetics for A01

Status: **PARTIALLY BOUNDED — do not yet promote to a universal model parameter**

## Question

Can we bound the calcium-loss / ion-exchange timescale that controls weakening of the A01 cellulose/CNF + Ca-alginate candidate strongly enough to calibrate a CleanCoin lifecycle model?

## Primary quantitative anchor

Tavakoli, Laisak, Gao & Tang (2019), *Materials Science and Engineering: C* 104, 109951. DOI: 10.1016/j.msec.2019.109951.

Experimental system:

- low-viscosity sodium alginate: 4% w/w
- CaCl₂ crosslink bath: 100 mM
- droplet/bead fabrication through gauge-18 syringe under 50 rpm stirring
- crosslinking times compared: 1 min and 5 min
- beads rinsed in distilled water for 1 min
- swelling/degradation measured in distilled water and 3% w/w NaCl solution
- wet samples tested immediately after crosslinking; dry samples dried for 24 h
- Ca²⁺ in the external swelling environment quantified using SA-4CO₂Na AIE fluorescence

Reported time-resolved observations:

### 1-minute crosslink

- 0–60 min: external Ca²⁺ release rate ≈ **0.046 mM/min**
- 60–120 min: external Ca²⁺ release rate ≈ **0.0034 mM/min**
- swelling and degradation were not separated by the long plateau seen in the more strongly crosslinked sample

### 5-minute crosslink

During the reported 0–240 min swelling regime, the external Ca²⁺ release rate decreased approximately as:

- 0–60 min: **0.067 mM/min**
- 60–120 min: **0.025 mM/min**
- 120–240 min: **0.007 mM/min**
- 240–360 min: approximately negligible release / equilibrium plateau before the later degradation regime

The same study reports that a 3% w/w NaCl swelling environment reduced swelling and reduced Ca²⁺ release relative to distilled water after 200 min, indicating that ionic strength / osmotic conditions materially alter the observed kinetics.

Mechanistically, the authors distinguish weaker/temporary Ca²⁺ junctions that dissociate during swelling from more stable chelate junctions; degradation occurs after network expansion reaches a critical state and the stronger junctions dissociate.

## Supporting evidence

### Bjørnøy et al. 2016 — reaction-diffusion description is viable

*Acta Biomaterialia* 44, 243–253. DOI: 10.1016/j.actbio.2016.07.046.

A calcium/alginate reaction-diffusion model reproduced experimentally observed gelation kinetics over a range of gelling-ion concentrations and geometries. The paper also cites an experimental gel-front velocity of ~100 μm/min for 50 mM CaCl₂. This supports using a transport + reaction formulation rather than a single empirical timer.

### Potter et al. 1994 — calcium transport is diffusion-limited and structure-dependent

*Carbohydrate Research* 257, 117–126. DOI: 10.1016/0008-6215(94)84112-8.

MRI tracking found the sol/gel interface displacement proportional to sqrt(time), consistent with diffusion-limited calcium transport. Effective calcium transport depended on initial calcium concentration, ionic strength and pore size.

### Urbanová et al. 2019 — environment changes the transformation pathway

*Biomacromolecules* 20, 4158–4170. DOI: 10.1021/acs.biomac.9b01052.

Solid-state NMR and dissolution studies show that alginate gels undergo coupled ion exchange, protonation, swelling, dissolution and secondary-phase formation depending on the surrounding medium. Ca²⁺ release cannot be treated as an environment-independent material constant.

### Zhang et al. 2026 — crosslink concentration strongly changes persistence

*Frontiers in Bioengineering and Biotechnology* 14, 1828848. DOI: 10.3389/fbioe.2026.1828848.

2% w/v alginate crosslinked with 50, 100 or 200 mM CaCl₂ formed stable hydrogels and released Ca²⁺ gradually in PBS over 24–72 h. Higher CaCl₂ concentration reduced swelling. This is useful as a high-persistence contrast case, but the geometry, preparation and PBS environment are too different to transfer its time constants directly to CleanCoin.

## What is now bounded

We have a credible empirical **order-of-magnitude timescale** showing that weakly/briefly Ca²⁺-crosslinked alginate can exhibit substantial Ca²⁺ redistribution and swelling/degradation changes over **tens of minutes to hours**, and that crosslinking duration can move the system between qualitatively different temporal regimes.

This is a real positive signal for HYP-001: the desired timer is not obviously incompatible with calcium-alginate physics.

## What is NOT bounded

The current `hydration_crosslink_rate_s` (`k_h`) in `src/cleancoin_lab/model.py` must remain uncalibrated.

The reported mM/min values are **external-bath concentration rates**, not fractional network crosslink-loss constants. Converting them to `k_h` requires, at minimum:

1. initial bound Ca²⁺ inventory per sample;
2. bath volume and sampling/replacement protocol;
3. bead geometry / surface area / characteristic diffusion length;
4. mapping from Ca²⁺ loss to load-bearing junction density;
5. medium composition and temperature;
6. distinction between temporary junction release and chelate-junction failure.

A direct assignment such as `k_h = release_rate / concentration` would create false precision and violate the model contract.

## Model implication

The next A01 model should replace the single first-order hydration-loss term with an explicit calcium state, approximately:

- mobile/bath Ca²⁺ transport;
- reversibly bound / temporary Ca²⁺ junctions;
- strongly bound / chelate junctions;
- swelling-dependent or connectivity-threshold failure.

A minimal reduced model may still be fitted before molecular simulation, but it must preserve geometry and bath conditions.

## RQ-001 decision

**PARTIAL PASS.** There is sufficient primary evidence to justify continuing A01 and building a source-calibrated reaction/diffusion model. There is **not** yet enough evidence to claim a CleanCoin working lifetime or assign a universal calcium-loss rate.

Next action: digitize/fetch the Tavakoli 2019 time-series sufficiently to fit a geometry-aware reduced model, then test whether any plausible thin/porous geometry can shift the collapse window toward the 10–30 min HYP-001 target without requiring implausible parameter extrapolation.
