# RQ-003 — bounded surface-strength anchors

Date: 2026-08-22
Purpose: constrain the deliberately broad surface work/strength envelope that drove the merged RQ-003 classification-change screen. This is an evidence note, not a promoted abrasion model.

## Quantitative anchors

| System / test | Quantitative result | Relevance / limitation |
|---|---:|---|
| Calcium-alginate gels, compression to fracture (six alginate grades) | fracture stress ~123–679 kPa; work of deformation ~17–101 kJ/m^3; fracture strain ~0.52–0.60 | Direct calcium-alginate bulk failure scale. Composition-dependent; not a surface-shear or wet-scrub measurement. Source: Fu et al., *Relevance of Rheological Properties of Sodium Alginate in Solution to Calcium Alginate Gel Properties* (2011), PMCID PMC3134659. |
| Ionic alginate gel after physiological NaCl exposure | after 15 h, compressive modulus -63%, equilibrium shear modulus -84%, dynamic shear modulus -90% vs control | Direct evidence that ionic environment can move alginate shear/compression strength scales substantially; exposure is much longer than the target wash window. Source: LeRoux et al., *Compressive and shear properties of alginate gel: effects of sodium ions and alginate concentration* (1999), PMID 10400879. |
| Alginate gels, torsion/compression fracture | fracture stress depends on Ca2+ and alginate concentration; fracture strain comparatively insensitive to composition | Supports parameterising failure strength by crosslink/composition state rather than treating one universal surface-strength constant as physical. Source: Zhang et al., *Fracture Analysis of Alginate Gels* (J Food Sci, DOI 10.1111/j.1365-2621.2005.tb11471.x). |
| Soft vs hard alginate gels, pure shear / cavitation | soft: fracture energy ~0.2–0.3 J/m^2; hard: ~4.2–4.3 J/m^2; moduli ~2.9 vs 17.8 kPa | Direct alginate fracture-energy scale spans >10x with formulation. Geometry is fracture, not abrasion/fibre pullout. Source: *Cavitation induced fracture of intact brain tissue* validation gels (2022), PMCID PMC9382329. |

## Decision impact

The merged 200k-sample screen showed 19.147% overall classification changes and 70.242% in the highest work/strength quartile. These anchors confirm that alginate failure scales vary by formulation/crosslink state and environment by large factors, so a single unconstrained work/strength ratio should not be interpreted as a calibrated abrasion prediction.

However, the sources above still do **not** provide the missing quantity directly: wet surface shear/abrasive work or fibre-pullout strength for the proposed A01 coating under a wash-like contact. Therefore they constrain plausibility but do not justify a high-fidelity surface model.

## Next frozen gate

Before promoting any abrasion/fibre-pullout model, obtain at least one direct wash-relevant surface measurement or primary-data proxy that bounds both sides of the ratio used by the existing screen:

1. applied tangential work/stress at the coating surface under a defined contact/load/speed; and
2. wet interfacial/surface failure work or strength for a materially comparable calcium-alginate layer.

Then rerun the **same** merged classification rule with the narrower evidence-backed envelope. Do not change the acceptance rule merely to reduce the observed classification-change rate.
