"""RQ-003 coupling screens for surface integrity on the transport clock.

These remain structural sensitivity models, not calibrated abrasion models.
The transport front supplies the only dimensional clock; surface loss may only
advance failure along that existing trajectory.
"""
from __future__ import annotations

import math

from .coupled_failure import retained_path_state


def coupled_surface_integrity(
    time_s: float,
    front_time_s: float,
    tangential_work_rate: float,
    interface_strength: float,
    *,
    coupling_exponent: float = 1.0,
) -> float:
    """Integrate surface integrity while network state follows the front.

    ds/dt = -(work/strength) * (1-n(t))**q * s,
    n(t)=max(0, 1-sqrt(t/front_time)).  For t beyond front traversal the
    weakening term remains one.  q=1 has a closed form; other exponents use
    the corresponding analytic integral of (t/front_time)**(q/2) before the
    front completes.
    """
    if time_s < 0 or front_time_s <= 0:
        raise ValueError("time_s must be >= 0 and front_time_s must be > 0")
    if tangential_work_rate < 0:
        raise ValueError("tangential_work_rate must be >= 0")
    if interface_strength <= 0 or coupling_exponent <= 0:
        raise ValueError("interface_strength and coupling_exponent must be > 0")

    traversed = min(time_s, front_time_s)
    integral = (traversed ** (1.0 + coupling_exponent / 2.0)) / (
        (1.0 + coupling_exponent / 2.0) * front_time_s ** (coupling_exponent / 2.0)
    )
    if time_s > front_time_s:
        integral += time_s - front_time_s
    return math.exp(-(tangential_work_rate / interface_strength) * integral)


def coupled_surface_threshold_time_s(
    front_time_s: float,
    tangential_work_rate: float,
    interface_strength: float,
    failure_integrity: float,
    *,
    coupling_exponent: float = 1.0,
) -> float:
    """Return first surface-threshold crossing on the transport trajectory."""
    if front_time_s <= 0:
        raise ValueError("front_time_s must be > 0")
    if tangential_work_rate < 0:
        raise ValueError("tangential_work_rate must be >= 0")
    if interface_strength <= 0 or coupling_exponent <= 0:
        raise ValueError("interface_strength and coupling_exponent must be > 0")
    if not 0.0 < failure_integrity < 1.0:
        raise ValueError("failure_integrity must be in (0, 1)")
    if tangential_work_rate == 0:
        return math.inf

    target = -math.log(failure_integrity) * interface_strength / tangential_work_rate
    q = coupling_exponent
    integral_at_front = front_time_s / (1.0 + q / 2.0)
    if target <= integral_at_front:
        return (target * (1.0 + q / 2.0) * front_time_s ** (q / 2.0)) ** (1.0 / (1.0 + q / 2.0))
    return front_time_s + target - integral_at_front


def network_coupled_surface_integrity(
    time_s: float,
    front_time_s: float,
    tangential_work_rate: float,
    interface_strength: float,
    *,
    coupling_exponent: float = 1.0,
    strength_exponent: float = 1.0,
    residual_strength_fraction: float = 0.2,
    integration_steps: int = 256,
) -> float:
    """Surface integrity with interface strength tied to network weakening.

    The previous bounded screen treated interface strength as an independent
    constant.  The RQ-003 physical-regime evidence instead requires strength to
    weaken monotonically with the same transport/network state.  This function
    implements only that structural change:

        strength(n) = strength_0 * [r + (1-r) * n**p]

    where ``r`` is the residual strength fraction after severe network loss.
    The surface-loss rate remains activated by ``(1-n)**q``.  A deterministic
    trapezoidal quadrature is used because the combined rate has no useful
    closed form for general p and q.

    ``residual_strength_fraction`` and ``strength_exponent`` are sensitivity
    parameters, not calibrated CleanCoin properties.
    """
    if time_s < 0 or front_time_s <= 0:
        raise ValueError("time_s must be >= 0 and front_time_s must be > 0")
    if tangential_work_rate < 0:
        raise ValueError("tangential_work_rate must be >= 0")
    if interface_strength <= 0 or coupling_exponent <= 0 or strength_exponent <= 0:
        raise ValueError(
            "interface_strength, coupling_exponent and strength_exponent must be > 0"
        )
    if not 0.0 < residual_strength_fraction <= 1.0:
        raise ValueError("residual_strength_fraction must be in (0, 1]")
    if integration_steps < 8:
        raise ValueError("integration_steps must be >= 8")
    if time_s == 0 or tangential_work_rate == 0:
        return 1.0

    dt = time_s / integration_steps
    integral = 0.0
    for index in range(integration_steps + 1):
        t = index * dt
        network_state = retained_path_state(t, front_time_s)
        weakening = (1.0 - network_state) ** coupling_exponent
        strength_fraction = residual_strength_fraction + (
            1.0 - residual_strength_fraction
        ) * network_state**strength_exponent
        integrand = weakening / strength_fraction
        weight = 0.5 if index in (0, integration_steps) else 1.0
        integral += weight * integrand

    integral *= dt
    return math.exp(-(tangential_work_rate / interface_strength) * integral)


def network_coupled_surface_threshold_time_s(
    front_time_s: float,
    tangential_work_rate: float,
    interface_strength: float,
    failure_integrity: float,
    *,
    coupling_exponent: float = 1.0,
    strength_exponent: float = 1.0,
    residual_strength_fraction: float = 0.2,
    integration_steps: int = 256,
) -> float:
    """Return the first threshold crossing for network-coupled strength.

    Bisection keeps the threshold calculation deterministic and avoids adding a
    second timescale.  The search expands only after the transport front has
    traversed; beyond that point ``retained_path_state`` stays at zero.
    """
    if front_time_s <= 0:
        raise ValueError("front_time_s must be > 0")
    if tangential_work_rate < 0:
        raise ValueError("tangential_work_rate must be >= 0")
    if interface_strength <= 0 or coupling_exponent <= 0 or strength_exponent <= 0:
        raise ValueError(
            "interface_strength, coupling_exponent and strength_exponent must be > 0"
        )
    if not 0.0 < residual_strength_fraction <= 1.0:
        raise ValueError("residual_strength_fraction must be in (0, 1]")
    if not 0.0 < failure_integrity < 1.0:
        raise ValueError("failure_integrity must be in (0, 1)")
    if integration_steps < 8:
        raise ValueError("integration_steps must be >= 8")
    if tangential_work_rate == 0:
        return math.inf

    kwargs = {
        "coupling_exponent": coupling_exponent,
        "strength_exponent": strength_exponent,
        "residual_strength_fraction": residual_strength_fraction,
        "integration_steps": integration_steps,
    }
    lower = 0.0
    upper = front_time_s
    while network_coupled_surface_integrity(
        upper,
        front_time_s,
        tangential_work_rate,
        interface_strength,
        **kwargs,
    ) > failure_integrity:
        upper *= 2.0
        if upper > front_time_s * 1_000_000:
            return math.inf

    for _ in range(60):
        midpoint = (lower + upper) / 2.0
        if network_coupled_surface_integrity(
            midpoint,
            front_time_s,
            tangential_work_rate,
            interface_strength,
            **kwargs,
        ) > failure_integrity:
            lower = midpoint
        else:
            upper = midpoint
    return upper


def surface_advances_transport_failure(
    front_time_s: float,
    tangential_work_rate: float,
    interface_strength: float,
    failure_integrity: float,
    *,
    coupling_exponent: float = 1.0,
) -> bool:
    """Whether the bounded surface term crosses before full front traversal."""
    return coupled_surface_threshold_time_s(
        front_time_s,
        tangential_work_rate,
        interface_strength,
        failure_integrity,
        coupling_exponent=coupling_exponent,
    ) < front_time_s
