"""Calibration utilities for source-derived release-curve shapes.

The functions in this module intentionally separate *shape calibration* from
absolute calcium-inventory calibration. This lets HYP-001 use time-resolved
external Ca2+ data even when bath volume or initial bound-Ca inventory is not
reported, while preventing an apparent release timescale from being mislabeled
as an intrinsic junction-dissociation constant.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np


@dataclass(frozen=True)
class ApparentRateFit:
    rate_s: float
    characteristic_time_s: float
    sse: float
    normalized_prediction: dict[float, float]


def cumulative_from_piecewise_rates(
    segments: list[tuple[float, float, float]],
) -> dict[float, float]:
    """Integrate piecewise-constant interval-average rates.

    Parameters
    ----------
    segments:
        ``[(start_min, end_min, rate_mM_per_min), ...]`` in chronological
        non-overlapping order.

    Returns
    -------
    Mapping from each interval end time (minutes) to cumulative concentration-
    equivalent release. The result preserves the source's concentration scale;
    no bath-volume inference is made.
    """
    if not segments:
        raise ValueError("segments must not be empty")

    cumulative = 0.0
    out: dict[float, float] = {}
    previous_end: float | None = None
    for start, end, rate in segments:
        if end <= start:
            raise ValueError("each segment must have end > start")
        if rate < 0:
            raise ValueError("release rate must be nonnegative")
        if previous_end is not None and not np.isclose(start, previous_end):
            raise ValueError("segments must be contiguous and chronological")
        cumulative += (end - start) * rate
        out[float(end)] = float(cumulative)
        previous_end = end
    return out


def normalize_cumulative(
    cumulative: Mapping[float, float],
    reference_time_min: float | None = None,
) -> dict[float, float]:
    """Normalize cumulative release by a chosen observed reference time."""
    if not cumulative:
        raise ValueError("cumulative data must not be empty")
    if reference_time_min is None:
        reference_time_min = max(cumulative)
    if reference_time_min not in cumulative:
        raise ValueError("reference time must be present in cumulative data")
    scale = float(cumulative[reference_time_min])
    if scale <= 0:
        raise ValueError("reference cumulative release must be > 0")
    return {float(t): float(v / scale) for t, v in cumulative.items()}


def normalized_first_order(rate_s: float, time_min: float, reference_min: float) -> float:
    """Return normalized ``1-exp(-kt)`` evaluated relative to reference time."""
    if rate_s <= 0 or time_min < 0 or reference_min <= 0 or time_min > reference_min:
        raise ValueError("invalid rate/time arguments")
    numerator = -np.expm1(-rate_s * time_min * 60.0)
    denominator = -np.expm1(-rate_s * reference_min * 60.0)
    return float(numerator / denominator)


def fit_apparent_first_order(
    normalized_observations: Mapping[float, float],
    reference_time_min: float | None = None,
    rate_bounds_s: tuple[float, float] = (1e-6, 1e-2),
    grid_size: int = 100_000,
) -> ApparentRateFit:
    """Fit a descriptive first-order timescale to a normalized release curve.

    This returns ``k_app`` only. It MUST NOT be interpreted as the intrinsic
    temporary-junction dissociation rate without a transport/geometry model.
    """
    if not normalized_observations:
        raise ValueError("observations must not be empty")
    if reference_time_min is None:
        reference_time_min = max(normalized_observations)
    if grid_size < 100:
        raise ValueError("grid_size must be >= 100")
    lo, hi = rate_bounds_s
    if not 0 < lo < hi:
        raise ValueError("rate bounds must satisfy 0 < lo < hi")

    observations = {
        float(t): float(y)
        for t, y in normalized_observations.items()
        if float(t) < float(reference_time_min)
    }
    if not observations:
        raise ValueError("at least one observation before reference time is required")

    rates = np.geomspace(lo, hi, grid_size)
    sse = np.zeros_like(rates)
    for t, y in observations.items():
        pred = (-np.expm1(-rates * t * 60.0)) / (
            -np.expm1(-rates * float(reference_time_min) * 60.0)
        )
        sse += (pred - y) ** 2

    idx = int(np.argmin(sse))
    best = float(rates[idx])
    prediction = {
        float(t): normalized_first_order(best, float(t), float(reference_time_min))
        for t in normalized_observations
    }
    return ApparentRateFit(
        rate_s=best,
        characteristic_time_s=1.0 / best,
        sse=float(sse[idx]),
        normalized_prediction=prediction,
    )
