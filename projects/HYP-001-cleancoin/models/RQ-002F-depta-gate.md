# RQ-002F — Depta adaptation gate

Depta et al. DOI `10.1021/acs.jcim.1c01076` Case 4: 500 nm periodic cube, 0.5 wt% high-G alginate, 200 kDa, 571 dimer beads/chain, IM1, f=0.5.

The source calcium assay verifies `f = mol Ca / mol alginate monomer`; therefore f=0.5 is one available Ca per dimer. Ions are implicit in IM1.

Assuming 1.000 g/cm3 solution density, concentration bookkeeping gives ~1883 chains, or ~1.075 million moving dimer beads. This count is derived, not source-reported.

Full IM2 is expensive: the paper reports 17 days for 40 us on an Nvidia A100. More importantly, IM2 retained nearly the same mean coordination and pore fraction as IM1 even though roughly half the GG-GG contacts lost their ion.

Therefore Ca loss must not be equated directly with network collapse. Adaptation order is: reproduce source topology -> impose Ca depletion/unbinding -> measure connectivity and swelling -> add cyclic mechanical damage only after topology is understood.
