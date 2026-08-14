#!/usr/bin/env python3
"""Reproduce the RQ-003 reduced contact-load uncertainty screen.

The default ranges are deliberately broad exploratory envelopes, not calibrated
CleanCoin parameter bounds. The output is a sensitivity result only.
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from cleancoin_lab.contact_load import monte_carlo_contact_screen


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=20260814)
    args = parser.parse_args()

    result = monte_carlo_contact_screen(args.samples, seed=args.seed)
    drive = (
        result.localization_factor
        * result.dimensionless_load
        / result.failure_strain
    )
    edges = np.quantile(drive, [0.0, 0.25, 0.5, 0.75, 1.0])

    quartiles = []
    for index in range(4):
        lower = edges[index]
        upper = edges[index + 1]
        mask = (drive >= lower) & (
            (drive < upper) if index < 3 else (drive <= upper)
        )
        quartiles.append(
            {
                "quartile": index + 1,
                "drive_range": [float(lower), float(upper)],
                "median_onset_s": float(np.median(result.onset_time_s[mask])),
                "fraction_10_to_30_min": float(
                    np.mean(
                        (result.onset_time_s[mask] >= 600.0)
                        & (result.onset_time_s[mask] <= 1800.0)
                    )
                ),
                "fraction_immediate": float(
                    np.mean(result.onset_time_s[mask] == 0.0)
                ),
            }
        )

    summary = {
        "samples": args.samples,
        "seed": args.seed,
        "ranges_are_calibrated": False,
        "fraction_10_to_30_min": result.fraction_in_window(600.0, 1800.0),
        "fraction_immediate": result.fraction_failed_at_initial_state,
        "onset_time_quantiles_s": {
            key: float(value)
            for key, value in zip(
                ["p05", "p10", "p25", "p50", "p75", "p90", "p95"],
                np.quantile(
                    result.onset_time_s,
                    [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95],
                ),
                strict=True,
            )
        },
        "effective_drive_quartiles": quartiles,
        "interpretation": (
            "If the target-window fraction and onset time move strongly across "
            "effective contact-drive quartiles, mechanics is not a robust timer "
            "under this reduced model; retain it as a terminal accelerator."
        ),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
