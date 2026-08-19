# RQ-003 surface shear / fibre-pullout decision

Status: **model-structure decision; parameters remain uncalibrated**
Date: 2026-08-19

## Question

Can the existing bulk transport/contact-failure coupling stand in for wash-surface shear/abrasion, or does CleanCoin need a separate surface/fibre-pullout term before RQ-003 can close?

## Primary evidence checked

- Bai et al., *Extreme Mechanics Letters* 1 (2014) 90–96, DOI `10.1016/j.eml.2014.11.001`, **Fiber-reinforced tough hydrogels**. In a fibre-reinforced alginate–polyacrylamide hydrogel, the observed composite failure mode changes to fibre pull-out against friction rather than simply bulk hydrogel fracture. This is direct evidence that reinforcement can introduce an interface-controlled dissipation/failure mode not represented by a homogeneous bulk strain threshold.
- Markstedt et al., *ACS Applied Materials & Interfaces* (2017), DOI `10.1021/acsami.7b02756`, **3D-Printable Bioactivated Nanocellulose–Alginate Hydrogels**. Nanocellulose is used as a structural rheology/mechanics modifier in alginate systems; the fibre/network phase is not mechanically equivalent to neat alginate.
- Ojansivu et al., *Biomacromolecules* (2018), DOI `10.1021/acs.biomac.8b01325`, **Biomimetic Mineralization of 3D Printed Alginate/TEMPO-Oxidized Cellulose Nanofibril Scaffolds**. Adding cellulose nanofibrils substantially changes shear recovery of the alginate system (reported recovery ~66% versus ~16% for pure alginate under the study protocol), again showing a shear-sensitive composite response that a bulk compression-only state cannot be assumed to capture.
- Li et al., *ACS Applied Materials & Interfaces* (2017), DOI `10.1021/acsami.7b04216`, **3D Bioprinting of Highly Thixotropic Alginate/Methylcellulose Hydrogel with Strong Interface Bonding**. Interfacial bonding in alginate-based printed structures is experimentally sensitive to crosslinking/interface treatment, supporting interface strength as an independent state variable rather than a guaranteed consequence of bulk modulus.

## Decision

**Yes: retain a separate bounded surface/interface failure term.**

The existing RQ-003 bulk contact model should remain a terminal accelerator coupled to transport/network weakening, but it should not be used as a surrogate for scrubbing shear or fibre pull-out. The evidence is sufficient for the model-structure decision because interface-controlled pull-out and shear recovery are experimentally distinct from homogeneous bulk compression response.

This does **not** justify calibrating a detailed tribology model yet. The immediate model should use a deliberately low-dimensional surface integrity state, for example:

- `s = 1` intact surface/interface, `s = 0` fully lost;
- degradation rate activated by both network weakening and accumulated tangential work/slip;
- one explicit interface-strength / pull-out parameter kept separate from the bulk contact-load factor `C`;
- sensitivity screen first; physical calibration only if this term materially changes the 10–30 min acceptance conclusion.

## Gate consequence

RQ-003 can advance from the binary “do we need a separate surface term?” question: **the answer is yes.** The next machine-side gate is to add the smallest possible surface-integrity term to the existing coupled model and test whether it changes the robust timing decision across uncertainty. If it does not, keep it as a documented secondary failure mode rather than expanding into a high-fidelity abrasion model.

Transfer warning: none of the cited systems reproduces the exact CleanCoin cellulose/CNF + Ca-alginate architecture or household wash contact conditions. These sources support model structure, not CleanCoin parameter values or lifetime claims.
