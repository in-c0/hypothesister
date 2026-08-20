"""RQ-003 classification-change screen for the bounded surface channel.

This module reports sensitivity; it does not calibrate CleanCoin tribology.
The existing contact uncertainty sampler supplies the ensemble and the
transport-front time remains the sole dimensional clock.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .contact_load import monte_carlo_contact_screen
from .coupled_failure import coupled_local_failure_times_s
from .surface_coupling import coupled_surface_threshold_time_s


@dataclass(frozen=True)
class ClassificationChangeResult:
    n_samples: int
    bulk_accept_fraction: float
    combined_accept_fraction: float
    changed_fraction: float
    surface_first_fraction: float


def classification_change_screen(
    n_samples: int = 100_000,
    *,
    seed: int = 0,
    acceptance_window_s: tuple[float, float] = (600.0, 1800.0),
    surface_rate_over_strength_range: tuple[float, float] = (1e-5, 1e-2),
    coupling_exponent_range: tuple[float, float] = (0.5, 3.0),
    failure_integrity_range: tuple[float, float] = (0.2, 0.8),
) -> ClassificationChangeResult:
    """Measure how often an uncalibrated surface channel changes acceptance.

    Surface susceptibility is sampled log-uniformly over broad dimensionless
    rate/strength bounds. No bounds are selected to target the 10--30 min
    window. A classification is accepted when first terminal failure lies
    inside that window; the combined model uses min(bulk, surface) failure.
    """
    if n_samples <= 0:
        raise ValueError("n_samples must be > 0")
    lo, hi = acceptance_window_s
    if lo <= 0 or hi <= lo:
        raise ValueError("acceptance_window_s must satisfy 0 < lo < hi")
    if surface_rate_over_strength_range[0] <= 0 or surface_rate_over_strength_range[1] <= surface_rate_over_strength_range[0]:
        raise ValueError("invalid surface susceptibility range")
    if coupling_exponent_range[0] <= 0 or coupling_exponent_range[1] <= coupling_exponent_range[0]:
        raise ValueError("invalid coupling exponent range")
    if not 0 < failure_integrity_range[0] < failure_integrity_range[1] < 1:
        raise ValueError("failure integrity range must lie inside (0, 1)")

    contact = monte_carlo_contact_screen(n_samples=n_samples, seed=seed)
    # Reuse the sampled softening times as the reduced local transport-front
    # ensemble; this preserves the existing 15--45 min uncertainty envelope.
    front = contact.softening_tau_s
    bulk = coupled_local_failure_times_s(
        front,
        contact.dimensionless_load,
        contact.localization_factor,
        contact.failure_strain,
    )

    rng = np.random.default_rng(seed + 1)
    rate_over_strength = np.exp(rng.uniform(
        np.log(surface_rate_over_strength_range[0]),
        np.log(surface_rate_over_strength_range[1]),
        n_samples,
    ))
    exponent = rng.uniform(*coupling_exponent_range, size=n_samples)
    threshold = rng.uniform(*failure_integrity_range, size=n_samples)
    surface = np.fromiter(
        (
            coupled_surface_threshold_time_s(float(f), float(r), 1.0, float(s), coupling_exponent=float(q))
            for f, r, s, q in zip(front, rate_over_strength, threshold, exponent)
        ),
        dtype=float,
        count=n_samples,
    )
    combined = np.minimum(bulk, surface)
    bulk_accept = (bulk >= lo) & (bulk <= hi)
    combined_accept = (combined >= lo) & (combined <= hi)

    return ClassificationChangeResult(
        n_samples=n_samples,
        bulk_accept_fraction=float(np.mean(bulk_accept)),
        combined_accept_fraction=float(np.mean(combined_accept)),
        changed_fraction=float(np.mean(bulk_accept != combined_accept)),
        surface_first_fraction=float(np.mean(surface < bulk)),
    )
