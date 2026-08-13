from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .depta_system import BOND_NM, generate_case_chains

FINITE_SIZE_CASES = {
    200: 121,
    250: 235,
    300: 407,
    500: 1883,
}


def export_case_manifest(output_dir, *, chain_count, dimers_per_chain, box_nm, seed=0):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    chains = generate_case_chains(chain_count, dimers_per_chain, box_nm, seed=seed)
    meta = {
        "box_nm": float(box_nm),
        "periodic": [True, True, True],
        "chain_count": int(chain_count),
        "dimers_per_chain": int(dimers_per_chain),
        "particle_count": int(chain_count * dimers_per_chain),
        "bond_count": int(chain_count * max(0, dimers_per_chain - 1)),
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


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--box-nm", type=int, choices=sorted(FINITE_SIZE_CASES), default=200)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--output", default="results/depta-preflight")
    args = p.parse_args(argv)
    meta = export_case_manifest(
        args.output,
        chain_count=FINITE_SIZE_CASES[args.box_nm],
        dimers_per_chain=571,
        box_nm=args.box_nm,
        seed=args.seed,
    )
    print(json.dumps(meta, sort_keys=True))


if __name__ == "__main__":
    main()
