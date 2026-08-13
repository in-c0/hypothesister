"""Run an exploratory virtual parameter screen.

All ranges in v0 are assumptions for pipeline testing, not literature-derived
material bounds. Results therefore test the *research machinery*, not CleanCoin
feasibility.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from pathlib import Path
import numpy as np

from .model import Design, simulate
from .scoring import evaluate


def sample_designs(n: int, seed: int = 5192):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        yield Design(
            thickness_m=float(rng.uniform(0.0015, 0.006)),
            water_diffusivity_m2_s=float(10 ** rng.uniform(-9.5, -7.5)),
            hydration_crosslink_rate_s=float(10 ** rng.uniform(-5.0, -2.5)),
            mechanical_damage_rate_s=float(10 ** rng.uniform(-6.0, -3.0)),
            permanent_network_fraction=float(rng.uniform(0.02, 0.35)),
            initial_sacrificial_fraction=float(rng.uniform(0.55, 0.98)),
            scrub_load=float(rng.uniform(0.5, 2.0)),
        )


def run(n: int, seed: int, out: Path) -> dict[str, int | float]:
    rows = []
    attempted = 0
    unstable = 0
    for design in sample_designs(n, seed):
        attempted += 1
        try:
            result = simulate(design)
        except ValueError as exc:
            if "unstable" in str(exc):
                unstable += 1
                continue
            raise
        rows.append({**asdict(design), **evaluate(result)})

    rows.sort(key=lambda r: float(r["score"]), reverse=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    passes = sum(bool(r["pass"]) for r in rows)
    return {
        "attempted": attempted,
        "simulated": len(rows),
        "numerically_unstable_skipped": unstable,
        "passes_under_provisional_targets": passes,
        "best_score": float(rows[0]["score"]) if rows else 0.0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=5192)
    parser.add_argument("--out", type=Path, default=Path("projects/HYP-001-cleancoin/results/virtual_screen.csv"))
    args = parser.parse_args()
    summary = run(args.samples, args.seed, args.out)
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("WARNING: v0 ranges/targets are exploratory assumptions; these are not scientific feasibility results.")


if __name__ == "__main__":
    main()
