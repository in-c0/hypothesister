"""RQ-003 coupling screen for surface integrity on the transport clock.

This remains a structural sensitivity model, not a calibrated abrasion model.
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
