#!/usr/bin/env python3
"""RQ-003 classification-change screen for the bounded surface term.

This is a structural sensitivity experiment, not a calibrated CleanCoin
lifetime model. Surface parameters are deliberately swept across broad reduced
ranges. The transport/front-time envelope is likewise exploratory and anchored
to the existing RQ-002D 10–30 minute transport-scale gate.
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from cleancoin_lab.surface_coupling import coupled_surface_threshold_time_s


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=20260820)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)

    # Broad structural envelope only; these are not calibrated parameter bounds.
    front_time_s = rng.uniform(600.0, 1800.0, args.samples)
    work_over_strength = 10.0 ** rng.uniform(-5.0, -2.0, args.samples)
    coupling_exponent = rng.uniform(0.5, 2.0, args.samples)
    failure_integrity = rng.uniform(0.2, 0.8, args.samples)

    surface_time_s = np.fromiter(
        (
            coupled_surface_threshold_time_s(
                float(front),
                float(ratio),
                1.0,
                float(threshold),
                coupling_exponent=float(exponent),
            )
            for front, ratio, threshold, exponent in zip(
                front_time_s,
                work_over_strength,
                failure_integrity,
                coupling_exponent,
                strict=True,
            )
        ),
        dtype=float,
        count=args.samples,
    )
    combined_time_s = np.minimum(front_time_s, surface_time_s)

    # Classification asks whether the terminal failure remains inside the
    # existing 10–30 minute RQ-003 acceptance interval.
    bulk_in_window = (front_time_s >= 600.0) & (front_time_s <= 1800.0)
    combined_in_window = (combined_time_s >= 600.0) & (combined_time_s <= 1800.0)
    changed = bulk_in_window != combined_in_window
    surface_advances = surface_time_s < front_time_s

    log_ratio = np.log10(work_over_strength)
    edges = np.quantile(log_ratio, [0.0, 0.25, 0.5, 0.75, 1.0])
    quartiles = []
    for index in range(4):
        lower, upper = edges[index], edges[index + 1]
        mask = (log_ratio >= lower) & (
            (log_ratio < upper) if index < 3 else (log_ratio <= upper)
        )
        quartiles.append(
            {
                "quartile": index + 1,
                "work_over_strength_range": [10.0 ** float(lower), 10.0 ** float(upper)],
                "fraction_surface_advances": float(np.mean(surface_advances[mask])),
                "fraction_classification_changed": float(np.mean(changed[mask])),
                "median_combined_failure_s": float(np.median(combined_time_s[mask])),
            }
        )

    summary = {
        "samples": args.samples,
        "seed": args.seed,
        "ranges_are_calibrated": False,
        "bulk_acceptance_definition": "terminal failure in [600, 1800] s",
        "fraction_surface_advances_failure": float(np.mean(surface_advances)),
        "fraction_acceptance_classification_changed": float(np.mean(changed)),
        "combined_failure_quantiles_s": {
            key: float(value)
            for key, value in zip(
                ["p05", "p25", "p50", "p75", "p95"],
                np.quantile(combined_time_s, [0.05, 0.25, 0.50, 0.75, 0.95]),
                strict=True,
            )
        },
        "work_over_strength_quartiles": quartiles,
        "decision_rule": (
            "If classification changes are confined to a small boundary subset, "
            "retain surface loss as secondary. If changes span a material fraction, "
            "surface/interface calibration becomes a dominant RQ-003 uncertainty. "
            "If the conclusion is controlled by arbitrary sweep bounds, keep the gate unresolved."
        ),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
