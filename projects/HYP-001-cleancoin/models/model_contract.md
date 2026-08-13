# Model contract: HYP-001

A computational result is allowed to influence the stage gate only if every influential parameter has provenance and uncertainty.

## State variables required by first real continuum model

- `c_w(x,t)` — local water activity/concentration
- `c_ion(x,t)` — relevant mobile ion concentration(s)
- `q(x,t)` — crosslink/binder integrity state
- `u(x,t)` — displacement field
- `d(x,t)` — scalar damage / fracture field (or an explicitly justified alternative)

## Minimum coupled physics

1. water transport;
2. relevant ion/binder transport;
3. network association/dissociation kinetics;
4. swelling strain;
5. hydrated constitutive mechanics;
6. cyclic damage accumulation;
7. loss of connectivity / disintegration criterion.

## Calibration hierarchy

1. primary experimental literature;
2. secondary literature only as navigation to primary measurements;
3. molecular/coarse-grained simulation for missing high-sensitivity parameters;
4. targeted physical measurement only when uncertainty cannot be bounded virtually.

## Model levels

### `cleancoin_lab.model` — v0 workflow model

Infrastructure test only. It represents hydration plus a single sacrificial-network loss rate and is not chemistry-specific.

### `cleancoin_lab.ca_model` — A01 v0.1 reduced reaction-diffusion model

Intermediate-fidelity calibration scaffold. It explicitly represents hydration transport, temporary and strong Ca²⁺ junction populations, mobile Ca²⁺ diffusion, an ideal bath sink, calcium mass balance, and threshold-like activation of strong-junction loss.

It still omits finite-bath boundary conditions, ion rebinding/competitive exchange, swelling/poroelasticity, hydrated constitutive mechanics, cyclic fatigue, moving geometry and fracture/disintegration. Its default numerical values are exploratory.

A v0.1 sensitivity ranking may determine **which parameters to research next**, but its predicted lifetime or bath concentration MUST NOT be reported as evidence for HYP-001 until influential parameters are source-calibrated.

### `cleancoin_lab.prepare_use_model` — A01 v0.2 preparation-history model

Model-structure test motivated by Tavakoli 2019 and Patel 2017. It treats ionotropic gelation as a first simulation stage and the calcium-free rinse/use environment as a second stage. Calcium ingress creates a spatial distribution of free, temporary and coarse-grained persistent junction states; switching the boundary to a sink then produces preparation-history-dependent calcium egress.

The temporary-to-strong `maturation` state is explicitly a reduced-order proxy for preparation-induced network topology. It is **not** a claim that calcium alginate literally follows a two-state chemical mechanism.

v0.2 is allowed to answer questions such as:

- Can preparation history in principle change normalized release shape without assigning a different arbitrary use-stage rate to each sample?
- Which preparation-state variables are structurally identifiable from the 1-min versus 5-min source curves?
- Which missing measurements most reduce uncertainty?

v0.2 is not allowed to claim:

- a CleanCoin lifetime;
- a validated temporary/strong junction fraction;
- a physical maturation rate;
- mechanical performance or disintegration;
- a stage-gate pass.

A future calibrated version must replace or constrain the coarse-grained maturation law with source-backed preparation-state data and add swelling/mechanics before HYP-001 feasibility is evaluated.

## Reproducibility

All model changes should be covered by automated tests. GitHub Actions runs the repository test suite on pushes to `main` and pull requests. A passing software test means the implementation satisfies its coded invariants; it does **not** validate the physical model.

## Inference prohibition

None of the v0, v0.1 or uncalibrated v0.2 models may generate a stage-gate pass. A positive HYP-001 signal must come from source-calibrated physics with propagated uncertainty and robustness to nearby parameter/geometry perturbations.
