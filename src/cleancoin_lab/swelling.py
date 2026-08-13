"""Alginate-specific reduced swelling kinetics for HYP-001 RQ-002.

Davidovich-Pinhas & Bianco-Peled (2010),
DOI 10.1016/j.carbpol.2009.10.036, found calcium-alginate swelling kinetics to
obey a second-order law rather than the simple single-exponent power law often
used for polymer swelling. Their linearized expression is equivalent, for a
positive swelling process, to a normalized progress curve

    f(t) = lambda * t / (1 + lambda * t)

with ``lambda = k * M_eq`` for their tabulated second-order rate constant ``k``
and equilibrium uptake/weight scale ``M_eq``.

This module deliberately models only normalized progress. It does *not* assume
that the source tablet mass, equilibrium swelling ratio, or calcium variable can
be transferred directly to a porous 4 wt% CleanCoin composite. Absolute
swelling and the mapping from A01 network state to ``lambda`` remain calibration
problems.
"""

from __future__ import annotations

import math


def second_order_progress(time_s: float, lambda_s_inv: float) -> float:
    """Return normalized swelling progress in [0, 1) for positive kinetics."""
    if time_s < 0:
        raise ValueError("time_s must be >= 0")
    if lambda_s_inv < 0:
        raise ValueError("lambda_s_inv must be >= 0")
    if lambda_s_inv == 0 or time_s == 0:
        return 0.0
    x = lambda_s_inv * time_s
    return x / (1.0 + x)


def source_lambda_from_k_meq(
    rate_constant_min_inv_mg_inv: float,
    equilibrium_scale_mg: float,
) -> float:
    """Convert source ``k * M_eq`` to a characteristic rate in s^-1.

    This helper is valid only for positive-swelling source fits. Negative fitted
    constants reported for syneresis/de-swelling cases are not interpreted by
    this reduced swelling-progress model.
    """
    if rate_constant_min_inv_mg_inv < 0:
        raise ValueError("negative k represents a de-swelling regime; unsupported")
    if equilibrium_scale_mg <= 0:
        raise ValueError("equilibrium_scale_mg must be > 0")
    return (
        rate_constant_min_inv_mg_inv * equilibrium_scale_mg / 60.0
    )


def characteristic_half_time_s(lambda_s_inv: float) -> float:
    """Return t at which second-order normalized progress reaches 0.5."""
    if lambda_s_inv < 0:
        raise ValueError("lambda_s_inv must be >= 0")
    return math.inf if lambda_s_inv == 0 else 1.0 / lambda_s_inv
