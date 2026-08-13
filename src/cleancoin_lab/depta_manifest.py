from __future__ import annotations

import csv
import json
from pathlib import Path

from .depta_system import BOND_NM, generate_case_chains


def export_case_manifest(output_dir, *, chain_count, dimers_per_chain, box_nm, seed=0):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    chains = generate_case_chains(chain_count, dimers_per_chain, box_nm, seed=seed)

    particle_count = chain_count * dimers_per_chain
    bond_count = chain_count * max(0, dimers_per_chain - 1)
    meta = {
        "box_nm": float(box_nm),
        "periodic": [True, True, True],
        "chain_count": int(chain_count),
        "dimers_per_chain": int(dimers_per_chain),
        "particle_count": int(particle_count),
        "bond_count": int(bond_count),
        "seed": int(seed),
    }
    (out / "scene.json").write_text(json.dumps(meta, indent=2) + "\n")

    with (out / "particles.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "chain_id", "chain_index", "dimer", "x_nm", "y_nm", "z_nm"])
        particle_id = 0
        for chain_id, (dimers, positions) in enumerate(chains):
            for chain_index, (dimer, xyz) in enumerate(zip(dimers, positions)):
                w.writerow([particle_id, chain_id, chain_index, dimer, *map(float, xyz)])
                particle_id += 1

    with (out / "bonds.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "left_id", "right_id", "initial_length_nm"])
        bond_id = 0
        base = 0
        for dimers, _ in chains:
            for i in range(len(dimers) - 1):
                w.writerow([bond_id, base + i, base + i + 1, BOND_NM[(dimers[i], dimers[i + 1])]])
                bond_id += 1
            base += len(dimers)

    return meta
