# HYP-001 Virtual Lab v0

## Purpose

The first technical task is not to make a sponge. It is to establish whether a **robust physically plausible parameter region** can support delayed wet-state loss of cohesion.

## v0 model

The starter model intentionally represents only two coupled processes:

1. water diffusion through a 1-D slab;
2. water- and load-dependent loss of a sacrificial network.

It is intentionally falsifiable and replaceable. It omits swelling mechanics, poroelasticity, fibre pull-out, fracture, erosion, detergent chemistry, real cyclic stress fields, and chemistry-specific thermodynamics.

## Stage 1A — evidence acquisition (next)

Build a machine-readable parameter registry for 2–3 mechanistically distinct bio-derived architectures. Initial search families:

- cellulose / nanocellulose structural scaffold;
- alginate or related ionic polysaccharide network;
- starch / dextrin / pullulan / pectin sacrificial phase;
- chitosan or protein systems only where they add a distinct mechanism;
- benign ions/minerals when required for function.

For each parameter, store: value/range, units, conditions, material formulation, measurement method, DOI/source, uncertainty, and whether it transfers to our geometry.

### Required parameters

- water diffusivity / sorption kinetics;
- equilibrium swelling ratio;
- hydrated modulus vs composition/crosslink density;
- crosslink exchange / dissociation kinetics where available;
- fatigue/damage behaviour under wet cyclic loading;
- fracture/erosion/disintegration metrics;
- temperature, pH and ionic-strength dependence.

## Stage 1B — first real virtual model

Replace v0 assumptions with literature-calibrated priors and implement a coupled continuum model:

- diffusion / sorption;
- swelling strain;
- crosslink kinetics;
- constitutive wet mechanics;
- scalar damage or phase-field fracture;
- standardized cyclic loading protocol.

FEniCSx is a candidate for this layer because it provides programmable finite-element/PDE infrastructure. The choice should remain replaceable behind a backend interface.

## Stage 1C — molecular parameter estimation

Use molecular/coarse-grained simulation only where continuum parameters are missing or uncertainty analysis shows they dominate the outcome.

Candidate engines:

- LAMMPS for polymeric/coarse-grained/material MD;
- OpenMM where its Python-first molecular simulation workflow is advantageous;
- MACE / other ML interatomic potentials only when a suitable domain model exists or high-quality training/reference data justify one.

Do not run expensive atomistic work merely because it is available.

## Stage 1D — surrogate + active learning

Train a surrogate only after we have enough expensive simulator calls that approximation produces real leverage. The surrogate must carry uncertainty; candidate selection should optimize expected information gain and target satisfaction rather than raw predicted score alone.

## Gate to Market/IP

Proceed only when all are true:

1. >=2 mechanistically distinct architectures have literature-supported parameterizations;
2. at least one architecture has a **region**, not a point, satisfying the lifecycle targets;
3. the region survives uncertainty/perturbation analysis;
4. no dominant parameter remains completely unconstrained;
5. an independent reviewer can reproduce the result from code + provenance.

Only then do serious market and IP work.

## Physical experiments

Physical work is a sparse validation/calibration oracle, not the default search method. A physical measurement is justified when its expected information gain is higher than another simulation/literature action and the quantity cannot be bounded credibly otherwise.

## Initial architecture shortlist (evidence pass 0)

Three architectures are registered in `candidate_architectures.csv`. A01 and A02 are intentionally mechanistically different:

- **A01 — cellulose/CNF + Ca-alginate sacrificial network:** use diffusion/ion exchange to create a delayed gel-sol transition while the cellulose phase provides wet reinforcement.
- **A02 — cellulose fibre + pullulan-rich sacrificial binder:** use water plasticization/solubilization of a water-soluble microbial polysaccharide to progressively remove fibre-to-fibre cohesion.
- **A03 — cellulose + Ca-pectin:** retained as a backup plant-polysaccharide analogue to A01, not counted as an independent mechanism unless its kinetics prove materially different.

The evidence registry records only claims directly supported by identified primary papers and explicitly warns where geometry/conditions prevent direct transfer.
