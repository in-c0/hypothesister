#!/usr/bin/env python3
"""RQ-003 constrained structural rerun for the surface/contact gate.

This is still a sensitivity experiment, not a CleanCoin calibration or lifetime
claim. It preserves the frozen 10–30 minute acceptance classification while
making the two structural changes required by the merged physical-regime gate:
(1) interface strength weakens monotonically with the transport/network state,
and (2) the previous three-decade reduced work/strength sweep is narrowed to a
literature-anchored order-of-magnitude transfer band. Geometry remains broad.
"""
from __future__ import annotations

import argparse
import json

import numpy as np

from cleancoin_lab.surface_coupling import network_coupled_surface_threshold_time_s


def run(samples: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)

    # Preserve the existing RQ-002D/RQ-003 transport clock.
    front_time_s = rng.uniform(600.0, 1800.0, samples)

    # Reduced transfer band, not a product calibration. The prior screen used
    # 1e-5..1e-2; the evidence gate rules out treating the highest arbitrary
    # decade as equally plausible while still retaining two decades of contact/
    # geometry uncertainty.
    work_over_strength = 10.0 ** rng.uniform(-5.0, -3.0, samples)

    # Structural sensitivity axes retained from the previous screen.
    coupling_exponent = rng.uniform(0.5, 2.0, samples)
    failure_integrity = rng.uniform(0.2, 0.8, samples)

    # Strength now follows network weakening rather than being independent.
    strength_exponent = rng.uniform(0.5, 2.0, samples)
    residual_strength_fraction = rng.uniform(0.1, 0.4, samples)

    surface_time_s = np.fromiter(
        (
            network_coupled_surface_threshold_time_s(
                float(front),
                float(ratio),
                1.0,
                float(threshold),
                coupling_exponent=float(q),
                strength_exponent=float(p),
                residual_strength_fraction=float(residual),
                integration_steps=128,
            )
            for front, ratio, threshold, q, p, residual in zip(
                front_time_s,
                work_over_strength,
                failure_integrity,
                coupling_exponent,
                strength_exponent,
                residual_strength_fraction,
                strict=True,
            )
        ),
        dtype=float,
        count=samples,
    )

    combined_time_s = np.minimum(front_time_s, surface_time_s)
    bulk_in_window = (front_time_s >= 600.0) & (front_time_s <= 1800.0)
    combined_in_window = (combined_time_s >= 600.0) & (combined_time_s <= 1800.0)
    changed = bulk_in_window != combined_in_window
    surface_advances = surface_time_s < front_time_s

    log_ratio = np.log10(work_over_strength)
    edges = np.quantile(log_ratio, [0.0, 0.25, 0.5, 0.75, 1.0])
    quartiles: list[dict[str, object]] = []
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

    return {
        "samples": samples,
        "seed": seed,
        "ranges_are_calibrated": False,
        "bulk_acceptance_definition": "terminal failure in [600, 1800] s",
        "work_over_strength_transfer_band": [1e-5, 1e-3],
        "network_coupled_strength": True,
        "residual_strength_fraction_range": [0.1, 0.4],
        "strength_exponent_range": [0.5, 2.0],
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
            "Promote surface damage to a required model component only if the "
            "constrained rerun changes the frozen acceptance classification in a "
            "non-negligible stable fraction and the effect is not concentrated at "
            "one arbitrary transfer-band boundary. Otherwise retain it as a "
            "secondary failure mode and defer abrasion-model escalation."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260825)
    args = parser.parse_args()
    print(json.dumps(run(args.samples, args.seed), indent=2))


if __name__ == "__main__":
    main()
