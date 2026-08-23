# RQ-003 physical-regime bounds for the surface/contact screen

Status: bounded evidence update for the existing RQ-003 sensitivity gate. This is not a CleanCoin calibration, lifetime claim, or product specification.

## Why this note exists

The merged classification-change screen showed that the surface/interface term can change the 10–30 minute acceptance classification, but the effect was dominated by a deliberately broad, uncalibrated work/interface-strength envelope. The next gate is therefore to constrain the *order of magnitude and failure mode* of the mechanical regime using transferable primary evidence before any higher-fidelity abrasion model is promoted.

## Primary evidence anchors

| Source | Material / loading | Quantitative anchor | What it can constrain here | What it cannot justify |
|---|---|---:|---|---|
| LeRoux, Guilak & Setton (1999), J Biomed Mater Res, DOI 10.1002/(SICI)1097-4636(199910)47:1<46::AID-JBM6>3.0.CO;2-N | Ca-crosslinked alginate, 1–3% alginate; NaCl exposure; compression and shear tests | after 15 h in NaCl, compressive equilibrium modulus fell 63%, equilibrium shear modulus 84%, dynamic shear modulus 90% vs control | ion-exchange softening can strongly reduce both bulk and shear stiffness; surface/contact strength should not be sampled independently of chemical state | direct one-wash timescale or CleanCoin failure stress |
| Wang et al. (2017), J Biomater Sci Polym Ed, DOI 10.1080/09205063.2017.1279532 | Ca-crosslinked 3-D printed sodium-alginate scaffold vs bulk hydrogel | friction studied from 1e-6 to 1 m/s; at 0.3 kPa scaffold friction was reproducible and structure-dependent | sliding-speed/contact structure matter; a single universal friction/work coefficient is not defensible | direct abrasion threshold or product friction coefficient |
| Smith et al. (2020), J Mech Behav Biomed Mater, PMID 32807343 | calcium alginate under cyclic axial rotation | 10–100 N axial load, 100 cycles; alginate frictional torque increased with load (~0.08 to ~0.09 N m mean across the stated load range) | cyclic tangential work scales with normal load and should remain an explicit uncertainty axis | transfer of absolute force/torque into CleanCoin geometry |
| Mimar et al. (2020), Tribology study, PMID 32090909 | calcium alginate in cartilage defect, pin-on-disc in Ringer's solution | 0.06 MPa, 1 Hz; hydrogel/cartilage median friction coefficient ~0.38; high-speed data showed greatest wear in hydrogel/cartilage condition | wear can occur under repeated sliding even when bulk friction coefficient is not exceptional; surface failure is a credible separate channel | a universal coefficient of friction or direct useful-life claim |
| Lin et al. (2020), Nat Commun 11, 1363, DOI 10.1038/s41467-020-14871-3 | PAAm-alginate coating under reciprocating sliding | non-fatigue-resistant PAAm-alginate coating failed by ~90 cycles at 20 N in the reported cartilage tribology setup | alginate-containing hydrogel surface integrity can fail substantially earlier than bulk-cycle counts suggest; cycle-dependent surface damage is structurally plausible | transfer to pure calcium alginate or CleanCoin service conditions |

## Gate consequence

The evidence is sufficient to narrow the *model structure* but not to calibrate a product envelope:

1. **Couple strength to chemistry/network state.** Bulk/shear stiffness can collapse strongly after ion exchange, so the surface-strength term should decrease with the same weakening state rather than be sampled as a fully independent constant.
2. **Keep normal load, sliding speed/contact time, and tangential work explicit.** Published alginate friction/wear changes with load, speed, poroelastic/contact structure, and cycle count; collapsing them to one fixed work threshold would hide the dominant uncertainty.
3. **Use stress/work regimes only as transfer anchors.** Published loads, pressures and friction coefficients arise from different formulations and geometries. They can bound orders of magnitude for sensitivity analysis, but they are not CleanCoin calibration data.
4. **Do not promote a high-fidelity abrasion model yet.** The next useful computation is a *constrained structural rerun*: tie interface strength monotonically to the existing network state, restrict friction/work inputs to literature-anchored regimes, and test whether the previous 19.147% classification-change conclusion remains qualitatively stable.

## Decision rule for the next rerun

Keep the existing frozen 10–30 minute acceptance classification. Rerun the same deterministic ensemble with only these structural changes:

- interface strength is a monotone function of network/chemical weakening rather than an independent wide uniform draw;
- normal-pressure/contact-work inputs are restricted to literature-anchored order-of-magnitude bands, while preserving deliberately broad geometry uncertainty;
- sliding/cycle variables remain sensitivity axes, not independent dimensional clocks.

Advance surface damage to a required model component only if the constrained rerun still changes the acceptance classification in a non-negligible, stable fraction of the ensemble and the result is not dominated by one arbitrary boundary of the transfer envelope. Otherwise retain surface failure as a documented secondary mode and defer abrasion-model escalation.

## References

- LeRoux MA, Guilak F, Setton LA. Compressive and shear properties of alginate gel: effects of sodium ions and alginate concentration. J Biomed Mater Res. 1999;47(1):46-53. DOI: 10.1002/(SICI)1097-4636(199910)47:1<46::AID-JBM6>3.0.CO;2-N.
- Wang et al. Friction of sodium alginate hydrogel scaffold fabricated by 3-D printing. J Biomater Sci Polym Ed. 2017. DOI: 10.1080/09205063.2017.1279532.
- Smith et al. A technique for measuring the frictional torque of articular cartilage and replacement biomaterials. J Mech Behav Biomed Mater. 2020. PMID: 32807343.
- Mimar et al. A method for the assessment of the coefficient of friction of articular cartilage and a replacement biomaterial. 2020. PMID: 32090909.
- Lin et al. Fatigue-resistant adhesion of hydrogels. Nat Commun. 2020;11:1363. DOI: 10.1038/s41467-020-14871-3.
