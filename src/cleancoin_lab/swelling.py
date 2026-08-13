"""Alginate-specific reduced swelling state for HYP-001 RQ-002.

Davidovich-Pinhas & Bianco-Peled (2010),
DOI 10.1016/j.carbpol.2009.10.036, provide two useful empirical closures:

1. equilibrium volumetric swelling follows ``Q = A * [Ca]**n`` for each
   alginate chemistry; and
2. swelling kinetics follow a second-order law rather than a simple power law.

For a positive step toward an equilibrium state, their linearized second-order
law is equivalent to normalized progress

    f(t) = lambda * t / (1 + lambda * t)

where ``lambda = k * M_eq`` for the source's fitted mass-scale convention.

Important: ``[Ca]`` below is a *source-equivalent calcium variable*. The source
varied calcium during internal gel preparation. It is not automatically equal
to A01's total calcium inventory, free calcium concentration, or effective
mechanical crosslink density. Any A01 dynamic mapping into this variable must be
explicitly calibrated and uncertainty-propagated.
"""

from __future__ import annotations

import math

# Equilibrium swelling power-law fits from Davidovich-Pinhas & Bianco-Peled,
# Table 2. Q is dimensionless and calcium concentration is in the source's mM
# convention. LF240D is the closest source chemistry to the low-G A1112 prior.
EQUILIBRIUM_SWELLING_FITS = {
    "LF240D": (6.556, -0.509),   # 30-35% G
    "HF120RBS": (3.795, -0.472), # 45-55% G
    "LF200S": (3.175, -0.491),   # 65-75% G
}


def equilibrium_swelling_ratio(
    calcium_mM: float,
    *,
    prefactor: float,
    exponent: float,
) -> float:
    """Return source-empirical equilibrium volume ratio ``Q``.

    This is an empirical alginate closure, not Flory/Rehner theory. The source
    explicitly found standard chemically-crosslinked-network theories to be
    unsuitable for its calcium-alginate data.
    """
    if calcium_mM <= 0:
        raise ValueError("calcium_mM must be > 0")
    if prefactor <= 0:
        raise ValueError("prefactor must be > 0")
    return prefactor * calcium_mM**exponent


def equilibrium_swelling_ratio_for_alginate(
    calcium_mM: float,
    alginate: str = "LF240D",
) -> float:
    """Convenience wrapper for the three source-reported alginate fits."""
    try:
        prefactor, exponent = EQUILIBRIUM_SWELLING_FITS[alginate]
    except KeyError as exc:
        raise ValueError(f"unknown source alginate: {alginate}") from exc
    return equilibrium_swelling_ratio(
        calcium_mM,
        prefactor=prefactor,
        exponent=exponent,
    )


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


def second_order_relaxation_step(
    current_ratio: float,
    equilibrium_ratio: float,
    beta_s_inv_ratio_inv: float,
    dt_s: float,
) -> float:
    """Advance a dimensionless swelling ratio toward equilibrium.

    This symmetric reduced-order form implements

        dQ/dt = beta * sign(Qeq-Q) * |Qeq-Q|^2

    whose step response has the same rational second-order kinetic shape as the
    source swelling law. It supports both swelling and syneresis without reusing
    the source's negative fitted constants as positive rate constants.

    ``beta`` is formulation/state specific and is not yet calibrated for A01.
    """
    if current_ratio <= 0 or equilibrium_ratio <= 0:
        raise ValueError("swelling ratios must be > 0")
    if beta_s_inv_ratio_inv < 0:
        raise ValueError("beta must be >= 0")
    if dt_s < 0:
        raise ValueError("dt_s must be >= 0")
    delta = equilibrium_ratio - current_ratio
    if delta == 0 or beta_s_inv_ratio_inv == 0 or dt_s == 0:
        return current_ratio
    remaining = abs(delta) / (1.0 + beta_s_inv_ratio_inv * abs(delta) * dt_s)
    return equilibrium_ratio - math.copysign(remaining, delta)


def source_lambda_from_k_meq(
    rate_constant_min_inv_mg_inv: float,
    equilibrium_scale_mg: float,
) -> float:
    """Convert source ``k * M_eq`` to a characteristic rate in s^-1.

    Valid only for source fits classified as positive swelling. Negative fitted
    constants reported for syneresis cases are preserved in the source table but
    are not interpreted by this helper.
    """
    if rate_constant_min_inv_mg_inv < 0:
        raise ValueError("negative k represents a de-swelling regime; unsupported")
    if equilibrium_scale_mg <= 0:
        raise ValueError("equilibrium_scale_mg must be > 0")
    return rate_constant_min_inv_mg_inv * equilibrium_scale_mg / 60.0


def characteristic_half_time_s(lambda_s_inv: float) -> float:
    """Return t at which second-order normalized progress reaches 0.5."""
    if lambda_s_inv < 0:
        raise ValueError("lambda_s_inv must be >= 0")
    return math.inf if lambda_s_inv == 0 else 1.0 / lambda_s_inv
