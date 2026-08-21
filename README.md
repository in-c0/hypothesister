# Hypothesister × CleanCoin — Virtual Lab v0

This repository is the minimal Hypothesister research kernel plus the first CleanCoin virtual-lab scaffold.

## Research question

Can a predominantly bio-derived porous material be designed to:

1. remain compact and shelf-stable while dry;
2. hydrate/expand rapidly;
3. retain useful wet cohesion during one cleaning session; and
4. subsequently undergo accelerated loss of cohesion?

The repository deliberately separates **research infrastructure** from **scientific evidence**. The bundled simulator is a transparent mechanistic toy model for validating the workflow; it is **not calibrated to any real material** and must not be interpreted as evidence that CleanCoin is feasible.

## Why this exists before the platform/game

CleanCoin is being used to discover the reusable primitives that Hypothesister actually needs. Infrastructure only graduates into generic Hypothesister functionality after it proves reusable across multiple research projects.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
python -m cleancoin_lab.screen --samples 2000 --out projects/HYP-001-cleancoin/results/virtual_screen.csv
pytest
```

## Current layers

- `hypothesister/schemas/` — hypothesis/evidence/experiment/result contracts, plus the generic invention-candidate contract.
- `projects/HYP-001-cleancoin/` — project-specific scientific protocol.
- `src/cleancoin_lab/model.py` — 1-D hydration + sacrificial-crosslink model.
- `src/cleancoin_lab/screen.py` — uncertainty-aware parameter screening.
- `docs/VIRTUAL_LAB_V0.md` — stage gate and next implementation sequence.
- `docs/INVENTION_MODE_V0.md` — bounded problem → mechanism → falsification → prior-art triage workflow for technical invention discovery.

## Planned simulator hierarchy

1. Literature-derived parameter registry and provenance.
2. 1-D diffusion/reaction model (this repository starts here).
3. Coupled continuum swelling/damage model (FEniCSx candidate).
4. Molecular/coarse-grained parameter estimation (LAMMPS/OpenMM; MACE where justified).
5. Surrogate + active learning once high-fidelity simulations are expensive enough to warrant it.
6. Sparse physical validation only after a robust virtual design region exists.

## Non-negotiable rule

Every numerical parameter must eventually be one of:

- **measured**;
- **literature-derived with provenance**;
- **computed by a higher-fidelity model**; or
- explicitly marked **assumed / exploratory**.

No generated number silently becomes scientific evidence.
