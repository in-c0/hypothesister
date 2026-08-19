"""RQ-003 bounded surface/interface integrity sensitivity model.

This is deliberately a model-structure screen, not a calibrated CleanCoin
abrasion/lifetime model.  It asks whether adding the smallest independent
surface state can materially move a transport-governed vulnerability time.
"""
from __future__ import annotations

import math


def surface_integrity(
    time_s: float,
    network_state: float,
    tangential_work_rate: float,
    interface_strength: float,
    *,
    coupling_exponent: float = 1.0,
) -> float:
    """Return bounded surface state s in [0, 1].

    ds/dt = -k*s, with k=(work/strength)*(1-n)^q.  The rate activates only as
    the network weakens and keeps interface strength independent of bulk load.
    All inputs are reduced/dimensionless except time; parameter values remain
    uncalibrated until source-backed or measured bounds exist.
    """
    if time_s < 0:
        raise ValueError("time_s must be >= 0")
    if not 0.0 <= network_state <= 1.0:
        raise ValueError("network_state must be in [0, 1]")
    if tangential_work_rate < 0:
        raise ValueError("tangential_work_rate must be >= 0")
    if interface_strength <= 0 or coupling_exponent <= 0:
        raise ValueError("interface_strength and coupling_exponent must be > 0")

    weakening = (1.0 - network_state) ** coupling_exponent
    rate = (tangential_work_rate / interface_strength) * weakening
    return math.exp(-rate * time_s)


def surface_threshold_time_s(
    network_state: float,
    tangential_work_rate: float,
    interface_strength: float,
    failure_integrity: float,
    *,
    coupling_exponent: float = 1.0,
) -> float:
    """Time to cross a reduced surface-integrity threshold at fixed n.

    Returns infinity when the surface term is inactive.  Holding n fixed is
    intentional: this isolates whether the extra state can matter before a
    later coupled transport trajectory is justified.
    """
    if not 0.0 < failure_integrity < 1.0:
        raise ValueError("failure_integrity must be in (0, 1)")
    if not 0.0 <= network_state <= 1.0:
        raise ValueError("network_state must be in [0, 1]")
    if tangential_work_rate < 0:
        raise ValueError("tangential_work_rate must be >= 0")
    if interface_strength <= 0 or coupling_exponent <= 0:
        raise ValueError("interface_strength and coupling_exponent must be > 0")

    weakening = (1.0 - network_state) ** coupling_exponent
    rate = (tangential_work_rate / interface_strength) * weakening
    if rate == 0.0:
        return math.inf
    return -math.log(failure_integrity) / rate
